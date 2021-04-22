import csv
import psycopg2
conn = psycopg2.connect("postgresql://postgres:linge531@localhost:5432/Book_store")
cur = conn.cursor()
with open('books.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        cur.execute(
        "INSERT INTO books VALUES (%s, %s, %s, %s)",
        row
    )
conn.commit()