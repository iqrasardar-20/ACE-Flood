"""Choose the ACE-Flood predictor using ONLY training-period out-of-fold average precision (no test data)."""
import numpy as np, pandas as pd
from sklearn.metrics import average_precision_score
from pipeline import *
rows = []
for h in (1, 2, 3):
    tr, te, full = prepare(h)
    for seed in (0, 1, 2):
        for kind, spread in [("concat", False), ("daymet", False), ("ensemble_spread", False), ("ensemble_spread", True), ("persistence", False)]:
            oof, _ = crossfit(kind, tr, te.iloc[:5], seed)
            ok = ~np.isnan(oof[:, 0]); s = oof[ok, 0] + (oof[ok, 1] if spread else 0)
            rows.append(dict(h=h, seed=seed, score=kind + ("+spread" if spread else ""), OOF_AP=average_precision_score(tr.event.values[ok], s)))
df = pd.DataFrame(rows); df.to_csv("results/score_selection_oof.csv", index=False)
print(df.groupby(["score", "h"]).OOF_AP.mean().unstack().round(3)); print(df.groupby("score").OOF_AP.mean().sort_values(ascending=False).round(4))
