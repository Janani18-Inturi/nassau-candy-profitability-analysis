import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍬",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"], errors="coerce"
    )

    return df

df = load_data()
st.write("Dataset columns:",
df.columns.tolist())

st.title("🍬 Nassau Candy Distributor")
st.subheader("Product Line Profitability & Margin Performance Analysis")

st.markdown(
    "Explore sales performance, product profitability, "
    "profit margins, and business risks."
)

# Sidebar filters
st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()

if "Division" in df.columns:
    divisions = sorted(df["Division"].dropna().unique().tolist())

    selected_divisions = st.sidebar.multiselect(
        "Select Division",
        divisions,
        default=divisions
    )

    filtered_df = filtered_df[
        filtered_df["Division"].isin(selected_divisions)
    ]

if "Region" in filtered_df.columns:
    regions = sorted(filtered_df["Region"].dropna().unique().tolist())

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        regions,
        default=regions
    )

    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_regions)
    ]

if "Order Date" in filtered_df.columns:
    valid_dates = filtered_df["Order Date"].dropna()

    if not valid_dates.empty:
        start_date = valid_dates.min().date()
        end_date = valid_dates.max().date()

        selected_dates = st.sidebar.date_input(
            "Select Order Date Range",
            value=(start_date, end_date),
            min_value=start_date,
            max_value=end_date
        )

        if isinstance(selected_dates, (tuple, list)):
            if len(selected_dates) == 2:
                start, end = selected_dates

                filtered_df = filtered_df[
                    filtered_df["Order Date"].dt.date.between(
                        start, end
                    )
                ]

# KPI calculations
st.header("Key Performance Indicators")

sales = (
    pd.to_numeric(filtered_df["Sales"], errors="coerce").sum()
    if "Sales" in filtered_df.columns else 0
)

profit = (
    pd.to_numeric(filtered_df["Gross Profit"], errors="coerce").sum()
    if "Gross Profit" in filtered_df.columns else 0
)

units = (
    pd.to_numeric(filtered_df["Units"], errors="coerce").sum()
    if "Units" in filtered_df.columns else 0
)

if "Order ID" in filtered_df.columns:
    orders = filtered_df["Order ID"].nunique()
else:
    orders = 0

gross_margin = (profit / sales * 100) if sales else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${sales:,.2f}")
col2.metric("Total Profit", f"${profit:,.2f}")
col3.metric("Total Orders", f"{orders:,}")

col4, col5 = st.columns(2)

col4.metric("Total Units Sold", f"{units:,.0f}")
col5.metric("Gross Margin", f"{gross_margin:.2f}%")

# Dataset preview
st.header("Filtered Dataset Preview")

st.write(f"Records displayed: {len(filtered_df):,}")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)
# Product Profitability and Margin Analysis

st.header("Product Profitability & Margin Analysis")

required_columns = ["Product Name", "Sales", "Gross Profit"]

if all(col in filtered_df.columns for col in required_columns):

    product_data = filtered_df.copy()

    product_data["Sales"] = pd.to_numeric(
        product_data["Sales"], errors="coerce"
    ).fillna(0)

    product_data["Gross Profit"] = pd.to_numeric(
        product_data["Gross Profit"], errors="coerce"
    ).fillna(0)

    product_summary = (
        product_data.groupby("Product Name", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum")
        )
    )

    product_summary["Gross_Margin"] = (
        product_summary["Total_Profit"]
        .div(product_summary["Total_Sales"].where(
            product_summary["Total_Sales"] != 0
        ))
        .mul(100)
    )

    product_summary = product_summary.sort_values(
        "Total_Profit", ascending=False
    )

    st.subheader("Top 10 Products by Gross Profit")

    top_products = product_summary.head(10)

    st.bar_chart(
        top_products.set_index("Product Name")["Total_Profit"]
    )

    st.subheader("Product Sales Comparison")

    top_sales_products = product_summary.sort_values(
        "Total_Sales", ascending=False
    ).head(10)

    st.bar_chart(
        top_sales_products.set_index("Product Name")["Total_Sales"]
    )

    st.subheader("Product-Level Profitability Table")

    display_products = product_summary.rename(
        columns={
            "Total_Sales": "Total Sales",
            "Total_Profit": "Total Gross Profit",
            "Gross_Margin": "Gross Margin (%)"
        }
    )

    st.dataframe(
        display_products.style.format({
            "Total Sales": "${:,.2f}",
            "Total Gross Profit": "${:,.2f}",
            "Gross Margin (%)": "{:.2f}%"
        }),
        use_container_width=True
    )

    st.subheader("Highest and Lowest Margin Products")

    valid_margins = product_summary.dropna(
        subset=["Gross_Margin"]
    )

    if not valid_margins.empty:

        highest_margin = valid_margins.loc[
            valid_margins["Gross_Margin"].idxmax()
        ]

        lowest_margin = valid_margins.loc[
            valid_margins["Gross_Margin"].idxmin()
        ]

        col1, col2 = st.columns(2)

        col1.metric(
            "Highest Gross Margin Product",
            str(highest_margin["Product Name"]),
            f"{highest_margin['Gross_Margin']:.2f}%"
        )

        col2.metric(
            "Lowest Gross Margin Product",
            str(lowest_margin["Product Name"]),
            f"{lowest_margin['Gross_Margin']:.2f}%"
        )

else:
    st.warning(
        "Product profitability analysis requires "
        "'Product Name', 'Sales', and 'Gross Profit' columns."
    )# Division Performance Comparison

st.header("Division Performance Comparison")

required_columns = ["Division", "Sales", "Gross Profit"]

if all(col in filtered_df.columns for col in required_columns):

    division_data = filtered_df.copy()

    division_data["Sales"] = pd.to_numeric(
        division_data["Sales"], errors="coerce"
    ).fillna(0)

    division_data["Gross Profit"] = pd.to_numeric(
        division_data["Gross Profit"], errors="coerce"
    ).fillna(0)

    division_summary = (
        division_data.groupby("Division", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum")
        )
    )

    division_summary["Gross_Margin"] = (
        division_summary["Total_Profit"]
        .div(division_summary["Total_Sales"].where(
            division_summary["Total_Sales"] != 0
        ))
        .mul(100)
    )

    st.subheader("Sales by Division")

    st.bar_chart(
        division_summary.set_index("Division")["Total_Sales"]
    )

    st.subheader("Gross Profit by Division")

    st.bar_chart(
        division_summary.set_index("Division")["Total_Profit"]
    )

    st.subheader("Division Gross Margin Comparison")

    st.bar_chart(
        division_summary.set_index("Division")["Gross_Margin"]
    )

    st.subheader("Division Performance Summary")

    display_divisions = division_summary.rename(
        columns={
            "Total_Sales": "Total Sales",
            "Total_Profit": "Total Gross Profit",
            "Gross_Margin": "Gross Margin (%)"
        }
    )

    st.dataframe(
        display_divisions.style.format({
            "Total Sales": "${:,.2f}",
            "Total Gross Profit": "${:,.2f}",
            "Gross Margin (%)": "{:.2f}%"
        }),
        use_container_width=True
    )

else:
    st.warning(
        "Division comparison requires Division, Sales, "
        "and Gross Profit columns."
    )# Cost-versus-Margin Diagnostics

st.header("Cost-versus-Margin Diagnostics")

if all(
    col in filtered_df.columns
    for col in ["Product Name", "Sales", "Gross Profit"]
):

    cost_data = filtered_df.copy()

    cost_data["Sales"] = pd.to_numeric(
        cost_data["Sales"], errors="coerce"
    )

    cost_data["Gross Profit"] = pd.to_numeric(
        cost_data["Gross Profit"], errors="coerce"
    )

    cost_data = cost_data.dropna(
        subset=["Sales", "Gross Profit"]
    )

    # Estimate cost from sales and gross profit
    cost_data["Estimated Cost"] = (
        cost_data["Sales"] - cost_data["Gross Profit"]
    )

    cost_data["Gross Margin (%)"] = (
        cost_data["Gross Profit"]
        .div(cost_data["Sales"].where(cost_data["Sales"] != 0))
        .mul(100)
    )

    # Aggregate metrics by product
    cost_summary = (
        cost_data.groupby("Product Name", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Estimated_Cost=("Estimated Cost", "sum")
        )
    )

    cost_summary["Gross Margin (%)"] = (
        cost_summary["Total_Profit"]
        .div(cost_summary["Total_Sales"].where(
            cost_summary["Total_Sales"] != 0
        ))
        .mul(100)
    )

    st.subheader("Sales vs Estimated Cost")

    st.scatter_chart(
        cost_summary,
        x="Total_Sales",
        y="Estimated_Cost",
        x_label="Total Sales",
        y_label="Estimated Cost"
    )

    st.subheader("Estimated Cost vs Gross Margin")

    st.scatter_chart(
        cost_summary.dropna(
            subset=["Gross Margin (%)"]
        ),
        x="Estimated_Cost",
        y="Gross Margin (%)",
        x_label="Estimated Cost",
        y_label="Gross Margin (%)"
    )

    st.subheader("Products with Negative Gross Profit")

    negative_profit = cost_summary[
        cost_summary["Total_Profit"] < 0
    ].sort_values("Total_Profit")

    if not negative_profit.empty:

        st.warning(
            f"{len(negative_profit)} products have negative "
            "gross profit in the selected data."
        )

        st.dataframe(
            negative_profit.rename(
                columns={
                    "Total_Sales": "Total Sales",
                    "Total_Profit": "Total Gross Profit",
                    "Estimated_Cost": "Estimated Cost"
                }
            ),
            use_container_width=True
        )

    else:
        st.success(
            "No products with negative gross profit "
            "were found in the selected data."
        )

    st.subheader("Products with the Lowest Gross Margins")

    low_margin = cost_summary.dropna(
        subset=["Gross Margin (%)"]
    ).sort_values("Gross Margin (%)").head(10)

    st.dataframe(
        low_margin.rename(
            columns={
                "Total_Sales": "Total Sales",
                "Total_Profit": "Total Gross Profit",
                "Estimated_Cost": "Estimated Cost"
            }
        ).style.format({
            "Total Sales": "${:,.2f}",
            "Total Gross Profit": "${:,.2f}",
            "Estimated Cost": "${:,.2f}",
            "Gross Margin (%)": "{:.2f}%"
        }),
        use_container_width=True
    )

else:
    st.warning(
        "Cost-versus-margin analysis requires Product Name, "
        "Sales, and Gross Profit columns."
    )# Profit Concentration and Pareto Analysis

st.header("Profit Concentration & Pareto Analysis")

if all(
    col in filtered_df.columns
    for col in ["Product Name", "Sales", "Gross Profit"]
):

    pareto_data = filtered_df.copy()

    pareto_data["Sales"] = pd.to_numeric(
        pareto_data["Sales"], errors="coerce"
    ).fillna(0)

    pareto_data["Gross Profit"] = pd.to_numeric(
        pareto_data["Gross Profit"], errors="coerce"
    ).fillna(0)

    # Calculate profit contribution by product
    pareto_summary = (
        pareto_data.groupby("Product Name", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum")
        )
    )

    total_profit = pareto_summary["Total_Profit"].sum()

    if total_profit > 0:

        pareto_summary = pareto_summary.sort_values(
            "Total_Profit", ascending=False
        ).reset_index(drop=True)

        pareto_summary["Profit Contribution (%)"] = (
            pareto_summary["Total_Profit"] / total_profit
        ) * 100

        pareto_summary["Cumulative Profit (%)"] = (
            pareto_summary["Profit Contribution (%)"].cumsum()
        )

        pareto_summary["Cumulative Products (%)"] = (
            (pareto_summary.index + 1)
            / len(pareto_summary)
        ) * 100

        # Top products
        st.subheader("Top 10 Products by Gross Profit")

        st.bar_chart(
            pareto_summary.head(10).set_index("Product Name")[
                "Total_Profit"
            ]
        )

        # Pareto chart
        st.subheader("Cumulative Profit Contribution")

        st.line_chart(
            pareto_summary.set_index("Cumulative Products (%)")[
                "Cumulative Profit (%)"
            ]
        )

        # Top 20% contribution
        top_count = max(
            1, int(len(pareto_summary) * 0.20)
        )

        top_20_profit = pareto_summary.head(top_count)[
            "Total_Profit"
        ].sum()

        top_20_contribution = (
            top_20_profit / total_profit
        ) * 100

        col1, col2 = st.columns(2)

        col1.metric(
            "Number of Products",
            f"{len(pareto_summary):,}"
        )

        col2.metric(
            "Profit from Top 20% of Products",
            f"{top_20_contribution:.2f}%"
        )

        # Full contribution table
        st.subheader("Product Profit Contribution Table")

        display_pareto = pareto_summary.rename(
            columns={
                "Total_Sales": "Total Sales",
                "Total_Profit": "Total Gross Profit"
            }
        )

        st.dataframe(
            display_pareto.style.format({
                "Total Sales": "${:,.2f}",
                "Total Gross Profit": "${:,.2f}",
                "Profit Contribution (%)": "{:.2f}%",
                "Cumulative Profit (%)": "{:.2f}%",
                "Cumulative Products (%)": "{:.2f}%"
            }),
            use_container_width=True
        )

    else:
        st.warning(
            "Total gross profit is zero or negative. "
            "Standard profit contribution percentages "
            "cannot be interpreted reliably."
        )

else:
    st.warning(
        "Pareto analysis requires Product Name, Sales, "
        "and Gross Profit columns."
    )# Business Insights and Recommendations

st.header("Business Insights & Recommendations")

if not filtered_df.empty and {"Product Name", "Sales", "Gross Profit"}.issubset(filtered_df.columns):

    product_summary = (
        filtered_df.groupby("Product Name")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum")
        )
        .reset_index()
    )

    product_summary["Profit_Margin"] = (
        product_summary["Total_Profit"]
        / product_summary["Total_Sales"].replace(0, float("nan"))
    ) * 100

    best_product = product_summary.loc[
        product_summary["Total_Profit"].idxmax()
    ]

    lowest_margin_products = product_summary.dropna(
        subset=["Profit_Margin"]
    ).sort_values("Profit_Margin")

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Gross Profit"].sum()

    overall_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0 else 0
    )

    st.subheader("Key Business Findings")

    st.write(
        f"**1. Highest profit-generating product:** "
        f"{best_product['Product Name']} generated "
        f"${best_product['Total_Profit']:,.2f} in gross profit."
    )

    st.write(
        f"**2. Overall gross profit margin:** "
        f"The selected data has a gross profit margin of "
        f"{overall_margin:.2f}%."
    )

    if not lowest_margin_products.empty:
        low_margin_product = lowest_margin_products.iloc[0]

        st.write(
            f"**3. Product requiring margin review:** "
            f"{low_margin_product['Product Name']} has a gross profit "
            f"margin of {low_margin_product['Profit_Margin']:.2f}%."
        )

    st.subheader("Recommended Business Actions")

    st.markdown("""
    - **Improve low-margin products:** Review supplier costs, pricing,
      discounts, and product-level expenses.
    - **Protect profitable products:** Monitor the availability and
      demand of products contributing strongly to gross profit.
    - **Review product concentration:** Use the Pareto analysis to
      identify products that contribute a large share of total profit.
    - **Compare divisions:** Investigate differences in sales and
      gross profit margins across divisions.
    - **Monitor performance regularly:** Use the dashboard filters to
      compare performance across regions, divisions, and time periods.
    """)

else:
    st.info(
        "Business insights will appear when the filtered dataset contains "
        "product names, sales, and gross profit."
    )