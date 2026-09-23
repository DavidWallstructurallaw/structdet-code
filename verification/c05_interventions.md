# StructDet Code revision trace

Study: `owned-intervention-example`; trace: `intervention-and-reappearance`; material: `fixture`.

Task: `unit-graph-distances`; evidence policy: `fixture_only`.

Clock: `revision_ordinal`; selection: `declared-path-exact-ordinal/0.1`.

Roster: 2 runs; 2 recorded. Explicitly unrecorded: `[]`.

Cohort status: `compatible_descriptive`; reasons: `[]`.

Matched across every requested checkpoint: `['I1', 'I2']`.

Recorded stopping reasons: `{'budget': 2}`. Study runs outside this roster: `[]`.

Supplied interventions: 9; finite failure profiles: 4. The evidence section records exposure, reuse claims and reference-byte matches; causal effects are not estimated.

## Checkpoint populations

Available cases retain each recorded observation at that ordinal. Matched cases retain the same run IDs at every selected checkpoint.

| Ordinal | Cohort | Observed / roster | Admitted | Finite passed / observed | Support | SCI | Valid admitted | Valid SCI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | available | 2 / 2 | 2 | 1/2 | 1 | 1/1 | 1 | single_admitted_observation |
| 0 | matched | 2 / 2 | 2 | 1/2 | 1 | 1/1 | 1 | single_admitted_observation |
| 1 | available | 2 / 2 | 2 | 1/2 | 1 | 1/1 | 1 | single_admitted_observation |
| 1 | matched | 2 / 2 | 2 | 1/2 | 1 | 1/1 | 1 | single_admitted_observation |
| 2 | available | 2 / 2 | 2 | 2/2 | 1 | 1/1 | 2 | 1/1 |
| 2 | matched | 2 / 2 | 2 | 2/2 | 1 | 1/1 | 2 | 1/1 |

Missing outputs are not failed tests. Single-observation concentration is not applicable.

Whole declared-path transition states: `{'mechanism_switch': 4}`; supported adjacent counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-RELAX', 'count': 2}, {'from_class': 'DIST-RELAX', 'to_class': 'DIST-FIFO', 'count': 2}]`.

## Changes and joint outcomes

All numeric differences are later minus earlier, qualified by the recorded cohort and evidence.

### available: 0 to 1

Earlier runs: `['I1', 'I2']`; later runs: `['I1', 'I2']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: unavailable; `['fewer_than_two_admitted_runs']`.
- Finite pass fraction: 1/2 to 1/2; delta=0/1.

Joint observation: finite passing stable; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-RELAX']`; first observed `['DIST-FIFO']`; observed again `[]`; retained/reference=0/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-RELAX']`; first observed `['DIST-FIFO']`; observed again `[]`; retained/reference=0/1. Qualifiers: `[]`.

### available: 1 to 2

Earlier runs: `['I1', 'I2']`; later runs: `['I1', 'I2']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: unavailable; `['fewer_than_two_admitted_runs']`.
- Finite pass fraction: 1/2 to 2/2; delta=1/2.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-FIFO']`; first observed `[]`; observed again `['DIST-RELAX']`; retained/reference=0/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-FIFO']`; first observed `[]`; observed again `['DIST-RELAX']`; retained/reference=0/1. Qualifiers: `[]`.

### matched: 0 to 1

Earlier runs: `['I1', 'I2']`; later runs: `['I1', 'I2']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: unavailable; `['fewer_than_two_admitted_runs']`.
- Finite pass fraction: 1/2 to 1/2; delta=0/1.

Joint observation: finite passing stable; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-RELAX']`; first observed `['DIST-FIFO']`; observed again `[]`; retained/reference=0/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-RELAX']`; first observed `['DIST-FIFO']`; observed again `[]`; retained/reference=0/1. Qualifiers: `[]`.

### matched: 1 to 2

Earlier runs: `['I1', 'I2']`; later runs: `['I1', 'I2']`.

- `classified_all`: n=2 to 2; support delta=0; SCI delta=0/1; Gini-Simpson delta=0/1.
- `classified_valid`: unavailable; `['fewer_than_two_admitted_runs']`.
- Finite pass fraction: 1/2 to 2/2; delta=1/2.

Joint observation: finite passing rising; support stable; concentration stable.

`classified_all` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-FIFO']`; first observed `[]`; observed again `['DIST-RELAX']`; retained/reference=0/1. Qualifiers: `[]`.

`classified_valid` sets (comparable_observed_sets): retained `[]`; no longer observed `['DIST-FIFO']`; first observed `[]`; observed again `['DIST-RELAX']`; retained/reference=0/1. Qualifiers: `[]`.

## Missingness, risk sets and coverage

### Ordinal 0

Availability: `{'observed': 2}`.

Known stopped before this ordinal: `[]`; known reached: `['I1', 'I2']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| I1 | observed | I1-V0 |
| I2 | observed | I2-V0 |

available: class counts `{'DIST-RELAX': 2}`; valid counts `{'DIST-RELAX': 1}`; validity `{'failed': 1, 'passed_under_supplied_scope': 1}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


matched: class counts `{'DIST-RELAX': 2}`; valid counts `{'DIST-RELAX': 1}`; validity `{'failed': 1, 'passed_under_supplied_scope': 1}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.

### Ordinal 1

Availability: `{'observed': 2}`.

Known stopped before this ordinal: `[]`; known reached: `['I1', 'I2']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| I1 | observed | I1-V1 |
| I2 | observed | I2-V1 |

available: class counts `{'DIST-FIFO': 2}`; valid counts `{'DIST-FIFO': 1}`; validity `{'failed': 1, 'passed_under_supplied_scope': 1}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


matched: class counts `{'DIST-FIFO': 2}`; valid counts `{'DIST-FIFO': 1}`; validity `{'failed': 1, 'passed_under_supplied_scope': 1}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.

### Ordinal 2

Availability: `{'observed': 2}`.

Known stopped before this ordinal: `[]`; known reached: `['I1', 'I2']`; reach unknown: `[]`.

| Run | State | Selected revision |
| --- | --- | --- |
| I1 | observed | I1-V2 |
| I2 | observed | I2-V2 |

available: class counts `{'DIST-RELAX': 2}`; valid counts `{'DIST-RELAX': 2}`; validity `{'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


matched: class counts `{'DIST-RELAX': 2}`; valid counts `{'DIST-RELAX': 2}`; validity `{'passed_under_supplied_scope': 2}`; unadmitted `{}`.

Classification coverage observed=2/2; declared root groups `{'G-owned-fixtures': 2}`; unknown roots=0.


## Per-run trajectories

Rows follow supplied revision ordinals. Parent links determine lineage; sibling rows alone do not establish a mechanism transition. Repeated test receipts remain attached to their revision; their within-revision chronological order is unspecified.

### Run `I1`

Configuration: `fixture`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `I1-V2`.

Selected path: `['I1-V0', 'I1-V1', 'I1-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 50}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | I1-V0 / generation | none | DIST-RELAX | passed_under_supplied_scope / E-I1-V0 | none |
| 1 | I1-V1 / edit | I1-V0 | DIST-FIFO | passed_under_supplied_scope / E-I1-V1 | F-I1-V0 |
| 2 | I1-V2 / edit | I1-V1 | DIST-RELAX | passed_under_supplied_scope / E-I1-V2 | F-I1-V1 |

Ordinal gaps: `[]`; transition states: `{'mechanism_switch': 2}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-RELAX', 'count': 1}, {'from_class': 'DIST-RELAX', 'to_class': 'DIST-FIFO', 'count': 1}]`.

- I1-V0 (DIST-RELAX) to I1-V1 (DIST-FIFO): `mechanism_switch`; source changed=True; test scope changed=False.
- I1-V1 (DIST-FIFO) to I1-V2 (DIST-RELAX): `mechanism_switch`; source changed=True; test scope changed=False.

`I1-V0`: artifact `relax_good`, source `3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235`; assignment `M-relax_good`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-I1-V0`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7`.
- Receipt `T-I1-V0`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `8db9ff5837183c9fe92ebac9d601e1cc641698dcb7026ee0f43c3d0d31eccc49`.
- Feedback `F-I1-V0`: test, receipt `T-I1-V0`, visible=True, received by `['I1-V1']`.

`I1-V1`: artifact `fifo_good`, source `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6`; assignment `M-fifo_good`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-I1-V1`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7`.
- Receipt `T-I1-V1`: passed; attempted/completed/passed=10/10/10; visibility=feedback; selected=False; scope `8db9ff5837183c9fe92ebac9d601e1cc641698dcb7026ee0f43c3d0d31eccc49`.
- Feedback `F-I1-V1`: test, receipt `T-I1-V1`, visible=True, received by `['I1-V2']`.

`I1-V2`: artifact `relax_good`, source `3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235`; assignment `M-relax_good`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-I1-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7`.


### Run `I2`

Configuration: `fixture`; root group: `G-owned-fixtures`.

Stop: `budget` at supplied ordinal `2`; selected endpoint: `I2-V2`.

Selected path: `['I2-V0', 'I2-V1', 'I2-V2']`; excluded revisions: `[]`.

Budget: `{'max_revision_ordinal': 2, 'max_test_case_attempts': 50}`; recorded usage: `{'recorded_revisions': 3, 'maximum_ordinal': 2, 'generation_records': 1, 'no_op_revisions': 0, 'test_receipts': 5, 'test_case_attempts': 50, 'completed_test_cases': 50}`; recorded excess: `[]`.

| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |
| --- | --- | --- | --- | --- | --- |
| 0 | I2-V0 / generation | none | DIST-RELAX | failed / E-I2-V0 | none |
| 1 | I2-V1 / edit | I2-V0 | DIST-FIFO | failed / E-I2-V1 | F-I2-V0 |
| 2 | I2-V2 / edit | I2-V1 | DIST-RELAX | passed_under_supplied_scope / E-I2-V2 | F-I2-V1 |

Ordinal gaps: `[]`; transition states: `{'mechanism_switch': 2}`.

Supported adjacent selected-path transition counts: `[{'from_class': 'DIST-FIFO', 'to_class': 'DIST-RELAX', 'count': 1}, {'from_class': 'DIST-RELAX', 'to_class': 'DIST-FIFO', 'count': 1}]`.

- I2-V0 (DIST-RELAX) to I2-V1 (DIST-FIFO): `mechanism_switch`; source changed=True; test scope changed=False.
- I2-V1 (DIST-FIFO) to I2-V2 (DIST-RELAX): `mechanism_switch`; source changed=True; test scope changed=False.

`I2-V0`: artifact `relax_bad`, source `cc832ed979d21d53abed769b0c68241277181767d3a1d058e10f34f4ffce1634`; assignment `M-relax_bad`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-I2-V0`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7`.
- Receipt `T-I2-V0`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `8db9ff5837183c9fe92ebac9d601e1cc641698dcb7026ee0f43c3d0d31eccc49`.
- Feedback `F-I2-V0`: test, receipt `T-I2-V0`, visible=True, received by `['I2-V1']`.

`I2-V1`: artifact `fifo_bad`, source `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053`; assignment `M-fifo_bad`, basis `fixture`, evidence lines 1-16; missing parents `[]`.

- Receipt `E-I2-V1`: failed; attempted/completed/passed=10/10/4; visibility=withheld; selected=True; scope `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7`.
- Receipt `T-I2-V1`: failed; attempted/completed/passed=10/10/4; visibility=feedback; selected=False; scope `8db9ff5837183c9fe92ebac9d601e1cc641698dcb7026ee0f43c3d0d31eccc49`.
- Feedback `F-I2-V1`: test, receipt `T-I2-V1`, visible=True, received by `['I2-V2']`.

`I2-V2`: artifact `relax_good`, source `3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235`; assignment `M-relax_good`, basis `fixture`, evidence lines 1-14; missing parents `[]`.

- Receipt `E-I2-V2`: passed; attempted/completed/passed=10/10/10; visibility=withheld; selected=True; scope `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7`.

## Test scope identities

| Scope | Suite SHA-256 | Oracle | Environment fingerprint | Basis | Visibility |
| --- | --- | --- | --- | --- | --- |
| `12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `7eb27d55ac19445729a4d6cb5e72195239591d444010a2812c86278510c96a9b` | project_fixture_execution | withheld |
| `8db9ff5837183c9fe92ebac9d601e1cc641698dcb7026ee0f43c3d0d31eccc49` | `409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691` | unit-distance-properties/0.1 | `7eb27d55ac19445729a4d6cb5e72195239591d444010a2812c86278510c96a9b` | project_fixture_execution | feedback |

## What this result supports

This report describes source-bound revision histories and conditional distributions over the named run roster. The joint outcomes preserve both finite correctness and mechanism changes, with missing prerequisites beside unavailable comparisons.

Study binding: `0b97fc1cd6d97fcf7f27e9ed9c4e7f333ccf78eab899d1b213a625107e3bc35c`; design binding: `17d6125aaf6582bc557c269196d71b2c21d169b6412a4fe0a2f7ed937c22bea4`; task binding: `7cca04509c795eefdbb6cb3318922f89154f04c45236ba2021ab5be9316c79d1`.

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

## Interventions and supplied evidence

Evidence binding: a5e7c8ce6ba34504b16d64809877465b9146990ae84d69919d30f2ceb3488a6c. Material records: 3.

Study configurations describe the original context; these ordered records describe subsequent supplied exposure. More than one event can precede the same revision, so a subsequent class is not attributed to one event.

| Run | Order | After / before revision | Kind / visibility | Mechanism observation | Exact reference matches |
| --- | --- | --- | --- | --- | --- |
| I1 | 1 | None / I1-V0 | baseline_prompt / visible | first_observed (None to DIST-RELAX) | [] |
| I1 | 2 | I1-V0 / I1-V1 | test_feedback / visible | first_observed (DIST-RELAX to DIST-FIFO) | [] |
| I1 | 3 | I1-V1 / I1-V2 | test_feedback / visible | observed_again (DIST-FIFO to DIST-RELAX) | [] |
| I1 | 4 | I1-V1 / I1-V2 | reference_material / visible | observed_again (DIST-FIFO to DIST-RELAX) | ['reference'] |
| I2 | 1 | None / I2-V0 | baseline_prompt / visible | first_observed (None to DIST-RELAX) | [] |
| I2 | 2 | I2-V0 / I2-V1 | test_feedback / visible | first_observed (DIST-RELAX to DIST-FIFO) | [] |
| I2 | 3 | I2-V1 / I2-V2 | test_feedback / visible | observed_again (DIST-FIFO to DIST-RELAX) | [] |
| I2 | 4 | I2-V1 / I2-V2 | alternative_strategy / visible | observed_again (DIST-FIFO to DIST-RELAX) | [] |
| I2 | 5 | I2-V1 / I2-V2 | reference_material / withheld | observed_again (DIST-FIFO to DIST-RELAX) | ['reference'] |

Event I1-prompt: materials ['task']; feedback []; reuse claim none; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I1-test0: materials []; feedback ['F-I1-V0']; reuse claim none; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I1-test1: materials []; feedback ['F-I1-V1']; reuse claim none; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I1-reference: materials ['reference']; feedback []; reuse claim copied; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I2-prompt: materials ['task']; feedback []; reuse claim none; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I2-test0: materials []; feedback ['F-I2-V0']; reuse claim none; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I2-test1: materials []; feedback ['F-I2-V1']; reuse claim none; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I2-alternate: materials ['alternate']; feedback []; reuse claim unknown; agent-visible selected-path association True; uncaptured materials []. External recovery is not estimated.

Event I2-withheld: materials ['reference']; feedback []; reuse claim unknown; agent-visible selected-path association False; uncaptured materials []. External recovery is not estimated.

Material alternate: instruction, origin project_fixture, bytes captured True, SHA-256 bc0a74b5590f1ca1944b061252d1055939f8bef4d047bcfbba8d89ce948ed700; independence claim shared_origin (unverified).

Material reference: reference_code, origin project_fixture, bytes captured True, SHA-256 3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235; independence claim shared_origin (unverified).

Material task: instruction, origin project_fixture, bytes captured True, SHA-256 0a83b587c79466d7ed875cd2dd3e47378ccf2978e980b1f62252c72b619ddf13; independence claim shared_origin (unverified).

## Finite failure profiles

Profiles describe the explicitly supplied receipts, including any outside the analysis selection.

- P-E-I1-V0: receipt E-I1-V0, revision I1-V0; selected True; conformance passed; failed cases []; unobserved []; source 3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235; scope 12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7.
- P-E-I2-V0: receipt E-I2-V0, revision I2-V0; selected True; conformance passed; failed cases ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; unobserved []; source cc832ed979d21d53abed769b0c68241277181767d3a1d058e10f34f4ffce1634; scope 12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7.
- P-E-I2-V1: receipt E-I2-V1, revision I2-V1; selected True; conformance passed; failed cases ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; unobserved []; source 8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053; scope 12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7.
- P-E-I2-V2: receipt E-I2-V2, revision I2-V2; selected True; conformance passed; failed cases []; unobserved []; source 3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235; scope 12c5c9a08d001ed94959ef80b2427720a1103ad0c2e73356d5297e2401ff26e7.

- P-E-I1-V0 / P-E-I2-V0: completed in both 10/10; both failed []; left failed/right passed []; right failed/left passed ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; failures with other side unobserved [] / []; same bytes False, same run False.
- P-E-I1-V0 / P-E-I2-V1: completed in both 10/10; both failed []; left failed/right passed []; right failed/left passed ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; failures with other side unobserved [] / []; same bytes False, same run False.
- P-E-I1-V0 / P-E-I2-V2: completed in both 10/10; both failed []; left failed/right passed []; right failed/left passed []; failures with other side unobserved [] / []; same bytes True, same run False.
- P-E-I2-V0 / P-E-I2-V1: completed in both 10/10; both failed ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; left failed/right passed []; right failed/left passed []; failures with other side unobserved [] / []; same bytes False, same run True.
- P-E-I2-V0 / P-E-I2-V2: completed in both 10/10; both failed []; left failed/right passed ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; right failed/left passed []; failures with other side unobserved [] / []; same bytes False, same run True.
- P-E-I2-V1 / P-E-I2-V2: completed in both 10/10; both failed []; left failed/right passed ['T04', 'T05', 'T06', 'T07', 'T08', 'T10']; right failed/left passed []; failures with other side unobserved [] / []; same bytes False, same run True.

Failure independence and causal effects are not established.

- Intervention order, visibility and reuse are supplied records; source independence is not authenticated.
- Exact reference-byte matches describe content identity, without proof of how the program was produced.
- A mechanism observed after a visible intervention is an association, with no causal or autonomous-discovery claim.
- Failure overlap uses the same finite test scope and jointly completed cases; absent outcomes are not successes.
- Failure profiles do not establish independent errors, deployment reliability or a preferred candidate.
