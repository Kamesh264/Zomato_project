import psycopg2

# Database connection parameters
db = "postgres"
user = "postgres"
passwd = "2003"
host = "localhost"
port = "5432"

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        database=db,
        user=user,
        password=passwd,
        host=host,
        port=port
    )
    cursor = connection.cursor()
    print("Connected to the database successfully!")
except (Exception, psycopg2.Error) as error:
    print(f"Error connecting to PostgreSQL database: {error}")

# Function to create a table and load data from a CSV file
def create_table_and_load_data(filename, table_name, columns):
    # Drop table if it exists
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        connection.commit()
        print(f"Table '{table_name}' dropped successfully (if it existed).")
    except (Exception, psycopg2.Error) as error:
        print(f"Error dropping table: {error}")
        connection.rollback()

    # Create table
    try:
        column_definitions = ", ".join(columns)
        cursor.execute(f"CREATE TABLE {table_name} ({column_definitions})")
        connection.commit()
        # print(f"Table '{table_name}' created successfully!")
    except (Exception, psycopg2.Error) as error:
        print(f"Error creating table: {error}")

    column_names = [col.split()[0] for col in columns]  # Extract first element (column name)
    
    # print(f"Column names: {column_names}")  # Debugging: print column names

    # Load data using copy_expert
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cursor.copy_expert(
                f"COPY {table_name} ({','.join(column_names)}) FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',')",
                f
            )
        connection.commit()
        print("Data loaded successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error while loading data:", error)
        connection.rollback()  # Rollback changes on error

    # Close connection
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Column definitions for the restaurant table
restaurant_columns = [
    "Restaurant_ID VARCHAR(255) PRIMARY KEY",
    "Restaurant_Name VARCHAR(255)",
    "Country_Code VARCHAR(3)",  # Updated to accommodate longer values
    "City VARCHAR(255)",
    "Address VARCHAR(255)",
    "Locality VARCHAR(255)",
    "Locality_Verbose VARCHAR(255)",
    "Longitude FLOAT",
    "Latitude FLOAT",
    "Cuisines VARCHAR(255)",
    "Average_Cost_for_two INTEGER",
    "Currency VARCHAR(30)",
    "Has_Table_booking BOOLEAN",
    "Has_Online_delivery BOOLEAN",
    "Is_delivering_now BOOLEAN",
    "Switch_to_order_menu BOOLEAN",
    "Price_range INTEGER",
    "Aggregate_rating FLOAT",
    "Rating_color VARCHAR(50)",
    "Rating_text VARCHAR(50)",
    "Votes INTEGER",
    "Country VARCHAR(255)"
]

# Example usage
create_table_and_load_data('restaurants.csv', 'restaurant_info', restaurant_columns)
