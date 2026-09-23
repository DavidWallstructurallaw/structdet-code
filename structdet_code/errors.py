"""Stable input errors; no candidate content is included in messages."""


class StudyError(ValueError):
    """Malformed, contradictory, unsupported, or inaccessible study input."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise StudyError(code)
