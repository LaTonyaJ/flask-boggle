from boggle import Boggle
from flask import Flask, render_template, session, jsonify, request

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boggleflask'


@app.route('/')
def show_board():
    """Display Boggle Board and save to session"""

    board = boggle_game.make_board()
    session['board'] = board
    nplays = session.get('nplays', 0)
    highscore = session.get('highscore', 0)

    return render_template('board.html', board=board, nplays=nplays, highscore=highscore)


@app.route('/check-word')
def check_word():
    """Check if guessed word is a valid word from the dictionary and return a response.
    On the server, take the form value and check if it is a valid word in the dictionary"""

    guessed = request.args['guess_input']
    # print(guessed)
    board = session['board']
    # print(board)
    result = boggle_game.check_valid_word(board, guessed)
    return jsonify({'Result': result})


@app.route('/post-score', methods=['POST'])
def post_score():
    """Get score from front-end, increase number of plays, get the high score
    """
    score = request.json['score']
    # ?
    nplays = session.get('nplays', 0)
    highscore = session.get('highscore', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    return jsonify(brokeRecord=score > highscore)
