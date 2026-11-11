"""Main experiment (v2): all models, leads 1-3, seeds 0-4, test year 2002.
Outputs: results/main_runs.csv, main_basin_runs.csv, predictions_main.csv.gz, validity_alpha_eta.csv,
intervals.csv, prop2_bound.csv"""
import time, numpy as np, pandas as pd
from pipeline import *
SEEDS = CFG["seeds"]; t0 = time.time()
R, B, P, V, I, PB = [], [], [], [], [], []


def record(name, h, seed, o, wcol="warn", extra=None):
    w = o[wcol].values.astype(bool)
    r = dict(model=name, h=h, seed=seed, **warn_metrics(o.event.values, w, o.onset.values))
    if o.pred.notna().all():
        q_o, q_s = o.target.values * o.thr.values, o.pred.values * o.thr.values
        r.update(reg_metrics(q_o, q_s))
        r["NSE_median_basin"] = float(np.median([nse(q_o[o.basin.values == b], q_s[o.basin.values == b]) for b in BASINS]))
    if extra: r.update(extra)
    R.append(r)
    for b in BASINS:
        k = o.basin.values == b
        rb = dict(model=name, h=h, seed=seed, basin=b, **warn_metrics(o.event.values[k], w[k], o.onset.values[k]))
        if o.pred.notna().all():
            rb.update(reg_metrics(o.target.values[k] * o.thr.values[k], o.pred.values[k] * o.thr.values[k]))
        B.append(rb)
    P.append(pd.DataFrame(dict(model=name, h=h, seed=seed, date=o.date.values, basin=o.basin.values, warn=w.astype(np.int8),
                               score=o.score.values if "score" in o else np.nan, pred=o.pred.values, event=o.event.values, onset=o.onset.values)))


BL = [("B1 Persistence", bl_persistence), ("B2 Rainfall-threshold rule", bl_rain_rule), ("B3 Ridge regression", bl_ridge),
      ("B4 Logistic regression", bl_logreg), ("B5 Random forest", bl_rf), ("B6 LightGBM local", bl_lgb_local),
      ("B7 LightGBM Daymet only", bl_lgb_daymet), ("B8 LightGBM multi-forcing", bl_lgb_concat),
      ("B9 Quantile LightGBM q0.9", bl_qr90), ("B11 B8 + CSI-tuned threshold", bl_lgb_concat_tuned_threshold)]
DET = ("B1 Persistence", "B2 Rainfall-threshold rule", "B3 Ridge regression", "B4 Logistic regression")
for h in CFG["leads"]:
    tr, te, full = prepare(h)
    for seed in SEEDS:
        for name, f in BL:
            if seed > 0 and name in DET:
                continue
            o = f(tr, te, seed)
            record(name, h, seed, o, extra=dict(tau=o.attrs.get("tau", np.nan)))
        record("B10 Regional LSTM", h, seed, bl_lstm(tr, te, seed, full))
        # ---------------- ACE-Flood family
        variants = [("ACE-Flood", dict(kind="concat", calib="oof", test_score="foldmean")),
                    ("A4 ACE full-refit test score (v1)", dict(kind="concat", calib="oof", test_score="full")),
                    ("A2 ACE split calibration", dict(kind="concat", calib="split")),
                    ("A3 ACE causal (forward-chaining) calibration", dict(kind="concat", calib="causal", test_score="foldmean")),
                    ("A5 ACE Daymet-only predictor", dict(kind="daymet", calib="oof", test_score="foldmean")),
                    ("A6 ACE forcing-ensemble spread score", dict(kind="ensemble_spread", calib="oof", test_score="foldmean")),
                    ("B12 Persistence + CRC/ACI decision layer", dict(kind="persistence", calib="oof", test_score="foldmean"))]
        for tag, kw in variants:
            out, cal = ace_scores(tr, te, seed, **kw)
            ex = dict(n_cal_events=len(cal["pos"]))
            w, lam = apply_decision(out, cal, h, "aci"); out["warn"] = w
            record(tag, h, seed, out, extra=dict(ex, lam0=crc_fnr_threshold(cal["pos"], CFG["ace"]["alpha"])))
            if tag in ("ACE-Flood", "B12 Persistence + CRC/ACI decision layer"):
                w, _ = apply_decision(out, cal, h, "static"); out["warn"] = w
                record(tag + " [static, eta=0]", h, seed, out, extra=ex)
            if tag == "ACE-Flood":
                for strat, nm in [("expanding", "A7 ACE expanding-window recalibration"), ("rolling", "A8 ACE rolling-window recalibration"),
                                  ("empirical", "A9 ACE empirical quantile (no CRC correction)")]:
                    w, _ = apply_decision(out, cal, h, strat); out["warn"] = w; record(nm, h, seed, out, extra=ex)
                out = add_intervals(out, cal, h)
                for nm in ("qr", "cqr", "aci"):
                    I.append(dict(h=h, seed=seed, method=nm, **interval_metrics(out.target.values, out[f"L_{nm}"].values, out[f"U_{nm}"].values, CFG["ace"]["alpha_int"])))
                if seed == 0:
                    w, lam = apply_decision(out, cal, h, "aci"); out["warn"], out["lam"] = w, lam
                    out.to_csv(f"results/pred_ACE_h{h}_seed0.csv", index=False)
                for alpha in (0.05, 0.1, 0.2, 0.3, 0.4):
                    for eta in (0.0, 0.01, 0.05, 0.1):
                        w, lam = apply_decision(out, cal, h, "aci", alpha=alpha, eta=eta)
                        m = warn_metrics(out.event.values, w, out.onset.values)
                        V.append(dict(h=h, seed=seed, alpha=alpha, eta=eta, lam0=crc_fnr_threshold(cal["pos"], alpha), **m))
                        # Proposition 2 bound per basin (deterministic, any sequence)
                        if eta > 0:
                            for b in BASINS:
                                k = out.basin.values == b; K = int(out.event.values[k].sum())
                                s = out.score.values[k]; smin, smax = min(s.min(), np.min(cal["pos"])), max(s.max(), np.max(cal["pos"]))
                                bound = (smax - smin + 2 * (h + 1) * eta) / (eta * K) if K else np.nan
                                miss = 1 - w[k][out.event.values[k] == 1].mean() if K else np.nan
                                PB.append(dict(h=h, seed=seed, alpha=alpha, eta=eta, basin=b, K=K, s_min=smin, s_max=smax,
                                               bound=bound, miss=miss, abs_dev=abs(miss - alpha) if K else np.nan))
        print(f"h={h} seed={seed} {time.time()-t0:.0f}s", flush=True)
pd.DataFrame(R).to_csv("results/main_runs.csv", index=False)
pd.DataFrame(B).to_csv("results/main_basin_runs.csv", index=False)
pd.concat(P).to_csv("results/predictions_main.csv.gz", index=False)
pd.DataFrame(V).to_csv("results/validity_alpha_eta.csv", index=False)
pd.DataFrame(I).to_csv("results/intervals.csv", index=False)
pd.DataFrame(PB).to_csv("results/prop2_bound.csv", index=False)
print("TOTAL", time.time() - t0)
