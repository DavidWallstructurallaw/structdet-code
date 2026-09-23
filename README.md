# StructDet Code

Inspect solution-mechanism records, finite test observations, and code revision links.

**Development milestone: C01. Version: 0.1.0.dev1.** This delivery establishes
the task contract, passive input path, exact metrics and runnable project fixtures.
Mechanism recognition and review preparation are the C02 increment. Multi-run
convergence analysis is the C04 increment. The complete product requires C01-C06.

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

Do not relabel the example as empirical evidence. Real descriptive material uses
`reviewed_import` and supplied human-review records with source anchors. AI
proposals stay provisional. The inspector checks the consistency of those records;
it cannot establish their authenticity or substantive accuracy.

Only the bounded integer-sorting pack is implemented in C01. The task requires a
self-contained `sort_values(values)` function, lists of 0..256 plain integers in
0..4095, a new sorted output list, unchanged input, and no imported or delegated
sorting. The eight declared families follow the task-relative Bench definitions.
No automatic recognizer is advertised by this milestone.

`tools/build_c01_fixture.py` is a developer utility for the seven named,
project-owned source files. It executes those files and regenerates their example
receipts. It takes no candidate-path argument and is separate from passive intake.
Run it only on the unmodified reviewed project fixture files. It is not an
untrusted-code runner or sandbox.

## Verification and next increment

`verification/C01.md` records the actual checks and results. Numerical parity was
checked against StructDet-Bench's count component at a pinned source commit,
without using its task validation or claiming installation support for Bench on
this environment. `tools/check_bench_parity.py` reproduces the comparison when
given an explicitly trusted matching Bench checkout.

C02 adds bounded static observations, reviewed recognizers, review preparation
and a practical sorting-source workflow. C03 adds the graph pack and compatible
condition comparison. C04 adds per-run and cohort convergence analysis. C05 adds
integrated replay and intervention handling. C06 qualifies distributions and the
complete first-run experience.

Software: Apache-2.0. Documentation, task descriptors, fixture data and reports:
CC BY 4.0. Theory publications retain their separate licenses and are cited in
`SPEC.md`; their full texts are excluded. See `NOTICE` for asset boundaries.
