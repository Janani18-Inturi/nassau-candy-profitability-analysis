import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

df = df.dropna(subset=["Order Date"])

df["Year"] = df["Order Date"].dt.year

yearly_analysis = df.groupby("Year").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
    Total_Orders=("Order ID", "nunique")
).reset_index()

yearly_analysis = yearly_analysis.sort_values("Year")

print("Yearly Sales and Profit Analysis:")
print(yearly_analysis.round(2))

yearly_analysis.to_csv("yearly_analysis.csv", index=False)

print("\nYearly analysis saved successfully.")
