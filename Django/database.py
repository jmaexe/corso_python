import sqlite3

sqliteConn = sqlite3.connect("../data.sqlite")
cursor = sqliteConn.cursor()
cursor.execute("SELECT * FROM customers where country = 'France'")

result =  cursor.fetchall()

print(result[0])
