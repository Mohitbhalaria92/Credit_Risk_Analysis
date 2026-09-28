import pandas as pd

# Load Kaggle dataset
df = pd.read_csv("credit_risk_dataset.csv")

# 1. Filter out impossible age outliers (data entry errors)
df = df[df["person_age"] < 100]

# 2. Handle missing interest rates (fill with median interest rate per loan grade)
df["loan_int_rate"] = df.groupby("loan_grade")["loan_int_rate"].transform(
    lambda x: x.fillna(x.median())
)

# 3. Fill missing employment lengths with 0
df["person_emp_length"] = df["person_emp_length"].fillna(0)

# 4. Generate a clean unique loan ID primary key
df.insert(0, "loan_id", ["LN-" + str(10000 + i) for i in range(len(df))])

# Export clean CSV
df.to_csv("cleaned_loan_data.csv", index=False)
print(f"✅ Success: Processed {len(df)} records -> saved to cleaned_loan_data.csv")