"""Paired statistical comparison of ACE-Flood vs every baseline (all leads), from predictions_main.csv.gz.
Unit of resampling: blocks of 1, 2 or 4 consecutive ISO weeks shared by all four basins (keeps temporal and
cross-basin dependence). Statistic: mean over the 5 seeds of metric(ACE) - metric(baseline), metrics from pooled
counts. Two-sided paired sign-flip permutation test on the same blocks; Holm correction across baselines
within each lead and metric. Output: results/stats_paired.csv, results/stats_basin_signs.csv"""
import numpy as np, pandas as pd
from methods import paired_block_stats, holm, warn_metrics
from data import CFG
P = pd.read_csv("results/predictions_main.csv.gz", parse_dates=["date"], dtype={"basin": str})
P["basin"] = P.basin.str.zfill(8)
ACE = "ACE-Flood"; seeds = CFG["seeds"]; B = CFG["bootstrap"]
rows, signs = [], []
for h in sorted(P.h.unique()):
    Ph = P[P.h == h]
    key = Ph[(Ph.model == ACE) & (Ph.seed == 0)].sort_values(["basin", "date"])[["basin", "date"]]
    week = key.date.dt.isocalendar().week.values.astype(int)
    week = np.where((key.date.dt.month == 12).values & (week == 1), 53, week)
    def mat(model):
        m = Ph[Ph.model == model]
        out = []
        for s in seeds:
            ms = m[m.seed == s] if (m.seed == s).any() else m[m.seed == m.seed.min()]
            ms = key.merge(ms, on=["basin", "date"], how="left")
            out.append(ms.warn.values.astype(bool))
        ev = key.merge(m[m.seed == m.seed.min()], on=["basin", "date"]).event.values.astype(bool)
        return np.array(out), np.tile(ev, (len(seeds), 1))
    wa, ev = mat(ACE)
    for model in sorted(set(Ph.model) - {ACE}):
        wb, _ = mat(model)
        for metric in ("CSI", "POD", "FAR", "F1"):
            for L in B["block_weeks"]:
                r = paired_block_stats(ev, wa, wb, week, B["n_boot"], B["n_perm"], L, B["seed"], metric)
                rows.append(dict(h=h, baseline=model, metric=metric, block_weeks=L, **r))
        # per-basin sign of the CSI difference (seed-mean); 4 basins -> descriptive only
        for b in sorted(key.basin.unique()):
            k = key.basin.values == b
            da = np.mean([warn_metrics(ev[s][k], wa[s][k], np.zeros(k.sum()))["CSI"] for s in range(len(seeds))])
            db = np.mean([warn_metrics(ev[s][k], wb[s][k], np.zeros(k.sum()))["CSI"] for s in range(len(seeds))])
            signs.append(dict(h=h, baseline=model, basin=b, CSI_ACE=da, CSI_base=db, diff=da - db))
    print("h", h, "done", flush=True)
R = pd.DataFrame(rows)
R["p_holm"] = np.nan
for (h, metric, L), g in R.groupby(["h", "metric", "block_weeks"]):
    R.loc[g.index, "p_holm"] = holm(g.p_perm.values)
R.to_csv("results/stats_paired.csv", index=False); pd.DataFrame(signs).to_csv("results/stats_basin_signs.csv", index=False)
print(R[(R.metric == "CSI") & (R.block_weeks == 2)].round(4).to_string())
