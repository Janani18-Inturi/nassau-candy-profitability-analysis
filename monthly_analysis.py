import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

df = df.dropna(subset=["Order Date"])

df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_analysis = df.groupby("Month").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum")
).reset_index()

monthly_analysis = monthly_analysis.sort_values("Month")

print("Monthly Sales and Profit Analysis:")
print(monthly_analysis.round(2))

monthly_analysis.to_csv("monthly_analysis.csv", index=False)

print("\nMonthly analysis saved successfully.")