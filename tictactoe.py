import random
import time

class TicTacToe:
    def __init__(self, size=3):
        self.size = size
        self.board = [str(i) for i in range(size * size)]
        self.current_winner = None

    def make_move(self, square, letter):
        if self.board[square] == str(square):
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // self.size
        row = self.board[row_ind*self.size:(row_ind+1)*self.size]
        if all([s == letter for s in row]):
            return True

        col_ind = square % self.size
        column = [self.board[col_ind+i*self.size] for i in range(self.size)]
        if all([s == letter for s in column]):
            return True

        if square % (self.size + 1) == 0:
            diagonal1 = [self.board[i*(self.size+1)] for i in range(self.size)]
            if all([s == letter for s in diagonal1]):
                return True

        if square % (self.size - 1) == 0 and square != 0 and square != (self.size * self.size) - 1:
            diagonal2 = [self.board[(i+1)*(self.size-1)] for i in range(self.size)]
            if all([s == letter for s in diagonal2]):
                return True

        return False

    def empty_squares(self):
        return any(s.isdigit() for s in self.board)

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x.isdigit()]

    def num_empty_squares(self):
        return sum(1 for s in self.board if s.isdigit())

    def print_board(self):
        for row in [self.board[i*self.size:(i+1)*self.size] for i in range(self.size)]:
            print('| ' + ' | '.join(row) + ' |')
        print()

class MinimaxAI:
    def __init__(self, letter):
        self.letter = letter
        self.nodes_searched = 0

    def get_move(self, game):
        if len(game.available_moves()) == game.size * game.size:
            square = random.choice(game.available_moves())
        else:
            self.nodes_searched = 0
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        self.nodes_searched += 1
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)
            state.board[possible_move] = str(possible_move)
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

class AlphaBetaAI:
    def __init__(self, letter):
        self.letter = letter
        self.nodes_searched = 0

    def get_move(self, game):
        if len(game.available_moves()) == game.size * game.size:
            square = random.choice(game.available_moves())
        else:
            self.nodes_searched = 0
            square = self.alphabeta(game, self.letter, -float('inf'), float('inf'))['position']
        return square

    def alphabeta(self, state, player, alpha, beta):
        self.nodes_searched += 1
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.alphabeta(state, other_player, alpha, beta)
            state.board[possible_move] = str(possible_move)
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, sim_score['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, sim_score['score'])

            if beta <= alpha:
                break

        return best

if __name__ == '__main__':
    game = TicTacToe(size=3)
    minimax_ai = MinimaxAI('X')
    alphabeta_ai = AlphaBetaAI('O')
    current_letter = random.choice(['X', 'O'])

    game.print_board()

    while game.empty_squares() and game.current_winner is None:
        time.sleep(0.5)
        if current_letter == 'X':
            move = minimax_ai.get_move(game)
        else:
            move = alphabeta_ai.get_move(game)
        game.make_move(move, current_letter)
        print(f"{current_letter} moves to square {move}")
        game.print_board()
        current_letter = 'O' if current_letter == 'X' else 'X'

    if game.current_winner:
        print(f'{game.current_winner} wins!')
    else:
        print("It's a draw!")
    print(f"Minimax nodes searched: {minimax_ai.nodes_searched}")
    print(f"Alpha-Beta nodes searched: {alphabeta_ai.nodes_searched}")
