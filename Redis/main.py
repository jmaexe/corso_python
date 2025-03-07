import sqlite3

# import redis  # Togliere il commento se hai installato redis


def check_data_exists(data_value):
    # TODO: Inizializzare la connessione di redis
    # Esempio:
    # redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    # cached_result = redis_client.get(data_value)
    # if cached_result is not None:
    #     return cached_result == b'True'

    # Connessione ad un database sqlite
    # TODO: modificare il nome del db con quello dell'esercizio
    conn = sqlite3.connect("easy_exercise.db")
    cursor = conn.cursor()

    # TODO: inserire la query che vogliamo eseguire
    query = "SELECT COUNT(*) FROM candidate WHERE skill = ?"
    cursor.execute(query, (data_value,))
    result = cursor.fetchone()
    exists = result[0] > 0

    # TODO: Aggiornare la cache di Redis se necessario
    # Esempio:
    # redis_client.set(data_value, str(exists))

    # Chiusura della connessione col database.
    cursor.close()
    conn.close()

    return exists


if __name__ == "__main__":
    data_to_check = "Python"
    if check_data_exists(data_to_check):
        print(f"'{data_to_check}' esiste nel database.")
    else:
        print(f"'{data_to_check}' non esiste nel database.")
