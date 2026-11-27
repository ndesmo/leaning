---
name: prove
description: Run the full workflow for a new or extended result on the "Proofs by Claude" site, from choosing a target in LEDGER.md to a reviewed, published page. Holds the shared rules (claim labels, credit, no overclaiming) that every stage skill follows. Use when the user asks for a new proof or the next result; use a single stage skill when only that stage is wanted.
---

# /prove: from target to published proof

Results are published at https://ndesmo.github.io/leaning/ and credited to **Claude (AI model)**,
never to the user. Nothing here is peer reviewed, and every page says so.

## Shared rules (all stages follow these)

- **Label every claim** with exactly one of these:
  - `[Lean]`: proved in Lean, no `sorry`, standard axioms only.
  - `[Lean | hyp: …]`: proved in Lean from named, cited hypotheses.
  - `[paper: ref, Thm n]`: checked against the paper's own text.
  - `[preprint: ref, Thm n]`: an unrefereed preprint.
  - `[standard: ref]`: a classical textbook result.
  - `[numerical ± err]`: a computed value with its error bar.
  - `[conjecture]`: open.
  - `[own argument, unreviewed]` or `[own argument, reviewed <date>]`: an argument we wrote that no
    published source contains, including one that fills a gap a paper leaves open.
- **Combine labels honestly.** A claim resting on a paper plus our own step carries both, e.g.
  `[paper: DH10 Thm 2.5] + [own argument: Rem. 2.10 for stars, unreviewed]`. Never call such a
  claim settled, unconditional or proved until the own-argument part has passed `/review`.
- **Search with anything, claim only what is checked.**
  - Searches and experiments may use any tool: Lean, Python, solvers.
  - A computation proves nothing until its output is a certificate that is checked independently,
    ideally in Lean. Until then it is `[numerical]`, never "proved".
  - Keep search code and exact reproduction commands under `search/<slug>/`.
- **Never overclaim.**
  - Novelty is at most "not found in the works searched".
  - Partial results are published as partial, with the gap stated exactly.
  - An unchecked step goes in the open list, not the proof.
- **Keep one notes file per result,** `notes/<slug>.md`. Sections: Statement, Setting, Claims
  ledger (a table: claim | label | where), Literature, Review, Log. Date every log entry.
- **Privacy:** nothing that names the user, no machine paths (`C:\Users\…`), no email addresses,
  in anything committed.

## Finishing a result

A proof in the notes is not the end. A result is **finished** when all four of these hold:

1. **Reviewed.** The argument has passed `/review` and the reviewer agent.
2. **Citations checked.** Every step labelled `[standard]`, `[paper]` or `[preprint]` whose source
   text was not checked has been checked against that text, or replaced by our own derivation.
3. **Lean.** The statement actually proved is formalized, not just a weaker or special case. If that
   is out of reach for now, the notes say why. Lean units carry the label `lean`, and the
   formalizer agent does them.
4. **Page.** It has a page on the site (`/proof-page`), with every step labelled.

- **One item, one unit.** Each missing item is a unit of work, done in that order.
- **Page before Lean** only when the notes record why Lean is out of reach; update the page when
  the Lean lands.
- **One page per problem.** It grows as that problem's results do, rather than one page per
  partial result.

## Claims (several contributors may run agents at once)

Other people's agents may be working on the same repository. GitHub is the shared state, so
claim before you work and touch only your own claims.

- **Who you are:** `<me>` is `gh api user --jq .login`. "Your PRs" means
  `gh pr list --state open --author @me`, filtered to your role's branch prefix (`agent/` for the
  author, `explore/` for the explorer).
- **Claimed:** an issue is claimed while it has an assignee, or has `in-progress` with no assignee
  (an older claim). Never start work on an issue claimed by someone else.
- **To claim:**
  1. Run `gh issue edit <n> --add-assignee @me --add-label in-progress`.
  2. Comment `Claimed by <me>, branch <branch>.` Write the login without `@`, so nobody is
     notified.
  3. Re-read the issue (`gh issue view <n> --json assignees,comments`). If another login is also
     assigned and its claim comment is older than yours, you lost the race: remove yourself
     (`--remove-assignee @me`), delete nothing else, and pick another issue. In a takeover
     (below), ignore the stale holder you named in your takeover comment.
- **To release:** when your PR for the issue is merged or closed and you have no other open PR for
  it, remove yourself as assignee. Remove `in-progress` only if no one else is assigned. Never
  release or change anyone else's claim, except to take over a stale one (below).
- **Stale claims:** a claim is stale when, for 48 hours (7 days for a moonshot), its branch has had
  no push, its issue no comment, and no open PR of the claimant that references the issue
  (`Closes` or `Part of #<n>`) has had any activity. A claimant whose open PR for the issue is
  waiting on review or merge is never stale. You may take over a stale claim: comment
  `Taking over a stale claim from <login> (last activity <date>).`, remove that login as assignee
  (`--remove-assignee <login>`), then claim as above. Leave their branch alone.
- **Older claims:** an issue with `in-progress`, no assignee, and a claim comment or branch
  made by `<me>` is yours. Assign yourself to it.

## Workflow

**Where things live.** The work queue is GitHub Issues:
- `approved`: the owner said yes, and only the owner adds it;
- `gap`, `problem`, `follow-up`, `tooling`: what kind of item it is;
- `priority:*`: order;
- `in-progress` and `blocked`: state.

The knowledge lives in files: `LEDGER.md` (results, gaps, failed approaches), `PROBLEMS.md`
(scouted candidates and their evidence) and the notes. Each ledger gap and problem links its issue.

Start with `gh issue list --label approved` and `LEDGER.md`. Offer the user a short menu:
- two or three approved issues, each with a one-line view of how tractable it looks;
- the option of something new, which becomes a new issue for the owner to approve.

Agree whether the target extends an existing result (keep its slug, notes, Lean file and page) or
gets a new slug.

Then use the stage skills. This is a loop, not a fixed order: when an attack stalls, go back to
`/conjecture` for a weaker target or to `/literature` for a missing tool.

| Skill | Use it to | Exit when |
|---|---|---|
| `/conjecture` | find and stress-test a precise statement; list provable partial targets | the statement is exact, attacks on it are recorded, and targets are ranked |
| `/literature` | learn what is known; quote every theorem you will cite | each cited theorem is quoted verbatim with its hypotheses, and the search scope is recorded |
| `/attack` | derive the proof | every step is labeled and the edge-case audit is done |
| `/lean-check` | formalize and verify | `check.ps1` reports CLEAN |
| `/proof-page` | write the page | the page, index and README are updated |
| `/review` | get an independent check | every finding is fixed or rebutted in the notes |
| `/publish-proofs` | deploy | the pages return 200 on the live site |

- **Before `/publish-proofs`:** `/review` is required. Tell the user in one line what is about to
  go public.
- **Lessons:** concrete episodes behind these rules are in `lessons.md`, next to this file. Read
  the section for the stage you are in.
