from flask import Flask, render_template, redirect, url_for
import math
import time
from player import HumanPlayer, RandomComputerPlayer, SmartComputerPlayer

app = Flask(__name__)

# Global score dictionary
score = {"wins": 0, "losses": 0, "ties": 0}

# Define the TicTacToe class
class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

# Define the score update function
def update_score(result):
    if result == 'win':
        score["wins"] += 1
    elif result == 'loss':
        score["losses"] += 1
    elif result == 'tie':
        score["ties"] += 1

# Game play logic
def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):
            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switches player

        time.sleep(.8)

    if print_game:
        print('It\'s a tie!')
    return 'tie'

# Flask Route: Home Page to play the game
@app.route('/')
def index():
    game = TicTacToe()
    x_player = SmartComputerPlayer('X')
    o_player = HumanPlayer('O')
    
    # Start the game and get the result (win, loss, tie)
    result = play(game, x_player, o_player, print_game=False)
    
    # Update the score based on the result
    update_score(result)
    
    # Render the game board and updated score
    return render_template("index.html", score=score, board=game.board)

if __name__ == "__main__":
    app.run(debug=True)
