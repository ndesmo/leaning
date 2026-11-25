---
name: publish-proofs
description: Deploy new or updated proofs to the public "Proofs by Claude" site (https://ndesmo.github.io/leaning/, GitHub Pages from main /docs). Covers preflight checks (Lean clean, review done, ledger updated, privacy scan), commit, push to main and confirming the live pages. Use when a reviewed proof page is ready, or the user asks to deploy or publish.
---

# /publish-proofs: deploy to the site

The repo `ndesmo/leaning` is public, and Pages serves `main:/docs`. Everything pushed is
world-readable. Before pushing, tell the user in one line what is going public.

## Preflight (stop on any failure)

1. **Lean.** Run `check.ps1` from `/lean-check` on every Lean file changed since the last push, and
   confirm `lake build` exits 0.
2. **Review.** For every new or changed proof page, the notes' Review section has an entry dated
   after the page's last substantive change. Every finding in it is fixed or rebutted.
3. **Site.** Each page has the `Claude (AI model) · … · Not peer reviewed` byline, an entry in
   `docs/index.html`, and a row in `README.md`.
4. **Ledger.** `LEDGER.md` is updated:
   - **Results:** add or extend the result's entry.
   - **Reusable lemmas:** add any new reusable theorems.
   - **Open gaps:** close the gaps this settles, and add the gaps it leaves.
   - **Failed approaches:** add any approaches that failed.
   - **Issues:** the PR says `Closes #<n>` for each issue it finishes. New gaps it leaves get
     issues (labels `gap`, `follow-up`).
5. **Privacy.** Grep everything staged, including `.claude/`, for machine paths (`C:\Users`, the
   Windows user name), email addresses, tokens and the user's name. Remove each hit, except lines
   that only state the rule.
6. **Working tree.** Read `git status --short`. Stage only the intended files by name, never
   `git add -A`. Scratch files and `.lake/` must not go in.

## Commit and push

- **Message file.** Write the message to a file and use `git commit -F <file>`; here-strings with
  quotes break in PowerShell 5.1.
- **Message.** First line: `Publish <slug>: <one-line result>`. Body: what is proved and what Lean
  checks. End with the Co-Authored-By trailer from the current attribution guidance.
- **Push.** `git push origin main`. Never force-push or rewrite history.

## Confirm it is live

Poll `gh api repos/ndesmo/leaning/pages/builds/latest --jq .status` about every 10 s until it
reads `built` or `errored`. Then confirm that `https://ndesmo.github.io/leaning/` and each
`https://ndesmo.github.io/leaning/<slug>/` return 200 (`curl -s -o /dev/null -w '%{http_code}'`).

Report the live URLs. If the build errored, show its error from the same API and fix it before
saying anything is published.
