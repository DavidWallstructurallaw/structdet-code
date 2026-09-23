# StructDet Code

Inspect solution-mechanism records, finite test observations, and code revision links.

**Development milestone: C02. Version: 0.1.0.dev2.** Passive source preparation,
bounded static evidence, nine narrow sorting rules, review import and readable
coverage reports are implemented. Multi-run convergence analysis is the C04
increment. The complete product requires C01-C06.

## Inspect a sorting collection

Verified on Linux with CPython 3.12.14; no third-party runtime dependencies.
From this source directory:

```bash
python3 -m structdet_code inspect --study examples/static/study.json --format markdown
python3 -m structdet_code prepare --sources examples/minimal/sources --output /tmp/structdet-code-first-study --data-role fixture
python3 -m structdet_code inspect --study /tmp/structdet-code-first-study/study.json --format markdown
```

The output directory must be new. Preparation copies the seven project-owned
source files and supplies six exact rule assignments; the opaque implementation
remains unresolved. These six have three mechanisms and SCI 1/2. No validity
result is fabricated: this new collection has no test receipts. For your own
source directory, omit `--data-role fixture`; unknown origins stay unknown.

`review.json` is an unfilled decision template. A supplied human review can be
applied with `apply-review` into a new manifest while preserving old assignment
versions. AI proposals remain provisional. See [the C02 guide](docs/C02.md) for
commands, evidence policies, exact recognition boundaries and review fields.

## Run the C01 example

The verified environment is Linux with CPython 3.12.14. There are no third-party
runtime dependencies. From this source directory:

```bash
python3 -m structdet_code validate --study examples/minimal/study.json
python3 -m structdet_code inspect --study examples/minimal/study.json --format markdown
python3 -m structdet_code inspect --study examples/minimal/study.json --format json
python3 -m unittest discover -s tests -v
```

Inspection prints a result and leaves source files unchanged. Successful commands
exit 0. Malformed, contradictory, unsupported or inaccessible input exits 2 with
a bounded JSON error on stderr. `valid_records` means record validation succeeded.
It does not authenticate supplied reviewers or test execution.

Saved example output is in `verification/minimal_report.md` and
`verification/minimal_report.json`. The JSON result also includes source digests,
source line anchors, explicit revision ancestry and missing-history information.
Raw programs, private prompts and free-form feedback are not emitted in these reports.

The example is designed software-fixture material with zero model calls. Seven
source files and seven stipulated run roots describe ten revisions, including an
input-copy fix, a no-op revision and a mechanism-changing edit. The test receipts
record 100 actual executions of these reviewed project-owned functions against a
ten-case property suite. Their mechanism labels and run histories are stipulated
for software testing; no real agent convergence experiment is claimed.

| Selected initial-revision population | n | Class counts | Support | SCI |
| --- | ---: | --- | ---: | ---: |
| All admitted labels | 5 | INS 3, MERGE 1, SEL 1 | 3 | 11/25 |
| Admitted labels with passing finite validity | 4 | INS 2, MERGE 1, SEL 1 | 3 | 3/8 |

All seven initial revisions remain in the ledger. One opaque implementation and
one model-style proposal are unadmitted. The latter passes the finite tests but
its misleading proposed class is excluded from both distributions. The deliberate
input-reuse defect remains classifiable as insertion while failing validity.

## Input and development boundaries

`SPEC.md` defines the current contract, policies, reuse decision and next
increments. `examples/minimal/study.json` is a complete working example. Payload
paths are relative to that manifest and must remain inside its directory without
symlinks. JSON inputs are passive records. No imported candidate is executed,
imported or built by `validate` or `inspect`.

Do not relabel the example as empirical evidence. Descriptive material can use
`reviewed_import` for supplied human-review records or `static_or_reviewed` for
recomputed rule matches plus supplied reviews. AI proposals stay provisional.
The inspector checks record consistency and rule scope; it cannot authenticate
reviewers, origin claims or test execution.

Only the bounded integer-sorting pack is currently implemented. The task requires a
self-contained `sort_values(values)` function, lists of 0..256 plain integers in
0..4095, a new sorted output list, unchanged input, and no imported or delegated
sorting. The eight declared families follow the task-relative Bench definitions.
C02 rules cover exact complete-module variants in eight families, not arbitrary
implementations of those algorithms. Different control flow, opaque calls,
hybrids and unsupported forms remain review cases. Recognition does not execute
sources or assert their correctness.

`tools/build_c01_fixture.py` is a developer utility for the seven named,
project-owned source files. It executes those files and regenerates their example
receipts. It takes no candidate-path argument and is separate from passive intake.
Run it only on the unmodified reviewed project fixture files. It is not an
untrusted-code runner or sandbox.

## Verification and next increment

`verification/C01.md` and `verification/C02.md` record checks and results.
Numerical parity was checked against StructDet-Bench's count component at a pinned source commit,
without using its task validation or claiming installation support for Bench on
this environment. `tools/check_bench_parity.py` reproduces the comparison when
given an explicitly trusted matching Bench checkout.

C02 implements bounded static observations, scoped recognizers, review preparation
and a practical sorting-source workflow. C03 adds the graph pack and compatible
condition comparison. C04 adds per-run and cohort convergence analysis. C05 adds
integrated replay and intervention handling. C06 qualifies distributions and the
complete first-run experience.

Software: Apache-2.0. Documentation, task descriptors, fixture data and reports:
CC BY 4.0. Theory publications retain their separate licenses and are cited in
`SPEC.md`; their full texts are excluded. See `NOTICE` for asset boundaries.
