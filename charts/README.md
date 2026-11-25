# Charts for the submission document

Built by `analysis/charts.py` (`cd /tmp && uv run --quiet --with matplotlib python -I /home/samuel/trp2-delivery-challenge/analysis/charts.py`).

| File | Goes in | Place it | Backs up |
|---|---|---|---|
| `1_funnel.png` | Task 2 | Under the findings table | Finding 4: the 31% is replies; 3.2% bought |
| `4_wrong_channel.png` | Task 2 | After `1_funnel.png` | Finding 2: SMS leads answered by email (8% vs 34% replied, 0 vs 4 bought) |
| `2_vendor_vs_real.png` | Task 3 | Under the 100-word note | Why our 45% differs from the vendor's 92% |
| `3_model_test.png` | Task 4 | Under the results table | The answer to Marcus: same instructions, older model scored higher |

Notes:
- The model chart leaves out C3 (channel), so Ivy's "all three pass" is 11, not the 9 in the Task 4 table. The chart's source line says so.
- Chart 4 and Task 2 both compare SMS leads answered by SMS (34%) with SMS leads answered by email (8%).
- Charts don't count toward word limits, but captions might. Keep captions to the chart title only.
