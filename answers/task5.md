# Task 5: Spec for one fix — send "needs a person" messages to staff

**Problem.** In four weeks, 20 leads complained or asked for a person. Ivy sent all 20 a sales pitch and passed none to staff, though Lumen's rules require it for 16. Four of eight owner complaints describe this. Ivy's handoff already works for corporate-rate questions.

**Business priority it serves.** #1, owners renewing: 5 of 6 complaining owners renew in March.

**What will change.** Before replying, Ivy checks for billing or refunds, injuries, requests for a person, or "stop messaging". If found, Ivy sends a short fixed reply, not a pitch, and alerts the studio through the existing handoff. "Stop" ends follow-ups.

**Acceptance criteria**
1. Given a billing or refund message, when Ivy replies, then it says the studio team will respond within one business day, with no offer.
2. Given an injury or a request for a person, when Ivy replies, then staff get an alert with the lead's name, studio and message.
3. Given "stop messaging", when Ivy replies, then it apologises once and sends nothing more.
4. Given the 20 complaint and "talk to a person" messages from the data, when tested on the fixed Ivy, then none gets a pitch.
5. Given an ordinary pricing question, when Ivy replies, then nothing is handed off.

**Out of scope.** Duplicates, wrong channel, reply wording, a model change, billing errors.

**How we will know it worked.** Weekly: share of these messages reaching staff (0% now, target 100%), call-backs within a business day, and owner complaints about ignored requests (target 0).

*Word count: 250 / 250*
