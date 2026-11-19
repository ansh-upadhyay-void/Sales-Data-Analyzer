"""
Sales Data Analyzer
Python 3 project using Pandas and Matplotlib.

CSV columns required: Date, Product, Region, Quantity, Amount
Amount is treated as the total sales value for that transaction (not unit price).
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


REQUIRED_COLUMNS = ["Date", "Product", "Region", "Quantity", "Amount"]


def load_sales_data(csv_path):
    """Load, normalize, validate, and de-duplicate sales records."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    # Read as text first so invalid values can be reported and skipped safely.
    df = pd.read_csv(path, dtype=str)
    df.columns = [str(col).strip().title() for col in df.columns]

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            "CSV is missing required column(s): " + ", ".join(missing)
        )

    df = df[REQUIRED_COLUMNS].copy()
    original_count = len(df)

    # Normalize text fields.
    df["Product"] = df["Product"].fillna("").str.strip()
    df["Region"] = df["Region"].fillna("").str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # A valid row needs a date, product, region, positive quantity,
    # and a non-negative numeric transaction amount.
    valid_mask = (
        df["Date"].notna()
        & df["Product"].ne("")
        & df["Region"].ne("")
        & df["Quantity"].notna()
        & df["Amount"].notna()
        & df["Quantity"].gt(0)
        & df["Amount"].ge(0)
    )
    invalid_count = int((~valid_mask).sum())
    if invalid_count:
        print(f"{invalid_count} row(s) skipped: invalid or missing data.")

    df = df.loc[valid_mask].copy()
    df["Quantity"] = df["Quantity"].astype(int)

    before_dedup = len(df)
    df = df.drop_duplicates(subset=REQUIRED_COLUMNS, keep="first")
    duplicate_count = before_dedup - len(df)
    if duplicate_count:
        print(f"{duplicate_count} duplicate row(s) removed.")

    df = df.sort_values("Date").reset_index(drop=True)
    print(
        f"Data loaded: {len(df)} valid transaction(s) "
        f"({original_count} row(s) read)."
    )
    return df


def print_summary(df):
    """Print revenue, transaction count, units, and top five products."""
    if df.empty:
        print("No valid sales records available.")
        return

    total_revenue = df["Amount"].sum()
    transactions = len(df)
    units_sold = df["Quantity"].sum()

    print("\n--- SALES SUMMARY ---")
    print(
        f"Total Revenue: {total_revenue:g} | "
        f"Transactions: {transactions} | Units sold: {units_sold}"
    )

    product_sales = (
        df.groupby("Product", as_index=False)
        .agg(Revenue=("Amount", "sum"), Units=("Quantity", "sum"))
        .sort_values(["Revenue", "Units", "Product"], ascending=[False, False, True])
    )
    print("\nTop 5 selling products (ranked by revenue):")
    print(product_sales.head(5).to_string(index=False))


def group_by_product_and_region(df):
    """Display product-wise and region-wise revenue totals."""
    if df.empty:
        print("No valid sales records available.")
        return

    by_product = df.groupby("Product")["Amount"].sum().sort_values(ascending=False)
    by_region = df.groupby("Region")["Amount"].sum().sort_values(ascending=False)

    print("\n--- PRODUCT-WISE SALES ---")
    for product, amount in by_product.items():
        print(f"{product}: {amount:g}")

    print("\n--- REGION-WISE SALES ---")
    for region, amount in by_region.items():
        print(f"{region}: {amount:g}")

    print("\nBar chart 'Region-wise Sales' displayed.")
    plot_region_sales(by_region)


def plot_region_sales(region_sales):
    """Create a bar chart of total sales by region."""
    if region_sales.empty:
        return
    ax = region_sales.plot(kind="bar", title="Region-wise Sales", rot=0)
    ax.set_xlabel("Region")
    ax.set_ylabel("Sales Amount")
    ax.figure.tight_layout()
    plt.show()


def plot_summary_charts(df, output_dir="charts"):
    """Create the required bar chart (top products) and line chart (daily sales)."""
    if df.empty:
        print("Charts cannot be created because there are no valid records.")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    top_products = (
        df.groupby("Product")["Amount"].sum().sort_values(ascending=False).head(5)
    )
    ax = top_products.plot(kind="bar", title="Top 5 Products by Revenue", rot=30)
    ax.set_xlabel("Product")
    ax.set_ylabel("Sales Amount")
    ax.figure.tight_layout()
    ax.figure.savefig(output_path / "top_5_products.png")
    plt.show()
    plt.close(ax.figure)

    daily_sales = df.groupby(df["Date"].dt.date)["Amount"].sum().sort_index()
    ax = daily_sales.plot(kind="line", marker="o", title="Daily Sales Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sales Amount")
    ax.figure.tight_layout()
    ax.figure.savefig(output_path / "daily_sales_trend.png")
    plt.show()
    plt.close(ax.figure)

    print(f"Charts saved in: {output_path.resolve()}")


def run_menu(df):
    """Run the interactive project menu."""
    while True:
        print("\n===== SALES DATA ANALYZER =====")
        print("1. Summary")
        print("2. Group by Product & Region")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print_summary(df)
            plot_summary_charts(df)
        elif choice == "2":
            group_by_product_and_region(df)
        elif choice == "3":
            print("Thank you for using Sales Data Analyzer.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    parser = argparse.ArgumentParser(description="Analyze sales records from a CSV file.")
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="sales.csv",
        help="Path to the input CSV file (default: sales.csv)",
    )
    args = parser.parse_args()

    try:
        sales_df = load_sales_data(args.csv_file)
        if sales_df.empty:
            print("The CSV contains no valid sales records.")
            return
        run_menu(sales_df)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
