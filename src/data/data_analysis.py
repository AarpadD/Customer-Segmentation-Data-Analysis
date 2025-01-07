from HashMap import HashMap
from sqlalchemy import create_engine, text
from charts import plot_age_range_piechart, plot_discount_piechart

def fetch_aggregated_data(connection, hash_map):
    query = """
         SELECT
             CASE
                 WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                 WHEN Age BETWEEN 31 AND 50 THEN '31-50'
                 WHEN Age > 50 THEN '50+'
             END AS Age_Range,
             SUM(`Purchase Amount (USD)`) AS Total_Purchase_Amount
         FROM customer_purchases_view
         GROUP BY Age_Range
         ORDER BY Age_Range;
         """
    result = connection.execute(text(query)).fetchall()
    # Store results into the HashMap
    for row in result:
        age_range, total_purchase_amount = row
        hash_map.add(age_range, total_purchase_amount)

    return hash_map


def analyze_discounts(connection, hash_map):
    query = """
    SELECT
        `Discount Applied`,
        SUM(`Purchase Amount (USD)`) AS Total_Purchase_Amount,
        AVG(`Purchase Amount (USD)`) AS Average_Purchase_Amount
    FROM
        purchases_data
    GROUP BY
        `Discount Applied`;
    """

    result = connection.execute(text(query)).fetchall()
    # Store results in the HashMap
    for row in result:
        discount_applied, total_purchase_amount, avg_purchase_amount = row
        hash_map.add(discount_applied, {"Total": total_purchase_amount, "Average": avg_purchase_amount})

    return hash_map

# Functions to format and display data
def display_age_range_data(age_range_map):
    print("Spending by Age Range:\n")
    print("{:<10} {:>15}".format("Age Range", "Total Purchase Amount"))
    print("-" * 25)

    for pair in age_range_map.map:
        if pair:
            for age_range, total_purchase_amount in pair:
                print(f"{age_range:<10} {total_purchase_amount:>15}")


def display_discount_data(discount_map):
    print("\nDiscount Analysis:\n")
    print("{:<10} {:>15} {:>20}".format("Discount", "Total Amount", "Avg Amount(per purchase)"))
    print("-" * 45)

    for pair in discount_map.map:
        if pair:
            for discount_applied, data in pair:
                total = data["Total"]
                average = data["Average"]
                # round to 2 decimals
                print(f"{discount_applied:<10} {total:>15} {round(average, 2):>20}")


if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://arpad:NewStr0ngP%40ssword!@localhost/customer_segmentation')

    age_range_map = HashMap()
    discount_map = HashMap()

    with engine.connect() as connection:
        age_range_map = fetch_aggregated_data(connection, age_range_map)
        discount_map = analyze_discounts(connection, discount_map)

        display_age_range_data(age_range_map)
        display_discount_data(discount_map)

        # pie charts for visualization
        plot_age_range_piechart(age_range_map)
        plot_discount_piechart(discount_map)

