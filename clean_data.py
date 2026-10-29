import pandas as pd

df = pd.read_csv("Nassau Candy Distributor.csv")

print("Dataset shape before cleaning:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

df.columns = df.columns.str.strip()

df = df.drop_duplicates()

df = df.dropna(subset=["Product Name", "Sales", "Cost", "Gross Profit"])

df = df[(df["Sales"] > 0) & (df["Units"] > 0)]

df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100

df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

print("\nDataset shape after cleaning:", df.shape)

print("\nCleaned dataset preview:")
print(df.head())

print("\nUpdated column names:")
print(df.columns.tolist())

df.to_csv("cleaned_nassau_candy.csv", index=False)

print("\nCleaned dataset saved successfully.")