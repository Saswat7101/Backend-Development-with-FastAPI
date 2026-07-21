import sqlite3

# Make the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# Create a table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)"
)

# Drop a table
# cursor.execute("DROP TABLE shipment")

# Add shipment data
# cursor.execute(
#     "INSERT INTO shipment (id, content, weight, status) VALUES (12701, 'Wooden Table', 2.5, 'In Transit'), (12702, 'Ceramic Mugs', 0.8, 'Placed'), (12703, 'Office Chair', 14.2, 'Out for Delivery'), (12704, 'Wireless Headphones', 1.1, 'Delivered'), (12705, 'Kitchen Blender', 6.7, 'Processing'), (12706, 'Cotton Bed Sheets', 3.4, 'In Transit'), (12707, 'Floor Lamp', 9.5, 'Delayed'), (12708, 'Palm Trees', 8.0, 'Placed');"
# )
# connection.commit()

# Read a shipment by id
cursor.execute("SELECT * FROM shipment WHERE id = 12701")
result = cursor.fetchall()
print(result)

# Update a record
cursor.execute("UPDATE shipment SET status = 'In Transit' WHERE id = 12705")
connection.commit()

# Delete a record by id
# cursor.execute("DELETE FROM shipment WHERE id = 12703")
# connection.commit()

# Close the connection once db operations are done
connection.close()
