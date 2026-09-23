"""Bounded passive input acquisition for the qualified POSIX environment."""

import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat

from .errors import StudyError, require

MAX_JSON = 1_048_576
MAX_SOURCE = 262_144
MAX_TOTAL = 4_194_304


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _pairs(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_json_key")
        result[key] = value
    return result


def _constant(value: str):
    raise StudyError("nonfinite_json_number")


def json_bytes(data: bytes):
    require(len(data) <= MAX_JSON, "json_size_limit")
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
        todo = [(value, 0)]
        while todo:
            item, depth = todo.pop()
            require(depth <= 24, "json_depth_limit")
            if isinstance(item, float):
                require(math.isfinite(item), "nonfinite_json_number")
            if isinstance(item, dict):
                todo.extend((v, depth + 1) for v in item.values())
            elif isinstance(item, list):
                todo.extend((v, depth + 1) for v in item)
        return value
    except (UnicodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, StudyError):
            raise
        raise StudyError("invalid_json") from exc


class InputDirectory:
    """Hold a root descriptor and open only regular, no-follow local payloads."""

    def __init__(self, root: Path):
        require(os.name == "posix" and hasattr(os, "O_NOFOLLOW")
                and os.open in os.supports_dir_fd, "unsupported_safe_input_platform")
        try:
            self.fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except OSError as exc:
            raise StudyError("input_directory_unavailable") from exc
        self.total = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        os.close(self.fd)

    def read(self, relative: str, limit: int) -> bytes:
        require(isinstance(relative, str) and 0 < len(relative) <= 512
                and not any(ord(c) < 32 or c == "\\" for c in relative), "unsafe_path")
        path = PurePosixPath(relative)
        require(not path.is_absolute() and bool(path.parts) and ".." not in path.parts
                and path.as_posix() == relative and relative != ".", "unsafe_path")
        fd = os.dup(self.fd)
        try:
            for part in path.parts[:-1]:
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                  dir_fd=fd)
                os.close(fd)
                fd = next_fd
            payload_fd = os.open(path.parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                 dir_fd=fd)
            try:
                info = os.fstat(payload_fd)
                require(stat.S_ISREG(info.st_mode), "nonregular_payload")
                require(info.st_size <= limit, "payload_size_limit")
                with os.fdopen(payload_fd, "rb", closefd=False) as stream:
                    data = stream.read(limit + 1)
                require(len(data) <= limit, "payload_size_limit")
            finally:
                os.close(payload_fd)
        except OSError as exc:
            raise StudyError("payload_unavailable_or_unsafe") from exc
        finally:
            os.close(fd)
        self.total += len(data)
        require(self.total <= MAX_TOTAL, "total_input_size_limit")
        return data
