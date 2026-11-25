# Lumen data extract — findings

Source: `data/*.csv` (exported from the Drive sheet on 2026-11-25). Scripts: `analysis/explore*.py`
(run `explore2.py` then `explore4.py` first; they write `analysis/out/c.csv` and `l.csv` for the others).
Run with: `cd /tmp && uv run --quiet --with pandas python -I <script>`.

Data window: leads created 19 Oct – 15 Nov 2026 (4 weeks = Dana's "last four weeks").
250 leads, 429 Ivy messages, 40 studios. Every lead has at least one Ivy message.

## Headline numbers

| Metric | Value |
|---|---|
| Leads | 250 |
| Replied or further (= dashboard "conversion") | 78 → **31.2%** |
| Trial booked or further | 23 → 9.2% |
| Trial attended or further | 15 → 6.0% |
| **Membership purchased** | **8 → 3.2%** |
| Stage-to-stage | reply→book 29%, book→attend 65%, attend→buy 53% |
| Biggest leak | 172 leads (69%) never reply |
| Ivy first-reply time | median 2.9 min (1–5 min) — a real strength |

**The 31% is the reply rate, not paid memberships.** Paid conversion is 3.2%, about 1 in 10 of what
the dashboard suggests. Also, 20 of the 78 "replies" are complaints or requests for a human, so
the 31% even counts angry leads as wins. Without them: 58/250 = 23%.
Caveat: leads from 9–15 Nov have 0 purchases yet, so 3.2% may undercount a little (time lag).

## Findings (rough business-impact order)

1. **Handoff to staff never happens when policy requires it.** 20 messages were complaints (11) or
   requests for a person (9), covering billing, refunds, injuries and manager call-backs. **0 of 20
   were handed to staff.** All 20 got the same sales pitch: "The best way to experience <studio> is
   with a free first class. Our intro month is just $99. Shall I book you in?" 19 of 20 went out
   unedited. 16 of the 20 break a written policy: 7 billing/refund (refunds policy), 9 person
   requests (person policy; 3 of those also mention an injury, so also the injury policy). The
   other 4 are "stop sending me the same message" — no written rule covers them, but the pitch is
   still the wrong reply. So: **0 of 16 policy-required handoffs happened.**
   The 3 corporate-rate handoffs below are separate messages, not part of these 20.
   - A handoff exists and works: 3 of 3 "group or corporate rates for a team of 10?" were handed.
     So this is a routing/rules problem, not a missing feature. A cheap fix inside existing tools.
   - Aisha R. asked for a manager about a corporate rate, but her message was tagged "Asked for a
     person" and got the pitch. Handoff seems to trigger on topic/phrase, not intent.
   - Half of these (10/20) were at the 11 studios renewing in March 2027, which hold 30% of leads.
2. **Wrong channel: SMS leads answered by email.** 73 of 249 SMS messages (29%) were answered by
   email. Never the other way. 52 of 150 SMS leads (35%) got their *first* reply by email. Those
   leads replied **7.7%** vs 37.4% for everyone else, and **0 bought** (vs 4.0%). Steady every week,
   all sources, all topics except handoff. This is the biggest conversion leak we can see.
   Rough size: if those 52 converted like the rest, ~2 more memberships per 4 weeks (+25%).
3. **Duplicate messages.** 39 duplicate sends to 38 leads (15% of all leads). 34 of them came 2–5
   seconds apart (looks like a send bug). Spread over 27 studios, both channels, every week — so it
   is system-wide, not one studio. 6 of 8 owner complaints mention it. Duplicated leads do **not**
   convert worse in the data (39% reply, 2.6% buy), so the harm is trust and brand, not funnel.
   The other 5 duplicates are hours apart (lead asked again, got the same template).
   Numbers: duplicate 38 leads → replied 15 (39.5%), booked 3 (7.9%), bought 1 (2.6%);
   no duplicate 212 → 63 (29.7%), 20 (9.4%), 7 (3.3%). Biased (chatty leads get more duplicates)
   and tiny. **Decision:** frame duplicates as an owner-trust / renewal risk, not a conversion
   issue. Owners are Lumen's income, so their view counts even without a funnel effect.
4. **Ivy is ~13 fixed templates, so it often does not answer the question.** 367 "unique" messages
   are the same 13 texts with name and studio swapped in. Every schedule question (80: hot yoga,
   Saturday, after 7pm, early morning) gets "runs classes 6:30am to 8:30pm on weekdays, plus
   weekend mornings". Every location question (42: closest to downtown, showers, bike, train) gets
   "easy to reach and there's street parking nearby". Freeze-fee and sign-up-fee questions get
   templates that do not mention the fee. This is what owners call "robotic". It also suggests a
   new AI model alone may not change much, since the replies look templated, not generated.
5. **Wrong prices in Canada.** All 19 pricing replies at Canadian studios quote the intro month as
   **$99**. Fact sheet: CA$109. 16 of them say "CA$169 per month ... intro month for $99" (mixed
   currency). Staff edited ~75% of these before sending.
6. **Staff edit a lot, but only on some topics.** 135 of 429 drafts (31%) were edited. Pricing 67%,
   cancellation/freeze 76%, everything else ~10%. Staff are doing hidden work to fix Ivy. Unknown:
   do staff see every draft, or only some? If they see all, why did 19 of 20 sales-pitch replies to
   complaints go out unedited?
7. **Billing complaints pattern (not clearly Ivy's fault).** 7 messages from 6 leads at 6 studios
   (Kevin T. counted twice because of a duplicate): 3× "charged
   twice for my trial" (the trial is free), 1× charged twice this month, 2× charged for a class never
   booked, 1× "told the trial was free and then got a bill". Nothing shows Ivy takes payments. The
   booking system is covered by the same $500 tech fee, so it may be a Lumen-side billing issue.
   Do not speculate in the answer; raise it as an open question for Dana.

## Business / money

- 40 studios (30 US, 10 CA), 32 owners. 7 owners have more than one studio: Priya Shah 3; Daniel
  Brooks, Mei Lin, Isabelle Roy, Liam Tremblay, Kofi Mensah, Ahmed Karim 2 each.
- **11 studios renew 31 March 2027.** Next: 5 in Sept 2027. At renewal owners can stop paying for Ivy
  or leave the network.
- **5 of the 6 complaining owners renew in March**: Priya (Austin), Daniel (Seattle), Isabelle
  (Minneapolis), Rachel Kim (Nashville), Ethan Wright (Toronto Leslieville). Only Luca (Vancouver
  Lonsdale) renews later (June 2028). Priya, Daniel and Isabelle own 7 studios between them, so
  "leaving the network" puts more than their March studios at risk.
- Tech fee: 40 × $500 = $20,000/month, but it covers Ivy **and** the booking system. Ivy costs Lumen
  ~$6,000/month. Break-even if the whole fee is counted: 12 studios. The Ivy share of the fee is
  unknown — discovery question.
- 11 March studios × $500 = $5,500/month ≈ 92% of Ivy's cost.
- One US member ≈ $99 + 13 × $149 = **$2,036** over the 14-month average. Lumen's 7% ≈ **$143**.
  8 members per 4 weeks ≈ $16k to owners, ≈ $1.1k royalty to Lumen. Owners gain far more per member
  than Lumen does, which is why owners only care about paid memberships.
- Unknown: studio revenue (so royalty size), what conversion was **before** Ivy (no baseline, so we
  cannot say how many of the 8 members Ivy caused).

## Vendor eval (Brightline 92%)

- 50 tests, but only **25 unique questions**. "What time is the first class on Monday?" appears 7 times.
- Only 2 topics: class schedule (33) and studio location (17). Those topics are just **28%** of real
  traffic (122/429). **Zero tests** on pricing, cancellation, trial booking, complaints or handoffs —
  where the real failures are.
- Written by the vendor before launch, not real lead messages. No Ivy answers recorded, so nothing
  can be re-checked.
- Same question scored differently: "Is there a changing room?" Fail (T23) and Pass (T29); "Where is
  the studio?" Pass (T16) and Fail (T30). Scoring is not repeatable.
- Criteria (friendly, grammatical, answers the question) say nothing about correct facts, channel,
  policy, or handoff. Live data shows the schedule template does not answer "when is hot yoga", yet
  the same kind of question passed.

## Eval set (20 harder conversations, for Task 3)

This is the dataset the brief gives for Task 3. We build the **criteria** and score these 20 drafts;
we do not build a new dataset. First look (to be done properly in Task 3):
- Wrong facts: E01 ($129, should be $149), E02 ($79 intro, should be $99), E03 (packs "never
  expire", should be 6 months), E04 ("cancel anytime, no notice", should be 30 days' notice), E05
  ("freezes are free", should be $15/month, max 2 months).
- Missed handoff: E06 (back injury), E07 (refund), E08 (manager call), E09 (stop messaging).
- Wrong channel: E10, E11 (SMS lead, email reply).
- E12–E20 look mostly fine. E17: staff mention transferring to another studio, which is **not in
  the fact sheet** — be careful using staff replies as truth.
- Note: the eval set drafts have made-up prices that the live data does not show (live US prices are
  right). The eval set is a harder, different slice — say so when comparing.

## Discovery questions this raises

- Do staff review every Ivy draft before it goes out, or only some? Who, and how fast?
- What did lead-to-member conversion look like before Ivy? (needed to say if Ivy helps at all)
- How much of the $500 fee is Ivy, and can owners drop Ivy but keep the booking system?
- Rough membership revenue per studio (to size the royalty at risk).
- Which of the 11 March owners are the "two talking about leaving"?
- Who handles the billing complaints today, and is the trial double-charge a known booking-system issue?
- How does Ivy pick the reply channel and decide on handoff? (no system prompt or config was handed over)
