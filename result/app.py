from flask import Flask, render_template_string, jsonify
import psycopg2

app = Flask(__name__)

db = psycopg2.connect(
    host="postgres",
    user="postgres",
    password="postgres",
    database="votesdb"
)

HTML = """
<h1>Voting Results</h1>
<p>Cats: {{ cats }}</p>
<p>Dogs: {{ dogs }}</p>
"""

@app.route("/")
def results_page():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM votes WHERE vote='cats'")
    cats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM votes WHERE vote='dogs'")
    dogs = cursor.fetchone()[0]

    return render_template_string(HTML, cats=cats, dogs=dogs)


# NEW: API for frontend
@app.route("/api/results")
def results_api():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM votes WHERE vote='cats'")
    cats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM votes WHERE vote='dogs'")
    dogs = cursor.fetchone()[0]

    return jsonify({"cats": cats, "dogs": dogs})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
