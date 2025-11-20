import redis
import psycopg2
import time

redis_client = redis.Redis(host="redis", port=6379, db=0)

while True:
    try:
        vote = redis_client.blpop("votes", timeout=5)
        if vote:
            vote = vote[1].decode("utf-8")
            print("Processing vote:", vote)

            conn = psycopg2.connect(
                host="postgres",
                user="postgres",
                password="postgres",
                database="votesdb"
            )
            cursor = conn.cursor()

            # Ensure table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votes (
                    id SERIAL PRIMARY KEY,
                    vote_text VARCHAR(50)
                );
            """)

            cursor.execute("INSERT INTO votes (vote_text) VALUES (%s)", (vote,))

            conn.commit()
            cursor.close()
            conn.close()

    except Exception as e:
        print("Worker Error:", e)

    time.sleep(1)
