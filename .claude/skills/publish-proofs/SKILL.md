---
name: publish-proofs
description: Deploy new or updated proofs to the public "Proofs by Claude" site (https://ndesmo.github.io/leaning/, GitHub Pages from main /docs). Covers preflight checks, commit, push to main and confirming the live pages. Use when a proof page is ready or the user asks to deploy or publish.
---

# /publish-proofs: deploy to the site

The repo `ndesmo/leaning` is public, and Pages serves `main:/docs`. Everything pushed is world-
readable. Before pushing, tell the user in one line what is going public.

## Preflight (stop on any failure)

1. **Lean:** run `check.ps1` from `/lean-check` on every Lean file changed since the last push, and
   run `lake build` in `halfline_lt/`. Both must be clean.
2. **Pages:** each new or changed `docs/<slug>/index.html` must have the
   `Claude (AI model) · … · Not peer reviewed` byline, an entry in `docs/index.html` and a row in
   `README.md`.
3. **Ledger:** update `LEDGER.md`.
   - **Results:** add or extend the result's entry.
   - **Reusable lemmas:** add any new reusable theorems.
   - **Open gaps:** close the gaps this work settles, and add the gaps it leaves.
   - **Failed approaches:** add any approaches that failed.
4. **Privacy:** search `docs/`, `notes/` and `README.md` for `C:\Users\`, email addresses, tokens
   and the user's name. Remove anything found.
5. **Working tree:** read `git status --short`. Stage only the intended files by name, never
   `git add -A`. Scratch files and `.lake/` must not go in.

## Commit and push

- Write the message to a file and use `git commit -F <file>`: here-strings with quotes break in
  PowerShell 5.1.
- First line: `Publish <slug>: <one-line result>`. Body: what is proved and what Lean checks.
- End the message with the Co-Authored-By trailer from the current attribution guidance.
- `git push origin main`. Never force-push or rewrite history.

## Confirm it is live

Poll `gh api repos/ndesmo/leaning/pages/builds/latest --jq .status` about every 10 s until it
reads `built` or `errored`. Then check that each URL returns 200:

```
curl -s -o /dev/null -w '%{http_code}' https://ndesmo.github.io/leaning/
curl -s -o /dev/null -w '%{http_code}' https://ndesmo.github.io/leaning/<slug>/
```

Report the live URLs to the user. If the build errored, show its error from the same API and fix it
before saying anything is published.
