import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

product_analysis = df.groupby("Product Name").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
    Total_Cost=("Cost", "sum")
).reset_index()

product_analysis["Gross_Margin_Percent"] = (
    product_analysis["Total_Profit"] /
    product_analysis["Total_Sales"] * 100
)

product_analysis["Profit_Per_Unit"] = (
    product_analysis["Total_Profit"] /
    product_analysis["Total_Units"]
)

product_analysis = product_analysis.sort_values(
    by="Total_Profit", ascending=False
)

print("\nTop 10 Products by Gross Profit:")
print(product_analysis.head(10).to_string(index=False))

print("\nBottom 10 Products by Gross Profit:")
print(product_analysis.tail(10).to_string(index=False))

product_analysis.to_csv("product_profitability.csv", index=False)

print("\nProduct profitability analysis saved successfully.")