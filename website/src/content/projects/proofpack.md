---
title: "proofpack"
tagline: "Seal, replay, and prove what an agent evaluator actually catches."
eyebrow: "07 — Agent proofs"
description: "A fail-closed evaluation toolkit that packages behavioral cases, mutations, replay receipts, and provenance into one tamper-evident artifact."
url: "https://github.com/sersoage/proofpack"
category: "proofs"
tags: ["Python", "Evals", "Traces"]
order: 7
stackOrder: 7
stackAction: "Certify"
stackRole: "Sealed eval evidence"
accent: "rose"
icon: "proof"
status: "open source"
metric: "sealed proof.lock"
metricLabel: "hash-bound artifact inventory"
command: "proofpack env verify ./bundle"
---

ProofPack turns agent evaluation into a reproducible, inspectable artifact. It records what was tested, what was mutated, what changed the outcome, and packages the evidence so another person can re-derive the decision from the same bytes.
