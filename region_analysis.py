import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

region_analysis = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum")
).reset_index()

region_analysis["Gross_Margin_Percent"] = (
    region_analysis["Total_Profit"] / region_analysis["Total_Sales"]
) * 100

region_analysis = region_analysis.sort_values(
    by="Total_Profit", ascending=False
)

print("Regional Profitability Analysis:")
print(region_analysis.round(2))

print("\nHighest revenue region:")
print(region_analysis.loc[region_analysis["Total_Sales"].idxmax(), "Region"])

print("\nHighest profit region:")
print(region_analysis.loc[region_analysis["Total_Profit"].idxmax(), "Region"])

region_analysis.to_csv("region_analysis.csv", index=False)

print("\nRegional analysis saved successfully.")