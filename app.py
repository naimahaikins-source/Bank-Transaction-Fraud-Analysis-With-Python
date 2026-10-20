import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bank Fraud Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    data = pd.read_csv("/content/bank_fraud_dashboard_data.csv")
    data["transaction_date"] = pd.to_datetime(
        data["transaction_date"], errors="coerce"
    )
    data["is_fraud"] = pd.to_numeric(
        data["is_fraud"], errors="coerce"
    )
    return data

df = load_data()

# ---------------- DESIGN ----------------
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem;}
    div[data-testid="stMetric"] {
        background-color: #F5F0FF;
        border: 1px solid #E2D5FA;
        padding: 16px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Bank Transaction Fraud Analytics")
st.caption(
    "Interactive analysis of transaction patterns, "
    "fraud cases and financial exposure."
)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("Dashboard Filters")

countries = sorted(df["country"].dropna().unique().tolist())
methods = sorted(df["payment_method"].dropna().unique().tolist())
merchants = sorted(
    df["merchant_category"].dropna().unique().tolist()
)

selected_countries = st.sidebar.multiselect(
    "Country", countries, default=countries
)
selected_methods = st.sidebar.multiselect(
    "Payment Method", methods, default=methods
)
selected_merchants = st.sidebar.multiselect(
    "Merchant Category", merchants, default=merchants
)

date_min = df["transaction_date"].min()
date_max = df["transaction_date"].max()

if pd.notna(date_min) and pd.notna(date_max):
    date_range = st.sidebar.date_input(
        "Transaction Date Range",
        value=(date_min.date(), date_max.date()),
        min_value=date_min.date(),
        max_value=date_max.date()
    )
else:
    date_range = None

# ---------------- APPLY FILTERS ----------------
filtered = df[
    df["country"].isin(selected_countries)
    & df["payment_method"].isin(selected_methods)
    & df["merchant_category"].isin(selected_merchants)
].copy()

if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["transaction_date"].dt.date.between(
            start_date, end_date
        )
    ]

# Only records with known fraud status count towards
# the fraud rate and legitimate/fraud case totals.
known = filtered[filtered["is_fraud"].isin([0, 1])].copy()
fraud = known[known["is_fraud"] == 1].copy()

total = len(known)
fraud_count = len(fraud)
legitimate_count = int((known["is_fraud"] == 0).sum())

fraud_rate = fraud_count / total * 100 if total else 0
fraud_value = fraud["transaction_amount"].sum()
avg_fraud_value = fraud["transaction_amount"].mean() if fraud_count else 0

# ---------------- KPI CARDS ----------------
st.subheader("Fraud Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Transactions", f"{total:,}")
c2.metric("Fraud Cases", f"{fraud_count:,}")
c3.metric("Fraud Rate", f"{fraud_rate:.2f}%")
c4.metric("Fraud Transaction Value", f"{fraud_value:,.2f}")

c5, c6 = st.columns(2)
c5.metric("Legitimate Transactions", f"{legitimate_count:,}")
c6.metric("Average Fraud Transaction", f"{avg_fraud_value:,.2f}")

st.caption(
    "Values use the dataset's transaction units. "
    "Fraud transaction value is not necessarily confirmed financial loss."
)

# ---------------- CHARTS ----------------
st.divider()
st.subheader("Transaction Distribution")

left, right = st.columns(2)

with left:
    status = pd.DataFrame({
        "Status": ["Legitimate", "Fraudulent"],
        "Transactions": [legitimate_count, fraud_count]
    })
    fig = px.pie(
        status,
        names="Status",
        values="Transactions",
        hole=0.55,
        title="Legitimate vs Fraudulent"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    type_counts = (
        fraud["fraud_type"].fillna("Unknown")
        .value_counts()
        .rename_axis("Fraud Type")
        .reset_index(name="Cases")
    )
    fig = px.bar(
        type_counts,
        x="Fraud Type",
        y="Cases",
        title="Fraud Cases by Type",
        color="Cases",
        color_continuous_scale="Purples"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- FINANCIAL ANALYSIS ----------------
st.divider()
st.subheader("Financial Impact")

financial = (
    known.groupby("is_fraud")["transaction_amount"]
    .agg(["count", "sum", "mean", "median"])
    .reset_index()
)
financial["Status"] = financial["is_fraud"].map({
    0: "Legitimate", 1: "Fraudulent"
})

left, right = st.columns(2)

with left:
    fig = px.bar(
        financial,
        x="Status",
        y="sum",
        color="Status",
        title="Transaction Value by Status",
        labels={"sum": "Transaction Value", "Status": ""}
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    type_financial = (
        fraud.groupby("fraud_type", dropna=False)
        ["transaction_amount"].sum()
        .reset_index()
    )
    type_financial["fraud_type"] = (
        type_financial["fraud_type"].fillna("Unknown")
    )
    type_financial = type_financial.sort_values(
        "transaction_amount"
    )
    fig = px.bar(
        type_financial,
        x="transaction_amount",
        y="fraud_type",
        orientation="h",
        title="Transaction Value by Fraud Type",
        labels={
            "transaction_amount": "Transaction Value",
            "fraud_type": "Fraud Type"
        },
        color="transaction_amount",
        color_continuous_scale="Purples"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TIME ANALYSIS ----------------
st.divider()
st.subheader("Transaction Timing")

hourly = (
    known.groupby("hour_of_day")
    .agg(
        Transactions=("is_fraud", "size"),
        Fraud_Cases=("is_fraud", "sum")
    )
    .reset_index()
)
hourly["Fraud Rate (%)"] = (
    hourly["Fraud_Cases"] / hourly["Transactions"] * 100
)

left, right = st.columns(2)

with left:
    fig = px.line(
        hourly,
        x="hour_of_day",
        y="Fraud_Cases",
        markers=True,
        title="Fraud Cases by Hour",
        labels={
            "hour_of_day": "Hour of Day",
            "Fraud_Cases": "Fraud Cases"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    payment = (
        known.groupby("payment_method")
        .agg(
            Transactions=("is_fraud", "size"),
            Fraud_Cases=("is_fraud", "sum")
        )
        .reset_index()
    )
    payment["Fraud Rate (%)"] = (
        payment["Fraud_Cases"] / payment["Transactions"] * 100
    )
    payment = payment.sort_values("Fraud Rate (%)")
    fig = px.bar(
        payment,
        x="Fraud Rate (%)",
        y="payment_method",
        orientation="h",
        title="Fraud Rate by Payment Method",
        labels={"payment_method": "Payment Method"},
        color="Fraud Rate (%)",
        color_continuous_scale="Purples"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- GEOGRAPHIC ANALYSIS ----------------
st.divider()
st.subheader("Geographic Fraud Patterns")

geo = (
    known.groupby("country")
    .agg(
        Transactions=("is_fraud", "size"),
        Fraud_Cases=("is_fraud", "sum")
    )
    .reset_index()
)
geo["Fraud Rate (%)"] = (
    geo["Fraud_Cases"] / geo["Transactions"] * 100
)
geo = geo.sort_values("Fraud Rate (%)", ascending=False)

fig = px.bar(
    geo,
    x="country",
    y="Fraud Rate (%)",
    title="Fraud Rate by Country",
    color="Fraud Rate (%)",
    color_continuous_scale="Purples"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.divider()
st.subheader("Explore Transactions")

search_status = st.selectbox(
    "Transaction Status",
    ["All", "Fraudulent", "Legitimate"]
)

table = filtered.copy()

if search_status == "Fraudulent":
    table = table[table["is_fraud"] == 1]
elif search_status == "Legitimate":
    table = table[table["is_fraud"] == 0]

st.dataframe(table, use_container_width=True, hide_index=True)

st.download_button(
    "Download Filtered Data as CSV",
    data=table.to_csv(index=False).encode("utf-8"),
    file_name="filtered_bank_transactions.csv",
    mime="text/csv"
)

st.caption(
    f"Showing {len(table):,} records after the selected filters."
)
