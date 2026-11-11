"""All figures for the revised paper (v2). Every figure is drawn from results/*.csv produced by the run scripts."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 200, "savefig.dpi": 200})
GREY, DARK, BLUE, RED = "#8a8a8a", "#333333", "#1f5fbf", "#c0392b"
NAMES = {"01022500": "01022500 Narraguagus R., ME", "01547700": "01547700 Marsh Cr., PA",
         "02064000": "02064000 Falling R., VA", "03015500": "03015500 Brokenstraw Cr., PA"}
rd = lambda f, **k: pd.read_csv("results/" + f, **k)

# ---------------- Fig 1: framework
fig, ax = plt.subplots(figsize=(10, 4.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 4.4)
def box(x, y, w, h, title, body, col):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc=col, ec="#333", lw=1))
    ax.text(x + w / 2, y + h - 0.2, title, ha="center", va="top", fontsize=9.5, weight="bold")
    ax.text(x + w / 2, y + h - 0.55, body, ha="center", va="top", fontsize=7.8)
def arrow(x1, y1, x2, y2, txt=""):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", lw=1.2))
    if txt: ax.text((x1 + x2) / 2 + 0.08, (y1 + y2) / 2, txt, fontsize=7.5, style="italic", va="center")
box(0.05, 2.45, 2.25, 1.85, "Inputs (available at t)", "gauge Q up to t (gaps allowed)\nDaymet / Maurer / NLDAS up to t\nphysiographic attributes\nflood threshold Q_thr", "#f0efec")
box(2.6, 2.45, 2.25, 1.85, "Stage 1: Features", "y = Q / Q_thr\nlast valid y, lags, data age\nrain sums, API, snow model\nseason, static attributes", "#e7f1fb")
box(5.15, 2.45, 2.25, 1.85, "Stage 2: Predictor", "pooled LightGBM,\nall 3 forcing products\nK = 8 fold models f_k\nscore s_t = mean_k f_k(x_t)", "#e7f1fb")
box(7.7, 2.45, 2.25, 1.85, "Stage 3: Calibration", "blocked folds, 7-day embargo\nout-of-fold scores of the\nn training flood-days\nCRC -> lambda_0 (Eq. 6)", "#e5f4e4")
box(5.15, 0.1, 4.8, 1.85, "Stage 4: Operation (per basin)", "issue  W_t = 1{ s_t >= lambda_t }\nat t+h, IF the gauge reading exists and it was a flood-day:\nlambda <- lambda + eta (alpha - miss)   (Eq. 7)\nif n < 1/alpha - 1: always warn, or flagged fallback", "#f9eeda")
box(0.05, 0.1, 4.8, 1.85, "Outputs", "warning with target miss rate alpha\n(finite-sample bound only under exchangeability;\nlong-run bound under any sequence, Prop. 2)\n90% CQR/ACI discharge interval", "#f0efec")
arrow(2.3, 3.35, 2.6, 3.35); arrow(4.85, 3.35, 5.15, 3.35); arrow(7.4, 3.35, 7.7, 3.35)
arrow(8.8, 2.45, 8.8, 1.95, "lambda_0"); arrow(6.3, 2.45, 6.3, 1.95, "s_t"); arrow(5.15, 1.0, 4.85, 1.0)
plt.tight_layout(); plt.savefig("figs/fig1_framework.png", bbox_inches="tight"); plt.close()

# ---------------- Fig 2: hydrographs
o = rd("pred_ACE_h1_seed0.csv", parse_dates=["date"], dtype={"basin": str}); o["basin"] = o.basin.str.zfill(8)
fig, axs = plt.subplots(4, 1, figsize=(10, 9.2), sharex=True)
for ax, (b, g) in zip(axs, o.groupby("basin")):
    g = g.sort_values("date"); d = g.date + pd.Timedelta(days=1)
    ax.fill_between(d, g.L_aci.clip(lower=0), g.U_aci, color=BLUE, alpha=0.15, lw=0, label="90% CQR+ACI interval")
    ax.plot(d, g.target, color="black", lw=1, label="observed y(t+1)")
    ax.plot(d, g.pred.clip(lower=0), color=BLUE, lw=1, label="forecast y(t+1)")
    ax.axhline(1, color=GREY, ls="--", lw=0.8)
    w = g[g.warn.astype(bool)]; ax.scatter(w.date + pd.Timedelta(days=1), np.full(len(w), -0.25), marker="|", color=RED, s=40, label="warning issued")
    ev = g[g.event == 1]; ax.scatter(ev.date + pd.Timedelta(days=1), np.full(len(ev), -0.45), marker="|", color="black", s=40, label="observed flood-day")
    ax.set_ylim(-0.6, max(2.0, g.target.max() * 1.05)); ax.set_ylabel("y = Q / Q95,LT  (-)"); ax.set_title(NAMES[b], loc="left", fontsize=9.5)
axs[0].legend(ncol=5, fontsize=7.2, loc="upper right", frameon=False)
fig.suptitle("Test year 2002, lead h = 1 day, seed 0 (forecast plotted at its target date)", x=0.01, ha="left", fontsize=10)
plt.tight_layout(); plt.savefig("figs/fig2_hydrographs.png", bbox_inches="tight"); plt.close()

# ---------------- Fig 3: validity
v = rd("validity_alpha_eta.csv")
fig, axs = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
for ax, h in zip(axs, (1, 2, 3)):
    for eta, col, lab in [(0.0, GREY, "static (eta = 0)"), (0.05, BLUE, "adaptive (eta = 0.05)")]:
        g = v[(v.h == h) & (v.eta == eta)].groupby("alpha").MissRate.agg(["mean", "std"])
        ax.errorbar(g.index, g["mean"], yerr=g["std"], marker="o", ms=4, color=col, label=lab, capsize=3)
    ax.plot([0, 0.45], [0, 0.45], color="black", lw=0.8, ls=":", label="miss rate = alpha")
    ax.set_title(f"lead h = {h} d", fontsize=10); ax.set_xlabel("target miss rate alpha")
axs[0].set_ylabel("realised 2002 miss rate (1 - POD)"); axs[0].legend(fontsize=7.5, frameon=False)
fig.suptitle("Realised vs target miss rate (mean +/- sd over 5 seeds)", x=0.01, ha="left", fontsize=10)
plt.tight_layout(); plt.savefig("figs/fig3_validity.png", bbox_inches="tight"); plt.close()

# ---------------- Fig 4: POD-FAR plane, h = 1
r = rd("main_runs.csv"); r1 = r[r.h == 1].groupby("model")[["POD", "FAR", "CSI"]].mean()
keep = ["B1 Persistence", "B2 Rainfall-threshold rule", "B3 Ridge regression", "B4 Logistic regression", "B5 Random forest",
        "B6 LightGBM local", "B8 LightGBM multi-forcing", "B9 Quantile LightGBM q0.9", "B10 Regional LSTM",
        "B11 B8 + CSI-tuned threshold", "B12 Persistence + CRC/ACI decision layer", "ACE-Flood", "ACE-Flood [static, eta=0]"]
fig, ax = plt.subplots(figsize=(8, 5.8)); sr = np.linspace(0.01, 1, 400)
for c in (0.2, 0.4, 0.6, 0.8):
    pod = 1 / (1 / c + 1 - 1 / sr); m = (pod > 0) & (pod <= 1); ax.plot(1 - sr[m], pod[m], color="#e2e2e2", lw=0.8)
    j = np.argmin(np.abs(pod - 0.98)); ax.text(1 - sr[j], 0.99, f"CSI {c}", fontsize=7, color=GREY, ha="center")
short = {k: k.split(" ", 1)[1] if k[0] in "B" else k for k in keep}
for m in keep:
    if m not in r1.index: continue
    x, y = r1.loc[m, "FAR"], r1.loc[m, "POD"]; col = BLUE if "ACE" in m else GREY
    ax.scatter(x, y, color=col, s=50 if m == "ACE-Flood" else 25, zorder=3)
    ax.annotate(m.split(" ")[0] if m[0] == "B" else m, (x, y), xytext={"ACE-Flood": (-58, -12), "B11": (6, 2), "B9": (6, -10), "B3": (6, -10)}.get(m.split(" ")[0] if m[0] == "B" else m, (5, 3)), textcoords="offset points", fontsize=7.5, color=col)
ax.axhline(0.8, color=BLUE, ls="--", lw=0.8); ax.text(0.02, 0.81, "target POD = 1 - alpha = 0.8", color=BLUE, fontsize=7.5)
ax.set_xlabel("false-alarm ratio FAR (-)"); ax.set_ylabel("probability of detection POD (-)"); ax.set_xlim(0, 0.8); ax.set_ylim(0, 1.03)
ax.set_title("Lead h = 1 d, test 2002, mean of 5 seeds (labels: model codes, see Table 3)", loc="left", fontsize=9.5)
plt.tight_layout(); plt.savefig("figs/fig4_pod_far.png", bbox_inches="tight"); plt.close()

# ---------------- Fig 5: lambda paths
fig, ax = plt.subplots(figsize=(9, 3.2))
for k, (b, g) in enumerate(o.groupby("basin")):
    g = g.sort_values("date"); ax.plot(g.date, g.lam, lw=1.3, label=NAMES[b], color=plt.cm.Blues(0.45 + 0.17 * k))
ax.axhline(o.lam.iloc[0], color=GREY, ls="--", lw=0.8); ax.text(o.date.min(), o.lam.iloc[0] + 0.005, "lambda_0 (cross-fitted CRC)", fontsize=7.5, color=GREY)
ax.set_ylabel("threshold lambda_t (y units)"); ax.legend(fontsize=7.5, frameon=False, ncol=2)
ax.set_title("Adaptive threshold in 2002 (h = 1, seed 0): +eta*alpha after a caught flood-day, -eta*(1-alpha) after a miss", loc="left", fontsize=9)
plt.tight_layout(); plt.savefig("figs/fig5_lambda.png", bbox_inches="tight"); plt.close()

# ---------------- Fig 6: calibration strategies under scarcity
try:
    s = rd("calibration_scarcity.csv")
    strat = [("C1 CRC + ACI (literal) = ACE-Flood", BLUE, "-"), ("C2 CRC + ACI, min-event fallback to native y>1", BLUE, "--"),
             ("C3 Expanding-window recalibration", "#5b8fd6", ":"), ("C5 ACI from native threshold, no calibration", DARK, "-."),
             ("Native threshold y>1 (no calibration)", GREY, "-"), ("B11 B8 + CSI-tuned threshold", GREY, "--"), ("B10 Regional LSTM", GREY, ":")]
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    for nm, col, ls in strat:
        g = s[s.strategy == nm].groupby("months")[["CSI", "POD", "FAR"]].mean()
        for ax, met in zip(axs, ("CSI", "POD", "FAR")):
            ax.plot(g.index, g[met], marker="o", ms=4, color=col, ls=ls, label=nm)
    for ax, met in zip(axs, ("CSI", "POD", "FAR")):
        ax.set_xlabel("training record (months, new gauge)"); ax.set_ylabel(met); ax.set_xticks([3, 6, 12, 23])
    axs[1].axhline(0.8, color=BLUE, lw=0.6, ls=":")
    fig.legend(*axs[0].get_legend_handles_labels(), fontsize=7, frameon=False, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.12))
    fig.suptitle("Calibration strategies under event scarcity (h = 1, mean of 3 seeds)", x=0.01, ha="left", fontsize=10)
    plt.tight_layout(); plt.savefig("figs/fig6_calibration.png", bbox_inches="tight"); plt.close()
except FileNotFoundError:
    print("calibration results missing")

# ---------------- Fig 7: lead time
fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
for m, col, ls in [("ACE-Flood", BLUE, "-"), ("B12 Persistence + CRC/ACI decision layer", BLUE, ":"), ("B1 Persistence", "black", "--"),
                   ("B8 LightGBM multi-forcing", GREY, "-"), ("B11 B8 + CSI-tuned threshold", GREY, "--"), ("B10 Regional LSTM", GREY, "-.")]:
    g = r[r.model == m].groupby("h")[["CSI", "OnsetPOD"]].agg(["mean", "std"]).fillna(0)
    for ax, met in zip(axs, ("CSI", "OnsetPOD")):
        ax.errorbar(g.index, g[(met, "mean")], yerr=g[(met, "std")], marker="o", ms=4, color=col, ls=ls, label=m, capsize=3)
for ax, met in zip(axs, ("CSI", "onset POD")):
    ax.set_xticks([1, 2, 3]); ax.set_xlabel("lead time h (days)"); ax.set_ylabel(met)
axs[0].legend(fontsize=7, frameon=False)
fig.suptitle("Skill vs lead time without rainfall forecasts (mean +/- sd, 5 seeds)", x=0.01, ha="left", fontsize=10)
plt.tight_layout(); plt.savefig("figs/fig7_leadtime.png", bbox_inches="tight"); plt.close()

# ---------------- Fig 8: missing data
try:
    mm = rd("missing_runs.csv"); mc = mm[mm.scenario == "MCAR"]; nat = mm[mm.scenario == "natural"]
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    for m, col, ls in [("ACE-Flood", BLUE, "-"), ("ACE-Flood (v1 bug: uses unobserved labels)", RED, ":"), ("A7 ACE expanding-window", "#5b8fd6", "--"),
                       ("B8 LightGBM multi-forcing", GREY, "-"), ("B11 B8 + CSI-tuned threshold", GREY, "--"), ("B1 Persistence (last valid reading)", "black", "-.")]:
        g = mc[mc.model == m].groupby("rate")[["CSI", "POD", "FAR"]].agg(["mean", "std"])
        for ax, met in zip(axs, ("CSI", "POD", "FAR")):
            ax.errorbar(g.index * 100, g[(met, "mean")], yerr=g[(met, "std")], marker="o", ms=4, color=col, ls=ls, label=m, capsize=3)
            if (nat.model == m).any():
                ax.scatter([nat.realised_missing.mean() * 100], [nat[nat.model == m][met].mean()], marker="*", s=90, color=col, zorder=4)
    for ax, met in zip(axs, ("CSI", "POD", "FAR")): ax.set_xlabel("gauge readings unavailable (%)"); ax.set_ylabel(met)
    axs[1].axhline(0.8, color=BLUE, lw=0.6, ls=":")
    axs[0].legend(fontsize=6.5, frameon=False); axs[2].text(0.02, 0.95, "stars: natural gap pattern", transform=axs[2].transAxes, fontsize=7.5)
    fig.suptitle("Missing gauge data, simulated MCAR gaps and natural gaps (h = 1, 3 mask seeds)", x=0.01, ha="left", fontsize=10)
    plt.tight_layout(); plt.savefig("figs/fig8_missing.png", bbox_inches="tight"); plt.close()
except FileNotFoundError:
    print("missing results missing")

# ---------------- Fig 9: paired CSI differences with 95% CI (h = 1, 2-week blocks)
try:
    st = rd("stats_paired.csv"); st = st[(st.metric == "CSI") & (st.block_weeks == 2)]
    fig, axs = plt.subplots(1, 3, figsize=(12, 5), sharey=True)
    order = [m for m in r[r.h == 1].groupby("model").CSI.mean().sort_values().index if m != "ACE-Flood"]
    for ax, h in zip(axs, (1, 2, 3)):
        g = st[st.h == h].set_index("baseline").reindex(order)
        y = np.arange(len(order))
        sig = g.p_holm < 0.05
        ax.hlines(y, g.lo, g.hi, color=np.where(sig, BLUE, GREY)); ax.scatter(g["diff"], y, color=np.where(sig, BLUE, GREY), s=18, zorder=3)
        ax.axvline(0, color="black", lw=0.8); ax.set_title(f"h = {h} d", fontsize=10); ax.set_xlabel("CSI(ACE-Flood) - CSI(baseline)")
    axs[0].set_yticks(np.arange(len(order))); axs[0].set_yticklabels(order, fontsize=7)
    fig.suptitle("Paired CSI difference, 95% block-bootstrap CI (2-week blocks, 5 seeds); blue = Holm-adjusted permutation p < 0.05", x=0.01, ha="left", fontsize=9.5)
    plt.tight_layout(); plt.savefig("figs/fig9_paired_csi.png", bbox_inches="tight"); plt.close()
except FileNotFoundError:
    print("stats missing")
print("figures done")
