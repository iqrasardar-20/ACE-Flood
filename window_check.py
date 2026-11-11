"""Independent check: for each daily product, which 24-h window of HOURLY NLDAS precipitation (timestamps UTC) best
matches it; and which window of hourly USGS discharge reproduces the USGS daily mean. Window for day D =
UTC hours [D 00:00 + s, D+1 00:00 + s). s = +5 h is the US Eastern Standard Time calendar day."""
import sys, os, numpy as np, pandas as pd, xarray as xr
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
from data import ROOT, CFG, load_all, BASINS
D, A = load_all(); ds = xr.open_dataset(os.path.join(ROOT, CFG["hourly_file"]))
print([v for v in ds.data_vars][:20])
P = ds["total_precipitation"].to_pandas().T; Q = ds["qobs_mm_per_hour"].to_pandas().T
def best(h, daily, agg):
    out = {}
    for s in range(-12, 37):
        x = h.copy(); x.index = x.index - pd.Timedelta(hours=s)
        d = (x.resample("D").sum(min_count=20) if agg=="sum" else x.resample("D").mean()).loc["2000-01-05":"2002-12-25"]
        out[s] = daily.reindex(d.index).corr(d)
    s = max(out, key=out.get); return s, round(out[s],3), round(out[5],3)
for b in BASINS:
    r = {"Q": best(Q[b], D[b]["q"], "mean")}
    for p in ("daymet","maurer","nldas"): r[p] = best(P[b], D[b]["forcing"][p].prcp, "sum")
    print(b, "  (best UTC offset s [h], r at best, r at local-day s=5):", r)
