# High-Performance-AI-Lab

Open infrastructure for high-performance, memory-first LLM inference —
built around the [muser](https://github.com/High-Performance-AI-Lab/muser)
program and measured end to end.

| Project | What it is |
|---|---|
| [muser](https://github.com/High-Performance-AI-Lab/muser) | Standalone Muse Glimmer (~30B) inference engine: Apple Silicon Metal decode, a kquant DFlash speculative lane, and disaggregated NVFP4 prefill handed off from a GB10 node |
| [kvpack](https://github.com/High-Performance-AI-Lab/kvpack) | Crash-safe, bitwise-exact KV-cache replay: save inference state once, restore it bit-identically across processes, crashes, and machines |
| [muser-console](https://github.com/High-Performance-AI-Lab/muser-console) | Secure live dashboard for muser engines — fleet health, cache savings, sessions, gap-preserving history |
| [muser-book](https://github.com/High-Performance-AI-Lab/muser-book) | *How to Write an Inference Engine* — the forty-chapter, receipt-cited book |

Everything we claim in public is scoped to retained evidence: measured
numbers cite receipts, fail-closed checks stay closed, and no number is
rounded into existence.
