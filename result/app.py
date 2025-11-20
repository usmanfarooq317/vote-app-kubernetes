from flask import Flask, render_template_string
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "postgres",
    "user": "postgres",
    "password": "postgres",
    "database": "votesdb"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Voting Results</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            padding: 30px;
        }
        .card {
            background: white;
            padding: 20px;
            width: 300px;
            margin: auto;
            border-radius: 10px;
            box-shadow: 0 0 10px #999;
            text-align: center;
        }
        h2 { color: #333; }
        .value { font-size: 40px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Voting Result</h2>
        <p class="value">🐱 Cats: {{ cats }}</p>
        <p class="value">🐶 Dogs: {{ dogs }}</p>
    </div>
</body>
</html>
"""

def get_results():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS votes (id SERIAL PRIMARY KEY, vote_text VARCHAR(50));")

    cursor.execute("SELECT COUNT(*) FROM votes WHERE vote_text='cats';")
    cats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM votes WHERE vote_text='dogs';")
    dogs = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    
    return cats, dogs


@app.route("/")
def home():
    cats, dogs = get_results()
    return render_template_string(HTML_TEMPLATE, cats=cats, dogs=dogs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
