"""Generate every results table of the paper (markdown) directly from results/*.csv -> results/tables.md"""
import numpy as np, pandas as pd
out = []
f = lambda v, d=3: "–" if pd.isna(v) else f"{v:.{d}f}"
pm = lambda m, s, d=3: "–" if pd.isna(m) else (f"{m:.{d}f}" if (pd.isna(s) or s == 0) else f"{m:.{d}f} ± {s:.{d}f}")
r = pd.read_csv("results/main_runs.csv")
order1 = None
def main_table(h, title):
    g = r[r.h == h].groupby("model"); m, s = g.mean(numeric_only=True), g.std(numeric_only=True)
    idx = m.CSI.sort_values(ascending=False).index
    rows = [f"**{title}**", "", "| Model | POD | FAR | CSI | F1 | Onset POD | Warnings | NSE (pooled) | NSE (median basin) | KGE | RMSE (mm/d) |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k in idx:
        nm = f"**{k}**" if k == "ACE-Flood" else k
        rows.append(f"| {nm} | {pm(m.loc[k,'POD'], s.loc[k,'POD'])} | {pm(m.loc[k,'FAR'], s.loc[k,'FAR'])} | {pm(m.loc[k,'CSI'], s.loc[k,'CSI'])} | {pm(m.loc[k,'F1'], s.loc[k,'F1'])} | {pm(m.loc[k,'OnsetPOD'], s.loc[k,'OnsetPOD'])} | {m.loc[k,'Warnings']:.1f} | {f(m.loc[k,'NSE'])} | {f(m.loc[k,'NSE_median_basin'])} | {f(m.loc[k,'KGE'])} | {f(m.loc[k,'RMSE'])} |")
    return "\n".join(rows)
out.append(main_table(1, "Table 3 — Test 2002, h = 1 d, pooled over 4 basins (63 flood-days, 22 onsets, 1,456 forecasts). Mean ± sd over 5 seeds; deterministic models show no sd; sorted by CSI."))
# Table 4: h = 2, 3 compact
keep = ["ACE-Flood", "ACE-Flood [static, eta=0]", "A7 ACE expanding-window recalibration", "B1 Persistence", "B12 Persistence + CRC/ACI decision layer",
        "B8 LightGBM multi-forcing", "B11 B8 + CSI-tuned threshold", "B9 Quantile LightGBM q0.9", "B10 Regional LSTM", "B4 Logistic regression", "B3 Ridge regression"]
rows = ["**Table 4 — Leads h = 2 and 3 d (mean of 5 seeds). CSI / POD / FAR; '–' = no warnings issued.**", "", "| Model | h = 2: CSI | POD | FAR | Warnings | h = 3: CSI | POD | FAR | Warnings |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for k in keep:
    c = []
    for h in (2, 3):
        x = r[(r.h == h) & (r.model == k)].mean(numeric_only=True)
        c += [f(x.CSI), f(x.POD), f(x.FAR), f"{x.Warnings:.1f}"]
    rows.append(f"| {k} | " + " | ".join(c) + " |")
out.append("\n".join(rows))
# Table 5: paired stats
s = pd.read_csv("results/stats_paired.csv")
keyb = ["B11 B8 + CSI-tuned threshold", "B9 Quantile LightGBM q0.9", "B10 Regional LSTM", "B8 LightGBM multi-forcing", "B3 Ridge regression", "B1 Persistence",
        "B12 Persistence + CRC/ACI decision layer", "B4 Logistic regression", "ACE-Flood [static, eta=0]", "A2 ACE split calibration"]
rows = ["**Table 5 — Paired comparison, Δ = ACE-Flood − baseline (mean over 5 seeds). 95% block-bootstrap CI with 2-week blocks; p = two-sided paired block sign-flip permutation p (raw / Holm-adjusted over 22 comparisons); p for 1- and 4-week blocks in parentheses (raw).**", "",
        "| h | Baseline | ΔCSI [95% CI] | p raw / Holm (L=1, L=4) | ΔPOD [95% CI] | ΔFAR [95% CI] |", "| --- | --- | --- | --- | --- | --- |"]
for h in (1, 2, 3):
    for b in keyb:
        def g(metric, L=2):
            return s[(s.h == h) & (s.baseline == b) & (s.metric == metric) & (s.block_weeks == L)].iloc[0]
        c, p, fa = g("CSI"), g("POD"), g("FAR")
        rows.append(f"| {h} | {b} | {c['diff']:+.3f} [{c.lo:+.3f}, {c.hi:+.3f}] | {c.p_perm:.3f} / {c.p_holm:.3f} ({g('CSI',1).p_perm:.3f}, {g('CSI',4).p_perm:.3f}) | {p['diff']:+.3f} [{p.lo:+.3f}, {p.hi:+.3f}] | {fa['diff']:+.3f} [{fa.lo:+.3f}, {fa.hi:+.3f}] |")
out.append("\n".join(rows))
# Table 6: decision-layer ablations at h=1
abl = ["ACE-Flood", "ACE-Flood [static, eta=0]", "A9 ACE empirical quantile (no CRC correction)", "B11 B8 + CSI-tuned threshold", "B8 LightGBM multi-forcing",
       "A4 ACE full-refit test score (v1)", "A3 ACE causal (forward-chaining) calibration", "A2 ACE split calibration", "A7 ACE expanding-window recalibration",
       "A8 ACE rolling-window recalibration", "A5 ACE Daymet-only predictor", "A6 ACE forcing-ensemble spread score"]
rows = ["**Table 6 — What the decision layer contributes (h = 1, mean of 5 seeds; λ₀ / τ = threshold in y units).**", "", "| Configuration | Threshold rule | λ₀ or τ | POD | FAR | CSI | Warnings |", "| --- | --- | --- | --- | --- | --- | --- |"]
rule = {"ACE-Flood": "CRC λ₀ + online update", "ACE-Flood [static, eta=0]": "CRC λ₀, fixed", "A9 ACE empirical quantile (no CRC correction)": "empirical 20% quantile of event scores",
        "B11 B8 + CSI-tuned threshold": "CSI-maximising τ on the same folds", "B8 LightGBM multi-forcing": "fixed y > 1", "A4 ACE full-refit test score (v1)": "CRC + update, test score from full refit",
        "A3 ACE causal (forward-chaining) calibration": "CRC + update, past-only folds", "A2 ACE split calibration": "CRC + update, held-out last 25%", "A7 ACE expanding-window recalibration": "CRC recomputed on all revealed events",
        "A8 ACE rolling-window recalibration": "CRC on last 40 events", "A5 ACE Daymet-only predictor": "as ACE, single forcing", "A6 ACE forcing-ensemble spread score": "as ACE, score + spread"}
for k in abl:
    x = r[(r.h == 1) & (r.model == k)].mean(numeric_only=True)
    th = x.get("lam0", np.nan) if not pd.isna(x.get("lam0", np.nan)) else x.get("tau", np.nan)
    th = "1 (fixed)" if k.startswith("B8") else ("−∞" if np.isneginf(th) else ("–" if pd.isna(th) else f"{th:.3f}"))
    rows.append(f"| {k} | {rule[k]} | {th} | {f(x.POD)} | {f(x.FAR)} | {f(x.CSI)} | {x.Warnings:.1f} |")
out.append("\n".join(rows))
# Table 7: calibration strategies under scarcity
c = pd.read_csv("results/calibration_scarcity.csv")
strat = ["C1 CRC + ACI (literal) = ACE-Flood", "C0 CRC static (literal: always-warn if n too small)", "C2 CRC + ACI, min-event fallback to native y>1", "C3 Expanding-window recalibration",
         "C4 Rolling-window recalibration (40 events)", "C5 ACI from native threshold, no calibration", "Native threshold y>1 (no calibration)", "C1 local per-basin calibration",
         "B11 B8 + CSI-tuned threshold", "B10 Regional LSTM"]
rows = ["**Table 7 — Calibration strategies vs training-record length, new-gauge setting (h = 1, mean of 3 seeds). Cells: CSI / POD / FAR; n = calibration flood-days.**", "",
        "| Strategy | 3 months (n = 1) | 6 months (n = 1) | 12 months (n = 18) | 23 months (n = 50) |", "| --- | --- | --- | --- | --- |"]
for k in strat:
    cells = []
    for mo in (3, 6, 12, 23):
        x = c[(c.strategy == k) & (c.months == mo)].mean(numeric_only=True)
        cells.append(f"{f(x.CSI)} / {f(x.POD)} / {f(x.FAR)}")
    rows.append(f"| {k} | " + " | ".join(cells) + " |")
chk = c.groupby("months").n_cal_events.mean().to_dict()
out.append("\n".join(rows) + f"\n\n(check: calibration events by record length = {chk})")
# Table 8: partially gauged
p = pd.read_csv("results/partially_gauged.csv"); p["target"] = p.target.astype(str).str.zfill(8)
g = p.groupby(["setting", "strategy"])[["POD", "FAR", "CSI", "Warnings"]].mean()
rows = ["**Table 8 — Partially gauged target: the target basin has only Oct–Dec 2001; donors have 23 months (h = 1; mean over 4 targets × 3 seeds).**", "", "| Setting | Strategy | POD | FAR | CSI | Warnings (target basin) |", "| --- | --- | --- | --- | --- | --- |"]
for (st, sg), x in g.iterrows():
    rows.append(f"| {st} | {sg} | {f(x.POD)} | {f(x.FAR)} | {f(x.CSI)} | {x.Warnings:.1f} |")
out.append("\n".join(rows))
# Table 10: threshold sensitivity
t = pd.read_csv("results/threshold_sensitivity.csv"); th = pd.read_csv("results/thresholds.csv")
rows = ["**Table 10 — Flood threshold from training years only (Q95 of 2000–2001). Mean of 5 seeds; CSI / POD / FAR.**", "",
        "| Model | h = 1 | h = 2 | h = 3 |", "| --- | --- | --- | --- |"]
for k in ["ACE-Flood", "ACE-Flood [static]", "B8 LightGBM multi-forcing", "B11 B8 + CSI-tuned threshold", "B1 Persistence", "B12 Persistence + CRC/ACI"]:
    cells = []
    for h in (1, 2, 3):
        x = t[(t.model == k) & (t.h == h)].mean(numeric_only=True); cells.append(f"{f(x.CSI)} / {f(x.POD)} / {f(x.FAR)}")
    rows.append(f"| {k} | " + " | ".join(cells) + " |")
ev = t.groupby("h")[["n_train_events", "n_test_events"]].mean().to_dict("index")
thr_txt = "; ".join(f"{str(b).zfill(8)}: {a:.2f} → {c_:.2f}" for b, a, c_ in zip(th.basin.astype(int).astype(str).str.zfill(8), th.Q95_LT_1989_2009, th.Q95_train_2000_2001))
out.append("\n".join(rows) + f"\n\nThresholds (mm/d, long-term → training-years): {thr_txt}. Events (train / test) by lead: {ev}.")
# Table 11: intervals
i = pd.read_csv("results/intervals.csv"); gi = i.groupby(["h", "method"])[["PICP", "MPIW", "IS"]].mean()
rows = ["**Table 11 — Nominal 90% intervals on y (mean of 5 seeds).**", "", "| Lead | Raw quantile LightGBM: PICP / MPIW / IS | + CQR: PICP / MPIW / IS | + CQR + ACI: PICP / MPIW / IS |", "| --- | --- | --- | --- |"]
for h in (1, 2, 3):
    rows.append(f"| h = {h} | " + " | ".join(f"{gi.loc[(h,m),'PICP']:.3f} / {gi.loc[(h,m),'MPIW']:.3f} / {gi.loc[(h,m),'IS']:.3f}" for m in ("qr", "cqr", "aci")) + " |")
out.append("\n".join(rows))
# Table 12: Prop 2 bound
pb = pd.read_csv("results/prop2_bound.csv"); pb = pb[(pb.alpha == 0.2) & (pb.eta == 0.05)]; pb["basin"] = pb.basin.astype(str).str.zfill(8)
gb = pb.groupby(["h", "basin"])[["K", "s_min", "s_max", "bound", "miss", "abs_dev"]].mean()
rows = ["**Table 12 — Proposition 2 bound vs realised deviation (α = 0.2, η = 0.05, mean of 5 seeds). The bound is vacuous whenever it exceeds 1.**", "", "| h | Basin | K (flood-days) | s_min | s_max | Bound on \\|miss − α\\| | Realised miss rate | Realised \\|miss − α\\| |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for (h, b), x in gb.iterrows():
    rows.append(f"| {h} | {b} | {x.K:.0f} | {x.s_min:.3f} | {x.s_max:.3f} | {x.bound:.2f} | {x.miss:.3f} | {x.abs_dev:.3f} |")
out.append("\n".join(rows))
# validity summary
v = pd.read_csv("results/validity_alpha_eta.csv"); vv = v.groupby(["h", "alpha", "eta"]).MissRate.mean().reset_index()
sub = vv[vv.eta.isin([0.0, 0.05])]; ex = sub[sub.MissRate > sub.alpha + 1e-9]
out.append("VALIDITY: combos=%d exceed=%d max_excess=%.3f; all-eta max_excess=%.3f\n%s" % (len(sub), len(ex), (ex.MissRate - ex.alpha).max() if len(ex) else 0, (vv.MissRate - vv.alpha).max(), ex.round(3).to_string()))
open("results/tables.md", "w").write("\n\n".join(out)); print("\n\n".join(out))
# Table 9: missing data
mm = pd.read_csv("results/missing_runs.csv")
models = ["ACE-Flood", "ACE-Flood (v1 bug: uses unobserved labels)", "ACE-Flood [static]", "A7 ACE expanding-window", "ACE-Flood w/o data-age feature",
          "B11 B8 + CSI-tuned threshold", "B8 LightGBM multi-forcing", "B1 Persistence (last valid reading)"]
cols = [("MCAR", 0.0), ("MCAR", 0.1), ("MCAR", 0.2), ("MCAR", 0.4), ("natural", None)]
hdr = ["0% (simulated)", "10% (simulated)", "20% (simulated)", "40% (simulated)", "natural gaps (9.4%)"]
rows = ["**Table 9 — Missing gauge readings (h = 1, mean of 3 mask seeds). Cells: CSI / POD / FAR.**", "", "| Model | " + " | ".join(hdr) + " |", "| --- | " + " | ".join(["---"] * len(hdr)) + " |"]
for k in models:
    cells = []
    for sc, rt in cols:
        x = mm[(mm.model == k) & (mm.scenario == sc)]
        if rt is not None: x = x[np.isclose(x.rate, rt)]
        x = x.mean(numeric_only=True); cells.append(f"{f(x.CSI)} / {f(x.POD)} / {f(x.FAR)}")
    rows.append(f"| {k} | " + " | ".join(cells) + " |")
info = mm[mm.model == "ACE-Flood"].groupby(["scenario", "rate"])[["realised_missing", "test_labels_unobserved", "n_cal_events"]].mean().round(3)
open("results/tables.md", "a").write("\n\n" + "\n".join(rows) + "\n\n" + info.to_string())
print("\n".join(rows)); print(info)
