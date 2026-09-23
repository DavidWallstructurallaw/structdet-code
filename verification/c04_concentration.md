# StructDet Code revision trace

Study: `owned-revision-examples`; trace: `fixture-concentration`; material: `fixture`.

Task: `unit-graph-distances`; evidence policy: `fixture_only`.

Clock: `revision_ordinal`; selection: `declared-path-exact-ordinal/0.1`.

Roster: 6 runs; 6 recorded. Explicitly unrecorded: `[]`.

Cohort status: `compatible_descriptive`; reasons: `[]`.

Matched across every requested checkpoint: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`.

Recorded stopping reasons: `{'budget': 6}`. Study runs outside this roster: `['A1', 'A2', 'A3', 'A4', 'A5', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']`.

## Checkpoint populations

Available cases retain each recorded observation at that ordinal. Matched cases retain the same run IDs at every selected checkpoint.

| Ordinal | Cohort | Observed / roster | Admitted | Finite passed / observed | Support | SCI | Valid admitted | Valid SCI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | available | 6 / 6 | 6 | 2/6 | 3 | 7/18 | 2 | 1/1 |
| 0 | matched | 6 / 6 | 6 | 2/6 | 3 | 7/18 | 2 | 1/1 |
| 1 | available | 6 / 6 | 6 | 4/6 | 2 | 5/9 | 4 | 5/8 |
| 1 | matched | 6 / 6 | 6 | 4/6 | 2 | 5/9 | 4 | 5/8 |
| 2 | available | 6 / 6 | 6 | 6/6 | 1 | 1/1 | 6 | 1/1 |
| 2 | matched | 6 / 6 | 6 | 6/6 | 1 | 1/1 | 6 | 1/1 |

Missing outputs are not failed tests. Single-observation concentration is not applicable.

Whole declared-path transition states: `{'mechanism_switch': 3, 'source_change_same_mechanism': 3, 'unchanged_source_and_mechanism': 6}`; supported adjacent counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 7}, {'from_class': 'DIST-RELAX', 'to_class': 'DIST-FIFO', 'count': 1}, {'from_class': 'DIST-SETTLE', 'to_class': 'DIST-FIFO', 'count': 2}, {'from_class': 'DIST-SETTLE', 'to_class': 'DIST-SETTLE', 'count': 2}]`.

## Changes and joint outcomes

All numeric differences are later minus earlier, qualified by the recorded cohort and evidence.

### available: 0 to 1

Earlier runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; later runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`.

- `classified_all`: n=6 to 6; support delta=-1; SCI delta=1/6; Gini-Simpson delta=-1/6.
- `classified_valid`: n=2 to 4; support delta=1; SCI delta=-3/8; Gini-Simpson delta=3/8.
- Finite pass fraction: 2/6 to 4/6; delta=1/3.

Joint observation: finite passing rising; support falling; concentration rising.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-SETTLE']`; no longer observed `['DIST-RELAX']`; first observed `[]`; observed again `[]`; retained/reference=2/3. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `['DIST-SETTLE']`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

### available: 1 to 2

Earlier runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; later runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`.

- `classified_all`: n=6 to 6; support delta=-1; SCI delta=4/9; Gini-Simpson delta=-4/9.
- `classified_valid`: n=4 to 6; support delta=-1; SCI delta=3/8; Gini-Simpson delta=-3/8.
- Finite pass fraction: 4/6 to 6/6; delta=1/3.

Joint observation: finite passing rising; support falling; concentration rising.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `['DIST-SETTLE']`; first observed `[]`; observed again `[]`; retained/reference=1/2. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `['DIST-SETTLE']`; first observed `[]`; observed again `[]`; retained/reference=1/2. Qualifiers: `[]`.

### matched: 0 to 1

Earlier runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; later runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`.

- `classified_all`: n=6 to 6; support delta=-1; SCI delta=1/6; Gini-Simpson delta=-1/6.
- `classified_valid`: n=2 to 4; support delta=1; SCI delta=-3/8; Gini-Simpson delta=3/8.
- Finite pass fraction: 2/6 to 4/6; delta=1/3.

Joint observation: finite passing rising; support falling; concentration rising.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO', 'DIST-SETTLE']`; no longer observed `['DIST-RELAX']`; first observed `[]`; observed again `[]`; retained/reference=2/3. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `[]`; first observed `['DIST-SETTLE']`; observed again `[]`; retained/reference=1/1. Qualifiers: `[]`.

### matched: 1 to 2

Earlier runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; later runs: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`.

- `classified_all`: n=6 to 6; support delta=-1; SCI delta=4/9; Gini-Simpson delta=-4/9.
- `classified_valid`: n=4 to 6; support delta=-1; SCI delta=3/8; Gini-Simpson delta=-3/8.
- Finite pass fraction: 4/6 to 6/6; delta=1/3.

Joint observation: finite passing rising; support falling; concentration rising.

`classified_all` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `['DIST-SETTLE']`; first observed `[]`; observed again `[]`; retained/reference=1/2. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `['DIST-FIFO']`; no longer observed `['DIST-SETTLE']`; first observed `[]`; observed again `[]`; retained/reference=1/2. Qualifiers: `[]`.

## Missingness, risk sets and coverage

### Ordinal 0

Availability: `{'observed': 6}`.

Known stopped before this ordinal: `[]`; known reached: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| C1 | observed | C1-V0 |
| C2 | observed | C2-V0 |
| C3 | observed | C3-V0 |
| C4 | observed | C4-V0 |
| C5 | observed | C5-V0 |
| C6 | observed | C6-V0 |

available: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'failed': 4, 'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 3, 'DIST-RELAX': 1, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 2}`; validity `{'failed': 4, 'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.

### Ordinal 1

Availability: `{'observed': 6}`.

Known stopped before this ordinal: `[]`; known reached: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| C1 | observed | C1-V1 |
| C2 | observed | C2-V1 |
| C3 | observed | C3-V1 |
| C4 | observed | C4-V1 |
| C5 | observed | C5-V1 |
| C6 | observed | C6-V1 |

available: class counts `{'DIST-FIFO': 4, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 3, 'DIST-SETTLE': 1}`; validity `{'failed': 2, 'passed_under_supplied_scope': 4}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 4, 'DIST-SETTLE': 2}`; valid counts `{'DIST-FIFO': 3, 'DIST-SETTLE': 1}`; validity `{'failed': 2, 'passed_under_supplied_scope': 4}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.

### Ordinal 2

Availability: `{'observed': 6}`.

Known stopped before this ordinal: `[]`; known reached: `['C1', 'C2', 'C3', 'C4', 'C5', 'C6']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| C1 | observed | C1-V2 |
| C2 | observed | C2-V2 |
| C3 | observed | C3-V2 |
| C4 | observed | C4-V2 |
| C5 | observed | C5-V2 |
| C6 | observed | C6-V2 |

available: class counts `{'DIST-FIFO': 6}`; valid counts `{'DIST-FIFO': 6}`; validity `{'passed_under_supplied_scope': 6}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 6}`; valid counts `{'DIST-FIFO': 6}`; validity `{'passed_under_supplied_scope': 6}`; unadmitted `{}`.

Classification coverage observed=6/6; declared root groups `{'G-owned-fixtures': 6}`; unknown roots=0.


## Per-run trajectories

Rows follow supplied revision ordinals. Parent links determine lineage; sibling rows alone do not establish a mechanism transition. Repeated test receipts remain attached to their revision; their within-revision chronological order is unspecified.

### Run `C1`

Configuration: `concentration`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `C1-V2`.

Selected path: `['C1-V0', 'C1-V1', 'C1-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 2, 'test_receipts': 6, 'test_case_attempts': 60, 'completed_test_cases': 60}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | C1-V0 / generation | none | DIST-FIFO | passed_under_supplied_scope / E-C1-V0 | none |
| 1 | C1-V1 / no_op | C1-V0 | DIST-FIFO | passed_under_supplied_scope / E-C1-V1 | F-C1-V0 |
| 2 | C1-V2 / no_op | C1-V1 | DIST-FIFO | passed_under_supplied_scope / E-C1-V2 | F-C1-V1 |

Ordinal gaps: `[]`; transition states: `{'unchanged_source_and_mechanism': 2}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- C1-V0 (DIST-FIFO) to C1-V1 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- C1-V1 (DIST-FIFO) to C1-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`C1-V0`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C1-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C1-V0`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C1-V0`: test, receipt `T-C1-V0`, visible=True, received by `['C1-V1']`.

`C1-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C1-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C1-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C1-V1`: test, receipt `T-C1-V1`, visible=True, received by `['C1-V2']`.

`C1-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C1-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `retest-C1-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=False; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `C2`

Configuration: `concentration`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `C2-V2`.

Selected path: `['C2-V0', 'C2-V1', 'C2-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 2, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | C2-V0 / generation | none | DIST-FIFO | passed_under_supplied_scope / E-C2-V0 | none |
| 1 | C2-V1 / no_op | C2-V0 | DIST-FIFO | passed_under_supplied_scope / E-C2-V1 | F-C2-V0 |
| 2 | C2-V2 / no_op | C2-V1 | DIST-FIFO | passed_under_supplied_scope / E-C2-V2 | F-C2-V1 |

Ordinal gaps: `[]`; transition states: `{'unchanged_source_and_mechanism': 2}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- C2-V0 (DIST-FIFO) to C2-V1 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- C2-V1 (DIST-FIFO) to C2-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`C2-V0`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C2-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C2-V0`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C2-V0`: test, receipt `T-C2-V0`, visible=True, received by `['C2-V1']`.

`C2-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C2-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C2-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C2-V1`: test, receipt `T-C2-V1`, visible=True, received by `['C2-V2']`.

`C2-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C2-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `C3`

Configuration: `concentration`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `C3-V2`.

Selected path: `['C3-V0', 'C3-V1', 'C3-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | C3-V0 / generation | none | DIST-FIFO | failed / E-C3-V0 | none |
| 1 | C3-V1 / edit | C3-V0 | DIST-FIFO | passed_under_supplied_scope / E-C3-V1 | F-C3-V0 |
| 2 | C3-V2 / no_op | C3-V1 | DIST-FIFO | passed_under_supplied_scope / E-C3-V2 | F-C3-V1 |

Ordinal gaps: `[]`; transition states: `{'source_change_same_mechanism': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 2}]`.

- C3-V0 (DIST-FIFO) to C3-V1 (DIST-FIFO): `source_change_same_mechanism`; source changed=True; test scope changed=False.
- C3-V1 (DIST-FIFO) to C3-V2 (DIST-FIFO): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.

`C3-V0`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C3-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C3-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C3-V0`: test, receipt `T-C3-V0`, visible=True, received by `['C3-V1']`.

`C3-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C3-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C3-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C3-V1`: test, receipt `T-C3-V1`, visible=True, received by `['C3-V2']`.

`C3-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C3-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `C4`

Configuration: `concentration`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `C4-V2`.

Selected path: `['C4-V0', 'C4-V1', 'C4-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | C4-V0 / generation | none | DIST-SETTLE | failed / E-C4-V0 | none |
| 1 | C4-V1 / edit | C4-V0 | DIST-SETTLE | passed_under_supplied_scope / E-C4-V1 | F-C4-V0 |
| 2 | C4-V2 / edit | C4-V1 | DIST-FIFO | passed_under_supplied_scope / E-C4-V2 | F-C4-V1 |

Ordinal gaps: `[]`; transition states: `{'mechanism_switch': 1, 'source_change_same_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-SETTLE', 'to_class': 'DIST-FIFO', 'count': 1}, {'from_class': 'DIST-SETTLE', 'to_class': 'DIST-SETTLE', 'count': 1}]`.

- C4-V0 (DIST-SETTLE) to C4-V1 (DIST-SETTLE): `source_change_same_mechanism`; source changed=True; test scope changed=False.
- C4-V1 (DIST-SETTLE) to C4-V2 (DIST-FIFO): `mechanism_switch`; source changed=True; test scope changed=False.

`C4-V0`: artifact `settle_bad`, source `20f58c6cc9a8ba1c44541bb0731eb3a48501f64903834c26be63884be0611701`; assignment `M-settle_bad`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-C4-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C4-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C4-V0`: test, receipt `T-C4-V0`, visible=True, received by `['C4-V1']`.

`C4-V1`: artifact `settle_good`, source `af2307adae53c9e5493a5479f4f0a2176e7171c1e8ce1a0386fc8e3ef6d55457`; assignment `M-settle_good`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-C4-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C4-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C4-V1`: test, receipt `T-C4-V1`, visible=True, received by `['C4-V2']`.

`C4-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C4-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `C5`

Configuration: `concentration`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `C5-V2`.

Selected path: `['C5-V0', 'C5-V1', 'C5-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 1, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | C5-V0 / generation | none | DIST-SETTLE | failed / E-C5-V0 | none |
| 1 | C5-V1 / no_op | C5-V0 | DIST-SETTLE | failed / E-C5-V1 | F-C5-V0 |
| 2 | C5-V2 / edit | C5-V1 | DIST-FIFO | passed_under_supplied_scope / E-C5-V2 | F-C5-V1 |

Ordinal gaps: `[]`; transition states: `{'mechanism_switch': 1, 'unchanged_source_and_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-SETTLE', 'to_class': 'DIST-FIFO', 'count': 1}, {'from_class': 'DIST-SETTLE', 'to_class': 'DIST-SETTLE', 'count': 1}]`.

- C5-V0 (DIST-SETTLE) to C5-V1 (DIST-SETTLE): `unchanged_source_and_mechanism`; source changed=False; test scope changed=False.
- C5-V1 (DIST-SETTLE) to C5-V2 (DIST-FIFO): `mechanism_switch`; source changed=True; test scope changed=False.

`C5-V0`: artifact `settle_bad`, source `20f58c6cc9a8ba1c44541bb0731eb3a48501f64903834c26be63884be0611701`; assignment `M-settle_bad`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-C5-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C5-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C5-V0`: test, receipt `T-C5-V0`, visible=True, received by `['C5-V1']`.

`C5-V1`: artifact `settle_bad`, source `20f58c6cc9a8ba1c44541bb0731eb3a48501f64903834c26be63884be0611701`; assignment `M-settle_bad`, basis `fixture`, evidence lines 1-21; missing parents `[]`.

- Receipt `E-C5-V1`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C5-V1`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C5-V1`: test, receipt `T-C5-V1`, visible=True, received by `['C5-V2']`.

`C5-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C5-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.


### Run `C6`

Configuration: `concentration`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `C6-V2`.

Selected path: `['C6-V0', 'C6-V1', 'C6-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 60}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | C6-V0 / generation | none | DIST-RELAX | failed / E-C6-V0 | none |
| 1 | C6-V1 / edit | C6-V0 | DIST-FIFO | failed / E-C6-V1 | F-C6-V0 |
| 2 | C6-V2 / edit | C6-V1 | DIST-FIFO | passed_under_supplied_scope / E-C6-V2 | F-C6-V1 |

Ordinal gaps: `[]`; transition states: `{'mechanism_switch': 1, 'source_change_same_mechanism': 1}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-FIFO', 'count': 1}, {'from_class': 'DIST-RELAX', 'to_class': 'DIST-FIFO', 'count': 1}]`.

- C6-V0 (DIST-RELAX) to C6-V1 (DIST-FIFO): `mechanism_switch`; source changed=True; test scope changed=False.
- C6-V1 (DIST-FIFO) to C6-V2 (DIST-FIFO): `source_change_same_mechanism`; source changed=True; test scope changed=False.

`C6-V0`: artifact `relax_bad`, source `cc832ed979d21d53abed769b0c68241277181767d3a1d058e10f34f4ffce1634`; assignment `M-relax_bad`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-C6-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C6-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C6-V0`: test, receipt `T-C6-V0`, visible=True, received by `['C6-V1']`.

`C6-V1`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C6-V1`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.
- Receipt `T-C6-V1`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff`.
- Feedback `F-C6-V1`: test, receipt `T-C6-V1`, visible=True, received by `['C6-V2']`.

`C6-V2`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-C6-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d`.

## Test scope identities

| Scope | Suite SHA-256 | Oracle | Environment fingerprint | Basis | Visibility |
| --- | --- | --- | --- | --- | --- |
| `306473802377d0ee6627427879783947540bf7596a803e6cbd02f95f04cf70ff` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `a515c93632fe1d25cb194362feb115da2f9336e9eea2f5beb5b6f0fb33c5f7f7` | project_fixture_execution | feedback |
| `a55a2b189c47d7accc505a7f6deedfe78e305e92ba412294374055d4a929467d` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `a515c93632fe1d25cb194362feb115da2f9336e9eea2f5beb5b6f0fb33c5f7f7` | project_fixture_execution | withheld |

## What this result supports

This report describes source-bound revision histories and conditional distributions over the named run roster. The joint outcomes preserve both finite correctness and mechanism changes, with missing prerequisites beside unavailable comparisons.

Study binding: `767121f008ccd461f04e055f64e23f41292a4f3428fda6de9cd7a11a7039f747`; design binding: `fd23528a075a111df3fdd56bd995c4a21446fc43d6207edbb9dcdf0ce7dc9552`; task binding: `7cca04509c795eefdbb6cb3318922f89154f04c45236ba2021ab5be9316c79d1`.

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
