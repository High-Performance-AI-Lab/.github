# .github — High-Performance-AI-Lab brand and profile assets

This repository holds the organization-level assets for
[High-Performance-AI-Lab](https://github.com/High-Performance-AI-Lab): the
organization avatar/logo, the org-homepage profile README, the social
preview for this repository itself. The organization website lives in its
own org-domain repository,
[high-performance-ai-lab.github.io](https://github.com/High-Performance-AI-Lab/high-performance-ai-lab.github.io).

## What is in here

| Path | What it is |
|---|---|
| `assets/org-logo.png` | The organization avatar (1024×1024). The mark — three ascending compute lanes under a rising trend line — sits entirely inside the circle-mask safe area. |
| `assets/org-logo.svg` | Hand-maintained vector twin of the logo geometry. |
| `assets/org-social-card.png` | This repo's 1200×630 social preview. |
| `profile/README.md` | The README GitHub renders on the organization homepage. |
| `scripts/generate_org_logo.py` | Deterministic generator for the raster assets — no randomness, no external inputs. |

## Regenerating the assets

```sh
python3 scripts/generate_org_logo.py           # regenerate logo + card
python3 scripts/generate_org_logo.py --check   # verify committed copies
```

`assets/org-logo.svg` is maintained by hand; keep it in sync with the
generator's geometry when the mark changes.

## Where things are configured (manual, one-time)

- **Organization avatar:** org → Settings → Organization profile →
  upload `assets/org-logo.png`.
- **This repo's social preview:** repo → Settings → General → Social
  preview → upload `assets/org-social-card.png`.
- **Org homepage README:** automatic once `profile/README.md` exists on the
  default branch and the repository is public.

The color range (teal `#3fb9aa` through blue `#62a0ff` on charcoal
`#0d1117`) is the family accent range shared by the social cards of the
muser, kvpack, muser-console, and muser-book repositories.

## License

MIT OR Apache-2.0, at your option.
