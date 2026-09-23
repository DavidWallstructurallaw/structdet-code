# StructDet Code inspection

Study: `c01-owned-sorting`
Material: `fixture`. Claim scope: `fixture_arithmetic`.

Selected observations: 7. Recorded runs: 7. Recorded revisions: 10.

| View | Classified n | Mechanisms | SCI | Gini-Simpson |
| --- | ---: | ---: | ---: | ---: |
| classified_all | 5 | 3 | 11/25 | 14/25 |
| classified_valid | 4 | 3 | 3/8 | 5/8 |

Assignment coverage: accepted=5, proposed=1, unresolved=1.
Validity: failed=2, passed_under_supplied_scope=5.

## Selected records

| Revision | Assignment | Mechanism label | Validity |
| --- | --- | --- | --- |
| R1V0 | accepted | SORT-INS | failed |
| R2V0 | accepted | SORT-INS | passed_under_supplied_scope |
| R3V0 | accepted | SORT-INS | passed_under_supplied_scope |
| R4V0 | accepted | SORT-MERGE | passed_under_supplied_scope |
| R5V0 | accepted | SORT-SEL | passed_under_supplied_scope |
| R6V0 | unresolved | unresolved | failed |
| R7V0 | proposed | SORT-MERGE | passed_under_supplied_scope |

## What this result supports

The two distributions summarize explicitly selected observations with admitted supplied labels. Proposed and unresolved labels contribute to coverage accounting only. The valid view additionally requires a complete passing receipt and supplied passing conformance review.

- Record checks do not authenticate reviews, provenance or test execution.
- Mechanism labels are supplied; automatic recognition starts in C02.
- Finite test passing is limited to the named suite and supplied conformance review.
- C01 preserves revision links; cohort convergence analysis is scheduled for C04.
