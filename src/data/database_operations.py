from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine('mysql+pymysql://arpad:NewStr0ngP%40ssword!@localhost/customer_segmentation')

# Load data from CSV files
def load_data_from_csv(connection):
    customer_data_path = "/Users/arpad/Library/Mobile Documents/com~apple~CloudDocs/Repositories/Personal Projects/Customer Segmentation/src/data/customer_data_backup.csv"
    items_data_path = "/Users/arpad/Library/Mobile Documents/com~apple~CloudDocs/Repositories/Personal Projects/Customer Segmentation/src/data/items_data_backup.csv"
    purchases_data_path = "/Users/arpad/Library/Mobile Documents/com~apple~CloudDocs/Repositories/Personal Projects/Customer Segmentation/src/data/purchases_data_backup.csv"

    customer_data = pd.read_csv(customer_data_path)
    items_data = pd.read_csv(items_data_path)
    purchases_data = pd.read_csv(purchases_data_path)

    customer_data.to_sql('customer_data', connection, if_exists='replace', index=False)
    print(f"Inserted data into 'customer_data' from {customer_data_path}.")

    items_data.to_sql('items_data', connection, if_exists='replace', index=False)
    print(f"Inserted data into 'items_data' from {items_data_path}.")

    purchases_data.to_sql('purchases_data', connection, if_exists='replace', index=False)
    print(f"Inserted data into 'purchases_data' from {purchases_data_path}.")


def output_table(connection, table_name):
    print(f"Contents of {table_name}:")
    result = connection.execute(text(f"SELECT * FROM {table_name} ORDER BY `Customer ID` DESC LIMIT 20;"))
    rows = result.fetchall()
    for row in rows:
        print(row)
    print("\n")

def verify_purchase(connection, purchase_id):
    print(f"Verifying purchase with ID {purchase_id}...")
    result = connection.execute(
        text("SELECT * FROM purchases_data WHERE `Purchase ID` = :purchase_id"),
        {"purchase_id": purchase_id}
    )
    rows = result.fetchall()
    if rows:
        print(f"Purchase {purchase_id} exists:")
        for row in rows:
            print(row)
    else:
        print(f"Purchase with ID {purchase_id} not found.")
    print("\n")


def output_view(connection, view_name):
    print(f"Contents of {view_name}:")
    result = connection.execute(text(f"SELECT * FROM {view_name};"))
    rows = result.fetchall()
    for row in rows:
        print(row)
    print("\n")

def insert_customer(connection, customer_id, age, gender, frequency_of_purchases):
    connection.execute(
        text("""
            INSERT INTO customer_data (`Customer ID`, `Age`, `Gender`, `Frequency of Purchases`)
            VALUES (:customer_id, :age, :gender, :frequency_of_purchases)
            """),
        {"customer_id": customer_id, "age": age, "gender": gender, "frequency_of_purchases": frequency_of_purchases}
    )
    print(f"Inserted new customer with ID {customer_id}.")

def insert_purchase(connection, purchase_id, customer_id, item_id, purchase_amount, discount_applied, season):
    connection.execute(
        text("""
                    INSERT INTO purchases_data (
                        `Purchase ID`, `Customer ID`, `Item ID`, `Purchase Amount (USD)`,
                        `Discount Applied`, `Season`
                    )
                    VALUES (
                        :purchase_id, :customer_id, :item_id, :purchase_amount,
                        :discount_applied, :season)
                """),
        {
            "purchase_id": purchase_id,
            "customer_id": customer_id,
            "item_id": item_id,
            "purchase_amount": purchase_amount,
            "discount_applied": discount_applied,
            "season": season
        }
    )
    print(f"Inserted new purchase with ID {purchase_id}.")

def update_customer_age(connection, customer_id, new_age):
    connection.execute(
        text("""
            UPDATE customer_data
            SET `Age` = :new_age
            WHERE `Customer ID` = :customer_id
            """),
        {"customer_id": customer_id, "new_age": new_age}
    )
    print(f"Updated age for customer with ID {customer_id} to {new_age}.")

def delete_customer(connection, customer_id):
    connection.execute(
        text("""
        DELETE FROM purchases_data
        WHERE `Customer ID` = :customer_id
        """),
        {"customer_id": customer_id}
    )
    connection.execute(
        text("""
        DELETE FROM customer_data
        WHERE `Customer ID` = :customer_id
        """),
        {"customer_id": customer_id}
    )
    print(f"Deleted customer with ID {customer_id}.")


sql_commands = [
    """
    CREATE TABLE IF NOT EXISTS customer_data (
        `Customer ID` BIGINT PRIMARY KEY,
        `Age` BIGINT NOT NULL,
        `Gender` TEXT NOT NULL,
        `Frequency of Purchases` TEXT NOT NULL
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS items_data (
        `Item ID` BIGINT PRIMARY KEY,
        `Item Purchased` TEXT NOT NULL,
        `Category` TEXT NOT NULL
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS purchases_data (
        `Purchase ID` BIGINT PRIMARY KEY,
        `Customer ID` BIGINT NOT NULL,
        `Item ID` BIGINT NOT NULL,
        `Purchase Amount (USD)` BIGINT NOT NULL,
        `Discount Applied` TEXT NOT NULL,
        `Season` TEXT NOT NULL,
        CONSTRAINT fk_customer FOREIGN KEY (`Customer ID`) REFERENCES customer_data(`Customer ID`),
        CONSTRAINT fk_item FOREIGN KEY (`Item ID`) REFERENCES items_data(`Item ID`)
    );
    """
]


view_commands = [
    """
    CREATE OR REPLACE VIEW customer_purchases_view AS
    SELECT
        c.`Customer ID`,
        c.`Age`,
        c.`Gender`,
        c.`Frequency of Purchases`,
        p.`Purchase ID`,
        p.`Purchase Amount (USD)`,
        p.`Discount Applied`,
        p.`Season`
    FROM
        customer_data c
    JOIN
        purchases_data p
    ON
        c.`Customer ID` = p.`Customer ID`;
    """,
    """
    CREATE OR REPLACE VIEW detailed_purchases_view AS
    SELECT
        p.`Purchase ID`,
        p.`Customer ID`,
        p.`Item ID`,
        i.`Item Purchased`,
        i.`Category`,
        p.`Purchase Amount (USD)`,
        p.`Discount Applied`,
        p.`Season`
    FROM
        purchases_data p
    JOIN
        items_data i
    ON
        p.`Item ID` = i.`Item ID`;
    """
]


if __name__ == "__main__":
    # Execute SQL commands -: connect() to test <or> begin() to save data
    with engine.connect() as connection:
        # create tables
        for sql in sql_commands:
            connection.execute(text(sql))

        output_table(connection, "customer_data")

        # Insert Example
        print("Testing INSERT operation...")
        insert_customer(connection, customer_id=3901, age=30, gender='Male', frequency_of_purchases='Monthly')
        insert_purchase(connection, purchase_id=5000, customer_id=3901, item_id=24, purchase_amount=300, discount_applied='Yes', season='Winter')
        insert_purchase(connection, purchase_id=5006, customer_id=24, item_id=24, purchase_amount=100, discount_applied='Yes', season='Winter')
        output_table(connection, "customer_data")
        output_table(connection, "purchases_data")
        verify_purchase(connection, purchase_id=5006)

        # Update Example
        print("Testing UPDATE operation...")
        update_customer_age(connection, customer_id=3900, new_age=54)
        output_table(connection, "customer_data")

        # Delete Example
        print("Testing DELETE operation...")
        delete_customer(connection, customer_id=3901)
        output_table(connection, "customer_data")
        output_table(connection, "purchases_data")

        # load data from .csv
        # load_data_from_csv(connection)
        # print("Data loaded successfully into tables.")

        # create views
        # for view_sql in view_commands:
        # connection.execute(text(view_sql))
        # print("Views created successfully.")

        # Output table contents
        # print("Outputting table data...")
        # output_table(connection, "customer_data")
        # output_table(connection, "items_data")
        # output_table(connection, "purchases_data")

        # Output view contents
        # print("Outputting view data...")
        # output_view(connection, "customer_purchases_view")
        # output_view(connection, "detailed_purchases_view")

