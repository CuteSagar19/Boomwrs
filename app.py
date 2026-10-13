import os
import uuid
import random
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
import game

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")

# Memory storing for game states
games = {}

# Load word lists at import time so gunicorn will too at the time for deployments
game.load_words()

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
                                                                f"transform: scale({size}) rotate({rotation}deg); background-color: {color};"
                                pieces.append(style)
                return pieces

@app.route("/game")
def game_view():
                if "username" not in session or "game_id" not in session:
                                return redirect(url_for("home"))
                                
                game_id = session["game_id"]
                if game_id not in games:
                                return redirect(url_for("play"))
                                
                state = games[game_id]
                colors = game.keyboard_colors(state["guesses"], state["answer"])
                
                board = []
                for guess in state["guesses"]:
                                scores = game.score_guess(guess, state["answer"])
                                board.append([{"letter": guess[i], "score": scores[i]} for i in range(len(guess))])
                                
                return render_template("game.html", 
                                                                                                            username=session["username"],
                                                                                                            state=state, 
                                                                                                            board=board,
                                                                                                            word_length=len(state["answer"]),
                                                                                                            keyboard_colors=colors)

@app.route("/key", methods=["POST"])
def key():
                if "game_id" not in session:
                                return redirect(url_for("home"))
                                
                game_id = session["game_id"]
                if game_id not in games:
                                return redirect(url_for("play"))
                                
                state = games[game_id]
                
                if state["status"] != "playing":
                                return redirect(url_for("game_view"))
                                
                state["message"] = ""
                state["new_row"] = False
                
                val = request.form.get("key", "")
                
                if val == "ENTER":
                                if len(state["draft"]) < len(state["answer"]):
                                                state["message"] = "Not enough letters"
                                elif not game.is_real_word(state["draft"]):
                                                state["message"] = "No such word is present"
                                                state["new_row"] = False 
                                else:
                                                state["guesses"].append(state["draft"])
                                                state["new_row"] = True
                                                
                                                if state["draft"] == state["answer"]:
                                                                state["status"] = "won"
                                                                state["message"] = "You won!"
                                                                state["confetti"] = generate_confetti()
                                                elif len(state["guesses"]) >= 6:
                                                                state["status"] = "lost"
                                                                state["message"] = ""
                                                                state["confetti"] = generate_confetti()
                                                                
                                                state["draft"] = ""
                elif val == "DELETE":
                                if len(state["draft"]) > 0:
                                                state["draft"] = state["draft"][:-1]
                else:
                                if len(state["draft"]) < len(state["answer"]) and val.isalpha() and len(val) == 1:
                                                state["draft"] += val.lower()
                                                
                return redirect(url_for("game_view"))

@app.route("/typed", methods=["POST"])
def typed():
                if "game_id" not in session:
                                return redirect(url_for("home"))
                                
                game_id = session["game_id"]
                if game_id not in games:
                                return redirect(url_for("play"))
                                
                state = games[game_id]
                
                if state["status"] != "playing":
                                return redirect(url_for("game_view"))
                                
                state["message"] = ""
                state["new_row"] = False
                
                word = request.form.get("word", "").strip().lower()
                
                if len(word) != len(state["answer"]):
                                state["message"] = "Not enough letters"
                                state["draft"] = word[:len(state["answer"])]
                elif not game.is_real_word(word):
                                state["message"] = "No such word is present"
                                state["draft"] = word
                else:
                                state["guesses"].append(word)
                                state["new_row"] = True
                                state["draft"] = ""
                                
                                if word == state["answer"]:
                                                state["status"] = "won"
                                                state["message"] = "You won!"
                                                state["confetti"] = generate_confetti()
                                elif len(state["guesses"]) >= 6:
                                                state["status"] = "lost"
                                                state["message"] = ""
                                                state["confetti"] = generate_confetti()
                                                
                return redirect(url_for("game_view"))

@app.route("/logout")
def logout():
                session.clear()
                return redirect(url_for("home"))

if __name__ == "__main__":
                app.run(debug=True)
