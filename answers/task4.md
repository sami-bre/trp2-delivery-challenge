# Task 4: Test a new AI model

Scoring sheet: [TRP2 W0 - New Model Test Scoring Sheet (Task 4)](https://docs.google.com/spreadsheets/d/1gvSU125wbeGCd8qIVgLh1RerCHJqZw5G6wfDX7GhxBA/edit). Prompt: [analysis/ivy_prompt.md](https://github.com/sami-bre/trp2-delivery-challenge/blob/main/analysis/ivy_prompt.md). Scripts: [analysis/generate.py](https://github.com/sami-bre/trp2-delivery-challenge/blob/main/analysis/generate.py), [analysis/grade.py](https://github.com/sami-bre/trp2-delivery-challenge/blob/main/analysis/grade.py).

**Method and limits.** We were not given Ivy's prompt or model. Ivy's live replies look templated: its 367 different messages are about 13 fixed texts with the name and studio swapped in. So we rebuilt Ivy's inputs: the full fact sheet, the lead's name, channel and message. We did not add any hints from our eval. To tell the model apart from the instructions, we gave the same prompt to an older model (GPT-5.6 Luna, July 2026) as a control. The sending system picks the channel, not the model, so C3 does not apply to the models. Neither model had studio schedules or the booking system, which Ivy has.

| Criterion | Ivy pass rate | New model pass rate (Inkling 2 Mini) | Control: older model, same prompt (GPT-5.6 Luna) |
|---|---|---|---|
| C1. Hands off to staff when it must | 16 / 20 (0 of 4 needed) | 19 / 20 (3 of 4 needed) | 20 / 20 (4 of 4 needed) |
| C2. Facts match the fact sheet | 14 / 20 | 18 / 20 | 20 / 20 |
| C3. Replies on the lead's channel | 18 / 20 | Not the model's choice | Not the model's choice |
| C4. Answers the question | 16 / 20 | 16 / 20 | 17 / 20 |
| **All criteria that apply** | **9 / 20** (11 / 20 without C3) | **14 / 20** | **17 / 20** |

**Model:** Inkling 2 Mini (Thinking Machines Lab), released 20 November 2026.

**Better than Ivy:** it passed 3 of 4 leads who needed staff to the team (Ivy: 0 of 4) and quoted correct prices.
**Worse:** it sent three simple questions to staff, including freezes, which the fact sheet answers. That adds staff work.
**Mistake we caught:** it told a returning lead "yes, the free trial is still available", though the trial is for first-time visitors only. Our AI judge passed it; a hand check caught it.

**Answer to Marcus: not yet.** With the same instructions, the older model scored higher (17/20) than the new one (14/20). The gain comes from clear instructions, not a newer model. Wrong channels and duplicates sit outside the model, and new AI costs are frozen until the board.

*Word count: 133 / 150*
