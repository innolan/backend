import psycopg2

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(
        dbname="lan",
        user="master",
        # password="secret",
        host="localhost",
    )
except Exception as e:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print(f"Can`t establish connection to database: {e}")
