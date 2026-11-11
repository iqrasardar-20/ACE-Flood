"""Data loading for CAMELS-US (default: the 4-basin subset shipped with NeuralHydrology's test data).
Dataset location: env var CAMELS_ROOT, else config.json 'camels_root' (relative to this folder)."""
import os, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json")))
ROOT = os.environ.get("CAMELS_ROOT", os.path.join(HERE, CFG["camels_root"]))
BASINS = CFG["basins"]
PRODUCTS = {"daymet": ("daymet", "cida"), "maurer": ("maurer_extended", "maurer"), "nldas": ("nldas", "nldas")}
START, END = CFG["period"]


def _check():
    if not os.path.isdir(ROOT):
        raise FileNotFoundError(f"CAMELS data not found at {ROOT}. Run get_data.sh or set CAMELS_ROOT (see README.md).")


def read_attrs():
    _check()
    d = None
    for f in ["topo", "clim", "soil", "vege", "hydro", "geol"]:
        a = pd.read_csv(f"{ROOT}/camels_attributes_v2.0/camels_{f}.txt", sep=";", dtype={"gauge_id": str}).set_index("gauge_id")
        d = a if d is None else d.join(a, rsuffix="_" + f)
    return d.loc[BASINS]


def read_forcing(basin, prod):
    folder, tag = PRODUCTS[prod]
    df = pd.read_csv(f"{ROOT}/basin_mean_forcing/{folder}/{basin}_lump_{tag}_forcing_leap.txt", sep=r"\s+", skiprows=3)
    df.columns = [c.lower() for c in df.columns]
    df.index = pd.to_datetime(dict(year=df["year"], month=df["mnth"], day=df["day"]))
    df = df.rename(columns={"prcp(mm/day)": "prcp", "srad(w/m2)": "srad", "tmax(c)": "tmax", "tmin(c)": "tmin",
                            "vp(pa)": "vp", "dayl(s)": "dayl", "swe(mm)": "swe"})
    df = df[["prcp", "srad", "tmax", "tmin", "vp", "dayl"]]
    # Time alignment (audit fix, Nov 2026). USGS daily discharge is the local (EST) calendar day. Matching each
    # product against the hourly NLDAS precipitation in the NeuralHydrology NetCDF file shows that the daily
    # accumulation window of 'day t' ends at ~19:00 local on day t (NLDAS), ~08:00 local on day t (Daymet, CAMELS
    # release) but ~04:00-08:00 local on day t+1 (Maurer). Maurer 'day t' therefore contains rainfall that falls
    # after a forecast issued at the end of day t. FORCING_LAG_DAYS shifts each product so that the value used at
    # issue day t ends no later than the issue time. Set {"maurer": 0} only to reproduce revision-2 results.
    lag = CFG.get("forcing_lag_days", {"daymet": 0, "maurer": 1, "nldas": 0}).get(prod, 0)
    if lag:
        df = df.shift(lag).bfill()
    return df.loc[START:END]


def read_q(basin, area_km2):
    df = pd.read_csv(f"{ROOT}/usgs_streamflow/{basin}_streamflow_qc.txt", sep=r"\s+", header=None,
                     names=["b", "y", "m", "d", "q", "flag"])
    idx = pd.to_datetime(dict(year=df.y, month=df.m, day=df.d))
    q = pd.Series(df.q.values, index=idx).astype(float)
    q[q < 0] = np.nan                                   # USGS -999 = missing
    q = q * 0.0283168466 * 86400 / (area_km2 * 1e6) * 1000   # cfs -> mm/day
    return q.loc[START:END], pd.Series(df.flag.values, index=idx).loc[START:END]


def load_all():
    attrs = read_attrs()
    out = {}
    for b in BASINS:
        q, flag = read_q(b, attrs.loc[b, "area_gages2"])
        out[b] = dict(q=q, flag=flag, forcing={p: read_forcing(b, p) for p in PRODUCTS})
    return out, attrs


def natural_daily_mask(frac_hours=0.5):
    """Days on which > frac_hours of the hourly USGS readings are missing in the hourly NeuralHydrology file.
    Used as a REAL (naturally occurring) gap pattern for the daily series."""
    import xarray as xr
    ds = xr.open_dataset(os.path.join(ROOT, CFG["hourly_file"]))
    q = ds["qobs_mm_per_hour"].to_pandas().T
    out = {}
    for b in BASINS:
        s = q[b]
        m = s.isna().groupby(s.index.normalize()).mean() > frac_hours
        m.index = pd.to_datetime(m.index)
        out[b] = m.reindex(pd.date_range(START, END), fill_value=False)
    return out
