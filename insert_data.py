from datetime import date
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('stock_data.db')
cur = conn.cursor()

try:
    # Insert sample data
    data = [
        ('AAPL', 150.00, 155.00, 'Buy', '2024-07-24', True),
        ('GOOGL', 2750.00, 2800.00, 'Hold', '2024-07-24', False),
        ('MSFT', 299.00, 310.00, 'Sell', '2024-07-24', True)
    ]
    
    for record in data:
        cur.execute('''
            INSERT INTO stock_predictions (ticker, current_price, traded_price, ai_response, date, correct)
            VALUES (?, ?, ?, ?, ?, ?);
        ''', record)
    
    # Commit the changes
    conn.commit()
    print("Data inserted successfully.")
    
except sqlite3.Error as e:
    print(f"The error '{e}' occurred")

finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
