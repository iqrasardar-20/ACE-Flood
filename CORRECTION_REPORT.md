# Correction report: revision 1 → revision 2

Each issue found in the audit, the fix, and how the results changed. All experiments were rerun after the fixes.


| # | Issue in revision 1 | Type | Fix in revision 2 | Effect on results |
| --- | --- | --- | --- | --- |
| 1 | The online threshold and ACI interval updates used gauge readings that were masked as missing | Information leak (implementation error) | `label_avail` flag; a forecast is revealed to the update only if its outcome was observed; unobserved training labels dropped | Under gaps, POD fell by 0.01–0.03 and FAR by 0.03–0.05; the miss-rate target now fails at 40% gaps (Table 9) |
| 2 | Baselines used Daymet only; ACE-Flood used three forcings | Unfair comparison | All learned baselines use the same multi-forcing features | The same LightGBM scores CSI 0.452 with Daymet only and 0.560 with all forcings; ACE-Flood's lead shrank |
| 3 | No baseline isolated the decision layer | Missing control | Added B11 (CSI-tuned threshold on the same predictor) and B12 (decision layer on persistence) | B11 is within 0.011 CSI of ACE-Flood at h = 1 and better at h = 2 |
| 4 | Significance came from a single-seed, i.i.d. bootstrap | Statistical error | Paired block bootstrap (1/2/4-week blocks shared across basins), sign-flip permutation test, 5 seeds, Holm correction over 22 comparisons | The claim "significantly better than the strongest baselines" is withdrawn |
| 5 | Baseflow index used as a static feature | Leakage (computed from the full record, including the test year) | Removed | Not measured separately |
| 6 | The flood threshold (long-term Q95) overlaps the test year | Possible leakage in the event definition | Kept as the main definition and added a run with a training-years-only threshold | ACE-Flood loses its h = 1 lead with the alternative threshold (Table 10) |
| 7 | LSTM input windows misaligned with targets; LSTM untuned and single-forcing | Implementation error, unfair baseline | Windowing fixed; multi-forcing inputs; tuned (hidden 32, 80 epochs) | LSTM CSI is now 0.594 |
| 8 | Scarcity runs let the "new gauge" use flow history from before its record started | Leakage | `new_gauge` masking | Short-record results recomputed (Table 7) |
| 9 | Calibration scores came from fold models, but the test score came from a full refit | Code did not match the method | Test score = mean of the fold models; the old behaviour is kept as ablation A4 | CSI 0.628 (A4) vs 0.631 |
| 10 | Literal CRC with too few events (λ = −∞, warn every day) was not reported | Hidden failure | Reported (A2, C0/C1); fallbacks evaluated (C2–C5) | Always-warn behaviour at n = 1 is documented |
| 11 | The miss rate was described as "guaranteed" | Overclaim | Stated as a conditional finite-sample result (Prop. 1) and a long-run bound that is vacuous here (Prop. 2); empirical in this study | Wording changed throughout |
| 12 | Hard-coded paths, no pinned environment, hardware not recorded | Reproducibility | `config.json`, `CAMELS_ROOT`, `get_data.sh`, `requirements.txt`, `results/environment.json` | – |
| 13 | Hyperparameters chosen informally | Reproducibility | Grid search on out-of-fold training data only (`tune.py`) | Edge-of-grid values reported as a limitation |
| 14 | One reference with unverifiable pages (Fekete 2015); one wrong title (Newman) | Citation error | Replaced by Ruhi et al. 2018; title corrected; all references checked | – |
| 15 | The data-age feature was claimed to help under gaps | Unsupported claim | Ablated | Effect ≤ 0.005 CSI; claim withdrawn |
| 16 | Figures 4 and 6 had overlapping labels or legends | Presentation | Label offsets and a shared legend | – |

# Revision 3 (11 November 2026): input time alignment

| # | Issue | Type | Fix | Effect on results |
| --- | --- | --- | --- | --- |
| 17 | Maurer "day t" precipitation accumulates until ~04:00–08:00 local time on day t + 1 (checked against hourly NLDAS precipitation; `window_check.py`), i.e. after the issue time | Information leak (input timing) | `data.py`: `forcing_lag_days` in `config.json`, Maurer lagged 1 day; every experiment rerun, hyperparameters re-tuned | ACE-Flood h = 1 CSI 0.631 → 0.451; now significantly below B11 (Holm p = 0.024) and, at h = 2, below persistence (Holm p = 0.007); multi-forcing benefit largely disappears; miss target fails from 10% missing readings |
| 18 | Reproducibility check | Environment | Corrected pipeline run on a Linux machine (without PyTorch; B10 skipped) and on the authors' Windows laptop (all models incl. B10) | All non-LSTM results identical on both machines; the authors' run supplies B10 (re-tuned: 16 hidden units, 20 epochs; h = 1 CSI 0.482) |

Revision-2 results (misaligned Maurer input) are kept in `results_original/` for comparison only (Table 12 of the paper).
