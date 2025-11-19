from flask import Flask, render_template_string, request
import redis
import psycopg2

app = Flask(__name__)
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Store last fetched results
current_results = {"cats": None, "dogs": None}

# Function to fetch results from Postgres
def get_db_results():
    try:
        conn = psycopg2.connect(
            host="postgres",
            user="postgres",
            password="postgres",
            database="votesdb"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM votes WHERE vote='cats'")
        cats = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM votes WHERE vote='dogs'")
        dogs = cursor.fetchone()[0]
        conn.close()
        return {"cats": cats, "dogs": dogs}
    except Exception as e:
        print("DB connection error:", e)
        return {"cats": 0, "dogs": 0}

# HTML template with simple CSS
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Voting App</title>
<style>
body { font-family: Arial, sans-serif; background-color: #f2f2f2; text-align: center; padding: 50px; }
h1 { color: #333; }
button { font-size: 18px; padding: 10px 20px; margin: 10px; cursor: pointer; border: none; border-radius: 5px; transition: 0.3s; }
button:hover { background-color: #555; color: white; }
.vote-btn { background-color: #4CAF50; color: white; }
.show-btn { background-color: #2196F3; color: white; }
.results { margin-top: 30px; padding: 20px; background-color: #fff; display: inline-block; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
</style>
</head>
<body>
<h1>Vote for Your Favorite!</h1>

<form method="post" action="/">
  <button class="vote-btn" name="vote" value="cats">Vote Cats</button>
  <button class="vote-btn" name="vote" value="dogs">Vote Dogs</button>
</form>

<form method="get" action="/show_results">
  <button class="show-btn" type="submit">Show Results from DB</button>
</form>

{% if show_results %}
<div class="results">
    <h2>Current Results</h2>
    <p>Cats: {{ cats }}</p>
    <p>Dogs: {{ dogs }}</p>
</div>
{% endif %}

</body>
</html>
"""

# Home route - voting
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        vote = request.form["vote"]
        redis_client.rpush("votes", vote)
    return render_template_string(HTML, show_results=False)

# Show results route
@app.route("/show_results")
def show_results():
    global current_results
    current_results = get_db_results()
    return render_template_string(
        HTML,
        show_results=True,
        cats=current_results["cats"],
        dogs=current_results["dogs"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
