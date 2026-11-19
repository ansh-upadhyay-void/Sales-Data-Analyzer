Project Summary: Sales Data Analyzer
Objective
Analyze a sales CSV file to calculate total revenue, identify the best-selling products, and compare region-wise performance.
Technology
- Language: Python 3
- Libraries: Pandas, Matplotlib
- Input: CSV file containing Date, Product, Region, Quantity, and Amount
Main Functions
1. Load sales data from the CSV file.
2. Validate fields, skip invalid records, and remove exact duplicate rows.
3. Calculate total revenue, transaction count, and units sold.
4. Display the top five products ranked by revenue.
5. Group and display sales by product and by region.
6. Visualize product revenue and daily sales using bar and line charts.
7. Visualize region-wise sales using a bar chart.
Revenue Calculation
Revenue is the sum of the Amount column. Amount represents the total value of a transaction and is not multiplied by Quantity. Quantity is summed separately to calculate units sold.
Expected Normal-Test Output
For the sample three-row input:
- Total Revenue: 155000
- Transactions: 3
- Units sold: 13
- Product revenue: Laptop = 105000, Mouse = 50000
- Region revenue: North = 100000, South = 55000
How to Run
Install dependencies with python -m pip install pandas matplotlib, then run python sales_data_analyzer.py. Choose option 1 for the summary and charts, option 2 for product/region grouping, or option 3 to exit.