import redis
import psycopg2
import time

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Connect to Postgres
db = psycopg2.connect(
    host="postgres",
    user="postgres",
    password="postgres",
    database="votesdb"
)
cursor = db.cursor()

# Ensure the table exists once
cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        animal TEXT NOT NULL
    )
""")
db.commit()

print("Worker started. Waiting for votes...")

while True:
    try:
        vote = redis_client.blpop("votes", timeout=5)
        if vote:
            vote_value = vote[1].decode("utf-8")
            print("Processing vote:", vote_value)

            # Insert into votes table
            cursor.execute("INSERT INTO votes (animal) VALUES (%s)", (vote_value,))
            db.commit()
    except Exception as e:
        print("Worker Error:", e)
    time.sleep(1)
