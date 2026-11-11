"""Hyper-parameter selection using ONLY the 2000-2001 training record (h = 1). Writes results/tuned_params.json."""
import json, itertools, time, numpy as np, pandas as pd
from sklearn.metrics import average_precision_score
from pipeline import *
t0 = time.time()
tr, te, full = prepare(1)
c = concat_columns(tr); out = {}
# --- LightGBM grid (blocked OOF RMSE on y)
rows = []
for nl, ne in itertools.product([7, 15, 31], [200, 400, 800]):
    oof = np.full(len(tr), np.nan)
    for a, b in folds(tr):
        oof[b] = lgb_fit(tr.iloc[a][c], tr.target.iloc[a], 0, num_leaves=nl, n_estimators=ne).predict(tr.iloc[b][c])
    ok = ~np.isnan(oof); rows.append(dict(num_leaves=nl, n_estimators=ne, OOF_RMSE=np.sqrt(np.mean((oof[ok] - tr.target.values[ok]) ** 2))))
g = pd.DataFrame(rows); g.to_csv("results/tuning_lgb.csv", index=False)
best = g.OOF_RMSE.min(); cand = g[g.OOF_RMSE <= best * 1.005].sort_values(["num_leaves", "n_estimators"]).iloc[0]
out["lgb_num_leaves"], out["lgb_n_estimators"] = int(cand.num_leaves), int(cand.n_estimators)
print(g.round(4).to_string(), "\nselected", dict(cand))
# --- ridge alpha (OOF RMSE), logistic C and RF leaf (OOF average precision)
def oof_fit(make, X, y, proba):
    o = np.full(len(tr), np.nan)
    for a, b in folds(tr):
        m = make().fit(X.iloc[a], y.iloc[a]); o[b] = m.predict_proba(X.iloc[b])[:, 1] if proba else m.predict(X.iloc[b])
    return o
rr = []
for a_ in (0.1, 1, 10, 100):
    o = oof_fit(lambda: make_pipeline(StandardScaler(), Ridge(alpha=a_)), tr[c].fillna(0), tr.target, False); ok = ~np.isnan(o)
    rr.append(dict(model="ridge", param=a_, score=np.sqrt(np.mean((o[ok] - tr.target.values[ok]) ** 2)), criterion="OOF RMSE"))
for C in (0.01, 0.1, 1, 10):
    o = oof_fit(lambda: make_pipeline(StandardScaler(), LogisticRegression(C=C, class_weight="balanced", max_iter=5000)), tr[c].fillna(0), tr.event, True); ok = ~np.isnan(o)
    rr.append(dict(model="logreg", param=C, score=average_precision_score(tr.event.values[ok], o[ok]), criterion="OOF AP"))
for leaf in (1, 3, 10):
    o = oof_fit(lambda: RandomForestClassifier(n_estimators=300, min_samples_leaf=leaf, max_features="sqrt", class_weight="balanced_subsample", random_state=0, n_jobs=2), tr[c].fillna(-1), tr.event, True); ok = ~np.isnan(o)
    rr.append(dict(model="rf", param=leaf, score=average_precision_score(tr.event.values[ok], o[ok]), criterion="OOF AP"))
r = pd.DataFrame(rr); print(r)
out["ridge_alpha"] = float(r[r.model == "ridge"].sort_values("score").param.iloc[0])
out["logreg_C"] = float(r[r.model == "logreg"].sort_values("score", ascending=False).param.iloc[0])
out["rf_leaf"] = int(r[r.model == "rf"].sort_values("score", ascending=False).param.iloc[0])
# --- LSTM: temporal validation inside training years
fit_part, val_part = tr[tr.date <= "2001-06-30"], tr[tr.date >= "2001-07-01"]
lr_rows = []
for hid, ep in itertools.product([16, 32, 64], [20, 40, 80]):
    p = fit_predict_lstm(full, fit_part, val_part, 0, hid=hid, epochs=ep)
    lr_rows.append(dict(model="lstm", hidden=hid, epochs=ep, VAL_RMSE=np.sqrt(np.mean((p - val_part.target.values) ** 2))))
    print(lr_rows[-1], flush=True)
L = pd.DataFrame(lr_rows); best = L.sort_values("VAL_RMSE").iloc[0]
out["lstm_hidden"], out["lstm_epochs"] = int(best.hidden), int(best.epochs)
pd.concat([r, L]).to_csv("results/tuning_baselines.csv", index=False)
json.dump(out, open("results/tuned_params.json", "w"), indent=1); print(out, f"{time.time()-t0:.0f}s")
