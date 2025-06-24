import mysql.connector
try : 
    conn = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "root",
        database = "testdb"
    )
    cursor = conn.cursor()
    print("Connessione riuscita!")
    cursor.execute("select * from persone")
    print(cursor.fetchall())
    
except mysql.connector.Error as err:
    print("errore: ", err)
finally:
    cursor.close()
    conn.close()