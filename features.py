"""Feature engineering for threshold-normalised, pooled flood-warning models.

Target: y_t = Q_t / Q_thr(basin), Q_thr = long-term daily Q95 from CAMELS attributes
(computed by Addor et al. 2017 over 1989-2009, i.e. independent of the 2000-2002 study window).
Event at lead h:  E_{t+h} = 1{ y_{t+h} > 1 }.
Only information available at issue time t is used (no meteorological forecasts).
"""
import numpy as np, pandas as pd
from data import PRODUCTS

META = ("target", "y_now_true", "basin", "thr", "date", "event", "onset", "prev_target", "label_avail")
# v2: hydrological signatures (e.g. baseflow_index, computed from 1989-2009 discharge, which overlaps the test year)
# are excluded to avoid target leakage. Remaining attributes are physiographic or climatic.
STATIC = ["area_gages2", "elev_mean", "slope_mean", "p_mean", "aridity", "frac_snow",
          "soil_porosity", "frac_forest"]


def snow_model(prcp, tmean, ddf=3.0, t0=0.0):
    """Single-store degree-day snow model -> (snowpack, liquid water input = rain + melt)."""
    swe, out_swe, out_win = 0.0, np.zeros(len(prcp)), np.zeros(len(prcp))
    for i, (p, t) in enumerate(zip(prcp, tmean)):
        if t < t0:
            swe += p; rain = 0.0
        else:
            rain = p
        melt = min(swe, max(0.0, ddf * (t - t0)))
        swe -= melt
        out_swe[i], out_win[i] = swe, rain + melt
    return out_swe, out_win


def forcing_features(f: pd.DataFrame, tag: str) -> pd.DataFrame:
    """Meteorological features from one forcing product (all strictly <= t)."""
    tmean = (f.tmax + f.tmin) / 2.0  # NLDAS in this release has tmax == tmin (daily mean) -> use mean for all
    swe, win = snow_model(f.prcp.values, tmean.values)
    X = pd.DataFrame(index=f.index)
    P = f.prcp
    X["P0"], X["P1"], X["P2"] = P, P.shift(1), P.shift(2)
    for k in (3, 7, 14, 30):
        X[f"P{k}d"] = P.rolling(k, min_periods=1).sum()
    api = np.zeros(len(P)); a = 0.0
    for i, p in enumerate(P.values):
        a = 0.9 * a + p; api[i] = a
    X["API"] = api
    X["T0"], X["T7"] = tmean, tmean.rolling(7, min_periods=1).mean()
    X["SWE"], X["WIN0"] = swe, win
    X["WIN3"] = pd.Series(win, index=f.index).rolling(3, min_periods=1).sum()
    X["SRAD"], X["VP"] = f.srad, f.vp
    return X.add_prefix(tag + "_")


def flow_features(y: pd.Series) -> pd.DataFrame:
    """Autoregressive streamflow features robust to gaps (forward-filled + age-of-data)."""
    obs = y.notna()
    yf = y.ffill()
    last_idx = pd.Series(np.where(obs, np.arange(len(y)), np.nan), index=y.index).ffill()
    X = pd.DataFrame(index=y.index)
    X["Y0"] = yf
    X["Y1"], X["Y2"] = yf.shift(1), yf.shift(2)
    X["dY"] = yf - yf.shift(1)
    X["Y7max"] = yf.rolling(7, min_periods=1).max()
    X["Y30mean"] = yf.rolling(30, min_periods=1).mean()
    X["AGE"] = np.arange(len(y)) - last_idx.values  # days since last valid gauge reading
    return X


def build_frame(d, attrs, basin, h, products=("daymet", "maurer", "nldas"), q_mask=None, thr=None):
    """Feature frame for one basin. q_mask (bool Series, True = reading unavailable) removes gauge readings
    from the INPUTS; the returned column 'label_avail' says whether the target reading y_{t+h} was observed.
    thr: flood threshold in mm/day (default: CAMELS long-term Q95)."""
    thr = attrs.loc[basin, "q95"] if thr is None else thr
    y = d[basin]["q"] / thr
    y_in = y.copy()
    if q_mask is not None:
        y_in[q_mask] = np.nan
    blocks = {p: forcing_features(d[basin]["forcing"][p], p) for p in products}
    X = flow_features(y_in)
    for p in products:
        X = X.join(blocks[p])
    # inter-product disagreement (input-uncertainty signal)
    for v in ("P0", "P3d", "WIN3"):
        cols = [f"{p}_{v}" for p in products]
        X[f"SPREAD_{v}"] = X[cols].std(axis=1)
    doy = X.index.dayofyear
    X["SIN"], X["COS"] = np.sin(2 * np.pi * doy / 365.25), np.cos(2 * np.pi * doy / 365.25)
    for s in STATIC:
        X["S_" + s] = attrs.loc[basin, s]
    X["target"] = y.shift(-h)           # y_{t+h} (true value; used for evaluation only when not observed)
    avail = pd.Series(True, index=y.index) if q_mask is None else ~q_mask.reindex(y.index, fill_value=False)
    X["label_avail"] = avail.shift(-h, fill_value=False).astype(bool)
    X["y_now_true"] = y                 # for diagnostics only, never a feature
    X["basin"] = basin
    X["thr"] = thr
    return X


def member_columns(X, product):
    """Feature columns for a single-forcing member (own product + flow + calendar + statics + spread)."""
    keep = []
    for c in X.columns:
        if c in META:
            continue
        if any(c.startswith(p + "_") for p in PRODUCTS):
            if c.startswith(product + "_"):
                keep.append(c)
        else:
            keep.append(c)
    return keep


def concat_columns(X):
    return [c for c in X.columns if c not in META]
