"""Afficionado Coffee Roasters - Sales Trend & Time-Based Performance Dashboard.
Run:  pip install -r requirements.txt  &&  streamlit run app.py
"""
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Afficionado Coffee Roasters | Time Analytics", page_icon="☕", layout="wide")
DEFAULT_FILE = os.path.join(os.path.dirname(__file__), "Afficionado_Coffee_Roasters_Cleaned.xlsx")
DOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
COLORS = {"Astoria": "#8c5a3c", "Hell's Kitchen": "#2e6f6a", "Lower Manhattan": "#d08c2e"}


@st.cache_data(show_spinner="Loading and preparing data...")
def load(src, start_date):
    df = pd.read_excel(src)
    # --- validation ---
    checks = {
        "Missing values": int(df.isna().sum().sum()),
        "Duplicate transaction IDs": int(df.transaction_id.duplicated().sum()),
        "Non-positive quantity/price": int(((df.transaction_qty <= 0) | (df.unit_price <= 0)).sum()),
    }
    t = pd.to_timedelta(df.transaction_time.astype(str))
    # The file has no calendar date. Rows are chronological, so each time-of-day reset = new trading day.
    df["day_idx"] = (t.diff() < pd.Timedelta(0)).cumsum()
    df["date"] = pd.Timestamp(start_date) + pd.to_timedelta(df.day_idx, unit="D")
    df["hour"] = (t.dt.total_seconds() // 3600).astype(int)
    df["dow"] = pd.Categorical(df.date.dt.day_name(), DOW, ordered=True)
    df["revenue"] = df.transaction_qty * df.unit_price
    df["bucket"] = pd.cut(df.hour, [-1, 5, 11, 16, 21, 23],
                          labels=["Late (22-5)", "Morning (6-11)", "Afternoon (12-16)", "Evening (17-21)", "Late (22-5)"],
                          ordered=False)
    df["week"] = df.date.dt.to_period("W-SUN").dt.start_time
    return df, checks


# ---------------- sidebar ----------------
st.sidebar.title("☕ Filters")
up = st.sidebar.file_uploader("Upload dataset (optional)", type="xlsx")
with st.sidebar.expander("Date assumption"):
    st.caption("The dataset has no date column. Days are rebuilt from time-of-day resets; "
               "set the first day below (brief states year 2025).")
    start = st.date_input("First trading day", pd.Timestamp("2025-01-01"))
df, checks = load(up if up else DEFAULT_FILE, str(start))

stores = st.sidebar.multiselect("Store location", sorted(df.store_location.unique()), default=sorted(df.store_location.unique()))
days = st.sidebar.multiselect("Day of week", DOW, default=DOW)
hr = st.sidebar.slider("Hour range", 0, 23, (6, 20))
metric = st.sidebar.radio("Metric", ["Revenue", "Quantity"], horizontal=True)
col, unit = ("revenue", "Revenue ($)") if metric == "Revenue" else ("transaction_qty", "Units sold")

f = df[df.store_location.isin(stores) & df.dow.isin(days) & df.hour.between(*hr)]
if f.empty:
    st.warning("No data for the selected filters."); st.stop()

st.title("Sales Trend & Time-Based Performance")
st.caption(f"{f.date.min():%d %b %Y} - {f.date.max():%d %b %Y} | {len(f):,} transactions | filters apply to every tab")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Day of week", "Hourly heatmaps", "Location comparison", "Data quality"])

# ---------------- overview ----------------
with tab1:
    c = st.columns(4)
    c[0].metric("Revenue", f"${f.revenue.sum():,.0f}")
    c[1].metric("Transactions", f"{len(f):,}")
    c[2].metric("Units sold", f"{f.transaction_qty.sum():,}")
    c[3].metric("Avg ticket", f"${f.revenue.sum() / len(f):.2f}")
    d = f.groupby("date")[col].sum().reset_index()
    d["7-day avg"] = d[col].rolling(7, center=True).mean()
    fig = px.line(d, x="date", y=[col, "7-day avg"], labels={"value": unit, "variable": ""}, title="Daily trend")
    fig.update_traces(selector=dict(name=col), line=dict(color="#c9b8a8", width=1))
    fig.update_traces(selector=dict(name="7-day avg"), line=dict(color="#5a3825", width=3))
    st.plotly_chart(fig)
    full = f[(f.week >= f.week.min() + pd.Timedelta(days=7 * (f.date.min().weekday() != 0))) & (f.week < f.week.max())]
    w = full.groupby(["week", "store_location"])[col].sum().reset_index()
    st.plotly_chart(px.line(w, x="week", y=col, color="store_location", color_discrete_map=COLORS,
                            labels={col: unit, "store_location": "Store"}, title="Weekly trend by store (complete weeks)"))
    m = f.groupby(f.date.dt.to_period("M").astype(str))[col].sum().reset_index()
    st.plotly_chart(px.bar(m, x="date", y=col, labels={"date": "Month", col: unit}, title="Monthly total",
                           color_discrete_sequence=["#8c5a3c"]))

# ---------------- day of week ----------------
with tab2:
    dd = f.groupby(["date", "dow"], observed=True).agg(v=(col, "sum"), n=("transaction_id", "count")).reset_index()
    g = dd.groupby("dow", observed=True).agg(avg_value=("v", "mean"), avg_txn=("n", "mean")).reindex([d for d in DOW if d in days])
    a, b = st.columns(2)
    a.plotly_chart(px.bar(g, y="avg_value", labels={"avg_value": f"Avg daily {unit}", "dow": ""}, title=f"Average daily {metric.lower()}",
                          color_discrete_sequence=["#8c5a3c"]))
    b.plotly_chart(px.bar(g, y="avg_txn", labels={"avg_txn": "Avg daily transactions", "dow": ""}, title="Average daily transactions",
                          color_discrete_sequence=["#2e6f6a"]))
    dd["Type"] = np.where(dd.dow.isin(["Saturday", "Sunday"]), "Weekend", "Weekday")
    wk = dd.groupby("Type").agg(avg_value=("v", "mean"), avg_txn=("n", "mean")).round(1)
    st.subheader("Weekday vs weekend"); st.write(wk)
    spread = (g.avg_value.max() - g.avg_value.min()) / g.avg_value.mean() * 100
    st.info(f"Busiest: **{g.avg_value.idxmax()}** | Slowest: **{g.avg_value.idxmin()}** | Gap between them: **{spread:.1f}%** of the average day.")

# ---------------- heatmaps ----------------
with tab3:
    n_days = f.groupby("dow", observed=True).date.nunique()
    p = f.groupby(["dow", "hour"], observed=True)[col].sum().unstack().reindex([d for d in DOW if d in days])
    p = p.div(n_days.reindex(p.index), axis=0)
    st.plotly_chart(px.imshow(p, aspect="auto", color_continuous_scale="YlOrBr", labels=dict(x="Hour", y="", color=f"Avg per day"),
                              title=f"Average {metric.lower()} per day: weekday x hour"))
    h = f.groupby("hour").agg(Revenue=("revenue", "sum"), Quantity=("transaction_qty", "sum"), Transactions=("transaction_id", "count")).reset_index()
    st.plotly_chart(px.bar(h, x="hour", y=metric if metric in h else "Revenue", title=f"Hourly {metric.lower()}",
                           color_discrete_sequence=["#8c5a3c"]))
    top = h.nlargest(3, "Transactions").hour.sort_values().tolist()
    st.info(f"Peak transaction hours in this selection: **{', '.join(f'{x}:00' for x in top)}**")

# ---------------- location ----------------
with tab4:
    p = f.groupby(["store_location", "hour"])[col].sum().unstack().reindex(columns=range(hr[0], hr[1] + 1)).fillna(0)
    st.plotly_chart(px.imshow(p, aspect="auto", color_continuous_scale="YlOrBr", labels=dict(x="Hour", y="", color=unit),
                              title=f"Hourly {metric.lower()} heatmap per store"))
    share = p.div(p.sum(axis=1), axis=0) * 100
    s = share.reset_index().melt("store_location", var_name="hour", value_name="share")
    st.plotly_chart(px.line(s, x="hour", y="share", color="store_location", color_discrete_map=COLORS,
                            labels={"share": "% of store's daily total", "store_location": "Store"},
                            title="Demand shape by store (normalised, so peak alignment is comparable)"))
    bk = f.groupby(["store_location", "bucket"], observed=True)[col].sum().reset_index()
    bk = bk[bk.bucket != "Late (22-5)"]
    st.plotly_chart(px.bar(bk, x="store_location", y=col, color="bucket", barmode="stack", labels={col: unit, "store_location": ""},
                           title="Time-bucket mix by store"))
    pk = f.groupby(["store_location", "hour"]).size().reset_index(name="n").sort_values("n").groupby("store_location").tail(1)
    st.write(pk.rename(columns={"store_location": "Store", "hour": "Peak hour", "n": "Transactions at peak"}))

# ---------------- data quality ----------------
with tab5:
    st.write("Validation on the full dataset (before filters):")
    st.write(pd.DataFrame(checks, index=["Count"]).T)
    st.write(f"Trading days reconstructed: **{df.day_idx.nunique()}** ({df.date.min():%d %b} - {df.date.max():%d %b %Y}). "
             f"Transactions occur between **{df.hour.min()}:00 and {df.hour.max()}:59** - the Late bucket (22-5) is empty.")
