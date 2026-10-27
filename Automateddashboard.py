
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Automated Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------- Session State ----------
if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = None

if "dashboard_ready" not in st.session_state:
    st.session_state.dashboard_ready = False


# ---------- Helper Function ----------
def prepare_data(df):
    df.columns = df.columns.str.strip()

    # Convert date if available
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"], errors="coerce"
        )

    # Convert numeric columns
    for col in ["Quantity", "Unit_Price", "Unit_Cost"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

    # Automatically calculate business metrics
    if {"Quantity", "Unit_Price"}.issubset(df.columns):
        df["Revenue"] = df["Quantity"] * df["Unit_Price"]

    if {"Quantity", "Unit_Cost"}.issubset(df.columns):
        df["Total Cost"] = df["Quantity"] * df["Unit_Cost"]

    if {"Revenue", "Total Cost"}.issubset(df.columns):
        df["Profit"] = df["Revenue"] - df["Total Cost"]

        df["Profit Margin (%)"] = (
            df["Profit"] / df["Revenue"].replace(0, float("nan"))
        ) * 100

    return df


def money(value):
    return f"₹{value:,.2f}"


# ---------- Tabs ----------
tab1, tab2 = st.tabs([
    "📁 Upload Data",
    "📊 Dashboard"
])


# ==================================================
# TAB 1: UPLOAD DATA
# ==================================================
with tab1:
    st.title("📁 Upload Your Business Data")

    st.write(
        "Upload a CSV or Excel file to generate "
        "an automated interactive dashboard."
    )

    uploaded_file = st.file_uploader(
        "Choose your data file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                raw_df = pd.read_csv(uploaded_file)
            else:
                raw_df = pd.read_excel(uploaded_file)

            st.success("File uploaded successfully!")

            st.subheader("Data Preview")
            st.dataframe(
                raw_df.head(10),
                use_container_width=True
            )

            st.write(f"Rows: {raw_df.shape[0]}")
            st.write(f"Columns: {raw_df.shape[1]}")

            if st.button(
                "🚀 Generate Dashboard",
                type="primary",
                use_container_width=True
            ):
                df = prepare_data(raw_df.copy())

                st.session_state.dashboard_data = df
                st.session_state.dashboard_ready = True

                st.success(
                    "Dashboard generated! "
                    "Open the Dashboard tab."
                )

        except Exception as e:
            st.error(f"Unable to read the file: {e}")

    else:
        st.info("Upload your CSV or Excel file to begin.")

        # Optional: load the supplied example CSV
        example_path = (
            Path(__file__).parent / "sales_data_week2(1).csv"
        )

        if example_path.exists():
            if st.button("Load Example Dataset"):
                raw_df = pd.read_csv(example_path)
                df = prepare_data(raw_df.copy())

                st.session_state.dashboard_data = df
                st.session_state.dashboard_ready = True

                st.success(
                    "Example dataset loaded! "
                    "Open the Dashboard tab."
                )


# ==================================================
# TAB 2: INTERACTIVE DASHBOARD
# ==================================================
with tab2:

    if (
        st.session_state.dashboard_ready
        and st.session_state.dashboard_data is not None
    ):
        df = st.session_state.dashboard_data.copy()

        st.title("📊 Automated Business Dashboard")
        st.caption(
            "Explore sales performance using interactive filters."
        )

        # ---------- Sidebar Filters ----------
        st.sidebar.header("Dashboard Filters")

        filtered_df = df.copy()

        if "Product" in filtered_df.columns:
            products = sorted(
                filtered_df["Product"].dropna().unique().tolist()
            )

            selected_products = st.sidebar.multiselect(
                "Select Products",
                options=products,
                default=products
            )

            filtered_df = filtered_df[
                filtered_df["Product"].isin(selected_products)
            ]

        if (
            "Date" in filtered_df.columns
            and filtered_df["Date"].notna().any()
        ):
            min_date = filtered_df["Date"].min().date()
            max_date = filtered_df["Date"].max().date()

            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if isinstance(date_range, (tuple, list)):
                if len(date_range) == 2:
                    start_date, end_date = date_range

                    filtered_df = filtered_df[
                        filtered_df["Date"].dt.date.between(
                            start_date, end_date
                        )
                    ]

                elif len(date_range) == 1:
                    selected_date = date_range[0]
                    filtered_df = filtered_df[
                        filtered_df["Date"].dt.date == selected_date
                    ]

        # ---------- KPI Cards ----------
        st.subheader("Key Performance Indicators")

        revenue = (
            filtered_df["Revenue"].sum()
            if "Revenue" in filtered_df else 0
        )

        cost = (
            filtered_df["Total Cost"].sum()
            if "Total Cost" in filtered_df else 0
        )

        profit = (
            filtered_df["Profit"].sum()
            if "Profit" in filtered_df else 0
        )

        margin = (profit / revenue * 100) if revenue else 0

        quantity = (
            filtered_df["Quantity"].sum()
            if "Quantity" in filtered_df else 0
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Total Revenue", money(revenue))
        c2.metric("Total Cost", money(cost))
        c3.metric("Total Profit", money(profit))
        c4.metric("Profit Margin", f"{margin:.2f}%")
        c5.metric("Units Sold", f"{quantity:,.0f}")

        st.divider()

        # ---------- Charts ----------
        st.subheader("Business Performance Analysis")

        if filtered_df.empty:
            st.warning(
                "No records match the selected filters. "
                "Please change your filters."
            )

        else:
            # Revenue and profit by product
            if "Product" in filtered_df.columns:
                product_summary = (
                    filtered_df.groupby("Product", as_index=False)
                    .agg({
                        "Revenue": "sum",
                        "Profit": "sum"
                    })
                    if {"Revenue", "Profit"}.issubset(filtered_df.columns)
                    else None
                )

                if product_summary is not None:
                    fig1 = px.bar(
                        product_summary,
                        x="Product",
                        y=["Revenue", "Profit"],
                        barmode="group",
                        title="Revenue and Profit by Product",
                        labels={"value": "Amount (₹)"}
                    )
                    st.plotly_chart(
                        fig1, use_container_width=True
                    )

            # Revenue trend over time
            if (
                "Date" in filtered_df.columns
                and "Revenue" in filtered_df.columns
                and filtered_df["Date"].notna().any()
            ):
                daily = (
                    filtered_df.dropna(subset=["Date"])
                    .groupby("Date", as_index=False)["Revenue"]
                    .sum()
                    .sort_values("Date")
                )

                fig2 = px.line(
                    daily,
                    x="Date",
                    y="Revenue",
                    markers=True,
                    title="Revenue Trend Over Time"
                )
                st.plotly_chart(
                    fig2, use_container_width=True
                )

            # Product quantity chart
            if (
                "Product" in filtered_df.columns
                and "Quantity" in filtered_df.columns
            ):
                quantity_summary = (
                    filtered_df.groupby("Product", as_index=False)
                    ["Quantity"].sum()
                    .sort_values("Quantity", ascending=False)
                )

                fig3 = px.pie(
                    quantity_summary,
                    names="Product",
                    values="Quantity",
                    hole=0.4,
                    title="Units Sold by Product"
                )
                st.plotly_chart(
                    fig3, use_container_width=True
                )

            # Detailed records
            st.subheader("Filtered Data")

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

            # Download filtered data
            csv_data = filtered_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download Filtered Data",
                data=csv_data,
                file_name="filtered_dashboard_data.csv",
                mime="text/csv",
                use_container_width=True
            )

    else:
        st.info(
            "No dashboard available yet. "
            "Go to the Upload Data tab, upload your dataset, "
            "and click Generate Dashboard."
        )
