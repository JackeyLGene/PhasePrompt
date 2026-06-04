# Disclosure Policy

Status: public research-preview policy.  
Last updated: 2026-06-04.

## Core Principle

Publish the bounded sidecar result. Do not publish a complete autonomous memory
engine.

PhasePrompt has practical relevance for long-context compression and agent
memory. It also points toward more sensitive architectures involving persistent
external codices. This repository therefore exposes enough material to evaluate
the reported result while holding back productionizable internals.

## Public Material

The following may be public:

- result reports;
- result JSONL artifacts;
- evaluation protocol;
- artifact verification scripts;
- high-level architecture diagrams;
- toy interface examples;
- limitations and failed/negative cases.

## Controlled Material

The following is not included in this repository:

- full LanguageWe implementation;
- continuous streaming state-update logic;
- TokenCodex and SyntaxCR internals;
- production compact-prompt generation strategy;
- agent integration loops;
- cross-session identity or autonomous memory extensions.

## Allowed Public Claim

> A zero-training structural sidecar improved query-agnostic conversation
> compaction in a LoCoMo-MC pilot when paired with a strong production LLM.

## Avoided Claims

Do not claim:

- that PhasePrompt beats all memory systems;
- that this is an AGI architecture;
- that this is a complete autonomous agent memory layer;
- that the current pilot is a full industry benchmark;
- that hidden implementation details are required to trust the saved result
  artifacts.

## Technical Review

Core implementation may be shared with selected technical reviewers under a
separate agreement or explicit written permission. The intended review question
is narrow:

> Does the sidecar generate a genuine structural signal that improves
> compression quality under the published protocol?

## License Boundary

No open-source license is granted for this repository. Viewing the repository
does not grant rights to reuse, modify, redistribute, or commercialize its
contents.

