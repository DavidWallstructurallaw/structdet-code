# 0.1.0 release guide

C06 provides version 0.1.0 source and distribution artifacts. Published versions
and their downloads are listed on
[GitHub Releases](https://github.com/DavidWallstructurallaw/structdet-code/releases).
The version in source identifies the code; it does not imply package-index
availability. This release process covers GitHub and includes no PyPI upload.

## What is ready

- Passive static preparation, sorting/graph recognition and source-bound review.
- Compatible condition comparison, per-run trajectories and checkpoint cohorts.
- Intervention/failure evidence, correction invalidation and exact offline replay.
- Installed example export and six runnable, replayed demonstrations.
- Wheel and source-archive packaging with task/example data and license texts.
- Linux/CPython 3.12.14 source regression and two installed distribution routes.
- User guides, related-work attribution and release notes in CHANGELOG.md.

The original C06 artifact sizes/hashes and route results are in
[`verification/c06_installation.json`](https://github.com/DavidWallstructurallaw/structdet-code/blob/main/verification/c06_installation.json).
Reproduce the checks using `tools/qualify_distribution.py` as documented in INSTALL.md.
Archive hashes describe that build, without a cross-build reproducibility claim.

Publication artifacts include the final README, guides and package keywords.
Their hashes belong in the release's `SHA256SUMS`; do not use the original C06
hashes for a later build. Verify package contents and the installed CLI after
documentation or metadata updates. The existing analysis qualification applies
when runtime, task and example bytes remain unchanged.

## Publishing the reviewed result

Create tag `v0.1.0` at the reviewed C06 merge after publishing authorization,
attach the qualified wheel and source archive with `SHA256SUMS`, and use
CHANGELOG.md's 0.1.0 entry as the release notes. Verify that the tagged
runtime/task/example bytes match those qualified.
If they change, build and qualify fresh artifacts before publication. PyPI
publication additionally requires the owner's chosen account/project authority;
there is no stored upload credential in this project.

Historical dev5 snapshots still require their original matching software/runtime.
A fresh 0.1.0 snapshot is required for 0.1.0 analysis. Task packs and record schema
identities are unchanged by the installation work.

## Repository About fields

GitHub description and package summary:

> Code diversity and coding agent evaluation for LLMs: analyze algorithmic diversity, solution convergence, and recorded revision trajectories. Offline Python CLI.

GitHub Topics and package keywords, in priority order:

```text
llm-evaluation
coding-agents
agent-evaluation
code-generation
code-diversity
algorithmic-diversity
agent-trajectory
trajectory-analysis
program-analysis
reproducible-research
python
```

The broad terms connect to LLM and coding-agent evaluation audiences; the
diversity and trajectory terms identify the actual specialty. Repository search
[uses names, descriptions and topics by default](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories#search-by-repository-name-description-or-contents-of-the-readme-file);
README search requires `in:readme`. Package `keywords` do not set GitHub topics.
These About fields therefore need to be applied separately from a README edit.

On the repository page, use the gear beside About to apply the description and
Topics. A package metadata update alone does not change these repository fields.

Use the README to answer concrete search intents: measuring code diversity,
evaluating recorded coding-agent revisions, separating passing from concentration,
accounting for stopped runs and replaying an evaluation. Its opening example
shows the supported question about rising finite passing and falling mechanism
coverage, with task scope stated near the top.

Keep `pass@k`, SWE-bench and agent observability in their explanatory context.
No pass@k estimator, benchmark adapter or live tracing integration is shipped.
MCP servers, RAG evaluation, AI authorship detection, plagiarism detection and
general model-collapse diagnosis are outside the current feature set and should
not be used as product capability tags.

The source quickstart follows `main`. To use a published version consistently,
check out its release tag or install the matching release artifact.
