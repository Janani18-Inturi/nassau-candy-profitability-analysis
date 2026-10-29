import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

customer_analysis = df.groupby("Customer ID").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum")
).reset_index()

customer_analysis = customer_analysis.sort_values(
    by="Total_Sales", ascending=False
)

print("Top 10 customers by sales:")
print(customer_analysis.head(10).round(2))

print("\nTop 10 customers by profit:")
print(
    customer_analysis.sort_values(
        by="Total_Profit", ascending=False
    ).head(10).round(2)
)

customer_analysis.to_csv("customer_analysis.csv", index=False)

print("\nCustomer analysis saved successfully.")