from flask import Flask, render_template_string, request
import redis

app = Flask(__name__)
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Homepage template
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Voting App</title>
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; text-align: center; padding: 50px; }
h1 { color: #333; margin-bottom: 30px; }
button { font-size: 18px; padding: 12px 25px; margin: 10px; cursor: pointer; border: none; border-radius: 5px; transition: 0.3s; }
button:hover { opacity: 0.8; }
.vote-btn { background-color: #4CAF50; color: white; }
.message { margin-top: 20px; font-size: 20px; color: #2E8B57; }
</style>
</head>
<body>
<h1>Vote for Your Favorite!</h1>

<form method="post" action="/">
  <button class="vote-btn" name="vote" value="cats">Vote Cats</button>
  <button class="vote-btn" name="vote" value="dogs">Vote Dogs</button>
</form>

{% if message %}
<div class="message">{{ message }}</div>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    if request.method == "POST":
        vote = request.form["vote"]
        redis_client.rpush("votes", vote)
        message = f"Your vote for '{vote}' has been recorded!"
    return render_template_string(HOME_HTML, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
