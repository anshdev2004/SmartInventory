import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SmartInventory Dashboard", layout="wide")

st.title("📦 SmartInventory — Manager Dashboard")
st.caption("Daily markdown recommendations for perishable inventory")

API_URL = "http://127.0.0.1:8000/markdowns"

try:
    response = requests.get(API_URL)
    data = response.json()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Could not reach the API. Make sure FastAPI is running. Error: {e}")
    st.stop()

# --- Top-level metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Batches", len(df))
col2.metric("Avg Discount %", f"{df['discount_%'].mean():.1f}%")
col3.metric("Revenue Recovered", f"${(df['revenue_with_discount'] - df['revenue_no_discount']).sum():.2f}")

st.divider()

# --- Urgent items first ---
st.subheader("🔴 Markdown Action List (sorted by urgency)")
st.dataframe(
    df.sort_values("days_left")[[
        "batch_id", "product", "days_left", "original_price",
        "recommended_price", "discount_%", "predicted_Q0"
    ]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# --- Revenue comparison chart ---
st.subheader("💰 Revenue: With vs Without Discount")
chart_df = df.groupby("product")[["revenue_no_discount", "revenue_with_discount"]].sum()
st.bar_chart(chart_df)