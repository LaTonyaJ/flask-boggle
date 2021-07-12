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
    return render_template('board.html', board=board)


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
