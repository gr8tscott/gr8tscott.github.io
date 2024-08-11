import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('stock_data.db')
cur = conn.cursor()

try:
    # Query the table
    cur.execute('SELECT * FROM stock_predictions')
    rows = cur.fetchall()
    
    # Print the results
    for row in rows:
        print(row)

finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
