from flask import Flask, render_template, request, redirect, url_for, session
import uuid
import game
import random

app = Flask(__name__)
app.secret_key = "forgotpassword"

# Memory storing for game states
games = {}

@app.route("/", methods=["GET", "POST"])
def home():
                if request.method == "POST":
                                username = request.form.get("username", "").strip()
                                # Username rule: 3 to 12 characters, letters and numbers only
                                if len(username) >= 3 and len(username) <= 12 and username.isalnum():
                                                session["username"] = username
                                                return redirect(url_for("play"))
                                else:
                                                return render_template("home.html", error="Name must be 3-12 letters and numbers only.")
                                                
                if "username" in session:
                                return render_template("home.html", username=session["username"])
                                
                return render_template("home.html")

@app.route("/play")
def play():
                if "username" not in session:
                                return redirect(url_for("home"))
                                
                game_id = str(uuid.uuid4())
                session["game_id"] = game_id
                
                answer = game.pick_word()
                
                games[game_id] = {
                                "answer": answer,
                                "guesses": [],
                                "draft": "",
                                "status": "playing",
                                "message": "",
                                "new_row": False,
                                "confetti": []
                }
                
                return redirect(url_for("game_view"))

def generate_confetti():
                # Generate 80 confetti pieces with random styles for the template
                pieces = []
                colors = ["#2fa866", "#f4a62a", "#e3def7", "#ffffff"]
                for i in range(80):
                                left = random.randint(0, 100)
                                delay = random.uniform(0, 3)
                                duration = random.uniform(2, 4)
                                size = random.uniform(0.5, 1.5)
                                rotation = random.randint(0, 360)
                                color = random.choice(colors)
                                
                                style = f"left: {left}%; animation-delay: {delay}s; animation-duration: {duration}s; " \
                                                                f"transform: scale({size}) rotate({rotation