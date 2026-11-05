"""One-at-a-time factor screen, then a joint model.

The main set is every pivotal vote whose question was an approval, benefit-risk,
or effectiveness question. The wording of an AMT-130 meeting is unset, so an
effectiveness question stays in. Restriction, dose, and labeling questions stay
out. A meeting with no final action stays in the vote screen and drops out of
the approval screen.

Run from data/ with scripts/ on PYTHONPATH. Does not edit the pivotal CSV.

Run from data/ with scripts/ on PYTHONPATH. Does not edit the pivotal CSV.

Each one-at-a-time fit drops a meeting only when that factor is unrecorded.
Priority review is the original application's designation. A sensitivity fills the
remaining blanks as standard, and again as priority. Priority enters the joint
model only when those two bounds agree and the recorded-review sample does not
remove another factor's association. The joint model is every other factor that
clears Fisher's exact test on the vote.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import beta as beta_dist
from scipy.stats import chi2
from scipy.stats import fisher_exact

from amt130_predict import (
    boot_pred,
    fit_logit,
    gate,
    predict_row,
    prepare,
    r2,
    refit,
    stratum_beta,
)

CHART = os.environ.get("CHART_DIR", "charts")
B = 400
SEED = 130

# Display order. Column in the prepared frame, short key, axis label.
FACTORS = [
    ("orphan_y", "orphan", "Orphan status"),
    ("cgt", "CGT", "Cell and gene therapy"),
    ("opioid_i", "opioid", "Opioid"),
    ("pri", "priority", "Priority review"),
    ("cber_i", "cber", "Biologics center"),
    ("cns", "CNS", "Neurology committees"),
    ("init_i", "initial", "Initial application"),
]
COL = {key: col for col, key, _ in FACTORS}
LABEL = {key: lab for _, key, lab in FACTORS}


def fisher_row(x, y):
    """2x2 of factor (rows) by outcome (columns). Returns counts and Fisher p."""
    a = int(((x == 1) & (y == 1)).sum())
    b = int(((x == 1) & (y == 0)).sum())
    c = int(((x == 0) & (y == 1)).sum())
    d = int(((x == 0) & (y == 0)).sum())
    # Table columns are the outcome, so the odds ratio is the factor's.
    oddsratio, p = fisher_exact([[a, b], [c, d]], alternative="two-sided")
    return dict(yes_event=a, yes_n=a + b, no_event=c, no_n=c + d, odds_ratio=float(oddsratio), fisher_p=float(p))


def phi_of(x, y):
    if len(x) < 3 or len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def one(df, col, y):
    use = df.dropna(subset=[col, y]).copy()
    x = use[col].to_numpy(float)
    yy = use[y].to_numpy(float)
    counts = fisher_row(x, yy)
    X = np.column_stack([np.ones(len(use)), x])
    b_p, ll_p, _ = fit_logit(X, yy, True)
    b_u, ll_u, stable = fit_logit(X, yy, False)
    _, ll0, _ = fit_logit(np.ones((len(yy), 1)), yy, False)
    nag, mcf = r2(ll_u if stable else ll_p, ll0, len(yy))
    lr = 2 * (ll_u - ll0) if stable else float("nan")
    lr_p = float(chi2.sf(lr, 1)) if stable and lr == lr else float("nan")
    aic = (-2 * ll_u + 2 * 2) if stable else float("nan")
    aic0 = -2 * ll0 + 2 * 1
    return dict(
        n=int(len(use)), events=int(yy.sum()),
        phi=phi_of(x, yy),
        log_odds=float(b_p[1]), intercept=float(b_p[0]),
        log_odds_unpen=float(b_u[1]) if stable else float("nan"),
        stable=bool(stable), nagelkerke=float(nag), mcfadden=float(mcf),
        aic=float(aic) if aic == aic else float("nan"),
        aic_null=float(aic0), lr=float(lr) if lr == lr else float("nan"), lr_p=lr_p,
        **counts,
    )


def joint_fit(df, keys, y):
    cols = [COL[k] for k in keys]
    use = df.dropna(subset=cols + [y]).copy()
    X = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in cols])
    yy = use[y].to_numpy(float)
    b_p, ll_p, _ = fit_logit(X, yy, True)
    b_u, ll_u, stable = fit_logit(X, yy, False)
    _, ll0, _ = fit_logit(np.ones((len(yy), 1)), yy, False)
    nag, mcf = r2(ll_u if stable else ll_p, ll0, len(yy))
    k = X.shape[1]
    aic = -2 * (ll_u if stable else ll_p) + 2 * k
    out = dict(
        n=int(len(use)), events=int(yy.sum()), factors="+".join(keys),
        stable=bool(stable), nagelkerke=float(nag), mcfadden=float(mcf),
        aic=float(aic), ll=float(ll_u if stable else ll_p),
        intercept=float(b_p[0]),
        log_odds={key: float(b_p[i + 1]) for i, key in enumerate(keys)},
        log_odds_unpen={key: (float(b_u[i + 1]) if stable else float("nan")) for i, key in enumerate(keys)},
    )
    # Drop-one likelihood-ratio against the unpenalized fit, only when both fits are stable.
    drops = {}
    for i, key in enumerate(keys):
        keep = [c for j, c in enumerate(cols) if j != i]
        Xr = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in keep]) if keep else np.ones((len(use), 1))
        _, ll_r, stable_r = fit_logit(Xr, yy, False)
        if stable and stable_r:
            stat = 2 * (ll_u - ll_r)
            drops[key] = dict(lr=float(stat), p=float(chi2.sf(stat, 1)), stable=True)
        else:
            drops[key] = dict(lr=float("nan"), p=float("nan"), stable=False)
    out["drop"] = drops
    return out


def boot_coefs(df, keys, y, B=B):
    cols = [COL[k] for k in keys]
    use = df.dropna(subset=cols + [y])
    X = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in cols])
    yy = use[y].to_numpy(float)
    rng = np.random.default_rng(SEED)
    got = []
    n = len(yy)
    for _ in range(B):
        ix = rng.integers(0, n, n)
        if len(np.unique(yy[ix])) < 2:
            continue
        if X.shape[1] > 1 and any(len(np.unique(X[ix, j])) < 2 for j in range(1, X.shape[1])):
            continue
        b, _, _ = fit_logit(X[ix], yy[ix], True)
        got.append(b[1:])
    arr = np.array(got) if got else np.empty((0, len(keys)))
    lo = np.quantile(arr, 0.025, axis=0) if len(arr) >= 50 else [float("nan")] * len(keys)
    hi = np.quantile(arr, 0.975, axis=0) if len(arr) >= 50 else [float("nan")] * len(keys)
    return {key: (float(lo[i]), float(hi[i]), int(len(arr))) for i, key in enumerate(keys)}


def jeffreys(k, n):
    if n <= 0:
        return float("nan"), float("nan"), float("nan")
    lo, med, hi = beta_dist.ppf([0.025, 0.5, 0.975], 0.5 + k, 0.5 + n - k)
    return float(med), float(lo), float(hi)


def screen_frame(df, y):
    rows = []
    for col, key, lab in FACTORS:
        rec = one(df, col, y)
        rec.update(factor=key, label=lab, outcome=y)
        alone_ci = boot_coefs(df, [key], y)
        rec["boot_lo"], rec["boot_hi"], rec["boot_n"] = alone_ci[key]
        rows.append(rec)
    return rows


def conditional_fisher(df, y):
    """Exact tests that do not need a separated likelihood.

    Cell and gene therapy occurs inside the orphan rows, so its incremental
    test is Fisher among orphan products. Orphan status does not vary inside
    the cell-and-gene-therapy rows when those rows are all orphan, so its
    incremental test is Fisher among the other rows.
    """
    out = {}
    sub = df.dropna(subset=["orphan_y", "cgt", y])
    orphan = sub[sub.orphan_y == 1]
    rest = sub[sub.cgt == 0]
    out["cgt_among_orphan"] = fisher_row(orphan.cgt.to_numpy(float), orphan[y].to_numpy(float))
    out["cgt_among_orphan"]["n"] = int(len(orphan))
    out["orphan_among_non_cgt"] = fisher_row(rest.orphan_y.to_numpy(float), rest[y].to_numpy(float))
    out["orphan_among_non_cgt"]["n"] = int(len(rest))
    both = sub[(sub.orphan_y == 1) & (sub.cgt == 1)]
    out["both_n"] = int(len(both))
    out["both_events"] = int(both[y].sum()) if len(both) else 0
    out["cgt_not_orphan"] = int(((sub.cgt == 1) & (sub.orphan_y == 0)).sum())
    out["cgt_and_cber"] = int(((sub.cgt == 1) & (sub.cber_i == 1)).sum())
    out["cgt_and_cns"] = int(((sub.cgt == 1) & (sub.cns == 1)).sum())
    out["cgt_n"] = int((sub.cgt == 1).sum())
    return out


def prediction_block(df, y, keys):
    fit = refit(df, keys, y, False)
    lo, hi = boot_pred(df, keys, y, False, 0, None)
    n, k, med, blo, bhi = stratum_beta(df, keys, y, 0, None)
    p = predict_row(fit["b_pen"], keys, False, 0, None) if fit and fit["stable"] or (fit and np.all(np.abs(fit["b_pen"]) < 8)) else float("nan")
    # predict_row is the penalized probability even when the unpenalized fit separates.
    if fit is not None:
        p = predict_row(fit["b_pen"], keys, False, 0, None)
    return dict(p=p, boot_lo=lo, boot_hi=hi, stratum_n=n, stratum_k=k,
                stratum_med=med, stratum_lo=blo, stratum_hi=bhi,
                n=None if fit is None else fit["n"], r2=None if fit is None else fit["nagelkerke"],
                aic=None if fit is None else fit["aic"], stable=None if fit is None else fit["stable"])


def vote_conditional(df, y, keys):
    """Approval given the vote, with and without the selected factors."""
    rows = {}
    for keyset in ([], keys):
        fit = refit(df, keyset, y, True)
        if fit is None:
            continue
        rec = dict(n=fit["n"], r2=fit["nagelkerke"], aic=fit["aic"], stable=fit["stable"])
        for vote, name in ((1, "favourable"), (0, "unfavourable")):
            rec[name] = predict_row(fit["b_pen"], keyset, True, 0, vote)
            lo, hi = boot_pred(df, keyset, y, True, 0, vote)
            rec[name + "_lo"] = lo
            rec[name + "_hi"] = hi
            n, k, med, blo, bhi = stratum_beta(df, keyset, y, 0, vote)
            rec[name + "_stratum"] = dict(n=n, k=k, med=med, lo=blo, hi=bhi)
        rows["+".join(keyset) or "(vote only)"] = rec
    return rows


def bounds_disagree(a, b):
    """True when the two filled-in samples do not support the same conclusion."""
    return bool((a["fisher_p"] < 0.05) != (b["fisher_p"] < 0.05) or (a["log_odds"] > 0) != (b["log_odds"] > 0))


def priority_sensitivity(frame, y):
    """Recorded review type, then the blanks filled as standard and as priority."""
    as_std = frame.copy()
    as_pri = frame.copy()
    as_std["pri"] = as_std["pri"].fillna(0.0)
    as_pri["pri"] = as_pri["pri"].fillna(1.0)
    blank = frame[frame.pri.isna()]
    kept = frame.dropna(subset=["pri"])
    others = {}
    for col, key, _lab in FACTORS:
        if key == "priority":
            continue
        others[key] = one(kept, col, y)
    return dict(
        recorded=one(frame, "pri", y),
        blanks_as_standard=one(as_std, "pri", y),
        blanks_as_priority=one(as_pri, "pri", y),
        n_blank=int(len(blank)),
        blank_events=int(blank[y].sum()) if len(blank) else 0,
        n_recorded=int(len(kept)),
        recorded_events=int(kept[y].sum()) if len(kept) else 0,
        others_on_recorded=others,
    )


def main():
    m = prepare(pd.read_csv("adcom_full_pivotal.csv", dtype=str).fillna(""))
    gate(m, pd.read_csv("two_by_two.csv"))
    base = m[(~m.replaced) & m.fav.notna()].copy()
    # Approval or benefit-risk, plus effectiveness. Restriction questions stay out.
    wide = base[base.vote_type.isin(["approval/benefit-risk", "effectiveness-only"])].copy()
    wide["y_fav"] = wide.fav
    known = wide[wide.approved.notna()].copy()
    known["y_app"] = known.approved.astype(float)
    known["y_fav"] = known.fav
    appr = base[base.vote_type == "approval/benefit-risk"].copy()
    appr_known = appr[appr.approved.notna()].copy()
    appr_known["y_app"] = appr_known.approved.astype(float)
    appr_known["y_fav"] = appr_known.fav

    payload = {}
    payload["n_base"] = int(len(base))
    payload["n_vote"] = int(len(wide))
    payload["n_known"] = int(len(known))
    payload["n_restriction"] = int((base.vote_type == "restriction/other").sum())
    payload["n_approval_questions"] = int(len(appr))
    payload["vote_type_counts"] = wide.vote_type.value_counts().to_dict()
    payload["vote_tiers"] = wide.vote_source_tier.value_counts().to_dict()
    payload["outcome_tiers"] = known.outcome_source_tier.value_counts().to_dict()
    payload["base_fav"] = dict(n=int(len(wide)), k=int(wide.y_fav.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(wide.y_fav.sum()), int(len(wide))))))
    payload["base_app"] = dict(n=int(len(known)), k=int(known.y_app.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(known.y_app.sum()), int(len(known))))))
    fav_yes = known[known.y_fav == 1]
    fav_no = known[known.y_fav == 0]
    payload["app_given_fav"] = dict(n=int(len(fav_yes)), k=int(fav_yes.y_app.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(fav_yes.y_app.sum()), int(len(fav_yes))))))
    payload["app_given_unfav"] = dict(n=int(len(fav_no)), k=int(fav_no.y_app.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(fav_no.y_app.sum()), int(len(fav_no))))))

    screens = {}
    frames = {"favourable": wide, "approval": known}
    ys = {"favourable": "y_fav", "approval": "y_app"}
    for name in ("favourable", "approval"):
        screens[name] = screen_frame(frames[name], ys[name])
    sens = {name: priority_sensitivity(frames[name], ys[name]) for name in frames}
    vote_bounds = bounds_disagree(sens["favourable"]["blanks_as_standard"], sens["favourable"]["blanks_as_priority"])
    flipped = []
    for r in screens["favourable"]:
        if r["factor"] == "priority" or not (r["fisher_p"] < 0.05):
            continue
        other = sens["favourable"]["others_on_recorded"][r["factor"]]
        if not (other["fisher_p"] < 0.05):
            flipped.append(r["factor"])
    use_priority = (not vote_bounds) and (not flipped)
    selected = []
    for r in screens["favourable"]:
        if r["fisher_p"] < 0.05 and (r["factor"] != "priority" or use_priority):
            selected.append(r["factor"])
    without_priority = [key for _c, key, _l in FACTORS if key != "priority"]
    all_factors = [key for _c, key, _l in FACTORS]
    three = ["orphan", "opioid", "CGT"]
    payload["priority_sensitivity"] = sens
    payload["priority_decision"] = dict(
        use_in_joint=use_priority,
        vote_bounds_disagree=vote_bounds,
        factors_lost_on_recorded_sample=flipped,
        selected=selected,
    )

    joints = {}
    conds = {}
    boots = {}
    preds = {}
    for name in ("favourable", "approval"):
        y = ys[name]
        frame = frames[name]
        joints[name] = {
            "selected": joint_fit(frame, selected, y),
            "without_priority": joint_fit(frame, without_priority, y),
            "all_factors": joint_fit(frame, all_factors, y),
            "orphan_cgt": joint_fit(frame, ["orphan", "CGT"], y),
            "three": joint_fit(frame, three, y),
        }
        same = frame.dropna(subset=[COL[k] for k in selected] + [y]) if selected else frame.dropna(subset=[y])
        joints[name]["alone_on_joint_sample"] = {key: one(same, COL[key], y) for key in selected}
        same3 = frame.dropna(subset=[COL[k] for k in three] + [y])
        joints[name]["alone_on_three"] = {key: one(same3, COL[key], y) for key in three}
        conds[name] = conditional_fisher(frame, y)
        boots[name] = boot_coefs(frame, selected, y) if selected else {}
        boots[name + "_three"] = boot_coefs(frame, three, y)
        preds[name] = {
            "orphan": prediction_block(frame, y, ["orphan"]),
            "selected": prediction_block(frame, y, selected),
            "three": prediction_block(frame, y, three),
            "intercept": prediction_block(frame, y, []),
        }
    payload["screens"] = screens
    payload["joints"] = joints
    payload["conditional"] = conds
    payload["joint_boot"] = boots
    payload["predictions"] = preds
    payload["vote_conditional"] = vote_conditional(known, "y_app", selected)
    payload["vote_conditional_three"] = vote_conditional(known, "y_app", three)

    idx = known[known.index_approved.notna()].copy()
    idx["y_idx"] = idx.index_approved.astype(float)
    payload["one_year"] = dict(
        n=int(len(idx)), k=int(idx.y_idx.sum()),
        screen=screen_frame(idx, "y_idx"),
        selected=joint_fit(idx, selected, "y_idx"),
        pred_orphan=prediction_block(idx, "y_idx", ["orphan"]),
        pred_selected=prediction_block(idx, "y_idx", selected),
        conditional=conditional_fisher(idx, "y_idx"),
    )
    both = known.dropna(subset=["index_approved"])
    payload["label_disagree"] = dict(
        n=int(len(both)),
        disagree=int((both.approved.astype(bool) != both.index_approved.astype(bool)).sum()),
    )

    # Approval questions alone, and every pivotal vote including restriction
    # questions. Sensitivities. The main screen is the block above.
    payload["approval_only"] = {}
    for y, name in (("y_fav", "favourable"), ("y_app", "approval")):
        payload["approval_only"][name] = dict(
            n=int(len(appr_known.dropna(subset=[y]))),
            screen=screen_frame(appr_known, y),
            selected_fit=joint_fit(appr_known, selected, y),
            conditional=conditional_fisher(appr_known, y),
            pred_selected=prediction_block(appr_known, y, selected),
            pred_orphan=prediction_block(appr_known, y, ["orphan"]),
        )

    piv = base[base.approved.notna()].copy()
    piv["y_app"] = piv.approved.astype(float)
    piv["y_fav"] = piv.fav
    payload["all_pivotal"] = {}
    for y, name in (("y_fav", "favourable"), ("y_app", "approval")):
        payload["all_pivotal"][name] = dict(
            n=int(len(piv.dropna(subset=[y]))),
            screen=screen_frame(piv, y),
            selected_fit=joint_fit(piv, selected, y),
            conditional=conditional_fisher(piv, y),
            pred_selected=prediction_block(piv, y, selected),
        )

    # Year term on the two-factor model.
    year_notes = {}
    for y, name in (("y_fav", "favourable"), ("y_app", "approval")):
        base_fit = refit(known, selected, y, False)
        yr_fit = refit(known, selected, y, False, extra=("year_c",))
        year_notes[name] = dict(
            aic=None if base_fit is None else base_fit["aic"],
            aic_year=None if yr_fit is None else yr_fit["aic"],
            r2_year=None if yr_fit is None else yr_fit["nagelkerke"],
            stable=None if yr_fit is None else yr_fit["stable"],
        )
    payload["year"] = year_notes

    # Name the meetings in the orphan and cell-and-gene-therapy cell.
    cell = known.dropna(subset=["orphan_y", "cgt"])
    cell = cell[(cell.orphan_y == 1) & (cell.cgt == 1)]
    names = []
    for _, r in cell.sort_values("meeting_date").iterrows():
        label = r.brand or r.generic or r.product_text
        names.append(dict(
            date=r.meeting_date, committee=r.committee, app=r.app, name=label,
            vote=r.adcom, yes=r.vote_yes, no=r.vote_no, vote_type=r.vote_type, final=r.final_action,
            priority=r.review_priority, vote_tier=r.vote_source_tier, outcome_tier=r.outcome_source_tier,
        ))
    payload["cgt_orphan_rows"] = names

    # Priority missingness composition, for the discussion.
    miss = known[known.pri.isna()]
    payload["priority_missing"] = dict(
        n=int(len(miss)),
        favourable=int(miss.y_fav.sum()),
        approved=int(miss.y_app.sum()),
        orphan=int((miss.orphan_y == 1).sum()),
        orphan_recorded=int(miss.orphan_y.notna().sum()),
        cgt=int((miss.cgt == 1).sum()),
        cns=int((miss.cns == 1).sum()),
        cber=int((miss.cber_i == 1).sum()),
        opioid=int((miss.opioid_i == 1).sum()),
    )

    def conv(o):
        if isinstance(o, dict):
            return {k: conv(v) for k, v in o.items()}
        if isinstance(o, list):
            return [conv(v) for v in o]
        if isinstance(o, (np.floating, float)):
            if o != o or np.isinf(o):
                return None
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o

    clean = conv(payload)
    with open("amt130_factor_compare.json", "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)

    flat = []
    for name, rows in screens.items():
        for r in rows:
            flat.append(dict(outcome=name, **{k: r[k] for k in r if k != "outcome"}))
    pd.DataFrame(flat).to_csv("amt130_one_at_a_time.csv", index=False)

    legend = "Joint model: " + ", ".join(LABEL[k] for k in selected) if selected else "No factor cleared the vote screen"
    draw(screens, joints, boots, joint_name="selected", legend=legend)
    print("wrote amt130_factor_compare.json")
    brief(clean)


def draw(screens, joints, boots, joint_name="selected", legend="Joint model"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    order = [key for _, key, _ in FACTORS]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.15), sharey=True)
    titles = {"favourable": "Favourable vote", "approval": "FDA approval"}
    for ax, name in zip(axes, ("favourable", "approval")):
        by = {r["factor"]: r for r in screens[name]}
        joint = joints[name][joint_name]["log_odds"]
        jboot = boots[name]
        ypos = np.arange(len(order))[::-1]
        ax.axvline(0, color="0.75", lw=0.8, zorder=0)
        for y, key in zip(ypos, order):
            r = by[key]
            ax.plot([r["boot_lo"], r["boot_hi"]], [y, y], color="0.45", lw=1.2, zorder=1)
            ax.plot(r["log_odds"], y, "o", color="0.1", ms=6, zorder=2)
            if key in joint:
                lo, hi, _ = jboot[key]
                ax.plot([lo, hi], [y - 0.18, y - 0.18], color="0.15", lw=1.2, zorder=1)
                ax.plot(joint[key], y - 0.18, "s", color="white", markeredgecolor="0.1",
                        markeredgewidth=1.1, ms=6, zorder=3)
        ax.set_yticks(ypos)
        ax.set_yticklabels([LABEL[key] for key in order], fontsize=8)
        ax.set_xlabel("Penalized log-odds", fontsize=9)
        ax.set_title(titles[name], fontsize=11)
    xs = []
    for name in ("favourable", "approval"):
        for r in screens[name]:
            xs.extend([r["boot_lo"], r["boot_hi"], r["log_odds"]])
        for lo, hi, _n in boots[name].values():
            xs.extend([lo, hi])
    finite = [x for x in xs if x == x]
    pad = 0.2
    xlim = (min(-0.4, min(finite) - pad), max(0.4, max(finite) + pad))
    for ax in axes:
        ax.set_xlim(*xlim)
        ax.tick_params(axis="x", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="0.1", markeredgecolor="0.1",
               ms=6, label="One factor at a time"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor="white", markeredgecolor="0.1",
               markeredgewidth=1.1, ms=6, label=legend),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    os.makedirs(CHART, exist_ok=True)
    path = os.path.join(CHART, "amt130_factor_compare.png")
    fig.savefig(path, dpi=150)
    plt.close()
    print("wrote", path)


def brief(p):
    def f(x, nd=2):
        if x is None:
            return "NA"
        return f"{x:.{nd}f}"

    print("--- base", p["base_fav"]["k"], "/", p["base_fav"]["n"], p["base_app"]["k"], "/", p["base_app"]["n"])
    for name in ("favourable", "approval"):
        print("==", name)
        for r in p["screens"][name]:
            print(f"  {r['factor']:10} n={r['n']:3} yes {r['yes_event']}/{r['yes_n']} no {r['no_event']}/{r['no_n']} "
                  f"phi={f(r['phi'], 3)} b={f(r['log_odds'])} boot {f(r['boot_lo'])}-{f(r['boot_hi'])} "
                  f"fisher={f(r['fisher_p'], 4)} stable={r['stable']} lr_p={f(r['lr_p'], 4)} R2={f(r['nagelkerke'], 3)}")
        chosen = p["joints"][name]["selected"]
        print("  JOINT", chosen["factors"], chosen["n"], "stable", chosen["stable"], "R2", f(chosen["nagelkerke"], 3),
              "AIC", f(chosen["aic"], 1), "b", {k: f(v) for k, v in chosen["log_odds"].items()}, "drop", chosen["drop"])
        wide_fit = p["joints"][name]["without_priority"]
        print("  WITHOUT PRIORITY n", wide_fit["n"], "stable", wide_fit["stable"], "R2", f(wide_fit["nagelkerke"], 3),
              "b", {k: f(v) for k, v in wide_fit["log_odds"].items()})
        every = p["joints"][name]["all_factors"]
        print("  ALL n", every["n"], "stable", every["stable"], "R2", f(every["nagelkerke"], 3),
              "b", {k: f(v) for k, v in every["log_odds"].items()})
        c = p["conditional"][name]
        print("  CGT|orphan", c["cgt_among_orphan"])
        print("  orphan|nonCGT", c["orphan_among_non_cgt"], "cgt_not_orphan", c["cgt_not_orphan"],
              "both", c["both_events"], "/", c["both_n"])
        pr = p["predictions"][name]
        print("  PRED orphan", {k: f(pr["orphan"][k]) if isinstance(pr["orphan"][k], float) else pr["orphan"][k] for k in ("p", "boot_lo", "boot_hi", "stratum_n", "stratum_k", "stratum_lo", "stratum_hi", "r2", "aic", "stable")})
        print("  PRED selected", {k: f(pr["selected"][k]) if isinstance(pr["selected"][k], float) else pr["selected"][k] for k in ("p", "boot_lo", "boot_hi", "stratum_n", "stratum_k", "stratum_lo", "stratum_hi", "r2", "aic", "stable")})
        three = p["joints"][name]["three"]
        print("  THREE", three["factors"], three["n"], "stable", three["stable"], "R2", f(three["nagelkerke"], 3),
              "AIC", f(three["aic"], 1), "b", {k: f(v) for k, v in three["log_odds"].items()}, "drop", three["drop"])
        print("  PRED three", {k: f(pr["three"][k]) if isinstance(pr["three"][k], float) else pr["three"][k] for k in ("p", "boot_lo", "boot_hi", "stratum_n", "stratum_k", "stratum_lo", "stratum_hi", "r2", "aic", "stable")})
        print("  THREE boot", {k: (f(lo), f(hi), n) for k, (lo, hi, n) in p["joint_boot"][name + "_three"].items()})
        same = p["joints"][name]["alone_on_joint_sample"]
        print("  ALONE on joint n", {k: (v["n"], f(v["log_odds"]), f(v["fisher_p"], 4)) for k, v in same.items()})
        alone3 = p["joints"][name]["alone_on_three"]
        print("  ALONE on three", {k: (v["n"], v["yes_event"], v["yes_n"], v["no_event"], v["no_n"], f(v["log_odds"]), f(v["fisher_p"], 4)) for k, v in alone3.items()})
    print("vote conditional", json.dumps(p["vote_conditional"], default=str)[:2000])
    print("vote conditional three", json.dumps(p["vote_conditional_three"], default=str)[:2000])
    print("priority decision", p["priority_decision"])
    for name in ("favourable", "approval"):
        s = p["priority_sensitivity"][name]
        print(" sensitivity", name,
              "recorded", s["recorded"]["yes_event"], "/", s["recorded"]["yes_n"], "vs", s["recorded"]["no_event"], "/", s["recorded"]["no_n"],
              "p", f(s["recorded"]["fisher_p"], 4),
              "as standard", s["blanks_as_standard"]["yes_event"], "/", s["blanks_as_standard"]["yes_n"], "vs",
              s["blanks_as_standard"]["no_event"], "/", s["blanks_as_standard"]["no_n"], "p", f(s["blanks_as_standard"]["fisher_p"], 4),
              "b", f(s["blanks_as_standard"]["log_odds"]),
              "as priority", s["blanks_as_priority"]["yes_event"], "/", s["blanks_as_priority"]["yes_n"], "vs",
              s["blanks_as_priority"]["no_event"], "/", s["blanks_as_priority"]["no_n"], "p", f(s["blanks_as_priority"]["fisher_p"], 4),
              "b", f(s["blanks_as_priority"]["log_odds"]),
              "blank", s["blank_events"], "/", s["n_blank"], "recorded events", s["recorded_events"], "/", s["n_recorded"])
    print("priority missing", p["priority_missing"])
    print("disagree", p["label_disagree"])
    print("year", p["year"])
    print("one year n", p["one_year"]["n"], p["one_year"]["k"], "selected", p["one_year"]["selected"]["log_odds"],
          "pred", p["one_year"]["pred_selected"]["p"], p["one_year"]["pred_orphan"]["p"])
    print("tiers", p["vote_tiers"], p["outcome_tiers"])
    print("CGT rows:")
    for row in p["cgt_orphan_rows"]:
        print(" ", row)
    print("all pivotal fisher:")
    for name in ("favourable", "approval"):
        block = p["all_pivotal"][name]
        print(" ", name, "n", block["n"], "selected", block["selected_fit"]["log_odds"], "stable", block["selected_fit"]["stable"],
              "pred", block["pred_selected"]["p"], "cond", block["conditional"]["cgt_among_orphan"]["fisher_p"],
              block["conditional"]["orphan_among_non_cgt"]["fisher_p"])
        for r in block["screen"]:
            print(f"    {r['factor']:10} {r['yes_event']}/{r['yes_n']} vs {r['no_event']}/{r['no_n']} p={r['fisher_p']:.4f} b={r['log_odds']:.2f} phi={r['phi']:.3f}")


if __name__ == "__main__":
    main()
