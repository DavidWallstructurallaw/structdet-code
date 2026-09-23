# 0.1.0 release preparation

C06 prepares reviewable source and distribution artifacts. Creating a version
tag, GitHub Release or PyPI upload is a separate publishing action and has not
been performed. Version 0.1.0 identifies the prepared code and artifacts; no
package-index availability is implied.

## What is ready

- Passive static preparation, sorting/graph recognition and source-bound review.
- Compatible condition comparison, per-run trajectories and checkpoint cohorts.
- Intervention/failure evidence, correction invalidation and exact offline replay.
- Installed example export and six runnable, replayed demonstrations.
- Wheel and source-archive packaging with task/example data and license texts.
- Linux/CPython 3.12.14 source regression and two installed distribution routes.
- User guides, related-work attribution and release notes in CHANGELOG.md.

The actual artifact sizes/hashes and route results are in
[`verification/c06_installation.json`](https://github.com/DavidWallstructurallaw/structdet-code/blob/main/verification/c06_installation.json).
Reproduce them using `tools/qualify_distribution.py` as documented in INSTALL.md.
Archive hashes describe that build, without a cross-build reproducibility claim.

## Publishing the reviewed result

After the C06 PR is accepted and explicit publishing authorization is given,
create the release tag at the reviewed merge, attach the qualified wheel and
source archive with their hashes, and use CHANGELOG.md's 0.1.0 entry as the release
notes. Verify that the tagged runtime/task/example bytes match those qualified.
If they change, build and qualify fresh artifacts before publication. PyPI
publication additionally requires the owner's chosen account/project authority;
there is no stored upload credential in this project.

Historical dev5 snapshots still require their original matching software/runtime.
A fresh 0.1.0 snapshot is required for 0.1.0 analysis. Task packs and record schema
identities are unchanged by the installation work.

## Repository About fields

Package metadata and README use this description:

> Analyze solution-mechanism diversity and coding-agent convergence from recorded programs, test results, and revision histories.

Suggested GitHub topics are `code-generation`, `algorithmic-diversity`,
`llm-evaluation`, `coding-agents`, `program-analysis`, `software-testing` and
`reproducible-research`. These fields accurately describe supported work without
claiming a general classifier or autonomous live-agent service. The currently
connected GitHub API exposes file/PR operations, without an About/topics setter;
the proposed settings are retained here for application with repository settings
access. The existing repository description already describes a development
toolkit for mechanisms, structural diversity and revision histories.
