# StructDet Code inspection

Study: `c02-static-sorting`
Material: `fixture`. Claim scope: `fixture_arithmetic`.
Evidence policy: `static_or_reviewed`.

Selected observations: 7. Recorded runs: 7. Recorded revisions: 7.

| View | Classified n | Mechanisms | SCI | Gini-Simpson |
| --- | ---: | ---: | ---: | ---: |
| classified_all | 6 | 3 | 1/2 | 1/2 |
| classified_valid | 0 | 0 | undefined (empty) | undefined (empty) |

Assignment coverage: accepted=6, unresolved=1.
Validity: not_assessed=7.
Admitted coverage: 6/7 selected observations. Rule matches: 6/7 source records.
Admitted bases: static_rule=6.
Unadmitted reasons: opaque_dependency=1.

## Mechanism distribution

| Mechanism | All admitted | Valid admitted |
| --- | ---: | ---: |
| SORT-INS | 4 | 0 |
| SORT-MERGE | 1 | 0 |
| SORT-SEL | 1 | 0 |

## Selected records

| Revision | Artifact | Assignment | Basis | Mechanism label | Validity |
| --- | --- | --- | --- | --- | --- |
| V001 | A001 | accepted | static_rule | SORT-INS | not_assessed |
| V002 | A002 | accepted | static_rule | SORT-INS | not_assessed |
| V003 | A003 | accepted | static_rule | SORT-INS | not_assessed |
| V004 | A004 | accepted | static_rule | SORT-INS | not_assessed |
| V005 | A005 | accepted | static_rule | SORT-MERGE | not_assessed |
| V006 | A006 | unresolved | static_rule | unresolved | not_assessed |
| V007 | A007 | accepted | static_rule | SORT-SEL | not_assessed |

## Static evidence and review needs

These observations cover syntax, including potentially inactive code. Only a complete rule match admits a static label.

| Artifact | Source SHA-256 | Rule or review reason | Evidence lines |
| --- | --- | --- | --- |
| A001 | `3b0cf517ed4de3908153985e38002fe656da6169359ab18774b3fffb2325e6d8` | sort-ins-shift-copy/1 | 1-11, 4-10, 7-7, 7-9, 8-8, 10-10 |
| A002 | `0172f09e271411f9469d50f9ab6f38aedee8c5e9f4bd56489462dd52928a76fe` | sort-ins-shift-copy/1 | 1-10, 3-9, 6-6, 6-8, 7-7, 9-9 |
| A003 | `12f24a5a1d3155298b1c8e5947c289da4481a50236b874e9a089b7fd9360117a` | sort-ins-shift-alias/1 | 1-11, 4-10, 7-7, 7-9, 8-8, 10-10 |
| A004 | `e0264b412cfb32d98ea9d2a0fff0fe0a5de64a402fd8ba54d58e708800d780f1` | sort-ins-shift-copy/1 | 1-10, 3-9, 6-6, 6-8, 7-7, 9-9 |
| A005 | `2e927eda21d5cbbd834102b5fbf68b038e837de217fc9e4630946040e30d3c08` | sort-merge-halves/1 | 1-18, 2-2, 9-9, 9-15, 10-10 |
| A006 | `f562aeb492fea4a9f6ee60dd335b1b3c9a056744b59ff3d2bd179d3e33557a6f` | opaque_dependency | review required |
| A007 | `f861f4e2a971e6d8d9bc36fc08df1a4bce367016e2748052135336b72a784af5` | sort-sel-extract/1 | 1-10, 4-9, 6-8, 7-7 |

## What this result supports

The two distributions summarize explicitly selected observations under the named evidence policy. Proposed and unresolved labels contribute to coverage accounting only. The valid view additionally requires a complete passing receipt and supplied passing conformance review.

- Record checks do not authenticate reviews, provenance or test execution.
- Static rules cover exact whole-module variants; unmatched code requires review.
- Static observations and recognizer matches do not establish finite-test validity.
- Finite test passing is limited to the named suite and supplied conformance review.
- Revision links are preserved; cohort convergence analysis is scheduled for C04.
