**Table 3 — Test 2002, h = 1 d, pooled over 4 basins (63 flood-days, 22 onsets, 1,456 forecasts). Mean ± sd over 5 seeds; deterministic models show no sd; sorted by CSI.**

| Model | POD | FAR | CSI | F1 | Onset POD | Warnings | NSE (pooled) | NSE (median basin) | KGE | RMSE (mm/d) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B9 Quantile LightGBM q0.9 | 0.762 ± 0.011 | 0.304 ± 0.020 | 0.572 ± 0.016 | 0.727 ± 0.013 | 0.473 ± 0.025 | 69.0 | – | – | – | – |
| B11 B8 + CSI-tuned threshold | 0.790 ± 0.007 | 0.354 ± 0.021 | 0.551 ± 0.014 | 0.711 ± 0.012 | 0.455 | 77.2 | 0.798 | 0.762 | 0.765 | 0.955 |
| B3 Ridge regression | 0.571 | 0.122 | 0.529 | 0.692 | 0.182 | 41.0 | 0.817 | 0.746 | 0.789 | 0.908 |
| B8 LightGBM multi-forcing | 0.575 ± 0.026 | 0.223 ± 0.023 | 0.493 ± 0.026 | 0.660 ± 0.023 | 0.427 ± 0.025 | 46.6 | 0.798 | 0.762 | 0.765 | 0.955 |
| B7 LightGBM Daymet only | 0.549 ± 0.027 | 0.199 ± 0.031 | 0.484 ± 0.031 | 0.651 ± 0.028 | 0.382 ± 0.025 | 43.2 | 0.775 | 0.701 | 0.746 | 1.008 |
| B1 Persistence | 0.651 | 0.349 | 0.482 | 0.651 | 0.000 | 63.0 | 0.773 | 0.704 | 0.886 | 1.013 |
| B10 Regional LSTM | 0.514 ± 0.021 | 0.114 ± 0.021 | 0.482 ± 0.020 | 0.650 ± 0.018 | 0.200 ± 0.052 | 36.6 | 0.786 | 0.712 | 0.707 | 0.983 |
| A7 ACE expanding-window recalibration | 0.835 ± 0.009 | 0.477 ± 0.003 | 0.474 ± 0.004 | 0.643 ± 0.003 | 0.527 ± 0.025 | 100.6 | 0.798 | 0.759 | 0.758 | 0.954 |
| B5 Random forest | 0.603 ± 0.011 | 0.329 ± 0.013 | 0.466 ± 0.012 | 0.635 ± 0.011 | 0.409 ± 0.032 | 56.6 | – | – | – | – |
| A4 ACE full-refit test score (v1) | 0.825 | 0.484 ± 0.008 | 0.465 ± 0.006 | 0.635 ± 0.006 | 0.500 | 100.8 | 0.798 | 0.762 | 0.765 | 0.955 |
| A8 ACE rolling-window recalibration | 0.844 ± 0.007 | 0.500 ± 0.010 | 0.458 ± 0.008 | 0.628 ± 0.007 | 0.555 ± 0.020 | 106.4 | 0.798 | 0.759 | 0.758 | 0.954 |
| A9 ACE empirical quantile (no CRC correction) | 0.835 ± 0.009 | 0.498 ± 0.010 | 0.457 ± 0.008 | 0.627 ± 0.007 | 0.527 ± 0.025 | 104.8 | 0.798 | 0.759 | 0.758 | 0.954 |
| **ACE-Flood** | 0.810 | 0.496 ± 0.015 | 0.451 ± 0.012 | 0.621 ± 0.011 | 0.500 | 101.2 | 0.798 | 0.759 | 0.758 | 0.954 |
| ACE-Flood [static, eta=0] | 0.835 ± 0.009 | 0.506 ± 0.010 | 0.450 ± 0.009 | 0.620 ± 0.009 | 0.527 ± 0.025 | 106.6 | 0.798 | 0.759 | 0.758 | 0.954 |
| B6 LightGBM local | 0.495 ± 0.013 | 0.204 ± 0.021 | 0.440 ± 0.013 | 0.611 ± 0.013 | 0.227 | 39.2 | 0.773 | 0.683 | 0.741 | 1.012 |
| A6 ACE forcing-ensemble spread score | 0.841 ± 0.022 | 0.544 ± 0.009 | 0.420 ± 0.011 | 0.592 ± 0.011 | 0.555 ± 0.050 | 116.2 | 0.789 | 0.734 | 0.743 | 0.975 |
| A5 ACE Daymet-only predictor | 0.873 | 0.578 ± 0.019 | 0.397 ± 0.017 | 0.569 ± 0.017 | 0.636 | 130.6 | 0.774 | 0.701 | 0.736 | 1.009 |
| A3 ACE causal (forward-chaining) calibration | 0.873 | 0.584 ± 0.022 | 0.392 ± 0.020 | 0.563 ± 0.020 | 0.636 | 132.6 | 0.803 | 0.734 | 0.763 | 0.942 |
| B12 Persistence + CRC/ACI decision layer | 0.857 | 0.642 | 0.338 | 0.505 | 0.591 | 151.0 | 0.773 | 0.704 | 0.886 | 1.013 |
| B4 Logistic regression | 0.873 | 0.678 | 0.307 | 0.470 | 0.636 | 171.0 | – | – | – | – |
| B12 Persistence + CRC/ACI decision layer [static, eta=0] | 0.873 | 0.688 | 0.299 | 0.460 | 0.636 | 176.0 | 0.773 | 0.704 | 0.886 | 1.013 |
| B2 Rainfall-threshold rule | 0.492 | 0.716 | 0.220 | 0.360 | 0.136 | 109.0 | – | – | – | – |
| A2 ACE split calibration | 1.000 | 0.957 | 0.043 | 0.083 | 1.000 | 1456.0 | 0.800 | 0.762 | 0.779 | 0.950 |

**Table 4 — Leads h = 2 and 3 d (mean of 5 seeds). CSI / POD / FAR; '–' = no warnings issued.**

| Model | h = 2: CSI | POD | FAR | Warnings | h = 3: CSI | POD | FAR | Warnings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACE-Flood | 0.136 | 0.886 | 0.861 | 403.0 | 0.130 | 0.778 | 0.865 | 364.8 |
| ACE-Flood [static, eta=0] | 0.118 | 0.927 | 0.881 | 491.8 | 0.122 | 0.759 | 0.873 | 377.8 |
| A7 ACE expanding-window recalibration | 0.131 | 0.863 | 0.866 | 407.0 | 0.131 | 0.765 | 0.863 | 353.0 |
| B1 Persistence | 0.286 | 0.444 | 0.556 | 63.0 | 0.178 | 0.302 | 0.698 | 63.0 |
| B12 Persistence + CRC/ACI decision layer | 0.143 | 0.857 | 0.853 | 368.0 | 0.113 | 0.841 | 0.884 | 457.0 |
| B8 LightGBM multi-forcing | 0.064 | 0.067 | 0.363 | 6.6 | 0.000 | 0.000 | – | 0.0 |
| B11 B8 + CSI-tuned threshold | 0.260 | 0.330 | 0.378 | 35.4 | 0.040 | 0.105 | 0.387 | 28.4 |
| B9 Quantile LightGBM q0.9 | 0.192 | 0.206 | 0.269 | 17.8 | 0.016 | 0.016 | 0.100 | 1.2 |
| B10 Regional LSTM | 0.123 | 0.127 | 0.209 | 10.2 | 0.003 | 0.003 | 0.000 | 0.2 |
| B4 Logistic regression | 0.148 | 0.714 | 0.843 | 286.0 | 0.109 | 0.635 | 0.883 | 343.0 |
| B3 Ridge regression | 0.217 | 0.238 | 0.286 | 21.0 | 0.071 | 0.079 | 0.583 | 12.0 |

**Table 5 — Paired comparison, Δ = ACE-Flood − baseline (mean over 5 seeds). 95% block-bootstrap CI with 2-week blocks; p = two-sided paired block sign-flip permutation p (raw / Holm-adjusted over 22 comparisons); p for 1- and 4-week blocks in parentheses (raw).**

| h | Baseline | ΔCSI [95% CI] | p raw / Holm (L=1, L=4) | ΔPOD [95% CI] | ΔFAR [95% CI] |
| --- | --- | --- | --- | --- | --- |
| 1 | B11 B8 + CSI-tuned threshold | -0.100 [-0.157, -0.052] | 0.001 / 0.025 (0.000, 0.006) | +0.019 [-0.034, +0.097] | +0.141 [+0.093, +0.204] |
| 1 | B9 Quantile LightGBM q0.9 | -0.121 [-0.187, -0.046] | 0.011 / 0.176 (0.001, 0.031) | +0.048 [-0.020, +0.162] | +0.192 [+0.130, +0.253] |
| 1 | B10 Regional LSTM | -0.031 [-0.173, +0.104] | 0.663 / 1.000 (0.613, 0.718) | +0.295 [+0.148, +0.495] | +0.381 [+0.312, +0.522] |
| 1 | B8 LightGBM multi-forcing | -0.043 [-0.138, +0.036] | 0.352 / 1.000 (0.275, 0.339) | +0.235 [+0.166, +0.332] | +0.273 [+0.195, +0.356] |
| 1 | B3 Ridge regression | -0.079 [-0.202, +0.095] | 0.310 / 1.000 (0.190, 0.391) | +0.238 [+0.094, +0.500] | +0.374 [+0.296, +0.468] |
| 1 | B1 Persistence | -0.032 [-0.127, +0.060] | 0.492 / 1.000 (0.496, 0.648) | +0.159 [+0.072, +0.302] | +0.146 [+0.062, +0.247] |
| 1 | B12 Persistence + CRC/ACI decision layer | +0.113 [+0.045, +0.184] | 0.004 / 0.061 (0.002, 0.025) | -0.048 [-0.102, +0.043] | -0.147 [-0.219, -0.076] |
| 1 | B4 Logistic regression | +0.144 [+0.081, +0.230] | 0.000 / 0.004 (0.000, 0.001) | -0.063 [-0.115, +0.000] | -0.183 [-0.261, -0.123] |
| 1 | ACE-Flood [static, eta=0] | +0.001 [-0.028, +0.033] | 0.946 / 1.000 (0.945, 0.965) | -0.025 [-0.078, +0.000] | -0.011 [-0.042, +0.020] |
| 1 | A2 ACE split calibration | +0.408 [+0.311, +0.491] | 0.000 / 0.004 (0.000, 0.000) | -0.190 [-0.286, -0.083] | -0.461 [-0.540, -0.353] |
| 2 | B11 B8 + CSI-tuned threshold | -0.124 [-0.202, -0.040] | 0.007 / 0.119 (0.003, 0.002) | +0.556 [+0.485, +0.648] | +0.484 [+0.321, +0.631] |
| 2 | B9 Quantile LightGBM q0.9 | -0.055 [-0.148, +0.034] | 0.267 / 1.000 (0.230, 0.063) | +0.679 [+0.624, +0.751] | +0.592 [+0.344, +0.843] |
| 2 | B10 Regional LSTM | +0.014 [-0.084, +0.112] | 0.815 / 1.000 (0.793, 0.682) | +0.759 [+0.684, +0.853] | +0.652 [+0.531, +0.837] |
| 2 | B8 LightGBM multi-forcing | +0.072 [+0.001, +0.148] | 0.215 / 1.000 (0.182, 0.104) | +0.819 [+0.747, +0.904] | +0.498 [-0.068, +0.858] |
| 2 | B3 Ridge regression | -0.081 [-0.189, +0.050] | 0.062 / 0.918 (0.100, 0.009) | +0.648 [+0.520, +0.821] | +0.576 [+0.282, +0.733] |
| 2 | B1 Persistence | -0.150 [-0.239, -0.068] | 0.000 / 0.008 (0.001, 0.002) | +0.441 [+0.337, +0.559] | +0.306 [+0.196, +0.407] |
| 2 | B12 Persistence + CRC/ACI decision layer | -0.007 [-0.027, +0.014] | 0.510 / 1.000 (0.455, 0.568) | +0.029 [-0.035, +0.111] | +0.008 [-0.014, +0.028] |
| 2 | B4 Logistic regression | -0.012 [-0.037, +0.017] | 0.433 / 1.000 (0.424, 0.503) | +0.171 [+0.084, +0.300] | +0.019 [-0.011, +0.044] |
| 2 | ACE-Flood [static, eta=0] | +0.018 [+0.006, +0.035] | 0.015 / 0.255 (0.007, 0.086) | -0.041 [-0.100, +0.013] | -0.020 [-0.039, -0.007] |
| 2 | A2 ACE split calibration | +0.093 [+0.054, +0.142] | 0.000 / 0.004 (0.000, 0.000) | -0.114 [-0.211, -0.033] | -0.095 [-0.148, -0.054] |
| 3 | B11 B8 + CSI-tuned threshold | +0.089 [+0.043, +0.134] | 0.080 / 0.885 (0.094, 0.082) | +0.673 [+0.537, +0.783] | +0.482 [+0.016, +0.529] |
| 3 | B9 Quantile LightGBM q0.9 | +0.114 [+0.064, +0.170] | 0.047 / 0.611 (0.057, 0.046) | +0.762 [+0.600, +0.900] | +0.765 [-0.162, +0.883] |
| 3 | B10 Regional LSTM | +0.126 [+0.073, +0.182] | 0.032 / 0.536 (0.038, 0.046) | +0.775 [+0.600, +0.924] | +0.868 [+0.805, +0.910] |
| 3 | B8 LightGBM multi-forcing | +0.130 [+0.074, +0.185] | 0.028 / 0.536 (0.034, 0.039) | +0.778 [+0.600, +0.930] | +nan [+nan, +nan] |
| 3 | B3 Ridge regression | +0.058 [-0.001, +0.125] | 0.254 / 1.000 (0.354, 0.153) | +0.698 [+0.545, +0.863] | +0.282 [-0.111, +0.373] |
| 3 | B1 Persistence | -0.048 [-0.128, +0.031] | 0.135 / 1.000 (0.239, 0.067) | +0.476 [+0.329, +0.638] | +0.167 [+0.020, +0.269] |
| 3 | B12 Persistence + CRC/ACI decision layer | +0.016 [-0.008, +0.042] | 0.213 / 1.000 (0.210, 0.125) | -0.063 [-0.211, +0.077] | -0.019 [-0.045, +0.005] |
| 3 | B4 Logistic regression | +0.020 [-0.014, +0.057] | 0.294 / 1.000 (0.239, 0.234) | +0.143 [-0.024, +0.333] | -0.018 [-0.055, +0.017] |
| 3 | ACE-Flood [static, eta=0] | +0.008 [-0.011, +0.030] | 0.477 / 1.000 (0.464, 0.441) | +0.019 [-0.074, +0.139] | -0.008 [-0.030, +0.012] |
| 3 | A2 ACE split calibration | +0.086 [+0.046, +0.134] | 0.000 / 0.004 (0.000, 0.000) | -0.222 [-0.400, -0.070] | -0.091 [-0.143, -0.050] |

**Table 6 — What the decision layer contributes (h = 1, mean of 5 seeds; λ₀ / τ = threshold in y units).**

| Configuration | Threshold rule | λ₀ or τ | POD | FAR | CSI | Warnings |
| --- | --- | --- | --- | --- | --- | --- |
| ACE-Flood | CRC λ₀ + online update | 0.677 | 0.810 | 0.496 | 0.451 | 101.2 |
| ACE-Flood [static, eta=0] | CRC λ₀, fixed | – | 0.835 | 0.506 | 0.450 | 106.6 |
| A9 ACE empirical quantile (no CRC correction) | empirical 20% quantile of event scores | – | 0.835 | 0.498 | 0.457 | 104.8 |
| B11 B8 + CSI-tuned threshold | CSI-maximising τ on the same folds | 0.781 | 0.790 | 0.354 | 0.551 | 77.2 |
| B8 LightGBM multi-forcing | fixed y > 1 | 1 (fixed) | 0.575 | 0.223 | 0.493 | 46.6 |
| A4 ACE full-refit test score (v1) | CRC + update, test score from full refit | 0.677 | 0.825 | 0.484 | 0.465 | 100.8 |
| A3 ACE causal (forward-chaining) calibration | CRC + update, past-only folds | 0.538 | 0.873 | 0.584 | 0.392 | 132.6 |
| A2 ACE split calibration | CRC + update, held-out last 25% | −∞ | 1.000 | 0.957 | 0.043 | 1456.0 |
| A7 ACE expanding-window recalibration | CRC recomputed on all revealed events | – | 0.835 | 0.477 | 0.474 | 100.6 |
| A8 ACE rolling-window recalibration | CRC on last 40 events | – | 0.844 | 0.500 | 0.458 | 106.4 |
| A5 ACE Daymet-only predictor | as ACE, single forcing | 0.532 | 0.873 | 0.578 | 0.397 | 130.6 |
| A6 ACE forcing-ensemble spread score | as ACE, score + spread | 0.642 | 0.841 | 0.544 | 0.420 | 116.2 |

**Table 7 — Calibration strategies vs training-record length, new-gauge setting (h = 1, mean of 3 seeds). Cells: CSI / POD / FAR; n = calibration flood-days.**

| Strategy | 3 months (n = 1) | 6 months (n = 1) | 12 months (n = 18) | 23 months (n = 50) |
| --- | --- | --- | --- | --- |
| C1 CRC + ACI (literal) = ACE-Flood | 0.043 / 1.000 / 0.957 | 0.043 / 1.000 / 0.957 | 0.371 / 0.884 / 0.610 | 0.458 / 0.810 / 0.487 |
| C0 CRC static (literal: always-warn if n too small) | 0.043 / 1.000 / 0.957 | 0.043 / 1.000 / 0.957 | 0.340 / 0.905 / 0.647 | 0.457 / 0.841 / 0.500 |
| C2 CRC + ACI, min-event fallback to native y>1 | 0.116 / 0.159 / 0.700 | 0.131 / 0.190 / 0.702 | 0.371 / 0.884 / 0.610 | 0.458 / 0.810 / 0.487 |
| C3 Expanding-window recalibration | 0.240 / 0.735 / 0.737 | 0.235 / 0.746 / 0.744 | 0.400 / 0.783 / 0.550 | 0.486 / 0.836 / 0.462 |
| C4 Rolling-window recalibration (40 events) | 0.240 / 0.725 / 0.736 | 0.234 / 0.730 / 0.744 | 0.387 / 0.783 / 0.567 | 0.476 / 0.841 / 0.477 |
| C5 ACI from native threshold, no calibration | 0.116 / 0.159 / 0.700 | 0.131 / 0.190 / 0.702 | 0.403 / 0.519 / 0.355 | 0.533 / 0.635 / 0.231 |
| Native threshold y>1 (no calibration) | 0.000 / 0.000 / – | 0.000 / 0.000 / – | 0.324 / 0.349 / 0.185 | 0.471 / 0.550 / 0.235 |
| C1 local per-basin calibration | 0.043 / 1.000 / 0.957 | 0.043 / 1.000 / 0.957 | 0.189 / 0.899 / 0.807 | 0.225 / 0.841 / 0.765 |
| B11 B8 + CSI-tuned threshold | 0.166 / 0.937 / 0.832 | 0.193 / 0.942 / 0.804 | 0.455 / 0.624 / 0.372 | 0.499 / 0.825 / 0.441 |
| B10 Regional LSTM | 0.000 / 0.000 / – | 0.000 / 0.000 / – | 0.145 / 0.148 / 0.125 | 0.505 / 0.540 / 0.113 |

(check: calibration events by record length = {3: 1.0, 6: 1.0, 12: 18.0, 23: 50.0})

**Table 8 — Partially gauged target: the target basin has only Oct–Dec 2001; donors have 23 months (h = 1; mean over 4 targets × 3 seeds).**

| Setting | Strategy | POD | FAR | CSI | Warnings (target basin) |
| --- | --- | --- | --- | --- | --- |
| local 3 months only | C1 CRC + ACI (literal) = ACE-Flood | 1.000 | 0.957 | 0.043 | 364.0 |
| local 3 months only | C2 CRC + ACI, min-event fallback to native y>1 | 0.016 | 0.833 | 0.014 | 2.5 |
| local 3 months only | C3 Expanding-window recalibration | 0.291 | 0.805 | 0.109 | 29.2 |
| pooled with donors | C1 CRC + ACI (literal) = ACE-Flood | 0.853 | 0.553 | 0.420 | 31.0 |
| pooled with donors | C3 Expanding-window recalibration | 0.832 | 0.478 | 0.480 | 25.5 |
| pooled with donors | Native threshold y>1 (no calibration) | 0.543 | 0.249 | 0.463 | 11.0 |

**Table 10 — Flood threshold from training years only (Q95 of 2000–2001). Mean of 5 seeds; CSI / POD / FAR.**

| Model | h = 1 | h = 2 | h = 3 |
| --- | --- | --- | --- |
| ACE-Flood | 0.629 / 0.820 / 0.270 | 0.267 / 0.810 / 0.715 | 0.220 / 0.755 / 0.763 |
| ACE-Flood [static] | 0.608 / 0.827 / 0.304 | 0.243 / 0.842 / 0.745 | 0.207 / 0.758 / 0.778 |
| B8 LightGBM multi-forcing | 0.641 / 0.776 / 0.214 | 0.364 / 0.403 / 0.210 | 0.095 / 0.121 / 0.696 |
| B11 B8 + CSI-tuned threshold | 0.640 / 0.760 / 0.197 | 0.397 / 0.524 / 0.361 | 0.209 / 0.427 / 0.695 |
| B1 Persistence | 0.566 / 0.723 / 0.277 | 0.345 / 0.513 / 0.487 | 0.221 / 0.361 / 0.639 |
| B12 Persistence + CRC/ACI | 0.441 / 0.815 / 0.510 | 0.224 / 0.790 / 0.761 | 0.182 / 0.782 / 0.808 |

Thresholds (mm/d, long-term → training-years): 01022500: 7.12 → 5.46; 01547700: 4.83 → 3.05; 02064000: 2.60 → 1.22; 03015500: 7.17 → 4.30. Events (train / test) by lead: {1: {'n_train_events': 139.0, 'n_test_events': 119.0}, 2: {'n_train_events': 139.0, 'n_test_events': 119.0}, 3: {'n_train_events': 139.0, 'n_test_events': 119.0}}.

**Table 11 — Nominal 90% intervals on y (mean of 5 seeds).**

| Lead | Raw quantile LightGBM: PICP / MPIW / IS | + CQR: PICP / MPIW / IS | + CQR + ACI: PICP / MPIW / IS |
| --- | --- | --- | --- |
| h = 1 | 0.822 / 0.254 / 0.688 | 0.841 / 0.255 / 0.687 | 0.889 / 0.269 / 0.686 |
| h = 2 | 0.776 / 0.281 / 1.098 | 0.824 / 0.286 / 1.093 | 0.887 / 0.393 / 1.102 |
| h = 3 | 0.764 / 0.303 / 1.271 | 0.821 / 0.311 / 1.262 | 0.882 / 0.492 / 1.310 |

**Table 12 — Proposition 2 bound vs realised deviation (α = 0.2, η = 0.05, mean of 5 seeds). The bound is vacuous whenever it exceeds 1.**

| h | Basin | K (flood-days) | s_min | s_max | Bound on \|miss − α\| | Realised miss rate | Realised \|miss − α\| |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 01022500 | 23 | 0.026 | 1.643 | 1.58 | 0.087 | 0.113 |
| 1 | 01547700 | 15 | 0.014 | 1.609 | 2.39 | 0.333 | 0.133 |
| 1 | 02064000 | 9 | 0.028 | 1.571 | 3.87 | 0.111 | 0.089 |
| 1 | 03015500 | 16 | 0.028 | 1.574 | 2.18 | 0.250 | 0.050 |
| 2 | 01022500 | 23 | 0.030 | 1.217 | 1.29 | 0.043 | 0.157 |
| 2 | 01547700 | 15 | 0.017 | 1.217 | 2.00 | 0.147 | 0.053 |
| 2 | 02064000 | 9 | 0.030 | 1.217 | 3.30 | 0.222 | 0.022 |
| 2 | 03015500 | 16 | 0.030 | 1.217 | 1.86 | 0.125 | 0.075 |
| 3 | 01022500 | 23 | 0.033 | 1.214 | 1.37 | 0.130 | 0.070 |
| 3 | 01547700 | 15 | 0.028 | 1.214 | 2.11 | 0.267 | 0.067 |
| 3 | 02064000 | 9 | 0.029 | 1.214 | 3.52 | 0.444 | 0.244 |
| 3 | 03015500 | 16 | 0.033 | 1.214 | 1.98 | 0.188 | 0.013 |

VALIDITY: combos=30 exceed=7 max_excess=0.063; all-eta max_excess=0.087
    h  alpha   eta  MissRate
46  3    0.1  0.05     0.146
48  3    0.2  0.00     0.241
50  3    0.2  0.05     0.222
52  3    0.3  0.00     0.302
54  3    0.3  0.05     0.311
56  3    0.4  0.00     0.403
58  3    0.4  0.05     0.463

**Table 9 — Missing gauge readings (h = 1, mean of 3 mask seeds). Cells: CSI / POD / FAR.**

| Model | 0% (simulated) | 10% (simulated) | 20% (simulated) | 40% (simulated) | natural gaps (9.4%) |
| --- | --- | --- | --- | --- | --- |
| ACE-Flood | 0.458 / 0.810 / 0.487 | 0.401 / 0.767 / 0.543 | 0.371 / 0.778 / 0.573 | 0.304 / 0.698 / 0.638 | 0.458 / 0.804 / 0.484 |
| ACE-Flood (v1 bug: uses unobserved labels) | 0.458 / 0.810 / 0.487 | 0.391 / 0.783 / 0.563 | 0.348 / 0.799 / 0.615 | 0.292 / 0.735 / 0.664 | 0.458 / 0.804 / 0.484 |
| ACE-Flood [static] | 0.451 / 0.831 / 0.503 | 0.399 / 0.794 / 0.555 | 0.333 / 0.788 / 0.625 | 0.285 / 0.698 / 0.657 | 0.432 / 0.820 / 0.523 |
| A7 ACE expanding-window | 0.471 / 0.831 / 0.478 | 0.429 / 0.778 / 0.512 | 0.420 / 0.735 / 0.498 | 0.341 / 0.646 / 0.575 | 0.471 / 0.820 / 0.474 |
| ACE-Flood w/o data-age feature | 0.458 / 0.810 / 0.487 | 0.411 / 0.762 / 0.527 | 0.377 / 0.783 / 0.568 | 0.315 / 0.683 / 0.620 | 0.461 / 0.810 / 0.483 |
| B11 B8 + CSI-tuned threshold | 0.548 / 0.788 / 0.357 | 0.511 / 0.735 / 0.370 | 0.493 / 0.709 / 0.377 | 0.361 / 0.508 / 0.414 | 0.516 / 0.815 / 0.414 |
| B8 LightGBM multi-forcing | 0.507 / 0.587 / 0.213 | 0.506 / 0.582 / 0.203 | 0.471 / 0.529 / 0.187 | 0.377 / 0.418 / 0.202 | 0.489 / 0.561 / 0.209 |
| B1 Persistence (last valid reading) | 0.482 / 0.651 / 0.349 | 0.444 / 0.608 / 0.375 | 0.419 / 0.577 / 0.382 | 0.342 / 0.466 / 0.430 | 0.451 / 0.651 / 0.406 |

                   realised_missing  test_labels_unobserved  n_cal_events
scenario rate                                                            
MCAR     0.000000             0.000                   0.000        50.000
         0.100000             0.106                   0.105        45.667
         0.200000             0.204                   0.217        42.667
         0.400000             0.405                   0.435        33.000
natural  0.093574             0.094                   0.115        50.000