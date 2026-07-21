import sqlite3

# Make the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# Create a table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS shipment (id INTEGER, content TEXT, weight REAL, status TEXT)"
)

# Close the connection once db operations are done
connection.close()
