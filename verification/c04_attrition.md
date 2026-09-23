# StructDet Code revision trace

Study: `owned-revision-examples`; trace: `fixture-attrition`; material: `fixture`.

Task: `unit-graph-distances`; evidence policy: `fixture_only`.

Clock: `revision_ordinal`; selection: `declared-path-exact-ordinal/0.1`.

Roster: 6 runs; 5 recorded. Explicitly unrecorded: `['A6']`.

Cohort status: `compatible_descriptive`; reasons: `[]`.

Matched across every requested checkpoint: `['A3', 'A4']`.

Recorded stopping reasons: `{'budget': 2, 'success': 2, 'timeout': 1}`. Study runs outside this roster: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

## Checkpoint populations

Available cases retain each recorded observation at that ordinal. Matched cases retain the same run IDs at every selected checkpoint.

| Ordinal | Cohort | Observed / roster | Admitted | Finite passed / observed | Support | SCI | Valid admitted | Valid SCI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | available | 5 / 6 | 5 | 2/5 | 3 | 11/25 | 2 | 1/2 |
| 0 | matched | 2 / 2 | 2 | 0/2 | 1 | 1/1 | 0 | empty_classified_population |
| 1 | available | 2 / 6 | 2 | 2/2 | 1 | 1/1 | 2 | 1/1 |
| 1 | matched | 2 / 2 | 2 | 2/2 | 1 | 1/1 | 2 | 1/1 |
| 2 | available | 2 / 6 | 2 | 2/2 | 1 | 1/1 | 2 | 1/1 |
| 2 | matched | 2 / 2 | 2 | 2/2 | 1 | 1/1 | 2 | 1/1 |

Missing outputs are not failed tests. Single-observation concentration is not applicable.

Whole declared-path transition states: `{'source_change_same_mechanism': 2, 'unchanged_source_and_mechanism': 2}`; supported adjacent counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 4}]`.

## Changes and joint outcomes

All numeric differences are later minus earlier, qualified by the recorded cohort and evidence.

### available: 0 to 1

Earlier runs: `['A1', 'A2', 'A3', 'A4', 'A5']`; later runs: `['A3', 'A4']`.

- `classified_all`: unavailable; `['cohort_membership_changed']`.
- `classified_valid`: unavailable; `['cohort_membership_changed']`.
- Finite pass fraction: 2/5 to 2/2; comparison unavailable; `['cohort_membership_changed']`.

Joint observation: `insufficient_comparable_evidence`; `['cohort_membership_changed']`.

`classified_all` sets (inventory_only): retained `['DIST-FIFO']`; no longer observed `['DIST-RELAX', 'DIST-SETTLE']`; first observed `[]`; observed again `[]`; retained/reference=1/3. Qualifiers: `['cohort_membership_changed']`.

`classified_valid` sets (inventory_only): retained `[]`; no longer observed `['DIST-RELAX', 'DIST-SETTLE']`; first observed `['DIST-FIFO']`; observed again `[]`; retained/reference=0/2. Qualifiers: `['cohort_membership_changed']`.

### available: 1 to 2

Earlier runs: `['A3', 'A4']`; later runs: `['A3', 'A4']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- Finite pass fraction: 2/2 to 2/2; delta=0/1.

Joint observation: finite passing stable; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

### matched: 0 to 1

Earlier runs: `['A3', 'A4']`; later runs: `['A3', 'A4']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: unavailable; `['fewer_than_two_admitted_runs']`.
- Finite pass fraction: 0/2 to 2/2; delta=1/1.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `[]`; no longer observed `[]`; first observed `['DIST-FIFO']`; observed again `[]`; retained/reference=undefined. Qualifiers: `[]`.

### matched: 1 to 2

Earlier runs: `['A3', 'A4']`; later runs: `['A3', 'A4']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- Finite pass fraction: 2/2 to 2/2; delta=0/1.

Joint observation: finite passing stable; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

## Missingness, risk sets and coverage

### Ordinal 0

Availability: `{'observed': 5, 'run_unrecorded': 1}`.

Known stopped before this ordinal: `[]`; known reached: `['A1', 'A2', 'A3', 'A4', 'A5']`; reach unknown: `['A6']`.

| Run | State | Selected revision |
| --- | --- | --- |
| A1 | observed | A1-V0 |
| A2 | observed | A2-V0 |
| A3 | observed | A3-V0 |
| A4 | observed | A4-V0 |
| A5 | observed | A5-V0 |
| A6 | run_unrecorded | none |

available: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 1}`; valid counts `{'DIST-RELAX': 1, 'DIST-SETTLE': 1}`; validity `{'failed': 3, 'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=5/5; declared root groups `{'G-owned-fixtures': 5}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 2}`; valid counts `{}`; validity `{'failed': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.

### Ordinal 1

Availability: `{'observed': 2, 'run_unrecorded': 1, 'stopped_success': 2, 'stopped_timeout': 1}`.

Known stopped before this ordinal: `['A1', 'A2', 'A5']`; known reached: `['A3', 'A4']`; reach unknown: `['A6']`.

| Run | State | Selected revision |
| --- | --- | --- |
| A1 | stopped_success | none |
| A2 | stopped_success | none |
| A3 | observed | A3-V1 |
| A4 | observed | A4-V1 |
| A5 | stopped_timeout | none |
| A6 | run_unrecorded | none |

available: class counts `{'DIST-FIFO': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.

### Ordinal 2

Availability: `{'observed': 2, 'run_unrecorded': 1, 'stopped_success': 2, 'stopped_timeout': 1}`.

Known stopped before this ordinal: `['A1', 'A2', 'A5']`; known reached: `['A3', 'A4']`; reach unknown: `['A6']`.

| Run | State | Selected revision |
| --- | --- | --- |
| A1 | stopped_success | none |
| A2 | stopped_success | none |
| A3 | observed | A3-V2 |
| A4 | observed | A4-V2 |
| A5 | stopped_timeout | none |
| A6 | run_unrecorded | none |

available: class counts `{'DIST-FIFO': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


## Per-run trajectories

Rows follow supplied revision ordinals. Parent links determine lineage; sibling rows alone do not establish a mechanism transition. Repeated test receipts remain attached to their revision; their within-revision chronological order is unspecified.

### Run `A1`

Configuration: `attrition`; root group: `G-owned-fixtures`.

Stop: `success` at supplied ordinal `0`; selected endpoint: `A1-V0`.

Selected path: `['A1-V0']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 1, 'maximum_ordinal': 0, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 1, 'test_case_attempts': 10, 'completed_test_cases': 10}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | A1-V0 / generation | none | DIST-SETTLE | passed_under_supplied_scope / E-A1-V0 | none |

Ordinal gaps: `[]`; transition states: `{}`.

Supported adjacent selected-path transition counts: `[]`.

`A1-V0`: artifact `settle_good`, source `af2307adae53c9e5493a5479f4f0a2176e7171c1e8ce1a0386fc8e3ef6d55457`; assignment `M-settle_good`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-A1-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `A2`

Configuration: `attrition`; root group: `G-owned-fixtures`.

Stop: `success` at supplied ordinal `0`; selected endpoint: `A2-V0`.

Selected path: `['A2-V0']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 1, 'maximum_ordinal': 0, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 1, 'test_case_attempts': 10, 'completed_test_cases': 10}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | A2-V0 / generation | none | DIST-RELAX | passed_under_supplied_scope / E-A2-V0 | none |

Ordinal gaps: `[]`; transition states: `{}`.

Supported adjacent selected-path transition counts: `[]`.

`A2-V0`: artifact `relax_good`, source `3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235`; assignment `M-relax_good`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-A2-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `A3`

Configuration: `attrition`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `A3-V2`.

Selected path: `['A3-V0', 'A3-V1', 'A3-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | A3-V0 / generation | none | DIST-FIFO | failed / E-A3-V0 | none |
| 1 | A3-V1 / edit | A3-V0 | DIST-FIFO | passed_under_supplied_scope / E-A3-V1 | F-A3-V0 |
| 2 | A3-V2 / no_op | A3-V1 | DIST-FIFO | passed_under_supplied_scope / E-A3-V2 | F-A3-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- A3-V0 (DIST-FIFO) to A3-V1 (DIST-FIFO): `source_change_same_mechanism`; source changed=True; test scope changed=False.
- A3-V1 (DIST-FIFO) to A3-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`A3-V0`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A3-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-A3-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-A3-V0`: test, receipt `T-A3-V0`, visible=True, received by `['A3-V1']`.

`A3-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A3-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-A3-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-A3-V1`: test, receipt `T-A3-V1`, visible=True, received by `['A3-V2']`.

`A3-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A3-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `A4`

Configuration: `attrition`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `A4-V2`.

Selected path: `['A4-V0', 'A4-V1', 'A4-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | A4-V0 / generation | none | DIST-FIFO | failed / E-A4-V0 | none |
| 1 | A4-V1 / edit | A4-V0 | DIST-FIFO | passed_under_supplied_scope / E-A4-V1 | F-A4-V0 |
| 2 | A4-V2 / no_op | A4-V1 | DIST-FIFO | passed_under_supplied_scope / E-A4-V2 | F-A4-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- A4-V0 (DIST-FIFO) to A4-V1 (DIST-FIFO): `source_change_same_mechanism`; source changed=True; test scope changed=False.
- A4-V1 (DIST-FIFO) to A4-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`A4-V0`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A4-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-A4-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-A4-V0`: test, receipt `T-A4-V0`, visible=True, received by `['A4-V1']`.

`A4-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A4-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-A4-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-A4-V1`: test, receipt `T-A4-V1`, visible=True, received by `['A4-V2']`.

`A4-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A4-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `A5`

Configuration: `attrition`; root group: `G-owned-fixtures`.

Stop: `timeout` at supplied ordinal `0`; selected endpoint: `A5-V0`.

Selected path: `['A5-V0']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 1, 'maximum_ordinal': 0, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 1, 'test_case_attempts': 10, 'completed_test_cases': 10}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | A5-V0 / generation | none | DIST-FIFO | failed / E-A5-V0 | none |

Ordinal gaps: `[]`; transition states: `{}`.

Supported adjacent selected-path transition counts: `[]`.

`A5-V0`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-A5-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `A6`

Explicitly unrecorded run. Supplied budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`.
## Test scope identities

| Scope | Suite SHA-256 | Oracle | Environment fingerprint | Basis | Visibility |
| --- | --- | --- | --- | --- | --- |
| `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `a515c93632fe1d25cb194362feb115da2f9336e9eea2f5beb5b6f0fb33c5f7f7` | project_fixture_execution | feedback |
| `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `a515c93632fe1d25cb194362feb115da2f9336e9eea2f5beb5b6f0fb33c5f7f7` | project_fixture_execution | withheld |

## What this result supports

This report describes source-bound revision histories and conditional distributions over the named run roster. The joint outcomes preserve both finite correctness and mechanism changes, with missing prerequisites beside unavailable comparisons.

Study binding: `767121f008ccd461f04e055f64e23f41292a4f3428fda6de9cd7a11a7039f747`; design binding: `c9586921233050a9f75ffea7a77d0db4078209e658c81012f84032375f83aafc`; task binding: `7cca04509c795eefdbb6cb3318922f89154f04c45236ba2021ab5be9316c79d1`.

Structural Half-Life: `not_applicable`. External Recovery Rate: `not_estimated`.

- Trajectories retain actual revision ordinals; test-only evidence and assignment versions add no code generations.
- Selected paths are supplied branch decisions. Missing ancestry and ordinal gaps do not become supported adjacent switches.
- Checkpoint selection is exact: no stopped endpoint, absent revision or passing receipt is carried forward.
- Available cases can change with stopping and missingness; matched cases retain the same observed runs at every selected checkpoint.
- Matched observation membership does not remove success-dependent selection or establish independent samples.
- Numeric trends require known compatible context and complete mechanism coverage; finite-pass trends also require a common known test scope.
- A single admitted observation has no population concentration result in trace output.
- Supplied budget, stopping, feedback and execution records are not authenticated; absent events remain unknown.
- Observed sets and reappearance concern these records, with no inference of general capacity loss, external recovery or causal effects.
