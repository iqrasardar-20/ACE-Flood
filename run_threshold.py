"""Sensitivity to the flood-threshold definition: Q95 from the training years only (no test information)."""
import time, numpy as np, pandas as pd
from pipeline import *
t0 = time.time(); R = []
thr = thresholds("train95"); lt = thresholds("lt95")
pd.DataFrame([dict(basin=b, Q95_LT_1989_2009=lt[b], Q95_train_2000_2001=thr[b]) for b in BASINS]).to_csv("results/thresholds.csv", index=False)
for h in (1, 2, 3):
    tr, te, full = prepare(h, thr_mode="train95")
    for seed in CFG["seeds"]:
        base = dict(h=h, seed=seed, n_train_events=int(tr.event.sum()), n_test_events=int(te.event.sum()))
        out, cal = ace_scores(tr, te, seed, kind="concat", calib="oof", test_score="foldmean")
        for strat, nm in [("aci", "ACE-Flood"), ("static", "ACE-Flood [static]")]:
            w, _ = apply_decision(out, cal, h, strat); R.append(dict(model=nm, **base, **warn_metrics(out.event.values, w, out.onset.values)))
        op, cp = ace_scores(tr, te, seed, kind="persistence", calib="oof", test_score="foldmean")
        w, _ = apply_decision(op, cp, h, "aci"); R.append(dict(model="B12 Persistence + CRC/ACI", **base, **warn_metrics(op.event.values, w, op.onset.values)))
        for nm, f in [("B1 Persistence", bl_persistence), ("B8 LightGBM multi-forcing", bl_lgb_concat), ("B11 B8 + CSI-tuned threshold", bl_lgb_concat_tuned_threshold)]:
            o = f(tr, te, seed); R.append(dict(model=nm, **base, **warn_metrics(o.event.values, o.warn.values, o.onset.values)))
    print(h, f"{time.time()-t0:.0f}s", flush=True)
pd.DataFrame(R).to_csv("results/threshold_sensitivity.csv", index=False)
