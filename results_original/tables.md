**Table 3 — Test 2002, h = 1 d, pooled over 4 basins (63 flood-days, 22 onsets, 1,456 forecasts). Mean ± sd over 5 seeds; deterministic models show no sd; sorted by CSI.**

| Model | POD | FAR | CSI | F1 | Onset POD | Warnings | NSE (pooled) | NSE (median basin) | KGE | RMSE (mm/d) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A8 ACE rolling-window recalibration | 0.844 ± 0.007 | 0.246 ± 0.009 | 0.662 ± 0.007 | 0.796 ± 0.005 | 0.682 | 70.6 | 0.861 | 0.843 | 0.871 | 0.792 |
| A7 ACE expanding-window recalibration | 0.892 ± 0.007 | 0.316 ± 0.015 | 0.632 ± 0.013 | 0.774 ± 0.010 | 0.727 | 82.2 | 0.861 | 0.843 | 0.871 | 0.792 |
| **ACE-Flood** | 0.870 ± 0.007 | 0.303 ± 0.033 | 0.631 ± 0.024 | 0.773 ± 0.018 | 0.727 | 78.8 | 0.861 | 0.843 | 0.871 | 0.792 |
| A4 ACE full-refit test score (v1) | 0.876 ± 0.007 | 0.311 ± 0.024 | 0.628 ± 0.020 | 0.771 ± 0.015 | 0.727 | 80.2 | 0.860 | 0.835 | 0.889 | 0.794 |
| B11 B8 + CSI-tuned threshold | 0.867 ± 0.014 | 0.315 ± 0.024 | 0.619 ± 0.014 | 0.765 ± 0.010 | 0.718 ± 0.020 | 79.8 | 0.860 | 0.835 | 0.889 | 0.794 |
| A9 ACE empirical quantile (no CRC correction) | 0.892 ± 0.007 | 0.340 ± 0.015 | 0.611 ± 0.013 | 0.759 ± 0.010 | 0.727 | 85.2 | 0.861 | 0.843 | 0.871 | 0.792 |
| B9 Quantile LightGBM q0.9 | 0.835 ± 0.014 | 0.306 ± 0.011 | 0.610 ± 0.012 | 0.758 ± 0.009 | 0.682 | 75.8 | – | – | – | – |
| ACE-Flood [static, eta=0] | 0.895 ± 0.009 | 0.350 ± 0.019 | 0.604 ± 0.014 | 0.753 ± 0.011 | 0.727 | 86.8 | 0.861 | 0.843 | 0.871 | 0.792 |
| A3 ACE causal (forward-chaining) calibration | 0.889 ± 0.016 | 0.349 ± 0.032 | 0.602 ± 0.021 | 0.751 ± 0.016 | 0.745 ± 0.025 | 86.2 | 0.854 | 0.811 | 0.854 | 0.812 |
| B10 Regional LSTM | 0.651 ± 0.056 | 0.123 ± 0.057 | 0.594 ± 0.041 | 0.745 ± 0.032 | 0.445 ± 0.038 | 47.0 | 0.873 | 0.835 | 0.836 | 0.756 |
| B3 Ridge regression | 0.619 | 0.114 | 0.574 | 0.729 | 0.227 | 44.0 | 0.843 | 0.792 | 0.850 | 0.841 |
| A6 ACE forcing-ensemble spread score | 0.873 | 0.378 ± 0.008 | 0.571 ± 0.007 | 0.727 ± 0.005 | 0.727 | 88.4 | 0.854 | 0.818 | 0.821 | 0.812 |
| B8 LightGBM multi-forcing | 0.654 ± 0.031 | 0.204 ± 0.017 | 0.560 ± 0.025 | 0.718 ± 0.021 | 0.555 ± 0.020 | 51.8 | 0.860 | 0.835 | 0.889 | 0.794 |
| B5 Random forest | 0.679 ± 0.013 | 0.282 ± 0.015 | 0.536 ± 0.015 | 0.698 ± 0.012 | 0.518 ± 0.025 | 59.6 | – | – | – | – |
| B6 LightGBM local | 0.594 ± 0.018 | 0.197 ± 0.017 | 0.518 ± 0.019 | 0.682 ± 0.016 | 0.382 ± 0.052 | 46.6 | 0.830 | 0.759 | 0.798 | 0.876 |
| A5 ACE Daymet-only predictor | 0.870 ± 0.007 | 0.476 ± 0.012 | 0.486 ± 0.010 | 0.654 ± 0.009 | 0.673 ± 0.020 | 104.6 | 0.822 | 0.754 | 0.789 | 0.897 |
| B1 Persistence | 0.651 | 0.349 | 0.482 | 0.651 | 0.000 | 63.0 | 0.773 | 0.704 | 0.886 | 1.013 |
| B7 LightGBM Daymet only | 0.524 ± 0.022 | 0.233 ± 0.015 | 0.452 ± 0.020 | 0.622 ± 0.019 | 0.391 ± 0.025 | 43.0 | 0.823 | 0.760 | 0.795 | 0.895 |
| B4 Logistic regression | 0.937 | 0.617 | 0.373 | 0.544 | 0.818 | 154.0 | – | – | – | – |
| B12 Persistence + CRC/ACI decision layer | 0.857 | 0.642 | 0.338 | 0.505 | 0.591 | 151.0 | 0.773 | 0.704 | 0.886 | 1.013 |
| B12 Persistence + CRC/ACI decision layer [static, eta=0] | 0.873 | 0.688 | 0.299 | 0.460 | 0.636 | 176.0 | 0.773 | 0.704 | 0.886 | 1.013 |
| B2 Rainfall-threshold rule | 0.524 | 0.703 | 0.234 | 0.379 | 0.182 | 111.0 | – | – | – | – |
| A2 ACE split calibration | 1.000 | 0.957 | 0.043 | 0.083 | 1.000 | 1456.0 | 0.852 | 0.820 | 0.888 | 0.816 |

**Table 4 — Leads h = 2 and 3 d (mean of 5 seeds). CSI / POD / FAR; '–' = no warnings issued.**

| Model | h = 2: CSI | POD | FAR | Warnings | h = 3: CSI | POD | FAR | Warnings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACE-Flood | 0.248 | 0.832 | 0.739 | 201.6 | 0.144 | 0.790 | 0.850 | 333.4 |
| ACE-Flood [static, eta=0] | 0.216 | 0.848 | 0.775 | 239.0 | 0.128 | 0.784 | 0.867 | 372.2 |
| A7 ACE expanding-window recalibration | 0.242 | 0.832 | 0.745 | 206.0 | 0.142 | 0.771 | 0.852 | 329.0 |
| B1 Persistence | 0.286 | 0.444 | 0.556 | 63.0 | 0.178 | 0.302 | 0.698 | 63.0 |
| B12 Persistence + CRC/ACI decision layer | 0.143 | 0.857 | 0.853 | 368.0 | 0.113 | 0.841 | 0.884 | 457.0 |
| B8 LightGBM multi-forcing | 0.276 | 0.314 | 0.307 | 28.6 | 0.013 | 0.013 | 0.250 | 1.2 |
| B11 B8 + CSI-tuned threshold | 0.332 | 0.562 | 0.548 | 79.4 | 0.085 | 0.200 | 0.523 | 53.0 |
| B9 Quantile LightGBM q0.9 | 0.329 | 0.425 | 0.405 | 45.2 | 0.062 | 0.063 | 0.244 | 5.4 |
| B10 Regional LSTM | 0.059 | 0.063 | 0.460 | 9.4 | 0.016 | 0.019 | 0.892 | 11.6 |
| B4 Logistic regression | 0.185 | 0.762 | 0.804 | 245.0 | 0.112 | 0.635 | 0.880 | 333.0 |
| B3 Ridge regression | 0.225 | 0.254 | 0.333 | 24.0 | 0.087 | 0.095 | 0.500 | 12.0 |

**Table 5 — Paired comparison, Δ = ACE-Flood − baseline (mean over 5 seeds). 95% block-bootstrap CI with 2-week blocks; p = two-sided paired block sign-flip permutation p (raw / Holm-adjusted over 22 comparisons); p for 1- and 4-week blocks in parentheses (raw).**

| h | Baseline | ΔCSI [95% CI] | p raw / Holm (L=1, L=4) | ΔPOD [95% CI] | ΔFAR [95% CI] |
| --- | --- | --- | --- | --- | --- |
| 1 | B11 B8 + CSI-tuned threshold | +0.011 [-0.027, +0.053] | 0.573 / 1.000 (0.556, 0.589) | +0.003 [-0.040, +0.057] | -0.012 [-0.042, +0.018] |
| 1 | B9 Quantile LightGBM q0.9 | +0.020 [-0.050, +0.123] | 0.623 / 1.000 (0.611, 0.505) | +0.035 [-0.040, +0.170] | -0.003 [-0.079, +0.053] |
| 1 | B10 Regional LSTM | +0.037 [-0.084, +0.173] | 0.592 / 1.000 (0.497, 0.573) | +0.219 [+0.101, +0.359] | +0.180 [+0.107, +0.248] |
| 1 | B8 LightGBM multi-forcing | +0.071 [-0.015, +0.169] | 0.175 / 1.000 (0.112, 0.253) | +0.216 [+0.130, +0.331] | +0.099 [+0.038, +0.158] |
| 1 | B3 Ridge regression | +0.057 [-0.025, +0.157] | 0.231 / 1.000 (0.305, 0.248) | +0.251 [+0.159, +0.395] | +0.190 [+0.115, +0.268] |
| 1 | B1 Persistence | +0.148 [+0.060, +0.245] | 0.014 / 0.216 (0.016, 0.051) | +0.219 [+0.122, +0.395] | -0.046 [-0.142, +0.034] |
| 1 | B12 Persistence + CRC/ACI decision layer | +0.293 [+0.191, +0.410] | 0.000 / 0.004 (0.000, 0.006) | +0.013 [-0.055, +0.120] | -0.339 [-0.472, -0.231] |
| 1 | B4 Logistic regression | +0.257 [+0.168, +0.367] | 0.000 / 0.004 (0.000, 0.000) | -0.067 [-0.123, +0.000] | -0.314 [-0.420, -0.231] |
| 1 | ACE-Flood [static, eta=0] | +0.027 [-0.017, +0.065] | 0.277 / 1.000 (0.215, 0.404) | -0.025 [-0.061, +0.000] | -0.047 [-0.075, -0.014] |
| 1 | A2 ACE split calibration | +0.587 [+0.507, +0.669] | 0.000 / 0.004 (0.000, 0.000) | -0.130 [-0.193, -0.052] | -0.654 [-0.747, -0.564] |
| 2 | B11 B8 + CSI-tuned threshold | -0.084 [-0.150, -0.022] | 0.026 / 0.335 (0.017, 0.002) | +0.270 [+0.204, +0.363] | +0.191 [+0.112, +0.276] |
| 2 | B9 Quantile LightGBM q0.9 | -0.082 [-0.182, +0.020] | 0.093 / 0.835 (0.087, 0.002) | +0.406 [+0.315, +0.528] | +0.334 [+0.229, +0.404] |
| 2 | B10 Regional LSTM | +0.189 [+0.094, +0.276] | 0.040 / 0.470 (0.016, 0.016) | +0.768 [+0.638, +0.870] | +0.279 [+0.015, +0.448] |
| 2 | B8 LightGBM multi-forcing | -0.028 [-0.124, +0.082] | 0.583 / 1.000 (0.603, 0.156) | +0.517 [+0.432, +0.635] | +0.432 [+0.261, +0.504] |
| 2 | B3 Ridge regression | +0.022 [-0.064, +0.115] | 0.700 / 1.000 (0.745, 0.324) | +0.578 [+0.497, +0.688] | +0.406 [+0.242, +0.577] |
| 2 | B1 Persistence | -0.038 [-0.108, +0.021] | 0.364 / 1.000 (0.466, 0.212) | +0.387 [+0.316, +0.483] | +0.183 [+0.103, +0.267] |
| 2 | B12 Persistence + CRC/ACI decision layer | +0.104 [+0.059, +0.156] | 0.000 / 0.004 (0.000, 0.001) | -0.025 [-0.128, +0.096] | -0.114 [-0.166, -0.069] |
| 2 | B4 Logistic regression | +0.063 [+0.029, +0.111] | 0.001 / 0.018 (0.001, 0.002) | +0.070 [+0.005, +0.133] | -0.065 [-0.114, -0.029] |
| 2 | ACE-Flood [static, eta=0] | +0.032 [+0.012, +0.051] | 0.005 / 0.078 (0.001, 0.047) | -0.016 [-0.053, +0.000] | -0.036 [-0.056, -0.016] |
| 2 | A2 ACE split calibration | +0.204 [+0.128, +0.275] | 0.000 / 0.004 (0.000, 0.000) | -0.168 [-0.302, -0.061] | -0.218 [-0.290, -0.139] |
| 3 | B11 B8 + CSI-tuned threshold | +0.059 [+0.018, +0.104] | 0.176 / 1.000 (0.231, 0.058) | +0.590 [+0.527, +0.672] | +0.322 [+0.020, +0.354] |
| 3 | B9 Quantile LightGBM q0.9 | +0.082 [-0.010, +0.169] | 0.145 / 1.000 (0.213, 0.044) | +0.727 [+0.630, +0.841] | +0.606 [-0.076, +0.881] |
| 3 | B10 Regional LSTM | +0.128 [+0.065, +0.188] | 0.036 / 0.546 (0.043, 0.016) | +0.771 [+0.633, +0.909] | -0.042 [-0.150, +0.025] |
| 3 | B8 LightGBM multi-forcing | +0.132 [+0.080, +0.188] | 0.031 / 0.530 (0.047, 0.016) | +0.778 [+0.652, +0.902] | +0.598 [+0.534, +0.640] |
| 3 | B3 Ridge regression | +0.057 [-0.005, +0.138] | 0.268 / 1.000 (0.394, 0.083) | +0.695 [+0.553, +0.859] | +0.350 [+0.286, +0.399] |
| 3 | B1 Persistence | -0.033 [-0.113, +0.045] | 0.344 / 1.000 (0.449, 0.119) | +0.489 [+0.349, +0.639] | +0.151 [+0.007, +0.255] |
| 3 | B12 Persistence + CRC/ACI decision layer | +0.031 [+0.009, +0.058] | 0.016 / 0.324 (0.015, 0.039) | -0.051 [-0.170, +0.068] | -0.034 [-0.063, -0.011] |
| 3 | B4 Logistic regression | +0.032 [-0.001, +0.069] | 0.101 / 1.000 (0.064, 0.039) | +0.156 [+0.000, +0.327] | -0.030 [-0.068, +0.003] |
| 3 | ACE-Flood [static, eta=0] | +0.016 [-0.001, +0.037] | 0.134 / 1.000 (0.090, 0.170) | +0.006 [-0.046, +0.095] | -0.017 [-0.039, +0.000] |
| 3 | A2 ACE split calibration | +0.101 [+0.057, +0.149] | 0.000 / 0.004 (0.000, 0.000) | -0.210 [-0.347, -0.069] | -0.107 [-0.160, -0.061] |

**Table 6 — What the decision layer contributes (h = 1, mean of 5 seeds; λ₀ / τ = threshold in y units).**

| Configuration | Threshold rule | λ₀ or τ | POD | FAR | CSI | Warnings |
| --- | --- | --- | --- | --- | --- | --- |
| ACE-Flood | CRC λ₀ + online update | 0.779 | 0.870 | 0.303 | 0.631 | 78.8 |
| ACE-Flood [static, eta=0] | CRC λ₀, fixed | – | 0.895 | 0.350 | 0.604 | 86.8 |
| A9 ACE empirical quantile (no CRC correction) | empirical 20% quantile of event scores | – | 0.892 | 0.340 | 0.611 | 85.2 |
| B11 B8 + CSI-tuned threshold | CSI-maximising τ on the same folds | 0.806 | 0.867 | 0.315 | 0.619 | 79.8 |
| B8 LightGBM multi-forcing | fixed y > 1 | 1 (fixed) | 0.654 | 0.204 | 0.560 | 51.8 |
| A4 ACE full-refit test score (v1) | CRC + update, test score from full refit | 0.779 | 0.876 | 0.311 | 0.628 | 80.2 |
| A3 ACE causal (forward-chaining) calibration | CRC + update, past-only folds | 0.761 | 0.889 | 0.349 | 0.602 | 86.2 |
| A2 ACE split calibration | CRC + update, held-out last 25% | −∞ | 1.000 | 0.957 | 0.043 | 1456.0 |
| A7 ACE expanding-window recalibration | CRC recomputed on all revealed events | – | 0.892 | 0.316 | 0.632 | 82.2 |
| A8 ACE rolling-window recalibration | CRC on last 40 events | – | 0.844 | 0.246 | 0.662 | 70.6 |
| A5 ACE Daymet-only predictor | as ACE, single forcing | 0.630 | 0.870 | 0.476 | 0.486 | 104.6 |
| A6 ACE forcing-ensemble spread score | as ACE, score + spread | 0.786 | 0.873 | 0.378 | 0.571 | 88.4 |

**Table 7 — Calibration strategies vs training-record length, new-gauge setting (h = 1, mean of 3 seeds). Cells: CSI / POD / FAR; n = calibration flood-days.**

| Strategy | 3 months (n = 1) | 6 months (n = 1) | 12 months (n = 18) | 23 months (n = 50) |
| --- | --- | --- | --- | --- |
| C1 CRC + ACI (literal) = ACE-Flood | 0.043 / 1.000 / 0.957 | 0.043 / 1.000 / 0.957 | 0.433 / 0.831 / 0.524 | 0.641 / 0.868 / 0.289 |
| C0 CRC static (literal: always-warn if n too small) | 0.043 / 1.000 / 0.957 | 0.043 / 1.000 / 0.957 | 0.426 / 0.884 / 0.549 | 0.608 / 0.894 / 0.344 |
| C2 CRC + ACI, min-event fallback to native y>1 | 0.154 / 0.206 / 0.621 | 0.157 / 0.222 / 0.653 | 0.433 / 0.831 / 0.524 | 0.641 / 0.868 / 0.289 |
| C3 Expanding-window recalibration | 0.282 / 0.741 / 0.687 | 0.247 / 0.735 / 0.729 | 0.455 / 0.852 / 0.506 | 0.634 / 0.889 / 0.311 |
| C4 Rolling-window recalibration (40 events) | 0.276 / 0.725 / 0.692 | 0.247 / 0.730 / 0.729 | 0.468 / 0.820 / 0.478 | 0.654 / 0.841 / 0.253 |
| C5 ACI from native threshold, no calibration | 0.154 / 0.206 / 0.621 | 0.157 / 0.222 / 0.653 | 0.467 / 0.593 / 0.313 | 0.556 / 0.688 / 0.257 |
| Native threshold y>1 (no calibration) | 0.000 / 0.000 / – | 0.000 / 0.000 / – | 0.448 / 0.503 / 0.194 | 0.491 / 0.587 / 0.250 |
| C1 local per-basin calibration | 0.043 / 1.000 / 0.957 | 0.043 / 1.000 / 0.957 | 0.281 / 0.910 / 0.711 | 0.400 / 0.889 / 0.579 |
| B11 B8 + CSI-tuned threshold | 0.249 / 0.884 / 0.742 | 0.243 / 0.852 / 0.746 | 0.524 / 0.693 / 0.318 | 0.604 / 0.847 / 0.322 |
| B10 Regional LSTM | 0.000 / 0.000 / – | 0.016 / 0.016 / 0.000 | 0.484 / 0.513 / 0.090 | 0.607 / 0.677 / 0.143 |

(check: calibration events by record length = {3: 1.0, 6: 1.0, 12: 18.0, 23: 50.0})

**Table 8 — Partially gauged target: the target basin has only Oct–Dec 2001; donors have 23 months (h = 1; mean over 4 targets × 3 seeds).**

| Setting | Strategy | POD | FAR | CSI | Warnings (target basin) |
| --- | --- | --- | --- | --- | --- |
| local 3 months only | C1 CRC + ACI (literal) = ACE-Flood | 1.000 | 0.957 | 0.043 | 364.0 |
| local 3 months only | C2 CRC + ACI, min-event fallback to native y>1 | 0.031 | 0.667 | 0.029 | 2.5 |
| local 3 months only | C3 Expanding-window recalibration | 0.301 | 0.753 | 0.133 | 23.8 |
| pooled with donors | C1 CRC + ACI (literal) = ACE-Flood | 0.843 | 0.372 | 0.563 | 21.4 |
| pooled with donors | C3 Expanding-window recalibration | 0.857 | 0.343 | 0.593 | 21.5 |
| pooled with donors | Native threshold y>1 (no calibration) | 0.627 | 0.252 | 0.514 | 13.3 |

**Table 10 — Flood threshold from training years only (Q95 of 2000–2001). Mean of 5 seeds; CSI / POD / FAR.**

| Model | h = 1 | h = 2 | h = 3 |
| --- | --- | --- | --- |
| ACE-Flood | 0.666 / 0.802 / 0.202 | 0.380 / 0.817 / 0.584 | 0.227 / 0.758 / 0.755 |
| ACE-Flood [static] | 0.686 / 0.818 / 0.191 | 0.357 / 0.802 / 0.609 | 0.214 / 0.756 / 0.770 |
| B8 LightGBM multi-forcing | 0.697 / 0.837 / 0.193 | 0.435 / 0.553 / 0.328 | 0.163 / 0.217 / 0.606 |
| B11 B8 + CSI-tuned threshold | 0.690 / 0.812 / 0.178 | 0.432 / 0.592 / 0.369 | 0.219 / 0.363 / 0.636 |
| B1 Persistence | 0.566 / 0.723 / 0.277 | 0.345 / 0.513 / 0.487 | 0.221 / 0.361 / 0.639 |
| B12 Persistence + CRC/ACI | 0.441 / 0.815 / 0.510 | 0.224 / 0.790 / 0.761 | 0.182 / 0.782 / 0.808 |

Thresholds (mm/d, long-term → training-years): 01022500: 7.12 → 5.46; 01547700: 4.83 → 3.05; 02064000: 2.60 → 1.22; 03015500: 7.17 → 4.30. Events (train / test) by lead: {1: {'n_train_events': 139.0, 'n_test_events': 119.0}, 2: {'n_train_events': 139.0, 'n_test_events': 119.0}, 3: {'n_train_events': 139.0, 'n_test_events': 119.0}}.

**Table 11 — Nominal 90% intervals on y (mean of 5 seeds).**

| Lead | Raw quantile LightGBM: PICP / MPIW / IS | + CQR: PICP / MPIW / IS | + CQR + ACI: PICP / MPIW / IS |
| --- | --- | --- | --- |
| h = 1 | 0.811 / 0.198 / 0.464 | 0.869 / 0.203 / 0.461 | 0.896 / 0.225 / 0.469 |
| h = 2 | 0.758 / 0.230 / 0.924 | 0.872 / 0.242 / 0.914 | 0.888 / 0.285 / 0.920 |
| h = 3 | 0.721 / 0.256 / 1.229 | 0.855 / 0.273 / 1.212 | 0.883 / 0.488 / 1.274 |

**Table 12 — Proposition 2 bound vs realised deviation (α = 0.2, η = 0.05, mean of 5 seeds). The bound is vacuous whenever it exceeds 1.**

| h | Basin | K (flood-days) | s_min | s_max | Bound on \|miss − α\| | Realised miss rate | Realised \|miss − α\| |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 01022500 | 23 | -0.124 | 2.181 | 2.18 | 0.096 | 0.104 |
| 1 | 01547700 | 15 | -0.071 | 2.124 | 3.19 | 0.200 | 0.000 |
| 1 | 02064000 | 9 | -0.048 | 2.132 | 5.29 | 0.111 | 0.089 |
| 1 | 03015500 | 16 | -0.001 | 2.012 | 2.77 | 0.125 | 0.075 |
| 2 | 01022500 | 23 | -0.001 | 1.262 | 1.36 | 0.052 | 0.148 |
| 2 | 01547700 | 15 | -0.012 | 1.254 | 2.09 | 0.160 | 0.040 |
| 2 | 02064000 | 9 | 0.004 | 1.254 | 3.44 | 0.444 | 0.244 |
| 2 | 03015500 | 16 | 0.020 | 1.267 | 1.93 | 0.188 | 0.013 |
| 3 | 01022500 | 23 | 0.008 | 1.366 | 1.53 | 0.130 | 0.070 |
| 3 | 01547700 | 15 | 0.004 | 1.366 | 2.35 | 0.213 | 0.013 |
| 3 | 02064000 | 9 | 0.016 | 1.366 | 3.89 | 0.444 | 0.244 |
| 3 | 03015500 | 16 | 0.024 | 1.366 | 2.18 | 0.188 | 0.013 |

VALIDITY: combos=30 exceed=7 max_excess=0.024; all-eta max_excess=0.056
    h  alpha   eta  MissRate
46  3    0.1  0.05     0.111
48  3    0.2  0.00     0.216
50  3    0.2  0.05     0.210
52  3    0.3  0.00     0.324
54  3    0.3  0.05     0.314
56  3    0.4  0.00     0.403
58  3    0.4  0.05     0.406

**Table 9 — Missing gauge readings (h = 1, mean of 3 mask seeds). Cells: CSI / POD / FAR.**

| Model | 0% (simulated) | 10% (simulated) | 20% (simulated) | 40% (simulated) | natural gaps (9.4%) |
| --- | --- | --- | --- | --- | --- |
| ACE-Flood | 0.613 / 0.873 / 0.326 | 0.558 / 0.815 / 0.360 | 0.527 / 0.815 / 0.393 | 0.426 / 0.709 / 0.484 | 0.624 / 0.852 / 0.300 |
| ACE-Flood (v1 bug: uses unobserved labels) | 0.613 / 0.873 / 0.326 | 0.545 / 0.836 / 0.391 | 0.497 / 0.825 / 0.444 | 0.415 / 0.735 / 0.512 | 0.624 / 0.852 / 0.300 |
| ACE-Flood [static] | 0.596 / 0.899 / 0.361 | 0.536 / 0.831 / 0.397 | 0.485 / 0.825 / 0.455 | 0.401 / 0.709 / 0.519 | 0.595 / 0.878 / 0.351 |
| A7 ACE expanding-window | 0.626 / 0.894 / 0.324 | 0.560 / 0.825 / 0.364 | 0.544 / 0.810 / 0.373 | 0.431 / 0.693 / 0.468 | 0.608 / 0.878 / 0.336 |
| ACE-Flood w/o data-age feature | 0.613 / 0.873 / 0.326 | 0.553 / 0.810 / 0.362 | 0.532 / 0.820 / 0.390 | 0.424 / 0.693 / 0.477 | 0.626 / 0.857 / 0.302 |
| B11 B8 + CSI-tuned threshold | 0.614 / 0.873 / 0.326 | 0.558 / 0.788 / 0.335 | 0.585 / 0.788 / 0.304 | 0.441 / 0.614 / 0.376 | 0.588 / 0.862 / 0.350 |
| B8 LightGBM multi-forcing | 0.575 / 0.672 / 0.201 | 0.504 / 0.608 / 0.253 | 0.490 / 0.587 / 0.249 | 0.444 / 0.513 / 0.222 | 0.541 / 0.640 / 0.225 |
| B1 Persistence (last valid reading) | 0.482 / 0.651 / 0.349 | 0.444 / 0.608 / 0.375 | 0.419 / 0.577 / 0.382 | 0.342 / 0.466 / 0.430 | 0.451 / 0.651 / 0.406 |

                   realised_missing  test_labels_unobserved  n_cal_events
scenario rate                                                            
MCAR     0.000000             0.000                   0.000        50.000
         0.100000             0.106                   0.105        45.667
         0.200000             0.204                   0.217        42.667
         0.400000             0.405                   0.435        33.000
natural  0.093574             0.094                   0.115        50.000