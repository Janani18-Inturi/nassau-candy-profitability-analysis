import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

ship_analysis = df.groupby("Ship Mode").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Orders=("Order ID", "nunique"),
    Total_Units=("Units", "sum")
).reset_index()

ship_analysis = ship_analysis.sort_values(
    by="Total_Sales", ascending=False
)

print("Shipping Mode Analysis:")
print(ship_analysis.round(2))

ship_analysis.to_csv("ship_mode_analysis.csv", index=False)

print("\nShipping mode analysis saved successfully.")