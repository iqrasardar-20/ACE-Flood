"""Audit diagnostic: (0) reproduce published ACE-Flood, ACE static, B8, B11 numbers; (1) Maurer lagged 1 day;
(2) all three forcing products lagged 1 day; (3) Maurer removed. LightGBM models only; leads 1-3; seeds 0-4."""
import sys, os, time, numpy as np, pandas as pd
SRC = sys.argv[1]; OUT = sys.argv[2]; variants = sys.argv[3].split(",")
sys.path.insert(0, SRC); os.chdir(SRC)
import types, sklearn, scipy.stats, lightgbm
_t = types.ModuleType("torch"); _t.Tensor = type("Tensor", (), {}); _t.nn = types.ModuleType("torch.nn"); _t.nn.Module = object
sys.modules["torch"] = _t   # audit stub: torch unavailable; only the LSTM baseline needs it and it is not run here
import pipeline as P
from methods import warn_metrics
ORIG = {b: {p: f.copy() for p, f in P._D[b]["forcing"].items()} for b in P.BASINS}
def lag(f): return f.shift(1).bfill()
rows = []; t0 = time.time()
for var in variants:
    prods = ("daymet","maurer","nldas")
    for b in P.BASINS:
        F = {p: ORIG[b][p].copy() for p in ORIG[b]}
        if var == "maurer_lag1": F["maurer"] = lag(F["maurer"])
        if var == "all_lag1": F = {p: lag(f) for p, f in F.items()}
        P._D[b]["forcing"] = F
    if var == "no_maurer":
        prods = ("daymet","nldas")
    P.PRODS = prods
    for h in (1,2,3):
        # build frames with chosen products
        thr = P.thresholds("lt95")
        tr, te, full = P.prepare(h)
        if var == "no_maurer":
            drop = [c for c in tr.columns if c.startswith("maurer_") or c.startswith("SPREAD_")]
            tr, te = tr.drop(columns=drop), te.drop(columns=drop)
        for seed in range(5):
            out, cal = P.ace_scores(tr, te, seed, kind="concat", calib="oof", test_score="foldmean")
            for strat, nm in (("aci","ACE-Flood"),("static","ACE-Flood [static]")):
                w, _ = P.apply_decision(out, cal, h, strat)
                rows.append(dict(variant=var, model=nm, h=h, seed=seed, **warn_metrics(out.event.values, w, out.onset.values)))
            for nm, f in (("B8 LightGBM multi-forcing", P.bl_lgb_concat), ("B11 B8 + CSI-tuned threshold", P.bl_lgb_concat_tuned_threshold)):
                o = f(tr, te, seed)
                rows.append(dict(variant=var, model=nm, h=h, seed=seed, **warn_metrics(o.event.values, o.warn.values, o.onset.values)))
            pd.DataFrame(rows).to_csv(OUT, index=False)
        print(var, h, f"{time.time()-t0:.0f}s", flush=True)
print("DONE")
