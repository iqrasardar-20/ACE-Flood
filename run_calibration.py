"""Calibration strategies under extreme event scarcity (h = 1). New-gauge setting: discharge before the
training start does not exist. Outputs results/calibration_scarcity.csv, results/partially_gauged.csv"""
import time, numpy as np, pandas as pd
from pipeline import *
from methods import decide
t0 = time.time(); A = CFG["ace"]; R, P = [], []


def strategies(out, cal, h=1):
    """All decision rules on the SAME scores. Returns {name: warnings}."""
    res = {}
    res["C0 CRC static (literal: always-warn if n too small)"] = apply_decision(out, cal, h, "static")[0]
    res["C1 CRC + ACI (literal) = ACE-Flood"] = apply_decision(out, cal, h, "aci")[0]
    res["C2 CRC + ACI, min-event fallback to native y>1"] = apply_decision(out, cal, h, "aci", fallback="native")[0]
    res["C3 Expanding-window recalibration"] = apply_decision(out, cal, h, "expanding")[0]
    res["C4 Rolling-window recalibration (40 events)"] = apply_decision(out, cal, h, "rolling")[0]
    res["C5 ACI from native threshold, no calibration"] = decide(out.date.values, out.basin.values, out.score.values, out.event.values,
                                                                 out.label_avail.values, h, "aci", A["alpha"], A["eta"], lam0=1.0)[0]
    res["Native threshold y>1 (no calibration)"] = out.score.values > 1
    return res


for months in (3, 6, 12, 23):
    start = max((pd.Timestamp("2002-01-01") - pd.DateOffset(months=months)).strftime("%Y-%m-%d"), TRAIN_START)
    tr, te, full = prepare(1, train_start=start, new_gauge=True)
    for seed in CFG["scarcity_seeds"]:
        out, cal = ace_scores(tr, te, seed, kind="concat", calib="oof", test_score="foldmean")
        for name, w in strategies(out, cal).items():
            R.append(dict(months=months, seed=seed, strategy=name, n_cal_events=len(cal["pos"]), n_train=len(tr),
                          **warn_metrics(out.event.values, w, out.onset.values)))
        o = bl_lgb_concat_tuned_threshold(tr, te, seed)
        R.append(dict(months=months, seed=seed, strategy="B11 B8 + CSI-tuned threshold", n_cal_events=len(cal["pos"]), n_train=len(tr),
                      **warn_metrics(o.event.values, o.warn.values, o.onset.values)))
        o = bl_lstm(tr, te, seed, full)
        R.append(dict(months=months, seed=seed, strategy="B10 Regional LSTM", n_cal_events=len(cal["pos"]), n_train=len(tr),
                      **warn_metrics(o.event.values, o.warn.values, o.onset.values)))
        # local (per-basin) calibration for comparison
        parts = []
        for b in BASINS:
            ob, cb = ace_scores(tr[tr.basin == b].reset_index(drop=True), te[te.basin == b].reset_index(drop=True), seed,
                                kind="concat", calib="oof", test_score="foldmean")
            ob["warn"] = apply_decision(ob, cb, 1, "aci")[0]; parts.append(ob)
        ol = pd.concat(parts)
        R.append(dict(months=months, seed=seed, strategy="C1 local per-basin calibration", n_cal_events=np.nan, n_train=len(tr),
                      **warn_metrics(ol.event.values, ol.warn.values, ol.onset.values)))
    print("months", months, f"{time.time()-t0:.0f}s", flush=True)
pd.DataFrame(R).to_csv("results/calibration_scarcity.csv", index=False)

for target in BASINS:
    bts = {b: TRAIN_START for b in BASINS}; bts[target] = "2001-10-01"
    tr, te, full = prepare(1, basin_train_start=bts, new_gauge=True)
    for seed in CFG["scarcity_seeds"]:
        out, cal = ace_scores(tr, te, seed, kind="concat", calib="oof", test_score="foldmean")
        k = out.basin.values == target
        for name, w in strategies(out, cal).items():
            if name.startswith(("C1", "C3", "Native")):
                P.append(dict(target=target, seed=seed, setting="pooled with donors", strategy=name, **warn_metrics(out.event.values[k], w[k], out.onset.values[k])))
        tb = tr[tr.basin == target].reset_index(drop=True); eb = te[te.basin == target].reset_index(drop=True)
        ob, cb = ace_scores(tb, eb, seed, kind="concat", calib="oof", test_score="foldmean")
        for name, w in strategies(ob, cb).items():
            if name.startswith(("C1", "C2", "C3")):
                P.append(dict(target=target, seed=seed, setting="local 3 months only", strategy=name, n_cal_events=len(cb["pos"]),
                              **warn_metrics(ob.event.values, w, ob.onset.values)))
    print("target", target, f"{time.time()-t0:.0f}s", flush=True)
pd.DataFrame(P).to_csv("results/partially_gauged.csv", index=False)
print("TOTAL", time.time() - t0)
