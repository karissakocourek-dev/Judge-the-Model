"""Starter app for Streamlit Community Cloud: three plain sections that read results/ and show correct numbers.

Run locally:  bash run_app.sh  (your agent writes it; it runs streamlit run streamlit_app.py)
Build each section up to its required minimum (see the activity website). Keep every number
coming from m11.py, and label every table and plot "Training" or "Test".
"""

import pandas as pd
import streamlit as st

import m11

TRAIN = "Training"
TEST = "Test"
SECTIONS = ["1. Beyond Accuracy", "2. A Threshold for the Job", "3. Training vs. Test"]

st.set_page_config(page_title="Judge the Model", layout="wide")

# Model names as displayed, with a capital first letter (e.g. "K-nearest neighbours"); m11.py stays unchanged.
LABEL = {k: v[:1].upper() + v[1:] for k, v in m11.MODEL_LABEL.items()}


@st.cache_data
def load(name: str):
    return m11.load(name)


def starter_note(text: str) -> None:
    st.info(f"Starter display: {text} Build this section up to its required minimum.")


def recommendations() -> None:
    d = load("decisions")
    recs = (d or {}).get("recommendations", {})
    with st.container(border=True):
        st.subheader("Recommendations")
        if not any(recs.values()):
            st.caption("No recommendations yet: fill in `Recommendations` in DECISIONS.md, run "
                       "`python -m analysis`, then commit and push.")
        for k in m11.DATASETS:
            if any(recs.values()):
                st.markdown(f"**{m11.DATASET_LABEL[k]}:** {recs.get(k) or '_not written yet_'}")


# ---- Plain-language wording for each dataset ---------------------------------
# Text only (copied from the data dictionary, data/datasets.json); every number comes from m11.
WORDS = {
    "readmission": {
        "one": "patient", "many": "patients",
        "positive": "Readmitted within 30 days", "negative": "Not readmitted within 30 days",
        "had": "were readmitted within 30 days", "had_not": "were not readmitted within 30 days",
    },
    "diabetes": {
        "one": "adult", "many": "adults",
        "positive": "Diabetes (doctor diagnosis or HbA1c ≥ 6.5%)", "negative": "No diabetes by this label",
        "had": "have diabetes by this label", "had_not": "do not have diabetes by this label",
    },
}
# The four groups of patients in a confusion matrix.
GROUPS = {"tp": "Correctly flagged", "fn": "Missed", "fp": "False alarm", "tn": "Correctly not flagged"}

st.markdown("""
<style>
.cm { border-collapse: collapse; width: 100%; margin: 0.25rem 0 0.5rem; }
.cm th, .cm td { border: 1px solid rgba(128,128,128,0.35); padding: 0.45rem 0.6rem; text-align: center; }
.cm th { font-weight: 600; font-size: 0.85rem; }
.cm td.ok  { background: rgba(46,160,67,0.16); }
.cm td.bad { background: rgba(218,54,51,0.16); }
.cm .n { font-size: 1.35rem; font-weight: 700; }
.cm .g { font-size: 0.8rem; opacity: 0.85; }
.cm.small th, .cm.small td { padding: 0.25rem 0.3rem; font-size: 0.78rem; }
.cm.small .n { font-size: 1rem; }
.cm-wrap.sel { outline: 2px solid rgba(255,140,0,0.9); outline-offset: 3px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


def confusion_html(c: dict, key: str, t: float, small: bool = False) -> str:
    """A confusion matrix as an HTML table: rows = actual, columns = predicted. Counts from m11.confusion."""
    w = WORDS[key]

    def cell(k: str) -> str:
        css = "ok" if k in ("tp", "tn") else "bad"
        label = k.upper() if small else f"{k.upper()} · {GROUPS[k]}"
        return f"<td class='{css}'><div class='n'>{c[k]:,}</div><div class='g'>{label}</div></td>"

    if small:
        head, pos_row, neg_row = ("Pred. +", "Pred. −"), "Actual +", "Actual −"
    else:
        head = (f"Predicted: flagged (≥ {t:.2f})", f"Predicted: not flagged (< {t:.2f})")
        pos_row, neg_row = f"Actual: {w['positive']}", f"Actual: {w['negative']}"
    return (f"<table class='cm{' small' if small else ''}'>"
            f"<tr><th></th><th>{head[0]}</th><th>{head[1]}</th></tr>"
            f"<tr><th>{pos_row}</th>{cell('tp')}{cell('fn')}</tr>"
            f"<tr><th>{neg_row}</th>{cell('fp')}{cell('tn')}</tr></table>")


# ---- 1. Beyond Accuracy ------------------------------------------------------
def beyond_accuracy(res: dict, model: str) -> None:
    t = 0.5
    key = res["dataset"]
    w = WORDS[key]
    p, y = m11.preds(res, model)            # Test probabilities and true outcomes
    c = m11.confusion(p, y, t)
    m = m11.metrics(c)
    name = LABEL[model]

    st.markdown(f"**Positive class:** {w['positive']}. A {w['one']} is *flagged* (predicted positive) "
                f"when the model's probability is at least {t:.2f}.")

    left, right = st.columns([3, 2], gap="large")
    with left:
        with st.container(border=True):
            st.markdown(f"**{TEST} · {name} · threshold {t:.2f}**")
            st.caption(f"Confusion matrix of the {m['n']:,} test {w['many']}: rows = actual, columns = predicted. "
                       "Green cells are correct, red cells are errors.")
            st.markdown(confusion_html(c, key, t), unsafe_allow_html=True)
            cols = st.columns(3)
            with cols[0]:
                st.metric(f"Sensitivity ({TEST})", m11.fmt_pct(m["sensitivity"]))
                st.caption(f"Of the {m['positives']:,} test {w['many']} who {w['had']}, the share flagged "
                           f"({c['tp']:,} of {m['positives']:,}).")
            with cols[1]:
                st.metric(f"Specificity ({TEST})", m11.fmt_pct(m["specificity"]))
                st.caption(f"Of the {m['negatives']:,} test {w['many']} who {w['had_not']}, the share not flagged "
                           f"({c['tn']:,} of {m['negatives']:,}).")
            with cols[2]:
                st.metric(f"Precision ({TEST})", m11.fmt_pct(m["precision"]))
                st.caption(f"Of the {m['flagged']:,} test {w['many']} flagged, the share who {w['had']} "
                           f"({c['tp']:,} of {m['flagged']:,}).")

    with right:
        with st.container(border=True):
            st.markdown(f"**Why accuracy alone misleads ({TEST})**")
            st.metric("Prevalence", m11.fmt_pct(m["prevalence"]))
            st.caption(f"{m['positives']:,} of {m['n']:,} test {w['many']} {w['had']}.")
            majority = w["negative"] if m["negatives"] >= m["positives"] else w["positive"]
            st.metric("Baseline accuracy: the most common class for everyone", m11.fmt_pct(m11.majority_accuracy(y)))
            st.caption(f"Calling every test {w['one']} “{majority}”, without looking at anyone, is right this often.")
            st.metric(f"{name} accuracy", m11.fmt_pct(m["accuracy"]))
            st.caption(f"Of all {m['n']:,} test {w['many']}, the share the model got right. Compare it with the "
                       f"baseline above: when most {w['many']} are in one class, high accuracy can come from simply predicting that class, "
                       "so check sensitivity too.")

    st.subheader(f"All five models at threshold {t:.2f} ({TEST})")
    tab_mx, tab_tbl = st.tabs(["Confusion matrices", "Metrics table"])
    models = [k for k in m11.MODELS if k in res["models"]]
    rows = []
    with tab_mx:
        st.caption(f"{TEST} · Each model at threshold {t:.2f}. Rows = actual, columns = predicted. "
                   "TP = correctly flagged, FN = missed, FP = false alarm, TN = correctly not flagged. "
                   "The selected model has an orange outline.")
        for col, k in zip(st.columns(len(models)), models):
            ck = m11.confusion(*m11.preds(res, k), t)
            with col:
                st.markdown(f"**{LABEL[k]}**  \n<small>{TEST}</small>", unsafe_allow_html=True)
                st.markdown(f"<div class='cm-wrap{' sel' if k == model else ''}'>{confusion_html(ck, key, t, small=True)}</div>",
                            unsafe_allow_html=True)
    for k in models:
        mk = m11.metrics(m11.confusion(*m11.preds(res, k), t))
        rows.append({
            "Model": ("▸ " if k == model else "") + LABEL[k],
            "Accuracy": m11.fmt_pct(mk["accuracy"]),
            "Sensitivity (recall, TPR)": m11.fmt_pct(mk["sensitivity"]),
            "Specificity": m11.fmt_pct(mk["specificity"]),
            "FPR (1 − specificity)": m11.fmt_pct(mk["fpr"]),
            "Precision": m11.fmt_pct(mk["precision"]),
            "F1": m11.fmt_num(mk["f1"], 2),
        })
    with tab_tbl:
        st.caption(f"{TEST} · Every model at threshold {t:.2f}. The ▸ marks the selected model.")
        st.table(pd.DataFrame(rows).set_index("Model"))
        st.caption(f"Sensitivity: of the test {w['many']} who {w['had']}, the share flagged. "
                   f"Specificity: of those who {w['had_not']}, the share not flagged. "
                   f"FPR: of those who {w['had_not']}, the share flagged (false alarms). "
                   f"Precision: of the {w['many']} flagged, the share who {w['had']}. "
                   "F1 combines precision and sensitivity into one score from 0 to 1. "
                   "“undefined” means the share has nothing to divide by (0 ÷ 0), e.g. precision when no one is flagged.")


# ---- 2. A Threshold for the Job ------------------------------------------------
def threshold_panel(c: dict, key: str, t: float, title: str) -> None:
    """One column of the comparison: the Test confusion matrix and its metrics at threshold t (all from m11)."""
    w = WORDS[key]
    m = m11.metrics(c)
    with st.container(border=True):
        st.markdown(f"**{TEST} · {title}**")
        st.metric(f"Flagged per 100 ({TEST})", m11.fmt_num(m["flagged_per_100"], 1))
        st.caption(f"Of every 100 test {w['many']}, how many the model flags ({m['flagged']:,} of {m['n']:,}).")
        st.markdown(confusion_html(c, key, t), unsafe_allow_html=True)
        a, b = st.columns(2)
        with a:
            st.metric(f"Sensitivity ({TEST})", m11.fmt_pct(m["sensitivity"]))
            st.caption(f"Of the {m['positives']:,} who {w['had']}, the share flagged ({c['tp']:,}).")
            st.metric(f"Precision ({TEST})", m11.fmt_pct(m["precision"]))
            st.caption(f"Of the {m['flagged']:,} flagged, the share who {w['had']} ({c['tp']:,}).")
        with b:
            st.metric(f"Specificity ({TEST})", m11.fmt_pct(m["specificity"]))
            st.caption(f"Of the {m['negatives']:,} who {w['had_not']}, the share not flagged ({c['tn']:,}).")
            st.metric(f"Accuracy ({TEST})", m11.fmt_pct(m["accuracy"]))
            st.caption(f"Of all {m['n']:,} test {w['many']}, the share the model got right.")


def threshold(res: dict, model: str) -> None:
    key = res["dataset"]
    w = WORDS[key]
    p, y = m11.preds(res, model)            # Test probabilities and true outcomes: the same at every threshold
    name = LABEL[model]

    t = st.slider("Threshold: flag a test patient when the model's probability is at least this value",
                  min_value=0.0, max_value=1.0, value=0.5, step=0.01, format="%.2f", key="threshold")
    st.info(f"Moving the slider changes **no probability and no AUROC, only who is flagged**. Each test {w['one']}'s "
            f"probability from {name} stays the same; the slider only moves the cut-off line. "
            f"The {TEST} AUROC of {name} is {m11.fmt_num(m11.auroc(p, y))} at every threshold, because AUROC describes "
            f"how well the model ranks {w['many']}, not where the line is drawn.")
    st.caption(f"Positive class: {w['positive']}. A lower threshold flags more {w['many']}: it finds more who "
               f"{w['had']}, and raises more false alarms. A higher threshold does the reverse.")

    left, right = st.columns(2, gap="large")
    with left:
        threshold_panel(m11.confusion(p, y, 0.5), key, 0.5, f"{name} · at the usual threshold 0.50")
    with right:
        threshold_panel(m11.confusion(p, y, t), key, t, f"{name} · at your threshold {t:.2f}")


# ---- 3. Training vs. Test ------------------------------------------------------
def train_vs_test(res: dict, model: str) -> None:
    starter_note("training and test AUROC of every model, in a table.")
    s = m11.auroc_summary(res)
    rows = [{"Model": LABEL[m], f"{TRAIN} AUROC": m11.fmt_num(v["train"]), f"{TEST} AUROC": m11.fmt_num(v["test"])}
            for m, v in s.items()]
    st.caption(f"{TRAIN} and {TEST} · AUROC on the rows each model learned from, and on rows it never saw")
    st.table(pd.DataFrame(rows).set_index("Model"))


RENDER = dict(zip(SECTIONS, [beyond_accuracy, threshold, train_vs_test]))

st.title("Judge the Model")
st.caption("Which classifier would you trust for this job, at what threshold, and with what limits?")
recommendations()
section = st.sidebar.radio("Section", SECTIONS)
key = st.sidebar.selectbox("Dataset", m11.DATASETS, format_func=m11.DATASET_LABEL.get)
res = load(key)
model = st.sidebar.selectbox("Model", m11.MODELS,
                             format_func=lambda m: LABEL[m] + ("" if m in res["models"] else " (not trained yet)"))
st.header(section)
st.caption(f"{m11.DATASET_LABEL[key]}: {res['train']['n']:,} training rows ({res['train']['n_pos']:,} positive), "
           f"{res['test']['n']:,} test rows ({res['test']['n_pos']:,} positive).")
if model in res["models"]:
    RENDER[section](res, model)
else:
    st.warning(f"{LABEL[model]} has no results yet: run `python -m analysis`, then commit and push `results/`.")
