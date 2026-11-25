# TRP2 Week 0 Delivery Challenge — Lumen Studios / Ivy

## Source files (Google Drive, read-only, folder "Delivery Content")

- Brief (Doc): `1KjrUV_RT9hqNr98sIx3PD_8eWX9nk3YO-qar996Z8ZI`
- Intro slides: `11CWJSDfPMSTtYewhnk4Q8z2-0g5ipKpMPt4HyxhumnE`
- Lumen Data Extract (Sheet, 7 tabs): `1X_rOe5e0fykrQ33pC3j64xcAwC8kZcoqRyLfwZLKqmw`

Deadline: **Thursday 26 Nov 2026, 11PM EAT**, on Tenx. One Google Doc, shared "anyone can view".

## Scenario in brief

We play Selam, a forward-deployed engineer at Tenacious, 4 days into the Lumen Studios account.
Lumen runs ~40 franchised yoga/fitness studios (US + Canada). It earns franchise fees plus a share
of every membership sold. Growth depends on (1) keeping franchise owners happy and (2) turning
leads into paying members.

Ivy is an AI agent a previous vendor launched 3 months ago. It follows up with new leads by SMS
and email and tries to book a free trial class. The vendor left a quality report (92%), a
dashboard (31% conversion) and little documentation.

| Stakeholder | Role | What they say / want |
|---|---|---|
| Dana Okafor | Head of Growth, main contact, not technical | Dashboard says 31% conversion, owners are furious. Board in 2 weeks: keep Ivy or switch it off? |
| Marcus Lee | CTO | Wants to switch Ivy to a new AI model to fix "robotic" replies. Wants yes/no this week. |
| Priya Shah | Franchise Owner Council chair, owns 3 studios | Owners losing patience; renewals coming up; some will drop Ivy "or worse". |
| Finance | Budget owners | No new spending before the board meeting. |

## The seven tasks (in order, all written, word limits are hard)

1. **Business wants (~1h).**
   - 1a: ranked table (Rank / What the business needs / Who wants it / Why it matters, with a number) + max 150 words on where wants conflict and how to resolve.
   - 1b: 5 discovery questions for Dana and Priya (Question / Who / What answer would change the plan, and how).
2. **What is really going on (~1.5h).** Findings table, max 6 rows: Issue / Evidence (numbers) / Business priority (from Task 1) / Impact / Confidence. Rank by business impact, not frequency.
3. **Build an eval (~1h).** 3–5 criteria, each protecting a Task 1 priority. Score all 20 Eval set drafts pass/fail, using staff reply + fact sheet as reference. Table: Criterion / Priority / Pass-fail rule / Ivy pass rate (/20). Max 100 words: overall score and why it differs from vendor's 92%. Link the scoring sheet.
4. **Test a new AI model (~1h).** A model released in the last 30 days that we have not used. Same info as Ivy (incl. fact sheet), same 20 conversations, scored with Task 3 eval. Table: Criterion / Ivy / New model. Max 150 words: model name + release date, better/worse, one mistake we caught, answer to Marcus (switch / don't / not yet) tied to priorities. Link the scoring sheet.
5. **Spec for one fix (~45m, max 250 words).** The one fix that best serves priority #1, shippable in 2 weeks, no new budget. Headings: Problem (with evidence) / Business priority / What will change / Acceptance criteria (3–5 "Given…, when…, then…") / Out of scope / How we will know it worked.
6. **Email to Dana (~45m, max 400 words).** Forwarded to Marcus and Priya, so all three must be able to read it. Recommendation first; what is really going on with key numbers; next 2 weeks + fallback; what we are sure of vs not; response to Marcus's model idea and to owners. One chart or table allowed.
7. **Reflection (~15m, max 150 words).** One thing we changed our mind about and the evidence; what to hand the next engineer so they start in days.

Show the **word count under each written part**.

## Rubric (100)

- Business understanding 25 — Tasks 1, 5
- Analysis and evaluation 20 — Tasks 2, 3
- Delivery judgment 20 — Tasks 4, 5, 6
- Client communication 20 — Task 6
- Adaptability 15 — Tasks 4, 7

## Rules for every answer (what "good" looks like)

- **Business first, then evidence, then recommendation.** Rank priorities before touching the data.
- **A requested solution is not a priority.** "Switch the model" (Marcus) is a solution. Name the need under it.
- **Check how every number is defined** before trusting it — the 31% dashboard figure and the 92% vendor score especially. Ask: what is the numerator, denominator, and test set?
- **Every claim needs evidence from the data.** Opinions, including the client's and stakeholders', are not evidence.
- **Rank by business impact, not frequency.**
- **Test an idea before agreeing to it.** Do not agree with whoever is most senior.
- **Respect constraints:** 2-week deadline, no new budget.
- **Lead with one clear recommendation.**
- **Say what is certain and what is not yet.** "I don't know yet, and here is how I will find out" beats a confident guess.
- **Do not speculate or blame anyone** — especially not the previous vendor.
- **Write for a non-technical reader** (the board). Plain language, short, numbers that matter.
- **Stay within word limits.** Going over costs points.
- Assume sources disagree; the emails matter as much as the numbers.
- AI use is fine; judgment is graded. Catch AI mistakes and say so (counts for Task 4 and 7).
- Track any change of mind as we go — Task 7 needs one, with the evidence behind it.

## Common mistakes to avoid (from the intro slides)

- Treating the client's ask as already clear
- Trusting a number before checking how it is measured
- Ranking issues by frequency, not business impact
- Saying yes to a solution before testing it
- Ignoring budget and deadline
- Going over word limits
- Writing for engineers when the reader is the board
- Long, technical or vague emails

## Project files

- `data/` — local copy of the sheet (`lumen_extract.xlsx`) and one CSV per tab.
- `analysis/explore*.py` — pandas scripts. Run `explore2.py` and `explore4.py` first (they write
  `analysis/out/`). Run with `cd /tmp && uv run --quiet --with pandas python -I <script>`.
- `notes/data-findings.md` — all findings from the data, with numbers. Read this before writing answers.

## Repo

This project will be pushed to a git repo, and the answers link to files in it.
- Links to repo files use the placeholder `REPO_URL` (e.g. `REPO_URL/blob/main/analysis/grade.py`).
  Replace every `REPO_URL` once the repo exists: `grep -rn REPO_URL answers/`.
- Before the first push: `.env` (OpenRouter key) must stay out — it's in `.gitignore`; check with
  `git status` that it isn't staged. `analysis/out/` holds results; keep it (the answers cite it).
- Ask the user before pushing or making the repo public.

## Decisions so far

- **Duplicate messages matter, even without a conversion hit.** The data shows no clear drop in
  conversion for leads who got a duplicate (2.6% vs 3.3% bought, 1 buyer — too small to say).
  But owners see duplicates as the main problem (6 of 8 complaints). Owners pay the $500 fee and
  bring in the 7% royalty, and 11 renew in March. So treat duplicates as an **owner-trust and
  renewal** issue, not a conversion issue. Say this honestly in the answers: "no evidence it hurts
  sign-ups, but it hurts owner trust".

- **E06 fails C2 (facts).** "Gentle flow is great for everyone" to a lead with a back injury is a
  made-up health claim. The AI judge caught it (2 of 3 runs); the hand pass had missed it. User
  agreed to keep it as Fail. Good "mistake caught" / "changed my mind" example for Task 7.

## Our working steps (flexible, change as needed)

1. ✅ Read the brief doc and intro slides; save rules here.
2. ✅ User shared their observations from the Lumen Data Extract sheet.
3. ✅ Claude went through every tab; findings in `notes/data-findings.md`.
4. Write answers task by task in `answers/taskN.md`; move into the Google Doc at the end.
   - Task 1 drafted (`answers/task1.md`). Ranking agreed: 1 owners renewing, 2 paid members,
     3 true measure for the board, 4 rules and brand, 5 current budget and deadline.
     Discovery questions have an extra "Why it matters" column (user asked).
   - Task 2 drafted (`answers/task2.md`, cells shortened; SMS row compares SMS-by-SMS 34% vs SMS-by-email 8%): 1 handoff, 2 wrong channel, 3 duplicates (user chose this order), 4 31% is
     reply rate, 5 generic replies + CA price, 6 billing (likely outside Ivy). Ranked to follow
     the Task 1 priority order, except wrong channel above duplicates.
   - Task 3 drafted (`answers/task3.md`). Grader: `analysis/grade.py` (C1 handoff + C3 channel by
     code; C2 facts + C4 answers by OpenRouter `z-ai/glm-5.3-flash`, 3 runs, majority). Key in
     `.env` (never print it). Ivy: C1 16, C2 14, C3 18, C4 16, all four 9/20 (45%). Results in
     `analysis/out/ivy_scores.csv`. Judge matched the hand pass on 79/80; E06 facts is the split.
     Reuse the same grader for Task 4.
   - Scoring sheet (Google Sheet, user's My Drive, id `1swOqkOm-SPvSRQUXH1KW1kdcVENunuYkuYDdfRfuBBg`):
     built by `analysis/build_scoring_sheet.py` (xlsx → Drive upload). Tabs: Summary (formulas),
     Ivy scores. No Sheets editor connector in this chat, so edits mean a new upload unless the
     user turns one on. Still needs "anyone with the link can view" before submission.
   - Task 4 drafted (`answers/task4.md`). New model: `thinkingmachines/inkling-2-mini` (OpenRouter
     released 20 Nov 2026 per thinkingmachines.ai/news/inkling-2-mini; OpenRouter listed it 21 Nov). Meta Muse Ember was
     geo-blocked. Control: `openai/gpt-5.6-luna` (July 2026), same prompt, to separate model from
     instructions. Prompt: `analysis/ivy_prompt.md` (fact sheet + lead fields, no eval hints).
     Generator: `analysis/generate.py`. C3 is N/A for models (system picks channel).
     Results (C1/C2/C4, all that apply): Ivy 16/14/16, 9 (11 w/o C3); Inkling 19/18/16, 14;
     Luna 20/20/17, 17. Hand overrides in `analysis/hand_overrides.csv` (Inkling E20 C2 → Fail).
     Grader reuses cached judge results by reply text. Answer to Marcus: not yet.
     Final doc must say Ivy's replies look templated, and explain the control model clearly.
   - Task 4 scoring sheet (Google Sheet, id `1gvSU125wbeGCd8qIVgLh1RerCHJqZw5G6wfDX7GhxBA`): one tab,
     uploaded as CSV from `analysis/build_task4_csv.py` (xlsx base64 was too big for one tool call).
     Multi-tab local version: `analysis/build_task4_sheet.py`. Ivy's numbers typed in, sourced to
     the Task 3 sheet. Needs "anyone with the link can view" before submission, like Task 3's.
   - Task 5 drafted (`answers/task5.md`, 249/250 words): fix = route "needs a person" messages
     (billing/refund, injury, person request, stop) to staff via the existing corporate-rate
     handoff; no pitch. Duplicates and wrong channel are out of scope (next fixes / Task 6 plan).
   - Task 6 drafted (`answers/task6.md`, under 400 incl. subject, sign-off and funnel table).
     Recommendation: keep Ivy, fix three things, no model switch yet. Fallback: staff daily check
     of Ivy messages. Calling back the 20 missed leads is in Week 1 (user agreed).
   - Task 7 drafted (`answers/task7.md`): change of mind = duplicates (expected revenue hit, data
     showed none → owner-trust issue). Handover = checklist, reusable eval, control-model test.
   - Charts: `charts/*.png` from `analysis/charts.py`; placement in `charts/README.md`
     (1 funnel + 4 wrong channel → Task 2, 2 vendor vs real → Task 3, 3 model test → Task 4).
   - All 7 tasks drafted. Left: assemble the Google Doc, share both sheets + doc "anyone can view",
     confirm Inkling release date, push repo and replace REPO_URL.
   - Write conflicts and answers so a reader with little context can follow.
