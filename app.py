import streamlit as st
import pandas as pd
import plotly.express as px

# Page Settings
st.set_page_config(
    page_title="🏡 Real Estate Investment Advisor Dashboard",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("sample_real_estate.csv")

# Create Extra Columns
df['Age_of_Property'] = 2026 - df['Year_Built']

df['Price_per_SqFt'] = (
    df['Price_in_Lakhs'] / df['Size_in_SqFt']
)

# Dashboard Title
st.title("🏡 Real Estate Investment Advisor Dashboard")

st.markdown(
    "Use the sidebar filters to explore property insights."
)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("🏠 Filter Properties")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=df['City'].unique(),
    default=df['City'].unique()
)

selected_property = st.sidebar.multiselect(
    "Select Property Type",
    options=df['Property_Type'].unique(),
    default=df['Property_Type'].unique()
)

selected_bhk = st.sidebar.multiselect(
    "Select BHK",
    options=sorted(df['BHK'].unique()),
    default=sorted(df['BHK'].unique())
)

selected_furnished = st.sidebar.multiselect(
    "Furnished Status",
    options=df['Furnished_Status'].unique(),
    default=df['Furnished_Status'].unique()
)

price_range = st.sidebar.slider(
    "Select Price Range (Lakhs)",
    int(df['Price_in_Lakhs'].min()),
    int(df['Price_in_Lakhs'].max()),
    (
        int(df['Price_in_Lakhs'].min()),
        int(df['Price_in_Lakhs'].max())
    )
)

# =========================
# FILTER DATA
# =========================

filtered_df = df[
    (df['City'].isin(selected_city)) &
    (df['Property_Type'].isin(selected_property)) &
    (df['BHK'].isin(selected_bhk)) &
    (df['Furnished_Status'].isin(selected_furnished)) &
    (df['Price_in_Lakhs'] >= price_range[0]) &
    (df['Price_in_Lakhs'] <= price_range[1])
]

# =========================
# KPI CARDS
# =========================

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Price",
    f"{filtered_df['Price_in_Lakhs'].mean():.2f} Lakhs"
)

col2.metric(
    "Average Size",
    f"{filtered_df['Size_in_SqFt'].mean():.0f} SqFt"
)

col3.metric(
    "Total Properties",
    filtered_df.shape[0]
)

# =========================
# CHARTS
# =========================

# Average Price by City
fig1 = px.bar(
    filtered_df.groupby('City')['Price_in_Lakhs']
    .mean()
    .reset_index(),
    x='City',
    y='Price_in_Lakhs',
    title='Average Price by City'
)

st.plotly_chart(fig1, use_container_width=True)

# Price vs Size
fig2 = px.scatter(
    filtered_df,
    x='Size_in_SqFt',
    y='Price_in_Lakhs',
    color='Property_Type',
    title='Price vs Size'
)

st.plotly_chart(fig2, use_container_width=True)

# Furnished Status vs Price
fig3 = px.box(
    filtered_df,
    x='Furnished_Status',
    y='Price_in_Lakhs',
    title='Furnished Status vs Price'
)

st.plotly_chart(fig3, use_container_width=True)

# Property Type Distribution
fig4 = px.pie(
    filtered_df,
    names='Property_Type',
    title='Property Type Distribution'
)

st.plotly_chart(fig4, use_container_width=True)

# Price per SqFt by State
fig5 = px.bar(
    filtered_df.groupby('State')['Price_per_SqFt']
    .mean()
    .reset_index(),
    x='State',
    y='Price_per_SqFt',
    color='Price_per_SqFt',
    title='📍 Average Price per SqFt by State'
)

st.plotly_chart(fig5, use_container_width=True)

# BHK Distribution
fig6 = px.histogram(
    filtered_df,
    x='BHK',
    color='Property_Type',
    title='🏠 BHK Distribution'
)

st.plotly_chart(fig6, use_container_width=True)

# Owner Type Distribution
fig7 = px.pie(
    filtered_df,
    names='Owner_Type',
    title='👤 Owner Type Distribution'
)

st.plotly_chart(fig7, use_container_width=True)

# Parking Space vs Price
fig8 = px.box(
    filtered_df,
    x='Parking_Space',
    y='Price_in_Lakhs',
    title='🚗 Parking Space vs Property Price'
)

st.plotly_chart(fig8, use_container_width=True)
