# Results summary (revision 3, forcing inputs aligned to the issue time)

Test year 2002, 4 basins, 63 flood-days, 22 onsets; target miss rate α = 0.2; mean of 5 seeds. Source: `results/tables.md`.

| h = 1 d | POD | FAR | CSI |
| --- | --- | --- | --- |
| B9 quantile LightGBM | 0.762 | 0.304 | 0.572 |
| B11 LightGBM + CSI-tuned threshold | 0.790 | 0.354 | 0.551 |
| B8 LightGBM multi-forcing | 0.575 | 0.223 | 0.493 |
| B1 persistence | 0.651 | 0.349 | 0.482 |
| B10 regional LSTM | 0.514 | 0.114 | 0.482 |
| **ACE-Flood** | 0.810 | 0.496 | 0.451 |

- ACE-Flood vs B11 at h = 1: ΔCSI −0.100 [−0.157, −0.052], Holm p = 0.025 (significant).
- ACE-Flood vs persistence at h = 2: ΔCSI −0.150 [−0.239, −0.068], Holm p = 0.008 (significant).
- Miss-rate target met at h = 1–2; exceeded by at most 0.063 at h = 3; not met with ≥ 10% missing gauge readings.
- Pooling calibration events across basins: CSI 0.043 → 0.420 for a gauge with 3 months of record.
