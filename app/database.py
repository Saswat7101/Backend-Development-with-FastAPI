import sqlite3

# Make the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# Create a table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS shipment (id INTEGER, content TEXT, weight REAL, status TEXT)"
)

# Add shipment data
# cursor.execute(
#     "INSERT INTO shipment VALUES (12702, 'basalt', 18.7, 'In Transit)"
# )
# cursor.commit()

# Read a shipment by id
cursor.execute("SELECT * FROM shipment WHERE id = 12701")
result = cursor.fetchall()
print(result)

# Close the connection once db operations are done
connection.close()
