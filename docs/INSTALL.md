# Installation and supported environment

Version 0.1.0 can be installed from a wheel or source archive. Check
[GitHub Releases](https://github.com/DavidWallstructurallaw/structdet-code/releases)
for published artifacts, or build the reviewed source. No PyPI upload is included.
The wheel includes both task packs and all 58 owned example files; a source
checkout is unnecessary after installation. Verify downloaded release artifacts
against their accompanying `SHA256SUMS` before installing.

## Qualified wheel route

Actual qualification used Linux x86_64, CPython 3.12.14, pip 26.2.1 and
setuptools 84.0.0. Runtime environments were newly created virtual environments
without system site-packages, with only `structdet-code` installed. Both console
and module commands ran from a directory outside the checkout. No package index
was accessed during the build/install qualification.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps /absolute/path/structdet_code-0.1.0-py3-none-any.whl
.venv/bin/structdet-code demo --output ./first-demo
```

Use a new output directory on each run. On Linux installations without venv/pip
support, install the corresponding components supplied by the Python distributor
before creating the environment. Installing the wheel requires no compiler or
third-party runtime package.

## Qualified source-distribution route

The second route rebuilt the actual `.tar.gz` using pip and the already installed
build backend, then installed that resulting wheel into a separate clean runtime.
This exercises the source archive's build contents and installed behavior. It
does not qualify downloading build requirements or PyPI publishing.

In a build environment with pip and `setuptools>=77.0.3` already installed:

```bash
python3.12 -m pip wheel --no-index --no-deps --no-build-isolation --no-cache-dir --wheel-dir ./built-wheels /absolute/path/structdet_code-0.1.0.tar.gz
python3.12 -m venv .source-venv
.source-venv/bin/python -m pip install --no-index --no-deps ./built-wheels/structdet_code-0.1.0-py3-none-any.whl
.source-venv/bin/structdet-code demo --output ./source-demo
```

Every decompressed member of the directly built wheel and source-rebuilt wheel
must match. Archive timestamps can differ; no byte-reproducible build claim is
made. The source archive also includes guides, tests and developer utilities.
Historical verification reports are retained in GitHub, outside the source
archive, so a report need not contain its own distribution hash.

## Support limits and common errors

| Situation | Meaning and next action |
| --- | --- |
| Python below 3.12 | Rejected by package metadata; use the qualified Python version |
| Other Python versions, macOS or Windows | Unqualified. The generic pure-Python wheel tag is not a platform support claim; safe input requires POSIX no-follow operations |
| `unsupported_safe_input_platform` | The required safe file operations are unavailable; use the qualified Linux environment |
| Existing output | Choose a new file/directory; output commands preserve existing results |
| `payload_unavailable_or_unsafe` | Check relative paths, regular files, permissions and absence of symlinks inside the input root |
| Source/task/study binding mismatch | Restore matching original bytes or explicitly prepare/review new inputs; do not rewrite hashes to hide a change |
| Replay software identity mismatch | Use the exact saved package/runtime identity or create a fresh snapshot with current software |
| `packaged_examples_unavailable` | Reinstall the complete wheel; keep its package resources together |

## Developer reproduction

From the reviewed repository or extracted source archive:

```bash
python3.12 -m unittest discover -s tests -v
python3.12 tools/qualify_distribution.py --output /absolute/path/to/new-qualification
```

The output must be outside the source tree. The script builds a wheel and sdist,
rebuilds from that sdist, installs into two fresh venvs, checks installed examples
against the authoritative bytes, runs user workflows and verifies relocated
snapshots after deleting the original inputs. It also checks passive handling of
a canary source, malformed input, stale evidence and tampered reports. The result
is `qualification.json`, distributions, generated reports and command logs.

Only the fixed project-owned fixture builders execute programs, when a developer
explicitly runs those tools. Packaging, production commands and installation
qualification never run imported candidate programs or call models.
