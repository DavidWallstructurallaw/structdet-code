# Related work and contribution boundaries

Algorithmic and structural diversity of generated code have direct precedents.
StructDet Code makes no first-discovery or comparative-superiority claim.

- Seonghyeon Lee, Heejae Chon, Joonwon Jang, Dongha Lee and Hwanjo Yu,
  [How Diversely Can Language Models Solve Problems? Exploring the Algorithmic
  Diversity of Model-Generated Code](https://arxiv.org/abs/2503.00691v2), 2025.
  They study algorithmic diversity using code clustering and examine factors
  affecting generated solution diversity. This is a direct precedent for studying
  diversity beyond whether generated code passes tests.
- Halley Young, Yimeng Zeng, Jacob Gardner and Osbert Bastani,
  [Improving Structural Diversity of Blackbox LLMs via Chain-of-Specification
  Prompting](https://arxiv.org/abs/2408.06186), 2024. They use user-specified feature
  mappings to define structural diversity and propose a prompting method to
  increase it. This is a direct precedent for diversity relative to explicit
  structural features, including code.
- [EvalPlus](https://github.com/evalplus/evalplus) supplies code-generation
  evaluation infrastructure. Correctness evaluation is relevant adjacent work;
  StructDet Code does not integrate its harness, execute its benchmarks or claim
  reproduced results against it.

The engineering emphasis here is explicit task-relative mechanism evidence,
source-bound reviews, unknown cases, finite correctness, recorded revision paths,
cohort coverage, interventions and exact passive replay. The shipped rules are
narrow whole-module recognizers. They do not reproduce the cited methods, prove
a unique mechanism ontology or demonstrate empirical performance advantages.
The six owned examples validate software behavior under designed conditions;
they are not observations of live model or agent populations.

The [StructDet-Bench baseline](https://github.com/DavidWallstructurallaw/structdet-bench/tree/0a9dc88deffd4b14264485b161bea06f027f68f5)
supplies the attributed sorting descriptor adaptation. Code's finite-count
arithmetic is independently implemented, with a pinned numerical parity check.
There is no Bench runtime dependency or claim to bypass its validation contract.

The three owner-supplied theory publications and the particular sections used
are identified in [SPEC.md](../SPEC.md#9-source-basis-and-attribution). They inform
interpretation and evidence boundaries. Engineering field names, rules and
adapters are not new theory theorems. Their full texts are not redistributed.
See [NOTICE](../NOTICE) for the Apache-2.0 / CC-BY-4.0 asset split.
