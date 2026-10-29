Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis

Project Overview

This project analyzes the Nassau Candy Distributor dataset to explore sales performance, product profitability, gross profit margins, and division-level performance.

An interactive dashboard built with Python and Streamlit allows users to explore business performance, identify products requiring further investigation, and examine profit concentration across the product portfolio.

Objectives

- Analyze sales and gross profit across products.
- Calculate and compare gross profit margins.
- Compare performance across business divisions.
- Explore cost-versus-margin relationships.
- Identify products contributing significantly to gross profit using Pareto analysis.
- Present business insights and recommendations through an interactive dashboard.

Key Features

- Business Performance KPIs: Total sales, gross profit, orders, units sold, and gross profit margin.
- Product Profitability Analysis: Compare product-level sales, gross profit, and margins.
- Division Performance: Examine differences in sales and profitability across divisions.
- Cost-versus-Margin Diagnostics: Investigate the relationship between estimated cost and gross profit margin.
- Pareto Analysis: Explore the concentration of gross profit among products.
- Business Recommendations: Present potential actions based on the analytical results.
- Interactive Filters: Explore the data using the available division, region, and date filters.

Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit
- CSV

Project Structure

Nassau_Candy_Analysis/
├── app.py
├── README.md
├── research_paper.md
├── executive_summary.md
├── Nassau Candy Distributor.csv
├── cleaned_nassau_candy.csv
├── inspect_data.py
├── clean_data.py
├── profitability_analysis.py
├── division_analysis.py
├── region_analysis.py
├── customer_analysis.py
├── monthly_analysis.py
├── profit_contribution.py
├── sales_analysis.py
├── yearly_analysis.py
├── ship_mode_analysis.py
└── state_analysis.py

Additional analysis scripts and output files may be present in the project folder.

Dashboard Results

The dashboard currently displays the following headline results for the selected dataset:

Metric| Value
Total Sales| $57,064.92
Total Gross Profit| $37,724.48
Total Orders| 3,462
Total Units Sold| 15,575
Gross Profit Margin| 66.11%

These figures reflect the current dashboard selection and should be interpreted according to the dataset and the calculations implemented in the application.

Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Navigate to the project folder

cd Nassau_Candy_Analysis

3. Install the required packages

pip install pandas numpy matplotlib streamlit

4. Run the dashboard

streamlit run app.py

The dashboard should open in your browser.

Documentation

- "research_paper.md" contains the project background, methodology, analysis approach, limitations, and recommendations.
- "executive_summary.md" provides a concise overview of the project and its business value.

Future Improvements

- Add sales forecasting.
- Develop customer segmentation.
- Automate periodic business reports.
- Incorporate additional operating expenses for a more comprehensive profitability analysis.
- Deploy the dashboard online.

Conclusion

This project demonstrates the use of Python-based data analysis and interactive visualization to investigate product profitability and margin performance. The dashboard supports exploratory analysis and provides a foundation for data-driven business decisions.