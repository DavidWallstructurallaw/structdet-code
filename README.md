# StructDet Code

Analyze solution-mechanism diversity and coding-agent convergence from recorded
programs, test results, and revision histories.

**Version 0.1.0, prepared for release in C06.** This repository provides passive
analysis of bounded sorting and unit-edge graph tasks, source-bound reviews,
compatible condition comparisons, revision trajectories, intervention/failure
evidence and exact offline replay. The prepared artifacts have not been published
to PyPI or as a tagged GitHub Release.

Qualified environment: **Linux, CPython 3.12.14**. No third-party runtime
dependencies or model account. Python metadata sets a 3.12 minimum; other Python
versions and operating systems have not been qualified. Input handling requires
POSIX no-follow file operations.

## Install and run

With the prepared wheel downloaded to an absolute path:

~~~bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps /absolute/path/structdet_code-0.1.0-py3-none-any.whl
.venv/bin/structdet-code --version
.venv/bin/structdet-code demo --output ./first-demo
~~~

The output directory must be new. Open `first-demo/summary.md`, then a named
scenario's `result.md`. The installed command creates and exactly replays all six
analyses without a source checkout, model call or candidate execution. The same
CLI is available as `.venv/bin/python -m structdet_code`.

| Demonstration | What the owned fixture shows |
| --- | --- |
| `surface` | Presentation variants retain their mechanism; admitted sorting counts are INS=4, MERGE=1, SEL=1 |
| `mechanisms` | Different graph mechanisms under one task; left SCI 3/8, right SCI 1 |
| `concentration` | Passing 2/6, 4/6, 6/6 with support 3, 2, 1 and SCI 7/18, 5/9, 1 |
| `stable` | The same passing counts with support 3 and SCI 7/18 throughout |
| `attrition` | Available counts 5, 2, 2; the matched pair retains FIFO |
| `interventions` | RELAX reappears; copied/withheld references and shared failures remain distinct |

These are designed project-owned fixtures. Their stipulated histories and finite
test receipts do not establish empirical model behavior.

See [installation and troubleshooting](docs/INSTALL.md) for the source-distribution
route, exact support scope and developer verification.

## Inspect examples and your own sources

Export the packaged examples into a new directory, then inspect a collection:

~~~bash
.venv/bin/structdet-code examples --output ./example-inputs
.venv/bin/structdet-code inspect --study ./example-inputs/static/study.json --format markdown
.venv/bin/structdet-code prepare --sources /absolute/path/to/python-sources --output ./my-study
.venv/bin/structdet-code inspect --study ./my-study/study.json --format markdown
~~~

`prepare` copies selected `.py` source bytes and creates `study.json` and an
unfilled `review.json`. Sources stay passive. Origins, test results and earlier
history remain unknown unless supplied. The default data role is `descriptive`;
use `fixture` only for an explicitly designed example. For graph programs, add
`--task unit-graph-distances`. See the [input guide](docs/INPUTS.md) for contracts,
review decisions and portable recorded histories.

Reports keep mechanism coverage, unknown cases and finite correctness separate.
SCI is the exact finite-population sum of squared class proportions; an empty
admitted population has undefined SCI. A high value describes concentration in
the specified observed population. It does not establish correctness, general
model capacity loss or independent sampling. Single-run traces show sequences
without a population concentration series.

## Follow an agent history and replay it

After exporting examples:

~~~bash
.venv/bin/structdet-code trace --study ./example-inputs/interventions/study.json --design ./example-inputs/interventions/design.json --evidence ./example-inputs/interventions/evidence.json --format markdown
.venv/bin/structdet-code snapshot --action trace --study ./example-inputs/interventions/study.json --design ./example-inputs/interventions/design.json --evidence ./example-inputs/interventions/evidence.json --output ./saved-analysis
.venv/bin/structdet-code replay --bundle ./saved-analysis --format markdown
~~~

A snapshot includes the private input bytes and both report formats. Move the
whole directory to retain it. Replay requires matching installed package code,
task data, Python implementation/version and platform family; it verifies the
captured bytes and recomputes exact JSON and Markdown. A different version needs
its own fresh analysis or the original matching environment. Keep private inputs
and snapshots private; ordinary reports omit raw programs and prompts.

## Scope and evidence

The current task packs cover bounded integer sorting and minimum hop distances
on directed unit-edge graphs. Whole-module rules recognize a small, explicit set
of implementations; human review can supply additional source-bound decisions.
Unknowns and unsupported forms remain outside hard mechanism counts. AI
suggestions remain provisional. Classification does not certify correctness.

Recorded revisions retain parent links, actual ordinals, test scope, selection,
stopping and missingness. Compatible cohorts show concentration alongside finite
correctness. Interventions preserve visibility and reuse claims; a reappearance,
equal reference bytes or temporal association does not establish autonomous
recovery or causality. Supplied provenance/reviewer/execution claims are not
authenticated. There is no generic algorithm classifier, provider-specific log
adapter, untrusted-code runner, fitted half-life or external recovery estimator.

Successful commands exit 0. Record, binding, unsupported-input and bounded I/O
errors exit 2 with JSON on stderr; argument errors use argparse's usage message.
`validate` confirms record consistency, without executing tests.

## Documentation and provenance

- [Input preparation and reading results](docs/INPUTS.md)
- [Sorting rules and review fields](docs/C02.md)
- [Graph task and condition comparison](docs/C03.md)
- [Revision histories and cohort fields](docs/C04.md)
- [Interventions, profiles, corrections and replay](docs/C05.md)
- [Specification and theory-source attribution](SPEC.md)
- [Related work and contribution boundaries](docs/RELATED_WORK.md)
- [Release preparation](docs/RELEASE.md) and [change history](CHANGELOG.md)
- [C06 installation verification](https://github.com/DavidWallstructurallaw/structdet-code/blob/main/verification/C06.md)

Python source, tests, tools and package configuration use Apache-2.0.
Documentation, task descriptors, fixture JSON/plain-text material and reports
use CC BY 4.0. See [NOTICE](NOTICE) for asset boundaries and attribution.
The cited theory publications retain their separate publication licenses;
their full texts are excluded from the distributions.
