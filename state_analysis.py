import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

state_analysis = df.groupby("State/Province").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Orders=("Order ID", "nunique"),
    Total_Units=("Units", "sum")
).reset_index()

state_analysis = state_analysis.sort_values(
    by="Total_Sales", ascending=False
)

print("Top 10 States by Sales:")
print(state_analysis.head(10).round(2))

state_analysis.to_csv("state_analysis.csv", index=False)

print("\nState analysis saved successfully.")