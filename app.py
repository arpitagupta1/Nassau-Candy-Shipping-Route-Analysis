
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="🍬",
    layout="wide"
)

# Load Data
df = pd.read_csv("Nassau Candy Distributor.csv")

# Clean numeric columns
for col in ["Sales", "Units", "Gross Profit", "Cost"]:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce"
    ).fillna(0)

# Convert dates
df["Order Date"] = pd.to_datetime(
    df["Order Date"], dayfirst=True, errors="coerce"
)

# Dashboard Title
st.title("🍬 Nassau Candy Business Dashboard")
st.subheader("Sales & Shipping Performance Analysis")

st.success("Business Data Loaded Successfully!")

# KPI Cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
c2.metric("Total Orders", f"{df['Order ID'].nunique():,}")
c3.metric("Gross Profit", f"${df['Gross Profit'].sum():,.2f}")
c4.metric("Total Units", f"{df['Units'].sum():,.0f}")

st.divider()

# Monthly Sales
st.subheader("📈 Monthly Sales Trend")

monthly = (
    df.dropna(subset=["Order Date"])
    .assign(Month=lambda x: x["Order Date"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)["Sales"].sum()
)

fig1 = px.line(
    monthly,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)
st.plotly_chart(fig1, width="stretch")

# Two column charts
left, right = st.columns(2)

with left:
    st.subheader("🌎 Sales by Region")
    region = (
        df.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    fig2 = px.bar(
        region,
        x="Region",
        y="Sales",
        title="Regional Sales"
    )
    st.plotly_chart(fig2, width="stretch")

with right:
    st.subheader("🚚 Shipping Mode Analysis")
    shipping = (
        df.groupby("Ship Mode", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    fig3 = px.bar(
        shipping,
        x="Ship Mode",
        y="Sales",
        title="Sales by Shipping Mode"
    )
    st.plotly_chart(fig3, width="stretch")

# Product Analysis
st.subheader("🍫 Top 10 Products by Sales")

products = (
    df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .nlargest(10, "Sales")
)

fig4 = px.bar(
    products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products"
)
st.plotly_chart(fig4, width="stretch")

# Country Analysis
st.subheader("🌍 Country-wise Sales")

countries = (
    df.groupby("Country/Region", as_index=False)["Sales"]
    .sum()
    .nlargest(10, "Sales")
)

fig5 = px.bar(
    countries,
    x="Country/Region",
    y="Sales",
    title="Top 10 Countries"
)
st.plotly_chart(fig5, width="stretch")

# Data Table
with st.expander("View Complete Dataset"):
    st.dataframe(df, width="stretch")

st.success("Your Professional Dashboard is Ready!")
# DATA QUALITY CHECK

st.header("Data Quality Analysis")

# Missing Values
st.subheader("Missing Values")
missing_values = df.isnull().sum()

st.dataframe(
    missing_values.reset_index().rename(
        columns={"index": "Column", 0: "Missing Values"}
    ),
    width="stretch"
)

# Duplicate Records
st.subheader("Duplicate Records")
duplicates = df.duplicated().sum()

st.metric("Total Duplicate Rows", duplicates)

# Dataset Information
st.subheader("Dataset Information")
st.write("Total Rows:", df.shape[0])
st.write("Total Columns:", df.shape[1])

# ==============================
# EXPLORATORY DATA ANALYSIS
# ==============================

st.header("Exploratory Data Analysis")

# 1. Total Sales
total_sales = df["Sales"].sum()
st.metric("Total Sales", f"${total_sales:,.2f}")

# 2. Total Gross Profit
total_profit = df["Gross Profit"].sum()
st.metric("Total Gross Profit", f"${total_profit:,.2f}")

# 3. Top 10 Products by Sales
st.subheader("Top 10 Products by Sales")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

st.bar_chart(
    top_products,
    x="Product Name",
    y="Sales"
)

# 4. Sales by Region
st.subheader("Sales by Region")


# 4. Sales by Region
st.subheader("Sales by Region")

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region",
    text_auto=".2s"
)

fig_region.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_region, width="stretch")

# Sales by Product
st.subheader("Sales by Product")

product_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.bar_chart(
    product_sales,
    x="Product Name",
    y="Sales"
)

# Profit Analysis
st.subheader("Profit Analysis by Product")

profit_data = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.bar_chart(
    profit_data,
    x="Product Name",
    y="Gross Profit"
)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True
)

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = (
    monthly_sales["Order Date"].astype(str)
)

st.line_chart(
    monthly_sales,
    x="Order Date",
    y="Sales"
)

# Interactive Filters
st.header("Interactive Sales Filters")

selected_region = st.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].dropna().unique().tolist())
)

selected_product = st.selectbox(
    "Select Product",
    ["All"] + sorted(df["Product Name"].dropna().unique().tolist())
)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["Product Name"] == selected_product
    ]

st.metric("Filtered Total Sales", round(filtered_df["Sales"].sum(), 2))

st.metric("Filtered Total Profit", round(filtered_df["Gross Profit"].sum(), 2))

st.dataframe(filtered_df, width="stretch")

# Business Insights
st.header("Business Insights")

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0 else 0
)

best_region = (
    df.groupby("Region")["Sales"].sum().idxmax()
)

best_product = (
    df.groupby("Product Name")["Gross Profit"].sum().idxmax()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")

with col3:
    st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.subheader("Key Findings")

st.write(f"🏆 Best Sales Region: {best_region}")

st.write(f"🍫 Most Profitable Product: {best_product}")

st.write(f"📊 Overall Profit Margin: {profit_margin:.2f}%")

# ==========================================
# MACHINE LEARNING: SHIPPING LEAD TIME PREDICTION
# ==========================================

import joblib

st.divider()
st.header("🤖 Machine Learning - Shipping Lead Time Prediction")

st.write(
    "Predict the estimated order-to-ship lead time "
    "using the trained Decision Tree model."
)

# Product to Factory mapping
factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

# Load trained model
try:
    ml_model = joblib.load("shipping_lead_time_model.pkl")

    st.success("Machine Learning Model Loaded Successfully!")

    # Dropdown options
    products_list = sorted(
        df["Product Name"].dropna().unique().tolist()
    )

    states_list = sorted(
        df["State/Province"].dropna().astype(str).unique().tolist()
    )

    regions_list = sorted(
        df["Region"].dropna().astype(str).unique().tolist()
    )

    ship_modes_list = sorted(
        df["Ship Mode"].dropna().astype(str).unique().tolist()
    )

    years_list = sorted(
        df["Order Date"].dropna().dt.year.unique().tolist()
    )

    with st.form("shipping_prediction_form"):

        st.subheader("Enter Order Details")

        selected_product = st.selectbox(
            "Select Product",
            products_list
        )

        selected_state = st.selectbox(
            "Customer State",
            states_list
        )

        selected_region = st.selectbox(
            "Customer Region",
            regions_list
        )

        selected_ship_mode = st.selectbox(
            "Shipping Mode",
            ship_modes_list
        )

        selected_year = st.selectbox(
            "Order Year",
            years_list
        )

        selected_month = st.selectbox(
            "Order Month",
            list(range(1, 13))
        )

        sales_value = st.number_input(
            "Sales",
            min_value=0.0,
            value=100.0
        )

        units_value = st.number_input(
            "Units",
            min_value=1,
            value=5
        )

        predict_button = st.form_submit_button(
            "Predict Shipping Lead Time"
        )

    if predict_button:

        # Identify factory and division from product
        selected_factory = factory_mapping.get(
            selected_product
        )

        division_values = df.loc[
            df["Product Name"] == selected_product,
            "Division"
        ].dropna()

        if selected_factory is None or division_values.empty:
            st.error("Factory or Division mapping not found.")

        else:
            selected_division = division_values.mode().iloc[0]

            # Prepare input in the same order used during training
            input_data = pd.DataFrame([{
                "Factory": selected_factory,
                "State/Province": selected_state,
                "Region": selected_region,
                "Ship Mode": selected_ship_mode,
                "Division": selected_division,
                "Product Name": selected_product,
                "Sales": sales_value,
                "Units": units_value,
                "Order Year": selected_year,
                "Order Month": selected_month
            }])

            # Make prediction
            prediction = ml_model.predict(input_data)[0]

            st.subheader("Prediction Result")

            st.metric(
                "Predicted Order-to-Ship Lead Time",
                f"{prediction:.0f} days"
            )

            st.info(
                "This is a model-based estimate of the recorded "
                "Order-to-Ship time, not the actual customer delivery time."
            )

            st.warning(
                "The source dataset contains unusually long shipping "
                "lead times (904–1642 days). Treat this prediction as "
                "experimental until the date data is verified."
            )

except FileNotFoundError:
    st.error(
        "Model file not found. Please keep "
        "shipping_lead_time_model.pkl in the project folder."
    )
