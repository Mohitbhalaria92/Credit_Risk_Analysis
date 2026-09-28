import duckdb

con = duckdb.connect()

query = """
WITH grade_summary AS (
    SELECT 
        loan_grade,
        COUNT(loan_id) AS total_loans,
        SUM(loan_amnt) AS total_funded,
        SUM(CASE WHEN loan_status = 1 THEN loan_amnt ELSE 0 END) AS default_exposure,
        AVG(loan_int_rate) AS avg_int_rate,
        AVG(loan_percent_income) AS avg_dti
    FROM 'cleaned_loan_data.csv'
    GROUP BY loan_grade
)
SELECT 
    loan_grade,
    total_loans,
    total_funded,
    default_exposure,
    ROUND((default_exposure / total_funded) * 100, 2) AS default_rate_pct,
    ROUND(avg_int_rate, 2) AS avg_int_rate,
    ROUND(avg_dti * 100, 2) AS avg_dti_pct
FROM grade_summary
ORDER BY loan_grade ASC;
"""

print(con.execute(query).df().to_string(index=False))