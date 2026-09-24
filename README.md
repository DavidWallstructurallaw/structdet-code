# StructDet Code: Code Diversity and Coding Agent Evaluation

**See when better test results come with fewer solution strategies.**

An offline Python toolkit for **LLM evaluation**, **algorithmic diversity** and
**coding agent trajectory analysis**. Inspect recorded code solutions, compare
their underlying mechanisms, and track how those mechanisms change across
revisions alongside the supplied test results.

Current task packs cover **bounded integer sorting** and **minimum hop distances
on directed unit-edge graphs**. Labels come from narrow static rules or supplied
source-bound reviews; unfamiliar code remains unresolved. No model account or
third-party runtime dependency is required.

## Questions you can investigate

| Your question | What StructDet Code reports |
| --- | --- |
| How diverse are the algorithms in an LLM code generation collection? | Admitted mechanism families, coverage, unresolved cases and concentration |
| Does iterative code repair improve correctness while narrowing solution diversity? | Recorded revision trajectories with finite passing, mechanism support and concentration at explicit checkpoints |
| Do two generation conditions produce different solution distributions? | Compatible condition comparisons with fixed-prefix selection and explicit missing outputs |
| Does apparent convergence come from some runs stopping early? | Available and matched cohorts, stopped runs and missing observations |
| What was recorded when a previously seen strategy returned? | Reappearance, supplied interventions, reference-byte matches, exposure and unknown provenance |
| Can someone reproduce the analysis later? | Captured passive inputs and exact offline replay of JSON and Markdown reports |

## Example: correctness improves while strategy coverage shrinks

In one supplied six-run fixture, passing increases while the number of observed
mechanism families falls:

| Revision ordinal | Runs passing the supplied finite tests | Mechanism families observed | SCI |
| --- | --- | --- | --- |
| 0 | 2/6 | 3 | 7/18 |
| 1 | 4/6 | 2 | 5/9 |
| 2 | 6/6 | 1 | 1 |

A second fixture reaches the same passing counts while retaining three families
and SCI 7/18 throughout. The reports let you see both outcomes.

SCI is the sum of squared admitted class proportions. Higher SCI means greater
concentration in that observed population. Coverage and correctness are reported
separately. These are designed project-owned demonstrations, with stipulated
histories and finite receipts; they do not establish empirical model behavior.

## Try the six demonstrations

Version **0.1.0** is prepared in [C06 PR #5](https://github.com/DavidWallstructurallaw/structdet-code/pull/5).
Before a tagged release is published, try the candidate source directly:

~~~bash
git clone --branch codex/c06-release-readiness --single-branch https://github.com/DavidWallstructurallaw/structdet-code.git
cd structdet-code
python3.12 -m structdet_code demo --output ./first-demo
~~~

Use **Linux with CPython 3.12.14**, the qualified environment. The source demo
requires only the Python standard library. Choose a new output directory, then
open `first-demo/summary.md` and a scenario's `result.md`. All six analyses are
saved and exactly replayed without a model call or candidate execution.

| Demonstration | What to inspect |
| --- | --- |
| `surface` | Presentation variants retain their mechanism; admitted sorting counts are INS=4, MERGE=1, SEL=1 |
| `mechanisms` | FIFO, SETTLE and RELAX under one graph task; differing condition distributions |
| `concentration` | Passing 2/6, 4/6, 6/6 with mechanism support 3, 2, 1 |
| `stable` | The same passing counts with support 3 and SCI 7/18 throughout |
| `attrition` | Available counts 5, 2, 2; the matched pair retains FIFO |
| `interventions` | RELAX reappears; copied/withheld references and shared failures remain distinct |

The prepared wheel also includes all examples and works outside a checkout.
If you have downloaded that artifact:

~~~bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps /absolute/path/structdet_code-0.1.0-py3-none-any.whl
.venv/bin/structdet-code demo --output ./installed-demo
~~~

There is no published PyPI package or tagged GitHub Release yet. See
[installation and troubleshooting](docs/INSTALL.md) for source-archive installation
and the supported environment. Other Python versions and operating systems are
unqualified; safe input handling requires POSIX no-follow file operations.

## Analyze your own code collection

The following examples use the source checkout from above. In an installed
environment, replace `python3.12 -m structdet_code` with `structdet-code`.

~~~bash
python3.12 -m structdet_code prepare --sources /absolute/path/to/python-sources --output ./my-study
python3.12 -m structdet_code inspect --study ./my-study/study.json --format markdown
~~~

Preparation copies selected `.py` files into a new study and creates an unfilled
`review.json`. The default task is bounded sorting; add
`--task unit-graph-distances` for the graph task. The default data role is
`descriptive`; origins, test results and earlier history remain unknown until
supplied. Candidate source is parsed as data and never executed.

Review unresolved cases using the copied sources and source-line evidence,
then apply actual decisions into a new manifest:

~~~bash
python3.12 -m structdet_code apply-review --study ./my-study/study.json --review ./my-study/review.json --output ./my-study/reviewed.json
~~~

Prior assignments are preserved. AI suggestions remain provisional. See the
[input guide](docs/INPUTS.md) for task contracts, portable study records and how
to read classification coverage, unknowns and finite correctness.

## Analyze a recorded agent trajectory

Export the bundled input examples, inspect a history and preserve the result:

~~~bash
python3.12 -m structdet_code examples --output ./example-inputs
python3.12 -m structdet_code trace --study ./example-inputs/interventions/study.json --design ./example-inputs/interventions/design.json --evidence ./example-inputs/interventions/evidence.json --format markdown
python3.12 -m structdet_code snapshot --action trace --study ./example-inputs/interventions/study.json --design ./example-inputs/interventions/design.json --evidence ./example-inputs/interventions/evidence.json --output ./saved-analysis
python3.12 -m structdet_code replay --bundle ./saved-analysis --format markdown
~~~

For your own histories, supply actual revision ordinals, parent links, source
artifacts, test receipts and feedback using the documented JSON study format.
Plain source preparation creates standalone observations; it cannot reconstruct
missing agent actions. Provider-specific log adapters are not included.

A snapshot contains private input bytes and both report formats. Move the whole
directory to retain it. Replay needs matching installed code, task data, Python
implementation/version and platform family, then verifies the inputs and
recomputes both reports exactly. Keep private snapshots private; ordinary reports
omit raw programs and prompts.

## How this fits into code evaluation

**Alongside correctness metrics.** Use the reports with your supplied test
results to examine algorithmic diversity and solution convergence. StructDet Code
does not calculate pass@k or run HumanEval, MBPP or SWE-bench. It accepts recorded
evidence for its supported task contracts.

**Recorded revision analysis.** Agent trajectory analysis here covers programs,
parent relationships, selected paths, tests, feedback and optional interventions.
It provides offline reports and replay. Live tracing integrations, tool-call
instrumentation and a production observability dashboard are outside this version.

**Evidence-qualified conclusions.** Unknown cases stay outside hard mechanism
counts. Empty admitted populations have undefined SCI; single-run traces retain
their sequence without a population concentration series. An observed reappearance,
reference-byte match or temporal association does not establish autonomous
recovery or causality. Supplied provenance, reviewers and execution claims are
not authenticated. Fitted half-life and external recovery estimates are absent.

Successful commands exit 0. Record, binding and bounded I/O errors exit 2 with
JSON on stderr; argument errors use argparse's usage message. `validate` checks
record consistency without running candidate tests.

## Documentation, verification and related work

- [Installation](docs/INSTALL.md) and [input preparation](docs/INPUTS.md)
- [Sorting rules and review fields](docs/C02.md)
- [Graph task and condition comparison](docs/C03.md)
- [Revision histories and cohort fields](docs/C04.md)
- [Interventions, failure profiles, corrections and replay](docs/C05.md)
- [Specification and theory-source attribution](SPEC.md)
- [Related work and contribution boundaries](docs/RELATED_WORK.md)
- [Release preparation](docs/RELEASE.md) and [change history](CHANGELOG.md)
- [C06 installation verification](https://github.com/DavidWallstructurallaw/structdet-code/blob/codex/c06-release-readiness/verification/C06.md)

C06 passed 142 regression methods and both installed distribution routes. Each
route exercised six demonstrations and exact replay outside the checkout.
See the linked record for artifact identities and the precise qualification scope.

Algorithmic diversity and user-defined structural diversity have direct research
precedents, acknowledged in the related-work guide. This project contributes
its documented evidence and recorded-revision workflow without claiming a
universal classifier or reproduced comparative superiority.

Python source, tests, tools and configuration use Apache-2.0. Documentation,
task descriptors, fixture JSON/plain-text material and reports use CC BY 4.0.
See [NOTICE](NOTICE) for asset boundaries. The cited theory publications retain
their separate licenses; their full texts are excluded from the distributions.
