---
title: "assay"
tagline: "Certified workflow-level model binding with statistically legal metadata."
eyebrow: "08 — Model binding"
description: "A proxy records every model call with statistically-legal metadata; an analyzer turns traces into workflows; the statistics layer decides what may be promoted; model.lock binds the selected release."
url: "https://github.com/sersoage/assay"
category: "proofs"
tags: ["Python", "Statistics", "Proxy"]
order: 8
stackOrder: 8
stackAction: "Bind"
stackRole: "Workflow-level model lock"
accent: "teal"
icon: "checkpoint"
status: "open source"
metric: "model.lock"
metricLabel: "versioned release binding"
command: "make verify"
---

Assay is the statistics and binding spine behind model selection. It records model calls, clusters workflows, computes promotion statistics with proper handling of intra-cluster correlation, and emits a `model.lock` that binds the chosen release to its evidence.
