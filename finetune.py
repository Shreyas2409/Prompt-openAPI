import psycopg2


host = ""
database = ""
user = ""
password = ""


conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)


cur = conn.cursor()


cur.execute("SELECT * FROM openai_chat_history")


results = cur.fetchall()

print(results)

cur.close()
conn.close()
