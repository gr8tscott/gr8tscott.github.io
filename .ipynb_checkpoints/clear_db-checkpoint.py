import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

try:
    # Drop the table if it exists
    cur.execute('DROP TABLE IF EXISTS stock_predictions;')
    conn.commit()
    print("Table dropped successfully.")
except psycopg2.Error as e:
    print(f"The error '{e}' occurred")
finally:
    cur.close()
    conn.close()
