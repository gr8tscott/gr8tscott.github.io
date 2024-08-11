import os
import psycopg2

import sqlite3

# Connect to the SQLite database (creates the file if it does not exist)
conn = sqlite3.connect('stock_data.db')

cur = conn.cursor()

# Drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS stock_predictions')

# Create the stock_predictions table
cur.execute('''
    CREATE TABLE stock_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        current_price REAL NOT NULL,
        traded_price REAL NOT NULL,
        ai_response TEXT NOT NULL,
        date TEXT NOT NULL,
        correct BOOLEAN NOT NULL
    );
''')

# Commit the changes
conn.commit()

print("Table 'stock_predictions' created successfully.")

# Close the cursor and connection
cur.close()
conn.close()
