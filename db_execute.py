
import csv
import psycopg2
conn = psycopg2.connect("postgresql://fhrgggnmrmrxkn:d9843ee1039f5c4b915f9e863e6bd74fabff6377b2933c78af4fde3845a2c7c6@ec2-52-21-252-142.compute-1.amazonaws.com:5432/dng8iia4pdh78")
cur = conn.cursor()
sql_file = open("database.sql")
sql_as_string = sql_file.read()
cur.execute(sql_as_string)
cur.commit()