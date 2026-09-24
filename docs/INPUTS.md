# Prepare inputs and interpret a first result

Use installed `structdet-code` commands, or `python -m structdet_code` in the
environment where the package is installed. Export a complete portable reference
set with `structdet-code examples --output ./example-inputs`.

## Static source collection

Each collection should represent one supplied condition. The default scan selects
top-level `.py` files. For a deliberate nested selection, repeat `--include` with
relative paths. There are at most 128 selected sources; each must be a regular,
UTF-8 file up to 256 KiB, inside its root without symlinks.

```bash
structdet-code prepare --sources /absolute/path/to/collection --include batch/one.py --include batch/two.py --output ./my-study --study-id my-collection
structdet-code inspect --study ./my-study/study.json --format markdown
```

Preparation creates one standalone observation per selected path. File order is
not chronology, and two identical files do not become independent generations.
The original source directory stays unchanged. No test receipt, model identity,
prompt, budget or history is fabricated.

| Task option | Required program contract | Current automatic scope |
| --- | --- | --- |
| `sorting-bounded` (default) | `sort_values(values)`; 0..256 plain integers in 0..4095; new sorted list, unchanged input, no delegated sort | Nine whole-module rules across eight declared families |
| `unit-graph-distances` | `shortest_distances(node_count, edges, start)`; 1..128 numbered vertices, directed unit edges; new minimum-hop list, unreachable entries `None` | Four whole-module rules across FIFO, SETTLE and RELAX |

Use the graph option with `prepare --task unit-graph-distances`. Weighted graphs,
different output contracts and arbitrary program equivalence are unsupported.
Exact recognition preserves operative AST structure while allowing documented
presentation/name variations. Unrecognized source remains a review case. Even
a recognized defective program can receive a mechanism class; correctness is a
separate evidence axis.

## Read and supply a review

Start with classification coverage and its unresolved reasons before interpreting
support or SCI. `classified_all` uses admitted mechanisms; `classified_valid`
also requires the selected finite receipt to pass under its supplied scope.
No receipt means `not_assessed`, with no invented passing result. Source digests,
line spans and exact selected revisions let a reviewer locate the private input.

Open `my-study/review.json` and the copied sources. Leave unchanged entries with
`decision: null`; fill only actual review decisions. Keep all source, task and
current-assignment bindings unchanged. Accepted human decisions need source-line
evidence. Unknowns keep a reason. Supplied AI decisions stay provisional. The
[review field guide](C02.md#review-and-apply) provides the exact accepted fields.

```bash
structdet-code apply-review --study ./my-study/study.json --review ./my-study/review.json --output ./my-study/reviewed.json
structdet-code inspect --study ./my-study/reviewed.json --format markdown
```

The new manifest must share the original manifest's directory, so relative
payload paths stay valid. Prior assignments remain present. A correction changes
the study hash: regenerate dependent trace/comparison/evidence bindings and make
a new snapshot. Old snapshots continue to describe their captured history.

## Recorded coding-agent histories

Plain source preparation cannot reconstruct missing history. Supply actual runs,
revision IDs/ordinals, parent links, source artifacts, receipts and feedback using
the portable study schema. `example-inputs/trace/study.json` and
`example-inputs/interventions/study.json` are complete owned examples. Provider-
specific log importers are not included.

```bash
structdet-code trace-template --study ./my-study/study.json --output ./my-study/trace.json
structdet-code evidence-template --study ./my-study/study.json --output ./my-study/evidence.json
```

The templates leave unknown values unknown. Fill only supported facts about the
roster, selected paths, checkpoints, configurations, protocol, budgets and stops.
Use [C04](C04.md) for exact trace fields. Missing checkpoints stay missing; stopped
endpoints do not fill later observations. Available and matched cohorts make
attrition visible, and single-run histories do not yield concentration trends.

Optional [C05 evidence](C05.md) records intervention material/visibility/reuse
and receipt-bound finite failure profiles. It is valid to omit it. Shared failures
need compatible scopes and observed per-case outcomes; unavailable outcomes do
not become passes. Source equality, supplied copying and observed reappearance
remain distinct. Public reports omit raw source, prompts and free-form logs;
input directories and snapshots retain those private bytes.

## Compare conditions and preserve a result

```bash
structdet-code comparison-template --left ./left/study.json --right ./right/study.json --output ./comparison.json
structdet-code compare --left ./left/study.json --right ./right/study.json --design ./comparison.json --format markdown
structdet-code snapshot --action inspect --study ./my-study/reviewed.json --output ./saved-analysis
structdet-code replay --bundle ./saved-analysis --format markdown
```

Before comparison, fill the generated design with actual matching task/frame,
condition controls, protocol, budgets and fixed-prefix accounting. Without those
facts the result reports inventories and missing prerequisites. Failed programs
stay in the observed population; later outputs cannot replace missing prefix
positions. See [C03](C03.md). A comparison result describes the qualified supplied
populations and does not authenticate collection or establish causality.
