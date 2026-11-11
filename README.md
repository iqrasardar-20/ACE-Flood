# ACE-Flood — code and results (revision 3)

Code and every result file for the paper
**"Adaptive Machine Learning for Early Flood Warning Under Data Scarcity and Uncertainty"**
by Abdul Haseeb Shaikh, Iqra Sardar and Iqra Gul (Aror University of Art, Architecture, Design and Heritage, Sukkur, Pakistan).

Every number in Section 13 of the paper is produced by the scripts below and stored in `results/`.

## What changed in revision 3

The daily Maurer precipitation in CAMELS accumulates until about 04:00–08:00 local time on the *following* day, i.e. after a
forecast issued at the end of day t (checked with `window_check.py`). All experiments now use Maurer lagged by one day
(`forcing_lag_days` in `config.json`). This lowers ACE-Flood's 1-day CSI from 0.631 to 0.451. See `CORRECTION_REPORT.md`.
The earlier (misaligned) results are kept in `results_original/` only for comparison (Table 12 of the paper).

## 1. Environment

Python 3.13, CPU only. Versions are pinned in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

The revision-3 results were produced on Windows 10 (Python 3.13.17). All results not involving the LSTM were also
reproduced exactly on Linux (Python 3.13.18).

## 2. Data

The experiments use the 4-basin CAMELS-US subset (basins 01022500, 01547700, 02064000, 03015500; 2000–2002;
Daymet, Maurer-extended and NLDAS forcings; CAMELS attributes v2.0; hourly streamflow) distributed with the
NeuralHydrology library (`test/test_data/camels_us`). The data are **not** included here; download them with

```bash
./get_data.sh            # sparse-clones that folder into data/camels_us
```

or point to an existing copy: `export CAMELS_ROOT=/path/to/camels_us`.
CAMELS and the extended Maurer forcing have their own terms of use; please consult them.

## 3. Run order

| Step | Script | Output (in `results/`) |
| --- | --- | --- |
| 1 | `tune.py` | `tuned_params.json`, `tuning_*.csv` |
| 2 | `select_score.py` | `score_selection_oof.csv` |
| 3 | `run_main.py` | `main_runs.csv`, `main_basin_runs.csv`, `predictions_main.csv.gz`, `validity_alpha_eta.csv`, `intervals.csv`, `prop2_bound.csv`, `pred_ACE_h*_seed0.csv` |
| 4 | `run_calibration.py` | `calibration_scarcity.csv`, `partially_gauged.csv` |
| 5 | `run_missing.py` | `missing_runs.csv` |
| 6 | `run_threshold.py` | `threshold_sensitivity.csv`, `thresholds.csv` |
| 7 | `stats.py` | `stats_paired.csv`, `stats_basin_signs.csv` |
| 8 | `make_tables.py` | `tables.md` |
| 9 | `figures.py` | `figs/fig1–fig9.png` |

On Windows, run steps 8–9 as `python -X utf8 make_tables.py` (the tables contain non-ASCII symbols).
Main experiment run time: about 16 minutes on a laptop CPU.

Input-timing checks (Section 10.3 and 13.8 of the paper):
`python window_check.py .` locates each forcing product's daily accumulation window;
`python diag_timing.py . out.csv original,maurer_lag1,all_lag1,no_maurer` reruns the LightGBM models under alternative alignments.

## 4. Code map

| File | Contents |
| --- | --- |
| `data.py` | Reading CAMELS files; cfs → mm/day; forcing time alignment; natural daily gap mask from hourly data |
| `features.py` | Lagged flow, rainfall sums, API, snow model, season, static attributes; `label_avail` flag |
| `pipeline.py` | Data preparation, folds, predictors, cross-fitting, ACE-Flood and baselines B1–B12 |
| `methods.py` | CRC threshold, observation-gated online update (`decide`), CQR/ACI intervals, metrics, paired block tests, Holm correction |
