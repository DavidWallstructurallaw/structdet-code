# StructDet Code specification

Version 0.4, extended for the owner-authorized C04 increment on 2026-09-23.

## 1. Product and increment boundary

The complete product analyzes task-relative mechanisms in collections of programs
and their recorded build/test/patch histories. Correctness observations, mechanism
assignments, realization differences and revision events remain separate axes.

C01 delivered a passive contract, runnable package skeleton, exact count
arithmetic, source-bound records and a small trace-shaped fixture. C02 adds
source preparation, bounded static evidence, narrow whole-module recognition,
review templates/import and classification coverage. C03 adds the bounded graph
pack and compatible descriptive condition comparison with explicit fixed-prefix
selection. C04 adds actual-ordinal trajectories, selected-path transitions,
available/matched checkpoint cohorts, stopping/missingness and joint finite
correctness/concentration reporting. C05/C06 remain required. Fitted half-life,
external recovery metrics, strict replay, provider adapters and untrusted
execution are not implemented.

## 2. Reuse decision

Baseline inspected: `DavidWallstructurallaw/structdet-bench`, commit
`0a9dc88deffd4b14264485b161bea06f027f68f5`, version 0.1.0.

| Candidate | Source finding | Decision |
| --- | --- | --- |
| Support and SCI | `structdet_bench.metrics.count_metrics` accepts a supplied count table and returns exact SCI fractions with empty/invalid states | Independently implement the stated finite-count mathematics; compare support, SCI and derived Gini-Simpson against this pinned function |
| Runtime dependency | Package metadata requires Python 3.13; the metrics module imports population, evidence, inventory and input modules; the README exposes bundle/study workflows rather than a separately supported count-only package API | No Bench runtime dependency in Code; C01 is qualified on available Linux/CPython 3.12.14 |
| Sorting task | `HERO_BENCHMARK_SPEC.md` defines a bounded domain and eight task-relative classes | Adapt its task descriptors under CC BY 4.0, retaining attribution and an explicit source pin |
| Input and evidence | Bench's M/V/L carriers implement a larger registered-study contract | Give Code its own compact record contract and evidence policies; do not bypass Bench validation or claim compatible carrier import |
| Longitudinal methods | Revision clocks, branch selection and success-dependent stopping need code-specific semantics | Build the revision layer in Code; assess any later numerical reuse against its actual assumptions |

The Code arithmetic implementation copies no Bench function bodies. The domain
descriptors are attributed adaptations. The optional parity check imports only
an explicitly trusted Bench source checkout in a separate developer process.
It is an arithmetic cross-check on the current environment, not upstream runtime
qualification or independent empirical validation. Fixed parity values and the
source identity are retained in the verification output.

## 3. Task and mechanism resolution

The sorting pack is `sorting-bounded/0.1`; its bytes and version are bound to
each study and assignment. It adopts `bounded_integer_sort/0.1` at
`sorting_mechanism_family/0.1` from the baseline.

- Input: plain lists of plain integers, length 0..256, keys 0..4095; no bools.
- Output: a new nondecreasing plain list with unchanged multiplicities; leave
  the caller's input unchanged.
- Allowed: self-contained Python loops, recursion, comparisons, integer
  operations, local containers and ordinary non-ordering builtins.
- Prohibited: imports, delegated sorting, dynamic execution, reflection,
  randomness, filesystem/network/process operations and persistent state.
- Consequence horizon: one complete invocation over the declared input domain.
- Mechanism signature: how ordering information is acquired, maintained and
  used to place values, including reachable nontrivial branches.
- Resolution ignores identifiers, formatting, comments, helper layout and
  equivalent recursion/explicit-stack or storage changes.

Eight hard classes: `SORT-ADJ`, `SORT-INS`, `SORT-SEL`, `SORT-MERGE`, `SORT-PIVOT`,
`SORT-HEAP`, `SORT-COUNT`, `SORT-RADIX`. Their operative distinctions and near
boundaries are in `structdet_code/tasks/sorting.json`. An algorithmic component
inside another strategy is not a second observation. A general alternate sorter
on subproblems larger than two creates an unresolved hybrid unless a new
versioned descriptor explicitly admits it.

Classification unknowns retain a reason: `insufficient_evidence`,
`unsupported_syntax`, `opaque_dependency`, `unresolved_reachability`, `hybrid`,
`schema_gap`, `review_disagreement`, or `not_reviewed`. No unknown bucket becomes
a ninth mechanism. A schema-gap case preserves its source and evidence. Revising
the class boundaries requires a new task-pack version and explicit reassessment.

The second implemented task is single-source shortest-path distances
on finite directed unit-edge graphs, `shortest_distances(node_count, edges, start)`.
Use 1..128 numbered vertices; start must be a vertex; edges are directed pairs of
plain integer vertices, with 0..16384 pairs, loops and duplicates allowed. Return a new length-n
list of nonnegative integer hop distances, with `None` for unreachable vertices;
leave supplied data unchanged. No imports or opaque graph solvers. The pack is
`unit-graph-distances/0.1`, resolution `distance_propagation_family/0.1`.
Its hard classes are `DIST-FIFO` (first-discovery FIFO or breadth layers),
`DIST-SETTLE` (global minimum tentative label selection and once-only finalization)
and `DIST-RELAX` (repeated complete-edge passes without per-vertex settlement).
A relaxation component does not create a second class. Queue-based repeated
correction, DAG-only propagation and reachable hybrids need unresolved review or
a new descriptor. Weighted graphs, arbitrary labels, undirected-mode switches and
path reconstruction are outside this contract. Four complete-module rules cover
these three families, including a FIFO distance-increment defect. The original
sorting pack bytes and rule meanings are unchanged. Both packs share the existing
intake, assignment, review, receipt, counting and reporting architecture.

## 4. Compact study contract

New UTF-8 JSON manifests use `schema_version: structdet-code.study/0.2`. Original
C01 `structdet-code.study/0.1` sorting manifests remain readable without the new
policy, graph pack and snapshot variants. Their relative local source and suite files are passive
payloads. Unknown fields are
rejected, so executable hooks cannot be smuggled into extensions.

| Field | Required record meaning |
| --- | --- |
| `study_id`, `data_role`, `evidence_policy` | Explicit identity; fixture/fixture_only, descriptive/reviewed_import, or either material role with static_or_reviewed in schema 0.2 |
| `task` | pack_id, pack_version, resolution_id, exact pack_sha256 |
| `configurations` | id, model, prompt, settings, selection_rule; unavailable metadata stays null |
| `artifacts` | id, relative path, exact sha256, python language, entry_point, origin, capture_status |
| `assignments` | id, artifact_id, source_sha256, pack_sha256, positive revision, status, basis, class_id, reason, reviewer_ref, evidence; optional note and rule_id |
| `suites` | id, passive JSON path, exact sha256, oracle_id |
| `receipts` | id, revision_id, artifact_id, source_sha256, suite_id, suite_sha256, environment, status, attempted/completed/passed, conformance, visibility, execution_basis |
| `runs` | id, configuration_id, declared root_group_id or null, stop_reason, endpoint_revision_id or null |
| `revisions` | id, run_id, actual ordinal, artifact_id, parents, explicitly missing_parents, kind, feedback_ids |
| `feedback` | id, examined revision_id, kind, optional receipt_id, visible_to_agent |
| `selection` | Explicit revision_id, optional assignment_id and receipt_id, at most one selected revision per run |

The fixture is the executable format example. IDs are bounded ASCII identifiers.
All record references, source digests, task digests, suite digests and source-line
anchors are checked. Assignment revision is a review-version clock, distinct from
the code revision ordinal. Older assignment records can remain, but a selection
must explicitly name the highest recorded assignment revision for its artifact.

The C01 suite carrier is `structdet-code.sort-suite/0.1`, with oracle identity
`sort-properties/0.1` and uniquely identified literal input cases. These carriers
are parsed, never executed. Arbitrary external harness import mappings are later
work and must preserve their original suite/oracle meanings.

The graph carrier is `structdet-code.graph-suite/0.1` with oracle
`unit-distance-properties/0.1`. Each case has an `id` and literal `input` object
containing `node_count`, `edges` and `start`, checked against the graph bounds.
The loader checks shape and bindings; it does not compute candidate outcomes.

## 5. Evidence and validity states

| Assignment status/basis | Current treatment |
| --- | --- |
| accepted + fixture | Admitted only under fixture_only, with complete source and nonempty in-range explanatory anchors; stipulated fixture evidence |
| accepted + human_review | Admitted under reviewed_import or static_or_reviewed, with reviewer reference and source anchors; supplied-review-record-qualified, not authenticated or independently validated |
| proposed + model_assisted | Candidate label may be displayed; excluded from admitted counts |
| unresolved or conflicted | class_id is null, a specific reason is required; excluded from admitted counts |
| accepted + static_rule | Admitted only under static_or_reviewed; recompute the complete rule and require matching class, rule identity and exact generated anchors |

Well-formed evidence fields cannot prove that a review occurred or that its
judgment is correct. Reports always retain `substantive_validation_performed:
false`. The inspector imports claims, checks bindings and computes conditional summaries.
It never labels a model-assisted proposal as independent human evidence.

A receipt binds a single exact revision, artifact and suite, including environment.
Its execution basis is `project_fixture_execution`, `fixture_stipulated` or
`external_report`; real descriptive imports require external_report. A complete
passing finite-test status requires attempted = completed = passed = suite size.
A failed status needs at least one completed failed test. Timeout, partial and
harness error remain distinguishable. Supplied source/interface conformance is
separate from functional test status.

The validity projection is `passed_under_supplied_scope` only for complete finite
test passing plus supplied passing conformance. A failed test or failed
conformance yields failed. Other supplied receipts yield undetermined. No receipt
yields not_assessed. This projection does not claim universal domain correctness,
deployment safety or authenticated execution.

## 6. Observation identity and revisions

Source byte identity and observation identity are separate. Distinct run roots
with identical source bytes remain distinct selected observations; the unique
byte inventory is a separate field. Repeated receipts add no selected observation.
An unchanged-byte `no_op` requires one parent with equal source digest. An `edit`
requires one parent with different bytes. A `merge` has at least two parents.
Initial `generation` records have no parents. Each run has at most one initial
generation or standalone snapshot, and ordinals are unique within the run.

Schema 0.2 adds `snapshot`, a standalone supplied observation with no claimed
generation or known ancestry. Preparation allocates one explicit collection slot
per selected file, uses ordinal zero only within that slot and leaves origin
groups, stopping, model, prompt and test results unknown. Filename order supplies
stable slot IDs, not chronology or independence. Snapshots have no parents and
do not increment the generation-record count.

Known parents must belong to the same run and have smaller actual ordinals. This
rejects cycles and future-parent links. Missing parents are allowed only when
explicitly named as missing. Gaps are retained as intervals, not renumbered,
filled or interpreted as an observed transition. Cross-run parent links are
unsupported in this initial contract; shared origin remains visible through
root_group_id and artifact origin.

Feedback may be received only by a later descendant of the examined revision.
A receipt-bearing event must name that exact revision's receipt. Withheld or
unknown-visibility receipts cannot be exposed as agent-visible feedback. Endpoints
and stop reasons remain supplied observations; no passing program is propagated
into later absent checkpoints.

C01 inspection returns these original links. C04 `trace` computes per-run
mechanism transitions and task-compatible multi-run checkpoint distributions,
including matched/available cohorts, branch decisions, stopping and attrition.
One selected program cannot establish a model-level concentration trend. No
recursive-training clock is assigned to ordinary repair.

## 7. Metrics, reporting and limits

For admitted hard counts n_z and n = sum(n_z): support is the number of positive
counts; empirical SCI = sum(n_z^2)/n^2; Gini-Simpson = 1 - SCI. Fractions are
retained exactly. No smoothing, finite-sample correction, confidence interval or
capacity inference is added. Invalid count totals are rejected. A known empty
classified population has support zero, undefined SCI/diversity and an explicit
qualifier. Failed intake produces no successful empty result.

`classified_all` includes admitted mechanisms regardless of validity.
`classified_valid` additionally requires passed_under_supplied_scope. Each view
retains its denominator and class counts. The ledger preserves selected attempts,
source inventory, assignment states, unadmitted reasons and validity states.
Tasks, conditions and revisions are not silently pooled into one capacity score.

JSON is the canonical result. Markdown uses the same object. Source references
are artifact IDs, digests and line spans; reports omit raw code, prompt bytes and
free-form logs. The top-level result states whether execution and recognition
were performed. Result schema 0.2 includes per-source bounded static observations,
admitted-basis counts and coverage denominators. Byte fingerprints identify inputs but are not a strict replay
implementation; replay is C05.

Intake limits: 1 MiB per JSON file; 256 KiB per source; 4 MiB cumulative reads;
24 JSON nesting levels; 128 sources/runs, 512 assignments/revisions, 1024
receipts/feedback events, 16 suites and 128 selections. Files must be regular,
relative, no-follow payloads. Resource refusal is an input error, not truncation.
The currently qualified input platform is Linux/POSIX with no-follow descriptor
operations. The package's Python lower bound does not assert a full platform matrix.

## 8. Remaining delivery sequence

| Increment | Exit |
| --- | --- |
| C01 | This specification, working skeleton, source/trace fixture, targeted checks and numerical parity |
| C02 | Implemented: bounded static extraction, exact scoped recognizers/review workflow, source preparation and sorting analysis |
| C03 | Implemented: graph task pack, exact graph rules and compatible fixed-prefix condition comparisons |
| C04 | Implemented: individual trajectories, selected-path transitions, available/matched checkpoint cohorts and joint correctness/concentration |
| C05 | Intervention records, integrated correction behavior, optional failure profiles, exact replay and six demonstrations |
| C06 | Actual package installation, first-run documentation, supported-platform qualification and release readiness |

No new approval registry, historical test-body preservation system or phase-specific
runner is required. Use the current tests during development, full regression for
integrated candidates and distribution qualification at release. There is no
fixed target test count. C05 is the next required implementation increment.

### C02 rule and review contract

The precise subset and user commands are in `docs/C02.md`. Scope
`sorting-whole-module-alpha-ast/1` permits leading docstring/comment/format changes
and consistent bijective non-reserved identifier renaming. It retains the complete
operative AST, including literal types, branches, calls, binding-name equality
and ordering. Nine rule identities cover eight sorting families, including one
input-alias defect with a recognizable insertion mechanism. No partial-pattern
vote or AST similarity score creates an assignment.

Automatic parsing has separate limits of 64 KiB/source, 4096 lexical tokens,
4096 AST nodes and depth 64. Invalid or resource-limited parsing is an explicit
unresolved analysis state, not a completed empty class result. Unmatched but
readable sources can still receive supplied human review. Syntax findings are
bounded to 32 per source with an omission count; rule anchors are bounded to eight.

`prepare` creates a new copied bundle, blank review template and recomputable
static assignments without test receipts. `review-template` binds blank decisions
to the study digest, task digest, source digests and current assignment IDs.
`apply-review` validates those bindings, appends assignment versions and explicitly
updates selected assignments, while preserving source/revision/receipt history.
Outputs are exclusive new files; existing outputs are refused. A changed source,
stale study, out-of-range anchor, model proposal promoted to accepted, or selected
accepted human label contradicting a rule under static_or_reviewed is rejected.
The reviewer can preserve disagreement as an unadmitted conflicted record.

### C03 condition comparison contract

`compare` consumes two validated studies and an optional passive
`structdet-code.comparison/0.1` design. `comparison-template` fills known study
bindings and selected revision IDs, leaving collection order, budget, planned
positions, protocol and varied field unknown. Filename order and code revision
ordinals never establish collection positions. See `docs/C03.md` for exact fields.

Comparisons require the same task/frame, material role and evidence policy, one
known chosen configuration per side, known model/prompt/settings, one declared
changed field and identical remaining fields/within-run selection rules. They
also require a supplied common protocol, equal positive per-slot budget limits,
one prefix size, and explicit slot accounting. These are supplied design claims,
not authenticated provenance, independently measured expenditure or causal evidence.

Every selected revision in the chosen configuration must map once to a unique
positive collection position within the planned count. Each requested prefix
position must explicitly name its selected revision or null for a missing output.
Incomplete accounting makes the prefix unavailable. Missing positions never take
later replacements. Failed, unresolved and undetermined observations remain in
the observed prefix, with separate classified and finite-passing subsets.
The later selected records are excluded and listed. Different total planned
counts are allowed when both cover the same requested prefix and per-slot budget.

All-classified differences are conditional descriptive right-minus-left changes
in support, exact SCI and Gini-Simpson. Their operands retain admitted population
sizes, observed/requested coverage, validity states and missingness. The
valid-classified difference additionally requires receipts for every observed
prefix output and one identical suite/oracle/environment/execution-basis scope
across both sides. Missing or changed test scopes block this difference without
blocking an otherwise compatible mechanism comparison. Empty classified
populations retain zero support and undefined SCI, and produce no numeric delta.

Results expose configuration fingerprints, root-group declarations, source
overlap and exact bindings, without raw prompts/settings/protocol text. No
independence, confidence interval, general capacity loss or causal effect follows
from these descriptive differences. Unspecified designs and incompatible studies
return separate side inventories, explicit reasons and unavailable contrasts;
they do not produce a pooled score. Malformed or stale bindings fail intake.
Limits: two studies at their existing per-study bounds; one 1 MiB design; prefix
1..128, planned positions 1..10000 and at most 256 slot records per side.

### C04 revision and cohort contract

The original study schema remains 0.2. One bound `structdet-code.trace/0.1` design
supplies a run roster, per-revision evidence selections, declared paths, exact
checkpoints, common configuration/protocol and budget/stopping context. Source,
assignment, receipt, parent and feedback records stay in the study. Evidence
selection uses the same checked projection as static inspection, including
latest-assignment enforcement and exact revision receipt bindings. A final
receipt cannot certify an earlier revision even when both use identical bytes.

The only clock is the actual nonnegative `revision_ordinal`. At most 32 strictly
increasing checkpoints are selected. Each of at most 128 roster entries names
a recorded run or explicitly declares an unrecorded run. Each recorded revision
in that roster, including excluded branches, has one assessment with explicit
assignment/receipt IDs or null. Unknown decisions remain unadmitted/unassessed.
One source digest cannot carry conflicting accepted classes in one trace.

A selected path lists exact revision IDs in increasing ordinal order and ends
at the study's selected endpoint when known. Known parent links must be followed
without jumping between siblings or omitting known intermediate parents. At a
merge, the path explicitly chooses its incoming lineage and the other parent
remains visible. A continuation across a missing direct parent is an unresolved
lineage assertion. Null paths preserve the complete recorded history while
leaving branch selection unknown. No default branch is chosen at an ambiguous merge.

Only consecutive ordinal, single-parent selected-path edges with admitted
labels enter the supported transition matrix. The states distinguish mechanism
switch, changed source with the same mechanism, unchanged source/mechanism,
unresolved assignment, ordinal gap, missing lineage and merge-parent comparison.
The complete sequence is retained, including first observations and observed
reappearance. Test-only receipts and assignment revisions create no generation
events. Existing study revision kinds retain their meanings.

Checkpoint selection requires an exact ordinal on the declared path. No nearest
snapshot, previous passing result, later replacement or stopped endpoint fills a
missing cell. Available-case populations contain the observed cells at that
checkpoint; the matched cohort is the intersection of observed run IDs across all
requested checkpoints, independent of labels or passing status. Matched exclusions,
roster membership, coverage and source/root-group identities remain explicit.

Stopping reason alone does not locate stopping in revision time. A nullable
supplied `stop_ordinal` is separate from the selected endpoint, must accompany a
terminal reason, and cannot precede any recorded revision of the run. Risk-set
output separates known stopped-before, known reached and unknown reach. A run
with an unknown stop time is not assumed active or stopped at a later checkpoint.

The budget carrier declares nullable limits for maximum revision ordinal and
total attempted finite test cases. Recorded usage sums every supplied receipt,
including repeated tests and excluded branches; it does not authenticate spending
or invent missing tests. Exceeded limits remain visible and block qualified
contrasts. Numeric trends require known common configuration/protocol and equal
known budgets for the participating cohort, with checkpoints inside those limits.
A matched subset can qualify even when an excluded run has an unknown budget.

Concentration differences require unchanged observed run membership and complete
admitted mechanism coverage at both endpoints. Finite-pass differences additionally
require a common suite/oracle/environment/execution-basis/visibility scope and
definite finite validity for every compared observation. Unknown visibility,
changed suites, partial/timeout outcomes and absent receipts yield explicit
unavailable comparisons. The all-classified mechanism view can remain comparable
when finite-validity scope changes. Joint directions derive from exact operands.

Observed-set reporting retains reference/current sets, retained, no-longer-observed,
newly observed and observed-again classes, with the actual reference-set denominator.
Incompatible or changing cohorts expose inventory-only set changes. Empty
populations retain zero support and undefined SCI. Trace populations with only one
admitted observation suppress SCI/Gini-Simpson as not applicable. A single run
supports a trajectory, without a model-level concentration trend.

The revision clock does not implement recursive Structural Half-Life. Observed
reappearance does not qualify an External Recovery Rate. No confidence interval,
causal estimate, independent-root claim or general capacity-loss conclusion is
added. Trace input is limited to 1 MiB and the formatted canonical JSON result to
4 MiB; exceeding the result bound is an explicit error with no successful truncation.
`docs/C04.md` documents the exact fields and commands.

## 9. Source basis and attribution

- Owner handoff: `StructDet_Code_Work_Handoff.md`, version 1.0, 2026-09-23.
- Xiangyu Guo, *The Structural Determinacy of LLM Generation*, August 2026:
  sections 3, 5, 9 and 12 inform task/horizon/resolution, evidence and interpretation.
- Xiangyu Guo, *Structural Inbreeding in Synthetic Data*, version 1.0, August 2026:
  sections 3 and 8 inform support, concentration and scoped recovery/half-life boundaries.
- Xiangyu Guo, *Evaluation Closure Benchmark Inbreeding and the Design of Open AI
  Evaluation*, supplied 2026 edition: sections 2, 4.5, 6 and 7 inform anomaly
  preservation, source integrity and type-appropriate validation.
- Baseline code and task source:
  https://github.com/DavidWallstructurallaw/structdet-bench/tree/0a9dc88deffd4b14264485b161bea06f027f68f5
- Related work to retain for productization: Lee et al., arXiv:2503.00691v2;
  Young et al., arXiv:2408.06186. No reproduced comparative performance claim.

The three theory PDFs are reference-only and retain CC BY-NC-ND 4.0 publication
licenses. Their exact local fingerprints appear in the C01 verification record.
No full publication text is included in the package. Field names, software
policies and domain adapters here are engineering choices, not new theory theorems.
