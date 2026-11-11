"""Shared pipeline (v2): data preparation, predictors, cross-fitted calibration, ACE-Flood and baselines."""
import os, json, numpy as np, pandas as pd, torch
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from data import load_all, BASINS, CFG
from features import build_frame, member_columns, concat_columns
from methods import *
from methods import _csi_from

PRODS = ("daymet", "maurer", "nldas")
TRAIN_START, TRAIN_END = CFG["train_start"], CFG["train_end"]
TEST_START, TEST_END = CFG["test_start"], CFG["test_end"]
_D, _A = load_all()
HERE = os.path.dirname(os.path.abspath(__file__))
_TUNED = os.path.join(HERE, "results", "tuned_params.json")
TUNED = json.load(open(_TUNED)) if os.path.exists(_TUNED) else {}
import methods as _m
if "lgb_num_leaves" in TUNED:   # tuned on training data only (tune.py)
    _m.LGB_BASE.update(num_leaves=TUNED["lgb_num_leaves"], n_estimators=TUNED["lgb_n_estimators"])


def thresholds(mode="lt95"):
    """Flood threshold per basin (mm/day). 'lt95': CAMELS long-term Q95 (1989-2009, overlaps test year);
    'train95': Q95 of observed daily discharge in the training years 2000-2001 only (no test information)."""
    if mode == "lt95":
        return {b: _A.loc[b, "q95"] for b in BASINS}
    return {b: _D[b]["q"].loc["2000-01-01":TRAIN_END].quantile(0.95) for b in BASINS}


def prepare(h, q_mask=None, train_start=TRAIN_START, basin_train_start=None, thr_mode="lt95", new_gauge=False):
    """Returns (train, test, full) pooled frames.
    q_mask: dict basin -> bool Series (True = reading unavailable), applied to inputs and label availability.
    basin_train_start: per-basin override of the training start (scarcity runs).
    new_gauge: if True, gauge readings before each basin's training start are treated as non-existent."""
    thr = thresholds(thr_mode)
    frames = []
    for b in BASINS:
        idx = _D[b]["q"].index
        m = pd.Series(False, index=idx)
        if q_mask is not None and b in q_mask:
            m = m | q_mask[b].reindex(idx, fill_value=False)
        s = train_start if basin_train_start is None else basin_train_start.get(b, train_start)
        if new_gauge:
            m = m | (idx < pd.Timestamp(s))
        frames.append(build_frame(_D, _A, b, h, PRODS, m if m.any() else None, thr[b]))
    full = pd.concat(frames); full["date"] = full.index
    full["event"] = (full.target > 1).astype(int)
    tr_parts, te_parts = [], []
    for b in BASINS:
        x = full[full.basin == b]
        s = train_start if basin_train_start is None else basin_train_start.get(b, train_start)
        last_issue = pd.Timestamp(TRAIN_END) - pd.Timedelta(days=h)
        tr_parts.append(x[(x.date >= s) & (x.date <= last_issue)])
        te_parts.append(x[(x.date >= TEST_START) & (x.date <= pd.Timestamp(TEST_END) - pd.Timedelta(days=h))])
    tr, te = pd.concat(tr_parts), pd.concat(te_parts)
    tr = tr[tr.target.notna() & tr.label_avail]          # a label that was never observed cannot be trained on
    te = te.copy()
    te["prev_target"] = te.groupby("basin").target.shift(1)
    te["onset"] = ((te.target > 1) & (te.prev_target <= 1)).astype(int)
    return tr.reset_index(drop=True), te.reset_index(drop=True), full.reset_index(drop=True)


def folds(tr, n_blocks=None, embargo=None, causal=False):
    """Blocked temporal folds. causal=False: train on all other blocks (minus embargo);
    causal=True: forward chaining, train only on blocks strictly before the held-out block (first block skipped)."""
    n_blocks = n_blocks or CFG["crossfit"]["n_blocks"]; embargo = embargo or CFG["crossfit"]["embargo_days"]
    dates = np.sort(tr.date.unique())
    for k, blk in enumerate(np.array_split(dates, n_blocks)):
        lo, hi = blk[0], blk[-1]
        test_idx = np.where((tr.date >= lo) & (tr.date <= hi))[0]
        emb_lo, emb_hi = lo - np.timedelta64(embargo, "D"), hi + np.timedelta64(embargo, "D")
        if causal:
            train_idx = np.where(tr.date < emb_lo)[0]
        else:
            train_idx = np.where((tr.date < emb_lo) | (tr.date > emb_hi))[0]
        if len(train_idx) < 30 or tr.iloc[train_idx].target.nunique() < 3:
            continue
        yield train_idx, test_idx


# ------------------------------------------------------------------ predictors
def cols_for(kind, df):
    return concat_columns(df) if kind in ("concat", "concat_q") else member_columns(df, "daymet")


def predictor(kind, tr, te, seed):
    """(centre, spread, lo, hi) of y_{t+h}. 'concat' = selected ACE-Flood predictor."""
    if kind in ("concat", "daymet"):
        c = cols_for(kind, tr)
        m = lgb_fit(tr[c], tr.target, seed).predict(te[c])
        lo = lgb_fit(tr[c], tr.target, seed, objective="quantile", alpha=0.05).predict(te[c])
        hi = lgb_fit(tr[c], tr.target, seed, objective="quantile", alpha=0.95).predict(te[c])
        return m, np.zeros_like(m), np.minimum(lo, m), np.maximum(hi, m)
    if kind == "ensemble_spread":
        pts, los, his = [], [], []
        for p in PRODS:
            c = member_columns(tr, p)
            pts.append(lgb_fit(tr[c], tr.target, seed).predict(te[c]))
            los.append(lgb_fit(tr[c], tr.target, seed, objective="quantile", alpha=0.05).predict(te[c]))
            his.append(lgb_fit(tr[c], tr.target, seed, objective="quantile", alpha=0.95).predict(te[c]))
        m = np.mean(pts, 0)
        return m, np.std(pts, 0), np.minimum(np.mean(los, 0), m), np.maximum(np.mean(his, 0), m)
    if kind == "persistence":
        v = te.Y0.values.astype(float)
        return v, np.zeros_like(v), v, v
    raise ValueError(kind)


def crossfit(kind, tr, te, seed, causal=False):
    """Out-of-fold predictions for every calibratable training row and fold-averaged test predictions.
    Returns oof (N_tr x 4, NaN where a row has no out-of-fold prediction) and te_fold (N_te x 4)."""
    oof = np.full((len(tr), 4), np.nan); te_acc = []
    for a, b in folds(tr, causal=causal):
        oof[b] = np.column_stack(predictor(kind, tr.iloc[a], tr.iloc[b], seed))
        te_acc.append(np.column_stack(predictor(kind, tr.iloc[a], te, seed)))
    te_fold = np.mean(te_acc, 0) if te_acc else np.full((len(te), 4), np.nan)
    return oof, te_fold


def ace_scores(tr, te, seed, kind="concat", calib="oof", test_score="full", use_spread=None):
    """Stage 2-3 of ACE-Flood. Returns test frame with score/pred/intervals + calibration material.
    calib: 'oof' (bidirectional cross-fitting), 'causal' (forward chaining), 'split' (last 25% held out).
    test_score: 'full' (model refit on all training data) or 'foldmean' (mean of the cross-fit fold models;
    the same models that produced the calibration scores)."""
    use_spread = (kind == "ensemble_spread") if use_spread is None else use_spread
    if calib in ("oof", "causal"):
        oof, te_fold = crossfit(kind, tr, te, seed, causal=(calib == "causal"))
        ok = ~np.isnan(oof[:, 0]); cal = tr[ok]; oof = oof[ok]
        if test_score == "foldmean":
            med, spread, lo, hi = te_fold.T
        else:
            med, spread, lo, hi = predictor(kind, tr, te, seed)
    else:
        cut = tr.date.quantile(0.75)
        fit_set, cal = tr[tr.date <= cut], tr[tr.date > cut]
        oof = np.column_stack(predictor(kind, fit_set, cal, seed))
        med, spread, lo, hi = predictor(kind, fit_set, te, seed)
    y_cal = cal.target.values
    s_cal = oof[:, 0] + (oof[:, 1] if use_spread else 0)
    out = te[["date", "basin", "thr", "target", "event", "onset", "label_avail"]].copy()
    out["pred"], out["score"] = med, med + (spread if use_spread else 0)
    out["L_qr"], out["U_qr"] = lo, hi
    return out, dict(pos=s_cal[cal.event.values == 1], n_cal=len(cal), lo=oof[:, 2], hi=oof[:, 3], y=y_cal)


def apply_decision(out, cal, h, strategy="aci", alpha=None, eta=None, n_min=None, window=None, fallback="always_warn"):
    """Stage 4. fallback when n_cal_events is too small for CRC: 'always_warn' (lam=-inf, the literal CRC
    answer) or 'native' (warn if score > 1, flagged as uncalibrated)."""
    A = CFG["ace"]; alpha = A["alpha"] if alpha is None else alpha; eta = A["eta"] if eta is None else eta
    n_min = A["n_min"] if n_min is None else n_min; window = A["rolling_window"] if window is None else window
    if strategy in ("expanding", "rolling"):
        lam0 = None
    else:
        lam0 = crc_fnr_threshold(cal["pos"], alpha)
        if fallback == "native" and len(cal["pos"]) < n_min:
            lam0 = 1.0
        if strategy == "empirical":
            lam0 = empirical_threshold(cal["pos"], alpha); strategy = "static"
    w, lam = decide(out.date.values, out.basin.values, out.score.values, out.event.values, out.label_avail.values,
                    h, strategy, alpha, eta, pool=cal["pos"], lam0=lam0, native=1.0, n_min=n_min, window=window)
    return w, lam


def add_intervals(out, cal, h, alpha=None, gamma=None):
    A = CFG["ace"]; alpha = A["alpha_int"] if alpha is None else alpha; gamma = A["gamma"] if gamma is None else gamma
    q = cqr_quantile(cal["lo"], cal["hi"], cal["y"], alpha)
    out["L_cqr"], out["U_cqr"] = out.L_qr - q, out.U_qr + q
    cs = np.maximum(cal["lo"] - cal["y"], cal["y"] - cal["hi"])
    out["L_aci"], out["U_aci"] = np.nan, np.nan
    for b in BASINS:
        i = np.where(out.basin.values == b)[0]
        if len(i) == 0:
            continue
        i = i[np.argsort(out.date.values[i])]
        L, U = aci_intervals(out.L_qr.values[i], out.U_qr.values[i], out.target.values[i], out.label_avail.values[i], cs, alpha, gamma, h)
        out.iloc[i, out.columns.get_loc("L_aci")] = L; out.iloc[i, out.columns.get_loc("U_aci")] = U
    return out


# ------------------------------------------------------------------ baselines (all use the SAME multi-forcing inputs as ACE-Flood unless named otherwise)
def base_out(te, pred=None, warn=None, score=None):
    o = te[["date", "basin", "thr", "target", "event", "onset", "label_avail"]].copy()
    o["pred"] = np.nan if pred is None else pred
    o["warn"] = (o.pred > 1).values if warn is None else warn
    o["score"] = score if score is not None else o["pred"]
    return o


def bl_persistence(tr, te, seed):
    return base_out(te, pred=te.Y0.values)


def bl_rain_rule(tr, te, seed):
    """Warn if the multi-product mean 3-day rainfall exceeds the basin's training 95th percentile."""
    p3 = lambda d: d[[f"{p}_P3d" for p in PRODS]].mean(1)
    w = np.zeros(len(te), bool)
    for b in BASINS:
        thr = np.quantile(p3(tr[tr.basin == b]), 0.95); i = te.basin.values == b
        w[i] = p3(te[i]).values > thr
    return base_out(te, warn=w)


def bl_ridge(tr, te, seed):
    c = concat_columns(tr)
    m = make_pipeline(StandardScaler(), Ridge(alpha=TUNED.get("ridge_alpha", 1.0))).fit(tr[c].fillna(0), tr.target)
    return base_out(te, pred=m.predict(te[c].fillna(0)))


def bl_logreg(tr, te, seed):
    c = concat_columns(tr)
    m = make_pipeline(StandardScaler(), LogisticRegression(C=TUNED.get("logreg_C", 1.0), class_weight="balanced", max_iter=5000)).fit(tr[c].fillna(0), tr.event)
    p = m.predict_proba(te[c].fillna(0))[:, 1]
    return base_out(te, warn=p >= 0.5, score=p)


def bl_rf(tr, te, seed):
    c = concat_columns(tr)
    m = RandomForestClassifier(n_estimators=500, min_samples_leaf=TUNED.get("rf_leaf", 3), max_features="sqrt",
                               class_weight="balanced_subsample", random_state=seed, n_jobs=2).fit(tr[c].fillna(-1), tr.event)
    p = m.predict_proba(te[c].fillna(-1))[:, 1]
    return base_out(te, warn=p >= 0.5, score=p)


def bl_lgb_local(tr, te, seed):
    c = concat_columns(tr); pred = np.zeros(len(te))
    for b in BASINS:
        a, k = tr.basin.values == b, te.basin.values == b
        pred[k] = lgb_fit(tr.loc[a, c], tr.target[a], seed, num_leaves=7).predict(te.loc[k, c])
    return base_out(te, pred=pred)


def bl_lgb_daymet(tr, te, seed):
    c = member_columns(tr, "daymet")
    return base_out(te, pred=lgb_fit(tr[c], tr.target, seed).predict(te[c]))


def bl_lgb_concat(tr, te, seed):
    c = concat_columns(tr)
    return base_out(te, pred=lgb_fit(tr[c], tr.target, seed).predict(te[c]))


def bl_qr90(tr, te, seed):
    c = concat_columns(tr)
    q = lgb_fit(tr[c], tr.target, seed, objective="quantile", alpha=0.9).predict(te[c])
    return base_out(te, warn=q > 1, score=q)


def bl_lgb_concat_tuned_threshold(tr, te, seed):
    """B8 with the threshold that maximised CSI on the SAME out-of-fold training predictions ACE-Flood uses."""
    c = concat_columns(tr)
    oof = np.full(len(tr), np.nan)
    for a, b in folds(tr):
        oof[b] = lgb_fit(tr.iloc[a][c], tr.target.iloc[a], seed).predict(tr.iloc[b][c])
    ok = ~np.isnan(oof); ev = tr.event.values[ok].astype(bool); s = oof[ok]
    grid = np.unique(np.quantile(s, np.linspace(0.80, 0.999, 400)))
    csi = [(_csi_from(*warn_counts(ev, s >= g))) for g in grid]
    tau = grid[int(np.nanargmax(csi))]
    pred = lgb_fit(tr[c], tr.target, seed).predict(te[c])
    o = base_out(te, pred=pred, warn=pred >= tau); o.attrs["tau"] = float(tau)
    return o


# ------------------------------------------------------------------ regional LSTM (Kratzert et al. 2019-style), multi-forcing inputs
LSTM_DYN = [f"{p}_{v}" for p in PRODS for v in ("P0", "T0", "SRAD", "VP", "SWE", "WIN0")] + ["Y0", "AGE", "SIN", "COS"]
LSTM_STAT = ["S_area_gages2", "S_elev_mean", "S_slope_mean", "S_p_mean", "S_aridity", "S_frac_snow", "S_soil_porosity", "S_frac_forest"]


class LSTMNet(torch.nn.Module):
    def __init__(self, nin, hid):
        super().__init__()
        self.lstm = torch.nn.LSTM(nin, hid, batch_first=True); self.drop = torch.nn.Dropout(0.2); self.head = torch.nn.Linear(hid, 1)

    def forward(self, x):
        o, _ = self.lstm(x)
        return self.head(self.drop(o[:, -1])).squeeze(-1)


def _sequences(full, part, cols, mu, sd, seq):
    """Windows of the last `seq` days up to and including each issue date, built from the CONTINUOUS
    per-basin frame (fixes the v1 bug where the train/test gap shifted windows)."""
    X, Y, idx = [], [], []
    for b in BASINS:
        fb = full[full.basin == b].sort_values("date")
        Z = ((fb[cols] - mu) / sd).fillna(0).values.astype(np.float32)
        pos = {d: k for k, d in enumerate(fb.date.values)}
        sub = part[part.basin == b]
        for r, d, y in zip(sub.index, sub.date.values, sub.target.values):
            k = pos[d]
            win = Z[max(0, k + 1 - seq):k + 1]
            if len(win) < seq:
                win = np.vstack([np.repeat(win[:1], seq - len(win), 0), win])
            X.append(win); Y.append(y); idx.append(r)
    return np.stack(X), np.array(Y, np.float32), np.array(idx)


def fit_predict_lstm(full, tr, te, seed, hid=None, epochs=None, seq=60):
    hid = hid or TUNED.get("lstm_hidden", 32); epochs = epochs or TUNED.get("lstm_epochs", 40)
    torch.manual_seed(seed); np.random.seed(seed); torch.set_num_threads(2)
    cols = LSTM_DYN + LSTM_STAT
    mu, sd = tr[cols].mean(), tr[cols].std().replace(0, 1).fillna(1)
    Xtr, Ytr, _ = _sequences(full, tr, cols, mu, sd, seq)
    Xte, _, ite = _sequences(full, te, cols, mu, sd, seq)
    net = LSTMNet(len(cols), hid); opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    Xt, Yt = torch.tensor(Xtr), torch.tensor(Ytr); g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        net.train(); perm = torch.randperm(len(Xt), generator=g)
        for k in range(0, len(perm), 64):
            bi = perm[k:k + 64]; opt.zero_grad()
            loss = torch.mean((net(Xt[bi]) - Yt[bi]) ** 2); loss.backward(); opt.step()
    net.eval()
    with torch.no_grad():
        p = net(torch.tensor(Xte)).numpy()
    return pd.Series(p, index=ite).reindex(te.index).values


def bl_lstm(tr, te, seed, full=None):
    return base_out(te, pred=fit_predict_lstm(full, tr, te, seed))
