# StructDet Code revision trace

Study: `owned-revision-examples`; trace: `fixture-stable`; material: `fixture`.

Task: `unit-graph-distances`; evidence policy: `fixture_only`.

Clock: `revision_ordinal`; selection: `declared-path-exact-ordinal/0.1`.

Roster: 6 runs; 6 recorded. Explicitly unrecorded: `[]`.

Cohort status: `compatible_descriptive`; reasons: `[]`.

Matched across every requested checkpoint: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

Recorded stopping reasons: `{'budget': 6}`. Study runs outside this roster: `['A1', 'A2', 'A3', 'A4', 'A5', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']`.

## Checkpoint populations

Available cases retain each recorded observation at that ordinal. Matched cases retain the same run IDs at every selected checkpoint.

| Ordinal | Cohort | Observed / roster | Admitted | Finite passed / observed | Support | SCI | Valid admitted | Valid SCI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | available | 6 / 6 | 6 | 2/6 | 3 | 7/18 | 2 | 1/1 |
| 0 | matched | 6 / 6 | 6 | 2/6 | 3 | 7/18 | 2 | 1/1 |
| 1 | available | 6 / 6 | 6 | 4/6 | 3 | 7/18 | 4 | 5/8 |
| 1 | matched | 6 / 6 | 6 | 4/6 | 3 | 7/18 | 4 | 5/8 |
| 2 | available | 6 / 6 | 6 | 6/6 | 3 | 7/18 | 6 | 7/18 |
| 2 | matched | 6 / 6 | 6 | 6/6 | 3 | 7/18 | 6 | 7/18 |

Missing outputs are not failed tests. Single-observation concentration is not applicable.

Whole declared-path transition states: `{'source_change_same_mechanism': 4, 'unchanged_source_and_mechanism': 8}`; supported adjacent counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 6}, {'from_class': 'DIST-RELAX', 'to_class': 'DIST-RELAX', 'count': 2}, {'from_class': 'DIST-SETTLE', 'to_class': 'DIST-SETTLE', 'count': 4}]`.

## Changes and joint outcomes

All numeric differences are later minus earlier, qualified by the recorded cohort and evidence.

### available: 0 to 1

Earlier runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; later runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

- `classified_all`: n=6 to 6; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: n=2 to 4; support delta=1; SCI delta=-3/8; Gini-Simpson delta=3/8.
- Finite pass fraction: 2/6 to 4/6; delta=1/3.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-RELAX', 'DIST-SETTLE']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=3/3. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `['DIST-SETTLE']`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

### available: 1 to 2

Earlier runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; later runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

- `classified_all`: n=6 to 6; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: n=4 to 6; support delta=1; SCI delta=-17/72; Gini-Simpson delta=17/72.
- Finite pass fraction: 4/6 to 6/6; delta=1/3.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-RELAX', 'DIST-SETTLE']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=3/3. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-SETTLE']`; no longer observed `[]`; first observed `['DIST-RELAX']`; observed again `[]`; retained/reference=2/2. Qualifiers: `[]`.

### matched: 0 to 1

Earlier runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; later runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

- `classified_all`: n=6 to 6; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: n=2 to 4; support delta=1; SCI delta=-3/8; Gini-Simpson delta=3/8.
- Finite pass fraction: 2/6 to 4/6; delta=1/3.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-RELAX', 'DIST-SETTLE']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=3/3. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `['DIST-SETTLE']`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

### matched: 1 to 2

Earlier runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; later runs: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

- `classified_all`: n=6 to 6; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: n=4 to 6; support delta=1; SCI delta=-17/72; Gini-Simpson delta=17/72.
- Finite pass fraction: 4/6 to 6/6; delta=1/3.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-RELAX', 'DIST-SETTLE']`; no longer observed `[]`; first observed `[]`; observed again `[]`; retained/reference=3/3. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-SETTLE']`; no longer observed `[]`; first observed `['DIST-RELAX']`; observed again `[]`; retained/reference=2/2. Qualifiers: `[]`.

## Missingness, risk sets and coverage

### Ordinal 0

Availability: `{'observed': 6}`.

Known stopped before this ordinal: `[]`; known reached: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| S1 | observed | S1-V0 |
| S2 | observed | S2-V0 |
| S3 | observed | S3-V0 |
| S4 | observed | S4-V0 |
| S5 | observed | S5-V0 |
| S6 | observed | S6-V0 |

available: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'failed': 4, 'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'failed': 4, 'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.

### Ordinal 1

Availability: `{'observed': 6}`.

Known stopped before this ordinal: `[]`; known reached: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| S1 | observed | S1-V1 |
| S2 | observed | S2-V1 |
| S3 | observed | S3-V1 |
| S4 | observed | S4-V1 |
| S5 | observed | S5-V1 |
| S6 | observed | S6-V1 |

available: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 3, 'DIST-SETTLE': 1}`; validity `{'failed': 2, 'passed_under_supplied_scope': 4}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 3, 'DIST-SETTLE': 1}`; validity `{'failed': 2, 'passed_under_supplied_scope': 4}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.

### Ordinal 2

Availability: `{'observed': 6}`.

Known stopped before this ordinal: `[]`; known reached: `['S1', 'S2', 'S3', 'S4', 'S5', 'S6']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| S1 | observed | S1-V2 |
| S2 | observed | S2-V2 |
| S3 | observed | S3-V2 |
| S4 | observed | S4-V2 |
| S5 | observed | S5-V2 |
| S6 | observed | S6-V2 |

available: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; validity `{'passed_under_supplied_scope': 6}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; validity `{'passed_under_supplied_scope': 6}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


## Per-run trajectories

Rows follow supplied revision ordinals. Parent links determine lineage; sibling rows alone do not establish a mechanism transition. Repeated test receipts remain attached to their revision; their within-revision chronological order is unspecified.

### Run `S1`

Configuration: `stable`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `S1-V2`.

Selected path: `['S1-V0', 'S1-V1', 'S1-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 2, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | S1-V0 / generation | none | DIST-FIFO | passed_under_supplied_scope / E-S1-V0 | none |
| 1 | S1-V1 / no_op | S1-V0 | DIST-FIFO | passed_under_supplied_scope / E-S1-V1 | F-S1-V0 |
| 2 | S1-V2 / no_op | S1-V1 | DIST-FIFO | passed_under_supplied_scope / E-S1-V2 | F-S1-V1 |

Ordinal gaps: `[]`; transition states: `{'unchanged_source_and_mechanism': 2}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- S1-V0 (DIST-FIFO) to S1-V1 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- S1-V1 (DIST-FIFO) to S1-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`S1-V0`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S1-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S1-V0`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S1-V0`: test, receipt `T-S1-V0`, visible=True, received by `['S1-V1']`.

`S1-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S1-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S1-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S1-V1`: test, receipt `T-S1-V1`, visible=True, received by `['S1-V2']`.

`S1-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S1-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `S2`

Configuration: `stable`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `S2-V2`.

Selected path: `['S2-V0', 'S2-V1', 'S2-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 2, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | S2-V0 / generation | none | DIST-FIFO | passed_under_supplied_scope / E-S2-V0 | none |
| 1 | S2-V1 / no_op | S2-V0 | DIST-FIFO | passed_under_supplied_scope / E-S2-V1 | F-S2-V0 |
| 2 | S2-V2 / no_op | S2-V1 | DIST-FIFO | passed_under_supplied_scope / E-S2-V2 | F-S2-V1 |

Ordinal gaps: `[]`; transition states: `{'unchanged_source_and_mechanism': 2}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- S2-V0 (DIST-FIFO) to S2-V1 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- S2-V1 (DIST-FIFO) to S2-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`S2-V0`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S2-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S2-V0`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S2-V0`: test, receipt `T-S2-V0`, visible=True, received by `['S2-V1']`.

`S2-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S2-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S2-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S2-V1`: test, receipt `T-S2-V1`, visible=True, received by `['S2-V2']`.

`S2-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S2-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `S3`

Configuration: `stable`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `S3-V2`.

Selected path: `['S3-V0', 'S3-V1', 'S3-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | S3-V0 / generation | none | DIST-FIFO | failed / E-S3-V0 | none |
| 1 | S3-V1 / edit | S3-V0 | DIST-FIFO | passed_under_supplied_scope / E-S3-V1 | F-S3-V0 |
| 2 | S3-V2 / no_op | S3-V1 | DIST-FIFO | passed_under_supplied_scope / E-S3-V2 | F-S3-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- S3-V0 (DIST-FIFO) to S3-V1 (DIST-FIFO): `source_change_same_mechanism`; source changed=True; test scope changed=False.
- S3-V1 (DIST-FIFO) to S3-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`S3-V0`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S3-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S3-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S3-V0`: test, receipt `T-S3-V0`, visible=True, received by `['S3-V1']`.

`S3-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S3-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S3-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S3-V1`: test, receipt `T-S3-V1`, visible=True, received by `['S3-V2']`.

`S3-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-S3-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `S4`

Configuration: `stable`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `S4-V2`.

Selected path: `['S4-V0', 'S4-V1', 'S4-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | S4-V0 / generation | none | DIST-SETTLE | failed / E-S4-V0 | none |
| 1 | S4-V1 / edit | S4-V0 | DIST-SETTLE | passed_under_supplied_scope / E-S4-V1 | F-S4-V0 |
| 2 | S4-V2 / no_op | S4-V1 | DIST-SETTLE | passed_under_supplied_scope / E-S4-V2 | F-S4-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-SETTLE', 'to_class': 'DIST-SETTLE', 'count': 2}]`.

- S4-V0 (DIST-SETTLE) to S4-V1 (DIST-SETTLE): `source_change_same_mechanism`; source changed=True; test scope changed=False.
- S4-V1 (DIST-SETTLE) to S4-V2 (DIST-SETTLE): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`S4-V0`: artifact `settle_bad`, source `20f58c6cc9a8ba1c44541bb0731eb3a48501f64903834c26be63884be0611701`; assignment `M-settle_bad`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-S4-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S4-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S4-V0`: test, receipt `T-S4-V0`, visible=True, received by `['S4-V1']`.

`S4-V1`: artifact `settle_good`, source `af2307adae53c9e5493a5479f4f0a2176e7171c1e8ce1a0386fc8e3ef6d55457`; assignment `M-settle_good`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-S4-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S4-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S4-V1`: test, receipt `T-S4-V1`, visible=True, received by `['S4-V2']`.

`S4-V2`: artifact `settle_good`, source `af2307adae53c9e5493a5479f4f0a2176e7171c1e8ce1a0386fc8e3ef6d55457`; assignment `M-settle_good`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-S4-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `S5`

Configuration: `stable`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `S5-V2`.

Selected path: `['S5-V0', 'S5-V1', 'S5-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | S5-V0 / generation | none | DIST-SETTLE | failed / E-S5-V0 | none |
| 1 | S5-V1 / no_op | S5-V0 | DIST-SETTLE | failed / E-S5-V1 | F-S5-V0 |
| 2 | S5-V2 / edit | S5-V1 | DIST-SETTLE | passed_under_supplied_scope / E-S5-V2 | F-S5-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-SETTLE', 'to_class': 'DIST-SETTLE', 'count': 2}]`.

- S5-V0 (DIST-SETTLE) to S5-V1 (DIST-SETTLE): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- S5-V1 (DIST-SETTLE) to S5-V2 (DIST-SETTLE): `source_change_same_mechanism`; source changed=True; test scope changed=False.

`S5-V0`: artifact `settle_bad`, source `20f58c6cc9a8ba1c44541bb0731eb3a48501f64903834c26be63884be0611701`; assignment `M-settle_bad`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-S5-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S5-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S5-V0`: test, receipt `T-S5-V0`, visible=True, received by `['S5-V1']`.

`S5-V1`: artifact `settle_bad`, source `20f58c6cc9a8ba1c44541bb0731eb3a48501f64903834c26be63884be0611701`; assignment `M-settle_bad`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-S5-V1`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S5-V1`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S5-V1`: test, receipt `T-S5-V1`, visible=True, received by `['S5-V2']`.

`S5-V2`: artifact `settle_good`, source `af2307adae53c9e5493a5479f4f0a2176e7171c1e8ce1a0386fc8e3ef6d55457`; assignment `M-settle_good`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-S5-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `S6`

Configuration: `stable`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `S6-V2`.

Selected path: `['S6-V0', 'S6-V1', 'S6-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | S6-V0 / generation | none | DIST-RELAX | failed / E-S6-V0 | none |
| 1 | S6-V1 / no_op | S6-V0 | DIST-RELAX | failed / E-S6-V1 | F-S6-V0 |
| 2 | S6-V2 / edit | S6-V1 | DIST-RELAX | passed_under_supplied_scope / E-S6-V2 | F-S6-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-RELAX', 'to_class': 'DIST-RELAX', 'count': 2}]`.

- S6-V0 (DIST-RELAX) to S6-V1 (DIST-RELAX): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- S6-V1 (DIST-RELAX) to S6-V2 (DIST-RELAX): `source_change_same_mechanism`; source changed=True; test scope changed=False.

`S6-V0`: artifact `relax_bad`, source `cc832ed979d21d53abed769b0c68241277181767d3a1d058e10f34f4ffce1634`; assignment `M-relax_bad`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-S6-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S6-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S6-V0`: test, receipt `T-S6-V0`, visible=True, received by `['S6-V1']`.

`S6-V1`: artifact `relax_bad`, source `cc832ed979d21d53abed769b0c68241277181767d3a1d058e10f34f4ffce1634`; assignment `M-relax_bad`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-S6-V1`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-S6-V1`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-S6-V1`: test, receipt `T-S6-V1`, visible=True, received by `['S6-V2']`.

`S6-V2`: artifact `relax_good`, source `3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235`; assignment `M-relax_good`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-S6-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.

## Test scope identities

| Scope | Suite SHA-256 | Oracle | Environment fingerprint | Basis | Visibility |
| --- | --- | --- | --- | --- | --- |
| `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `a515c93632fe1d25cb194362feb115da2f9336e9eea2f5beb5b6f0fb33c5f7f7` | project_fixture_execution | feedback |
| `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `a515c93632fe1d25cb194362feb115da2f9336e9eea2f5beb5b6f0fb33c5f7f7` | project_fixture_execution | withheld |

## What this result supports

This report describes source-bound revision histories and conditional distributions over the named run roster. The joint outcomes preserve both finite correctness and mechanism changes, with missing prerequisites beside unavailable comparisons.

Study binding: `767121f008ccd461f04e055f64e23f41292a4f3428fda6de9cd7a11a7039f747`; design binding: `70962ca4a96e690f9d364a0b26ebefe0e9dcc78ef2fa75960c395e52fd2c9603`; task binding: `7cca04509c795eefdbb6cb3318922f89154f04c45236ba2021ab5be9316c79d1`.

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
