"""Models, conformal decision rules, metrics and statistical tests (v2)."""
import numpy as np, pandas as pd, lightgbm as lgb, warnings, json, os
warnings.filterwarnings("ignore")
CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")))
LGB_BASE = dict(CFG["lgb"], verbose=-1, n_jobs=2)


def lgb_fit(X, y, seed, objective="regression", alpha=None, **over):
    p = dict(LGB_BASE, random_state=seed, objective=objective, **over)
    if alpha is not None:
        p["alpha"] = alpha
    return lgb.LGBMRegressor(**p).fit(X, y)


# ------------------------------------------------------------------ conformal risk control (miss rate)
def crc_fnr_threshold(scores_pos, alpha):
    """Largest lam with (#{i: s_i < lam} + 1)/(n+1) <= alpha  (CRC, Angelopoulos et al. 2024, B = 1).
    Returns -inf if unattainable (n < 1/alpha - 1), +inf if every calibration event may be missed."""
    s = np.sort(np.asarray(scores_pos, float))
    n = len(s)
    k = int(np.floor(alpha * (n + 1) - 1))
    if k < 0:
        return -np.inf
    if k >= n:
        return np.inf
    return s[k]


def empirical_threshold(scores_pos, alpha):
    """Plain empirical alpha-quantile of event scores (no +1 finite-sample correction)."""
    s = np.sort(np.asarray(scores_pos, float))
    if len(s) == 0:
        return -np.inf
    return s[int(np.floor(alpha * len(s)))] if np.floor(alpha * len(s)) < len(s) else np.inf


def decide(dates, basins, scores, events, label_avail, h, strategy, alpha, eta=0.05, pool=None, lam0=None,
           native=1.0, n_min=10, window=40):
    """Operational decision engine. Processes calendar days in order; at the end of day t it
    (1) reveals the outcome of each forecast issued at t-h, but ONLY if that gauge reading exists (label_avail),
    (2) updates the threshold(s), (3) issues W_t = 1{s_t >= lam}.
    Information used at t: scores issued up to t, outcomes of forecasts issued up to t-h that were observed.
    strategy:
      'static'    fixed lam0
      'aci'       per-basin lam, lam <- lam + eta*(alpha - miss) on revealed flood-days (Eq. 7)
      'expanding' shared lam = CRC(pool of OOF event scores + all revealed event scores); native rule while n < n_min
      'rolling'   as expanding but only the most recent `window` events
    Returns warnings (bool array, input order) and the lam in force for each forecast."""
    dates = pd.to_datetime(np.asarray(dates)); basins = np.asarray(basins)
    scores = np.asarray(scores, float); events = np.asarray(events, int); label_avail = np.asarray(label_avail, bool)
    n = len(scores)
    order = np.lexsort((basins, dates))
    w = np.zeros(n, bool); lam_used = np.full(n, np.nan)
    by_date = {}
    for i in order:
        by_date.setdefault(dates[i], []).append(i)
    issued = {}                                   # (basin, date) -> row index
    for i in range(n):
        issued[(basins[i], dates[i])] = i
    lam_b = {b: lam0 for b in np.unique(basins)}
    pool = list(pool) if pool is not None else []
    hd = pd.Timedelta(days=h)

    def pooled_lam():
        p = pool if strategy == "expanding" else pool[-window:]
        return crc_fnr_threshold(p, alpha) if len(p) >= n_min else native

    cur = pooled_lam() if strategy in ("expanding", "rolling") else None
    for t in sorted(by_date):
        for b in lam_b:                           # reveal outcomes of forecasts issued at t - h
            j = issued.get((b, t - hd))
            if j is None or not label_avail[j] or events[j] != 1:
                continue
            if strategy == "aci" and eta > 0 and np.isfinite(lam_b[b]):
                lam_b[b] += eta * (alpha - float(not w[j]))
            elif strategy in ("expanding", "rolling"):
                pool.append(scores[j])
        if strategy in ("expanding", "rolling"):
            cur = pooled_lam()
        for i in by_date[t]:
            lam = cur if strategy in ("expanding", "rolling") else lam_b[basins[i]]
            lam_used[i] = lam
            w[i] = scores[i] >= lam
    return w, lam_used


def cqr_quantile(lo, hi, y, alpha):
    e = np.maximum(lo - y, y - hi)
    n = len(e)
    return np.quantile(e, min(np.ceil((n + 1) * (1 - alpha)) / n, 1.0), method="higher")


def aci_intervals(lo, hi, y, label_avail, cal_scores, alpha, gamma, h):
    """ACI (Gibbs & Candes 2021) on CQR scores for ONE basin in date order; an outcome is used only once
    observed (h days later) and only if the reading exists."""
    T = len(lo); a_t = alpha; L, U = np.zeros(T), np.zeros(T)
    scores = list(cal_scores); err = np.zeros(T)
    for t in range(T):
        j = t - h
        if j >= 0 and label_avail[j]:
            a_t = a_t + gamma * (alpha - err[j])
            scores.append(max(lo[j] - y[j], y[j] - hi[j]))
        q = np.quantile(scores, 1 - np.clip(a_t, 1e-3, 0.999), method="higher")
        L[t], U[t] = lo[t] - q, hi[t] + q
        err[t] = float(not (L[t] <= y[t] <= U[t]))
    return L, U


# ------------------------------------------------------------------ metrics
def nse(o, s):
    return 1 - np.sum((s - o) ** 2) / np.sum((o - o.mean()) ** 2)


def kge(o, s):
    r = np.corrcoef(o, s)[0, 1]
    return 1 - np.sqrt((r - 1) ** 2 + (s.std() / o.std() - 1) ** 2 + (s.mean() / o.mean() - 1) ** 2)


def reg_metrics(o, s):
    o, s = np.asarray(o, float), np.asarray(s, float)
    return dict(NSE=nse(o, s), KGE=kge(o, s), RMSE=np.sqrt(np.mean((s - o) ** 2)), MAE=np.mean(np.abs(s - o)))


def warn_counts(ev, w):
    ev, w = np.asarray(ev, bool), np.asarray(w, bool)
    return np.sum(ev & w), np.sum(~ev & w), np.sum(ev & ~w)


def warn_metrics(ev, w, onset):
    ev, w, onset = np.asarray(ev, bool), np.asarray(w, bool), np.asarray(onset, bool)
    tp, fp, fn = warn_counts(ev, w)
    pod = tp / (tp + fn) if tp + fn else np.nan
    far = fp / (tp + fp) if tp + fp else np.nan       # undefined when no warnings are issued
    csi = tp / (tp + fp + fn) if tp + fp + fn else np.nan
    prec = tp / (tp + fp) if tp + fp else np.nan
    f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else np.nan
    opod = np.sum(onset & w) / onset.sum() if onset.sum() else np.nan
    return dict(TP=int(tp), FP=int(fp), FN=int(fn), POD=pod, FAR=far, CSI=csi, F1=f1, OnsetPOD=opod,
                Warnings=int(w.sum()), MissRate=1 - pod if pod == pod else np.nan)


def interval_metrics(o, L, U, alpha):
    cov = np.mean((o >= L) & (o <= U)); width = np.mean(U - L)
    iscore = np.mean((U - L) + 2 / alpha * (L - o) * (o < L) + 2 / alpha * (o - U) * (o > U))
    return dict(PICP=cov, MPIW=width, IS=iscore)


# ------------------------------------------------------------------ paired statistics
def _csi_from(tp, fp, fn):
    d = tp + fp + fn
    return tp / d if d else np.nan


def paired_block_stats(ev, wa, wb, week, n_boot=2000, n_perm=5000, block=1, seed=0, metric="CSI"):
    """Paired comparison of two warning series A and B on the same forecasts.
    ev, wa, wb : arrays of shape (S, N) - S seeds (rows) x N forecasts (all basins pooled);
    week       : array (N,) of ISO-week index; blocks of `block` consecutive weeks are the resampling unit,
                 shared by all basins (keeps temporal AND cross-basin dependence inside a block).
    Statistic  : mean over seeds of metric(A) - metric(B), metric from pooled counts.
    Returns bootstrap CI (percentile) and a two-sided paired sign-flip permutation p-value."""
    rng = np.random.default_rng(seed)
    ev, wa, wb = np.atleast_2d(ev).astype(bool), np.atleast_2d(wa).astype(bool), np.atleast_2d(wb).astype(bool)
    wk = np.asarray(week); uw = np.unique(wk)
    blk_of_week = {w: k // block for k, w in enumerate(uw)}
    blk = np.array([blk_of_week[x] for x in wk]); nb = blk.max() + 1
    S = ev.shape[0]

    def counts(w):   # per seed x block: tp, fp, fn
        out = np.zeros((S, nb, 3))
        for c, m in enumerate([(ev & w), (~ev & w), (ev & ~w)]):
            for s in range(S):
                out[s, :, c] = np.bincount(blk, weights=m[s], minlength=nb)
        return out
    if metric == "CSI":
        f = lambda c: c[..., 0] / (c[..., 0] + c[..., 1] + c[..., 2])
    elif metric == "POD":
        f = lambda c: c[..., 0] / (c[..., 0] + c[..., 2])
    elif metric == "FAR":
        f = lambda c: c[..., 1] / (c[..., 0] + c[..., 1])
    elif metric == "F1":
        f = lambda c: 2 * c[..., 0] / (2 * c[..., 0] + c[..., 1] + c[..., 2])
    ca, cb = counts(wa), counts(wb)
    obs = np.nanmean(f(ca.sum(1)) - f(cb.sum(1)))
    boots = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, nb, nb)
        boots[i] = np.nanmean(f(ca[:, idx].sum(1)) - f(cb[:, idx].sum(1)))
    perms = np.empty(n_perm)
    for i in range(n_perm):
        flip = rng.random(nb) < 0.5
        pa = np.where(flip[None, :, None], cb, ca).sum(1); pb = np.where(flip[None, :, None], ca, cb).sum(1)
        perms[i] = np.nanmean(f(pa) - f(pb))
    p = (np.sum(np.abs(perms) >= abs(obs) - 1e-12) + 1) / (n_perm + 1)
    return dict(diff=obs, lo=np.nanpercentile(boots, 2.5), hi=np.nanpercentile(boots, 97.5), p_perm=p, n_blocks=int(nb))


def holm(pvals):
    p = np.asarray(pvals, float); m = len(p); order = np.argsort(p); adj = np.empty(m); run = 0
    for r, i in enumerate(order):
        run = max(run, (m - r) * p[i]); adj[i] = min(1.0, run)
    return adj
