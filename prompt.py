import os
import psycopg2
import openai 
from openai import OpenAI
from dotenv import load_dotenv




load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)


pg_host = ""
pg_database = ""
pg_user = " "
pg_password =" "

conn = psycopg2.connect(
    host=pg_host,
    database=pg_database,
    user=pg_user,
    password=pg_password
)
cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS openai_chat_history (
        id SERIAL PRIMARY KEY,
        prompt TEXT,
        response TEXT
    )
""")
conn.commit()


initial_prompt = "I want to build a machine learning model to predict housing prices. Can you guide me through the steps?"


def generate_conversation(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

conversation = [initial_prompt]
response = generate_conversation(initial_prompt)
conversation.append(response)


cur.execute("INSERT INTO openai_chat_history (prompt, response) VALUES (%s, %s)", (initial_prompt, response))
conn.commit()


while True:
    follow_up_prompt = input("Enter a follow-up prompt (or 'exit' to stop): ")
    if follow_up_prompt.lower() == 'exit':
        break

    response = generate_conversation(follow_up_prompt)
    conversation.append(follow_up_prompt)
    conversation.append(response)


    cur.execute("INSERT INTO openai_chat_history (prompt, response) VALUES (%s, %s)", (follow_up_prompt, response))
    conn.commit()

    print(response)


cur.close()
conn.close()
