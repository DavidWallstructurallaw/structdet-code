# StructDet Code

Analyze solution mechanisms, finite test observations and recorded code-revision trajectories.

**Development milestone: C05. Version: 0.1.0.dev5.** Passive source preparation,
bounded sorting and graph recognition, review import and compatible condition
comparisons, per-run trajectories, checkpoint cohorts, intervention/failure
evidence and exact offline replay are implemented. Installation and distribution
qualification remain C06 work.

## Follow an intervention and replay the result

From this source directory, on Linux with CPython 3.12.14:

~~~bash
python3 -m structdet_code trace --study examples/interventions/study.json --design examples/interventions/design.json --evidence examples/interventions/evidence.json --format markdown
python3 -m structdet_code snapshot --action trace --study examples/interventions/study.json --design examples/interventions/design.json --evidence examples/interventions/evidence.json --output /tmp/structdet-code-replay
python3 -m structdet_code replay --bundle /tmp/structdet-code-replay --format markdown
~~~

The output directory must be new. This designed example records RELAX, FIFO and
RELAX again. It distinguishes an explicitly copied reference from an alternative
instruction, and keeps a withheld reference separate from agent-visible exposure.
Two different defective mechanisms fail the same six finite inputs. These
observations establish neither autonomous recovery nor independent failures.

A snapshot copies the private study inputs, source/suite bytes and any supplied
material alongside the results. Keep the bundle private when its inputs are
private; the ordinary report omits raw programs and prompts. Replay verifies the
captured bytes, matching installed software/runtime identity, and exact recomputed
JSON and Markdown. It needs no original input directory, model call or candidate
execution. A software mismatch requires the matching software or a fresh
analysis snapshot. See [the C05 guide](docs/C05.md) and
[verification and reports](verification/C05.md).

To run all six supplied demonstrations and replay each analysis:

~~~bash
python3 tools/run_demonstrations.py --output /tmp/structdet-code-six-demos
~~~

Open its summary.md, then the result.md inside any named demonstration directory.

## Follow recorded repair histories

From this source directory, on Linux with CPython 3.12.14:

```bash
python3 -m structdet_code trace --study examples/trace/study.json --design examples/trace/concentration.json --format markdown
python3 -m structdet_code trace --study examples/trace/study.json --design examples/trace/stable.json --format markdown
python3 -m structdet_code trace --study examples/trace/study.json --design examples/trace/attrition.json --format markdown
```

These three designed examples distinguish improved finite correctness with
increased concentration, improved correctness with stable mechanism coverage,
and apparent mechanism loss when some runs stop early. Their histories and
conditions are stipulated; their receipts record actual tests of project-owned
programs. No model was called.

The first example has six runs at revision ordinals 0, 1 and 2. Passing increases
from 2/6 to 4/6 to 6/6; support falls from 3 to 2 to 1, with SCI 7/18, 5/9 and 1.
The second example reaches the same passing counts while support stays at 3 and
SCI stays at 7/18. The attrition example keeps stopped and unrecorded runs visible
and shows a constant mechanism in the two runs observed at every checkpoint.

`trace` returns the recorded source, mechanism, receipt and feedback sequence for
each run, alongside exact-ordinal available and matched cohort views. Missing
revisions stay missing. Repeated tests add evidence; single-run outputs retain
the trajectory without a population concentration series. See [the C04 guide](docs/C04.md)
and [the saved trajectory report](verification/c04_concentration.md).

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

## Compare graph conditions

```bash
python3 -m structdet_code compare --left examples/graph/left/study.json --right examples/graph/right/study.json --design examples/graph/comparison.json --format markdown
python3 -m structdet_code prepare --task unit-graph-distances --sources examples/graph/left/sources --output /tmp/structdet-code-graph-study --data-role fixture
```

The second task uses directed unit-cost edges and returns minimum hop distances.
Its three mechanism families are FIFO first discovery, minimum-label settlement
and repeated full-edge relaxation. Four exact rules include a recognizable FIFO
implementation with an incorrect distance increment. Correctness remains separate.

The supplied comparison is a designed fixture with no model calls. Its four-slot
prefix keeps a missing third position on the right and excludes the later fifth
output. A failed program stays in the observed population. All-classified SCI is
3/8 on the left and 1 on the right, with admitted populations of 4 and 3. These
values describe this fixture, with differing coverage and finite correctness.

For your studies, `comparison-template` creates a bound template with unknown
positions, budgets and collection protocol left blank. `compare` without a
completed design returns inventories and missing prerequisites. The comparison
checks task/frame, condition controls, budgets and explicit prefix accounting;
valid-classified contrasts additionally require a common supplied test scope.
See [the C03 guide](docs/C03.md) and [saved comparison](verification/c03_graph_comparison.md).

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
imported or built by any production command.

Do not relabel the example as empirical evidence. Descriptive material can use
`reviewed_import` for supplied human-review records or `static_or_reviewed` for
recomputed rule matches plus supplied reviews. AI proposals stay provisional.
The inspector checks record consistency and rule scope; it cannot authenticate
reviewers, origin claims or test execution.

The bounded integer-sorting pack requires a
self-contained `sort_values(values)` function, lists of 0..256 plain integers in
0..4095, a new sorted output list, unchanged input, and no imported or delegated
sorting. The eight declared families follow the task-relative Bench definitions.
C02 rules cover exact complete-module variants in eight families, not arbitrary
implementations of those algorithms. Different control flow, opaque calls,
hybrids and unsupported forms remain review cases. Recognition does not execute
sources or assert their correctness. The graph pack follows the same recognition
and review policy; weighted graphs and alternative output contracts are outside
its supported domain.

`tools/build_c01_fixture.py` is a developer utility for the seven named,
project-owned source files. It executes those files and regenerates their example
receipts. It takes no candidate-path argument and is separate from passive intake.
Run it only on the unmodified reviewed project fixture files. It is not an
untrusted-code runner or sandbox. `tools/build_graph_example.py` likewise runs
only four reviewed graph references and their presentation variants. It takes no
candidate input arguments and regenerates the designed graph example and receipts.

## Verification and next increment

`verification/C01.md` through `verification/C05.md` record checks and results.
Numerical parity was checked against StructDet-Bench's count component at a pinned source commit,
without using its task validation or claiming installation support for Bench on
this environment. `tools/check_bench_parity.py` reproduces the comparison when
given an explicitly trusted matching Bench checkout.

C01-C05 implement the record contract, static workflow, graph task, compatible
condition comparison, per-run/cohort trajectories, intervention/failure evidence
and replay. C06 qualifies installation, distributions and the complete first-run
experience.

Software: Apache-2.0. Documentation, task descriptors, fixture data and reports:
CC BY 4.0. Theory publications retain their separate licenses and are cited in
`SPEC.md`; their full texts are excluded. See `NOTICE` for asset boundaries.
