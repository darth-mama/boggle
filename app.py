from flask import Flask, request, render_template, jsonify, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "mooncakes"
# debug = DebugToolbarExtension(app)

boggle_gameboard = Boggle()


@app.route('/')
def home_page():
    """Show Boggle Board"""
    board = boggle_gameboard.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_gameboard.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["GET", "POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    new_highscore = session.get("highscore")
    print(new_highscore)
    return jsonify(brokeRecord=score > highscore)
