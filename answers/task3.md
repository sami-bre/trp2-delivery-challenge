# Task 3: Build an eval

Scoring sheet: [TRP2 W0 - Ivy Eval Scoring Sheet (Task 3)](https://docs.google.com/spreadsheets/d/1swOqkOm-SPvSRQUXH1KW1kdcVENunuYkuYDdfRfuBBg/edit). It holds one row per conversation, pass or fail per criterion, and a reason for each.
Method: C1 and C3 were checked by code. C2 and C4 were checked by an AI judge (GLM-5.3-Flash), which ran
3 times per draft and took the majority. All 80 results were then checked by hand. Script: [analysis/grade.py](https://github.com/sami-bre/trp2-delivery-challenge/blob/main/analysis/grade.py).

| Criterion | Business priority it protects | Pass or fail rule | Ivy pass rate (out of 20) |
|---|---|---|---|
| C1. Hands off to staff when it must | 1 Owners renewing; 4 Rules and brand | If the lead raises billing, a refund, an injury, asks for a person, or asks Ivy to stop, the reply must say staff will follow up (or that messages will stop) and must not include a sales pitch. Otherwise it passes. | 16 / 20 (**0 of the 4** that needed a handoff) |
| C2. Facts match the fact sheet | 4 Rules and brand; 2 Paid members | Every price, offer and policy in the reply matches the fact sheet. Any wrong or made-up fact fails. Leaving a fact out does not. | 14 / 20 |
| C3. Replies on the lead's channel | 2 Paid members | The reply goes out on the channel the lead used (SMS gets SMS). | 18 / 20 |
| C4. Answers the question | 2 Paid members | The reply directly answers what the lead asked, not a generic line or only a booking push. | 16 / 20 |
| **All four** | | | **9 / 20 (45%)** |

**Ivy's overall score: 9 of 20 (45%)** pass all four criteria. Every failure is in a kind of conversation the vendor never tested.

The vendor's 92% measured something else. Its 50 test questions were written before launch, only 25 are different, and all are about class times or location. None covered prices, policies or requests for a person. Its rule checked friendliness, grammar and whether a question was answered, not facts, channel or handoffs. Our 20 conversations are harder than average, so 45% is not Ivy's score on all traffic. It shows where Ivy fails when it matters.

*Word count: 98 / 100*
