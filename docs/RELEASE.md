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

The later README/discoverability revision changes documentation only. The saved
C06 artifacts retain their originally qualified README and guides. Rebuild the
publication artifacts to include the updated documentation; verify their package
contents and installed CLI while retaining the existing analysis qualification
when runtime, task and example bytes are unchanged.

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

Recommended GitHub description:

> Code diversity and coding agent evaluation for LLMs: analyze algorithmic diversity, solution convergence, and recorded revision trajectories. Offline Python CLI.

Recommended topics, in priority order:

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

The current connection has no About/topics setter. On the repository page, use
the gear beside About, paste the description, add the topics and save. The
existing description remains accurate; the live Topics list was empty when
checked on 2026-09-24. The original C06 package metadata remains part of the
qualified artifacts and has not been rewritten by this documentation revision.

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

The source quickstart currently checks out the C06 candidate branch, where the
installed-example commands exist. Replace that branch-specific entry point with
the published release path when publishing 0.1.0.
