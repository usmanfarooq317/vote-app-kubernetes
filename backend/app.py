from flask import Flask, jsonify
import redis
import psycopg2

app = Flask(__name__)

redis_client = redis.Redis(host="redis", port=6379, db=0)

db = psycopg2.connect(
    host="postgres",
    user="postgres",
    password="postgres",
    database="votesdb"
)

cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        animal TEXT NOT NULL
    )
""")
db.commit()

@app.route("/process")
def process_votes():
    while redis_client.llen("votes") > 0:
        vote = redis_client.lpop("votes").decode()
        cursor.execute("INSERT INTO votes (animal) VALUES (%s)", (vote,))
        db.commit()
    return "Processed votes!"

@app.route("/results")
def results():
    cursor.execute("SELECT animal, COUNT(*) FROM votes GROUP BY animal")
    result = cursor.fetchall()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
