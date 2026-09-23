# StructDet Code condition comparison

Status: `compatible_descriptive`.

Selection: `fixed_prefix/0.1`; requested prefix: `4`.

All differences below are right minus left. Counts refer to admitted mechanism labels.

| Side | Material | Prefix observed / requested | Missing positions | Excluded later | Classified | Finite passed |
| --- | --- | --- | --- | --- | --- | --- |
| left: `graph-fixture-left` | fixture | 4 / 4 | none | 0 | 4 | 4 |
| right: `graph-fixture-right` | fixture | 3 / 4 | 3 | 1 | 3 | 2 |

## left: `graph-fixture-left`

Task: `unit-graph-distances`; frame: `7cca04509c795eefdbb6cb3318922f89154f04c45236ba2021ab5be9316c79d1`.

Study: `b9c30a515535174cc38bcc69c8688544cf92e11481b2b354e860761b85f55c10`; configuration: `C-fixture`.

Planned positions: `4`; per-slot budget: `{'unit': 'attempts', 'limit': 1}`.

Population: fixed prefix.

Validity states: `{'passed_under_supplied_scope': 4}`; admitted bases: `{'static_rule': 4}`.

Unadmitted reasons: `{}`.

Declared root groups: `{'G-project-fixtures': 4}`; unknown: 0.

- `classified_all`: n=4; counts `{'DIST-FIFO': 2, 'DIST-RELAX': 1, 'DIST-SETTLE': 1}`; support=3; SCI=3/8.
- `classified_valid`: n=4; counts `{'DIST-FIFO': 2, 'DIST-RELAX': 1, 'DIST-SETTLE': 1}`; support=3; SCI=3/8.

| Position | Revision | Class / state | Validity | Receipt | Source SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 1 | `V001` | `DIST-FIFO` | passed_under_supplied_scope | `T001` | `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6` |
| 2 | `V002` | `DIST-FIFO` | passed_under_supplied_scope | `T002` | `b88f5a2569848ca2cdac0a6a3befcc51c50fbcdcb901c717578936fb8dee5d50` |
| 3 | `V003` | `DIST-SETTLE` | passed_under_supplied_scope | `T003` | `af2307adae53c9e5493a5479f4f0a2176e7171c1e8ce1a0386fc8e3ef6d55457` |
| 4 | `V004` | `DIST-RELAX` | passed_under_supplied_scope | `T004` | `3aeaab133049367ebd4d6ff782b9c52b1d02e9cc2be3790e0506fba006fb3235` |

Test scopes: `[{'scope_sha256': '510c0b25cdd29645f5c8213239498f5bd078267993b8bca03461107ae1912767', 'suite_sha256': '409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691', 'oracle_id': 'unit-distance-properties/0.1', 'environment_sha256': '55c133f1d7eee6fd3637890006fb052b603534ad05cf892aef2aa973180e2fa8', 'execution_basis': 'project_fixture_execution'}]`.

Excluded later selected records: `[]`.

## right: `graph-fixture-right`

Task: `unit-graph-distances`; frame: `7cca04509c795eefdbb6cb3318922f89154f04c45236ba2021ab5be9316c79d1`.

Study: `dfe9a63010712a47363221bf89d8939ff67dfdd6b0bc5ce6f31abbcde4e4c340`; configuration: `C-fixture`.

Planned positions: `5`; per-slot budget: `{'unit': 'attempts', 'limit': 1}`.

Population: fixed prefix.

Validity states: `{'failed': 1, 'passed_under_supplied_scope': 2}`; admitted bases: `{'static_rule': 3}`.

Unadmitted reasons: `{}`.

Declared root groups: `{'G-project-fixtures': 3}`; unknown: 0.

- `classified_all`: n=3; counts `{'DIST-FIFO': 3}`; support=1; SCI=1/1.
- `classified_valid`: n=2; counts `{'DIST-FIFO': 2}`; support=1; SCI=1/1.

| Position | Revision | Class / state | Validity | Receipt | Source SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 1 | `V001` | `DIST-FIFO` | passed_under_supplied_scope | `T001` | `6e547db59981f39bd11483251b788ec0ee4b1acaa36853febd8fd3cd2de84bf6` |
| 2 | `V002` | `DIST-FIFO` | failed | `T002` | `8c40aedf4fcade93014e5c133f03be947e0f6a39570c3ebb18ea4ebccb58a053` |
| 4 | `V003` | `DIST-FIFO` | passed_under_supplied_scope | `T003` | `05aec4574962b9e2f4347d84eb57ec7312bde793f122f3683e9dba7442134bb8` |

Test scopes: `[{'scope_sha256': '510c0b25cdd29645f5c8213239498f5bd078267993b8bca03461107ae1912767', 'suite_sha256': '409ec3d6d0c14d9cdab3930955d1637475b9657fa400044eb6c59fa681ea1691', 'oracle_id': 'unit-distance-properties/0.1', 'environment_sha256': '55c133f1d7eee6fd3637890006fb052b603534ad05cf892aef2aa973180e2fa8', 'execution_basis': 'project_fixture_execution'}]`.

Excluded later selected records: `[{'position': 5, 'revision_id': 'V004'}]`.

## Conditional descriptive differences

- `classified_all`: left n=4, right n=3; support delta=-2; SCI delta=5/8; Gini-Simpson delta=-5/8.
- `classified_valid`: left n=4, right n=2; support delta=-2; SCI delta=5/8; Gini-Simpson delta=-5/8.

Shared source digests in the two prefixes: 1.

## Limits

- Condition, budget and slot records are supplied claims; their provenance is not authenticated.
- Deltas describe admitted populations under the supplied fixed-prefix design; coverage can differ.
- Missing outputs retain their positions; observed failures are kept; later outputs never backfill.
- Finite-test comparisons require one common supplied suite, oracle, environment and execution basis.
- Source overlap is disclosed; distinct bytes or run IDs do not establish independent samples.
- No causal effect, population uncertainty, general model capacity or degradation is estimated.
