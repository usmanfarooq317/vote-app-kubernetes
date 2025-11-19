import time
import redis
import psycopg2

# Redis
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Postgres
while True:
    try:
        db = psycopg2.connect(
            host="postgres",
            user="postgres",
            password="postgres",
            database="votesdb"
        )
        break
    except Exception as e:
        print("DB not ready, retrying in 3 sec...")
        time.sleep(3)
        
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    vote TEXT NOT NULL
)
""")
db.commit()

print("Worker started...")

while True:
    vote = redis_client.lpop("votes")
    if vote:
        vote = vote.decode()
        print("Processing vote:", vote)
        cursor.execute("INSERT INTO votes (vote) VALUES (%s)", (vote,))
        db.commit()
    else:
        time.sleep(1)
