import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

sales_analysis = df.groupby("Product Name").agg(
    Total_Sales=("Sales", "sum"),
    Total_Units=("Units", "sum"),
    Total_Profit=("Gross Profit", "sum")
).reset_index()

sales_analysis = sales_analysis.sort_values(
    by="Total_Sales", ascending=False
)

sales_analysis["Profit_Margin"] = (
    sales_analysis["Total_Profit"] / sales_analysis["Total_Sales"]
) * 100

print("Top 10 Products by Sales:")
print(sales_analysis.head(10).round(2))

sales_analysis.to_csv("sales_analysis.csv", index=False)

print("\nSales analysis saved successfully.")