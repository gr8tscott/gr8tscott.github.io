import psycopg2
import os
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to the database.")
    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")
