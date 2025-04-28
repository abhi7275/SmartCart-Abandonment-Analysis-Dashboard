# Filename: app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="SmartCart Abandonment Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('smart_cart_model_output.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
device_filter = st.sidebar.multiselect(
    "Select Device(s):",
    options=df['device'].unique(),
    default=df['device'].unique()
)

location_filter = st.sidebar.multiselect(
    "Select Location(s):",
    options=df['location'].unique(),
    default=df['location'].unique()
)

# Apply filters
filtered_df = df[
    (df['device'].isin(device_filter)) &
    (df['location'].isin(location_filter))
]

# Main Title
st.title("🛒 SmartCart Abandonment Analysis Dashboard")

# Top KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sessions = filtered_df['session_id'].nunique()
    st.metric("Total Sessions", total_sessions)

with col2:
    total_users = filtered_df['user_id'].nunique()
    st.metric("Total Users", total_users)

with col3:
    abandonment_rate = (filtered_df['cart_abandoned'].sum() / total_sessions) * 100
    st.metric("Cart Abandonment Rate (%)", f"{abandonment_rate:.2f}%")

with col4:
    avg_session_duration = filtered_df['session_duration'].mean()
    st.metric("Avg. Session Duration (sec)", f"{avg_session_duration:.1f}")

st.markdown("---")

# Funnel Plot
st.subheader("🔄 Funnel Movement")
funnel_data = filtered_df['page'].value_counts().reset_index()
funnel_data.columns = ['Page', 'Count']
fig_funnel = px.funnel(funnel_data, x='Count', y='Page', color='Page')
st.plotly_chart(fig_funnel, use_container_width=True)

# Event Type Distribution
st.subheader("⚡ Event Type Distribution")
fig_event = px.pie(filtered_df, names='event_type', title='Event Type Split', hole=0.5)
st.plotly_chart(fig_event, use_container_width=True)

# Session Duration Trend
st.subheader("⏱ Session Duration Over Time")
fig_time = px.line(
    filtered_df.sort_values('timestamp'),
    x='timestamp',
    y='session_duration',
    color='device',
    title='Session Duration Trend'
)
st.plotly_chart(fig_time, use_container_width=True)

# Predicted vs Actual
st.subheader("Prediction Performance (Actual vs Predicted Abandonment)")
pred_vs_actual = filtered_df['actual_vs_pred'].value_counts().reset_index()
pred_vs_actual.columns = ['Prediction Result', 'Count']
fig_pred = px.bar(pred_vs_actual, x='Prediction Result', y='Count', color='Prediction Result')
st.plotly_chart(fig_pred, use_container_width=True)

st.markdown("---")
st.caption("Built by Abhishek Kumar")
