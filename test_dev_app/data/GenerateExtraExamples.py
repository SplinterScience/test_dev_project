import sqlite3
import sys

# Connect to the database (or create one if it doesn't exist) named data.db
conn = sqlite3.connect('universe7.db')
cursor = conn.cursor()

# Create the table named 'routes'
cursor.execute('''
CREATE TABLE IF NOT EXISTS routes (
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    travel_time INTEGER NOT NULL
)
''')

# Insert the provided data
data = [
    ("T", "T", 6),
]

cursor.executemany('''
INSERT INTO routes (origin, destination, travel_time)
VALUES (?, ?, ?)
''', data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and data inserted successfully!")