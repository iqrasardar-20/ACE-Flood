"""Missing gauge data (h = 1). Simulated MCAR gaps (10/20/40%) and the NATURAL gap pattern of the hourly
USGS record. Missing readings are unavailable to features, to training labels, to calibration and to the
online update (label_avail). A 'v1 behaviour' row reproduces the old bug (updates used unobserved labels).
Output: results/missing_runs.csv"""
import time, numpy as np, pandas as pd
from pipeline import *
from data import natural_daily_mask
from pipeline import _D
t0 = time.time(); R = []


def mcar_mask(rate, seed, idx, mean_gap=5):
    rng = np.random.default_rng(seed); m = np.zeros(len(idx), bool)
    while m.mean() < rate:
        s = rng.integers(0, len(idx)); L = rng.geometric(1 / mean_gap); m[s:s + L] = True
    return pd.Series(m, index=idx)


scen = [("MCAR", r, ms) for r in (0.0, 0.1, 0.2, 0.4) for ms in CFG["mask_seeds"]] + [("natural", None, ms) for ms in CFG["mask_seeds"]]
nat = natural_daily_mask()
for kind, rate, ms in scen:
    if kind == "MCAR":
        masks = {b: mcar_mask(rate, 100 * ms + k, _D[b]["q"].index) for k, b in enumerate(BASINS)}
    else:
        masks = nat
    tr, te, full = prepare(1, q_mask=masks)
    real = float(np.mean([masks[b].loc[TRAIN_START:TEST_END].mean() for b in BASINS]))
    test_unobs = float(1 - te.label_avail.mean())
    ex = dict(scenario=kind, rate=rate if rate is not None else real, realised_missing=real, test_labels_unobserved=test_unobs, mask_seed=ms)
    out, cal = ace_scores(tr, te, ms, kind="concat", calib="oof", test_score="foldmean")
    ex["n_cal_events"] = len(cal["pos"])
    for strat, nm in [("aci", "ACE-Flood"), ("static", "ACE-Flood [static]"), ("expanding", "A7 ACE expanding-window")]:
        w, _ = apply_decision(out, cal, 1, strat)
        R.append(dict(model=nm, **ex, **warn_metrics(out.event.values, w, out.onset.values), **reg_metrics(out.target * out.thr, out.pred * out.thr)))
    bug = out.copy(); bug["label_avail"] = True        # v1 behaviour: updates from labels that were never observed
    w, _ = apply_decision(bug, cal, 1, "aci")
    R.append(dict(model="ACE-Flood (v1 bug: uses unobserved labels)", **ex, **warn_metrics(out.event.values, w, out.onset.values)))
    tr2, te2 = tr.drop(columns=["AGE"]), te.drop(columns=["AGE"])
    o2, c2 = ace_scores(tr2, te2, ms, kind="concat", calib="oof", test_score="foldmean")
    w, _ = apply_decision(o2, c2, 1, "aci")
    R.append(dict(model="ACE-Flood w/o data-age feature", **ex, **warn_metrics(o2.event.values, w, o2.onset.values)))
    for nm, f in [("B1 Persistence (last valid reading)", bl_persistence), ("B8 LightGBM multi-forcing", bl_lgb_concat),
                  ("B11 B8 + CSI-tuned threshold", bl_lgb_concat_tuned_threshold)]:
        o = f(tr, te, ms)
        r = dict(model=nm, **ex, **warn_metrics(o.event.values, o.warn.values, o.onset.values))
        if o.pred.notna().all(): r.update(reg_metrics(o.target * o.thr, o.pred * o.thr))
        R.append(r)
    print(kind, rate, ms, f"{time.time()-t0:.0f}s", flush=True)
pd.DataFrame(R).to_csv("results/missing_runs.csv", index=False)
print("TOTAL", time.time() - t0)
