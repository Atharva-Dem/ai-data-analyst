# eda.py
# This file handles automatic Exploratory Data Analysis (EDA)
# It takes your uploaded dataset and shows stats, charts, and patterns

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def run_eda(df):

    # Section 1 - Basic Overview
    st.subheader("📊 Dataset Overview")

    # Show 3 key numbers side by side
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Show first 5 rows of data
    st.subheader("👀 Preview of Your Data")
    st.dataframe(df.head(), use_container_width=True)

    # Section 2 - Column Info
    st.subheader("🔍 Column Details")
    col_info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.values,
        "Missing Count": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })
    st.dataframe(col_info, use_container_width=True)

    # Section 3 - Statistics (only for number columns)
    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)

    # Section 4 - Distribution Chart
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) >= 1:
        st.subheader("📉 Column Distribution")
        col = st.selectbox("Select a column to see its distribution", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color='steelblue')
        ax.set_title(f"Distribution of {col}")
        st.pyplot(fig)

    # Section 5 - Correlation Heatmap
    if len(numeric_cols) >= 2:
        st.subheader("🔗 Correlation Heatmap")
        st.caption("Shows how strongly columns are related to each other")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            df[numeric_cols].corr(),
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            ax=ax2
        )
        st.pyplot(fig2)