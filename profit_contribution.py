import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

product_profit = df.groupby("Product Name").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum")
).reset_index()

total_profit = product_profit["Total_Profit"].sum()

product_profit["Profit_Contribution_Percent"] = (
    product_profit["Total_Profit"] / total_profit
) * 100

product_profit = product_profit.sort_values(
    by="Total_Profit", ascending=False
)

product_profit["Cumulative_Profit_Percent"] = (
    product_profit["Profit_Contribution_Percent"].cumsum()
)

print("Top 10 products by profit contribution:")
print(product_profit.head(10).round(2))

product_profit.to_csv("profit_contribution.csv", index=False)

print("\nProfit contribution analysis saved successfully.")