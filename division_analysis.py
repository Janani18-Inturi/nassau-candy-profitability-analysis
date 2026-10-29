import pandas as pd

df = pd.read_csv("cleaned_nassau_candy.csv")

division_analysis = df.groupby("Division").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Units=("Units", "sum")
).reset_index()

division_analysis["Gross_Margin_Percent"] = (
    division_analysis["Total_Profit"] /
    division_analysis["Total_Sales"] * 100
)

division_analysis = division_analysis.sort_values(
    by="Total_Sales", ascending=False
)

print("\nDivision Performance Analysis")
print(division_analysis.to_string(index=False))

print("\nHighest revenue division:")
print(division_analysis.iloc[0]["Division"])

print("\nHighest profit division:")
print(
    division_analysis.loc[
        division_analysis["Total_Profit"].idxmax(), "Division"
    ]
)

division_analysis.to_csv("division_analysis.csv", index=False)

print("\nDivision analysis saved successfully.")