Sales Data Analyzer
A Python 3 console application that reads sales data from a CSV file, validates and cleans the records, calculates sales summaries, groups sales by product and region, and creates Matplotlib charts.
Features
- Reads CSV data with Pandas.
- Validates required fields and skips invalid rows.
- Removes exact duplicate records.
- Calculates total revenue, transaction count, and units sold.
- Displays the top five products ranked by revenue.
- Groups revenue by product and region.
- Creates a top-products bar chart and a daily-sales line chart.
- Creates a region-wise sales bar chart from menu option 2.
Requirements
- Python 3.9 or newer
- pandas
- matplotlib
Install dependencies:
python -m pip install pandas matplotlib
CSV format
The input file must contain these columns:
Date,Product,Region,Quantity,Amount
2026-08-01,Laptop,North,2,100000
2026-08-02,Mouse,South,10,50000
2026-08-03,Laptop,South,1,5000
Important: Amount is treated as the total sales amount for that transaction. It is not multiplied by Quantity. This matches the project test cases.
Run the project
Save your data as sales.csv in the same folder as sales_data_analyzer.py, then run:
python sales_data_analyzer.py
Or provide a CSV path:
python sales_data_analyzer.py path/to/your_sales.csv
Menu
1. Summary — prints total revenue, number of transactions, units sold, and the top five products. It also displays and saves a product bar chart and daily sales line chart.
2. Group by Product & Region — prints product-wise and region-wise revenue and displays a region-wise bar chart.
3. Exit — closes the program.
Charts from option 1 are saved in a charts/ folder as top_5_products.png and daily_sales_trend.png.
Data-cleaning rules
A row is skipped if its date cannot be parsed, product or region is blank, quantity or amount is not numeric, quantity is zero/negative, or amount is negative. Exact duplicate rows are removed after validation. The program prints counts of skipped and duplicate rows.
Expected results for the supplied normal test data
For the three example rows in the CSV above:
- Total Revenue: 155000
- Transactions: 3
- Units sold: 13
- Product totals: Laptop 105000, Mouse 50000
- Region totals: North 100000, South 55000
For the invalid-input test, a row with Amount equal to abc is skipped.
Project files
- sales_data_analyzer.py — main Python program
- sales.csv — sample input data
- SUMMARY.md — short project summary