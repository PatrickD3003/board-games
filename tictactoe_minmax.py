import random
# 変数の初期化
BOARD_SIZE = 3

# プレイヤー
SYMBOL_1 = "X"
SYMBOL_2 = "O"

EMPTY_SLOT = " "  # 何もない状態


class MiniMaxPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.player_name = "MiniMax AI" 
        self.player_depth = 0

    def get_player_symbol(self):
        return self.player_symbol
    
    def get_player_name(self):
        return self.player_name
    
    def get_player_depth(self):
        return self.player_depth
    
    def get_next_move(self, tictacboard):
        if self.player_symbol == "X":
            x, y, evaluation = self.minimax(tictacboard, 0, True)
            return y, x, evaluation
        elif self.player_symbol == "O":
            x, y, evaluation = self.minimax(tictacboard, 0, False)
            return y, x, evaluation

    def terminal_state_check(self, tictacboard):
        if tictacboard.check_winner("X"):  
            return True, 20000
        if tictacboard.check_winner("O"):
            return True, -20000
        if tictacboard.check_tie():
            return True, 0
        return False, 0
    
    def minimax(self, tictacboard, depth, maximizing_player):
        # 変数の初期化
        board = tictacboard.get_board()
        terminal, evaluation = self.terminal_state_check(tictacboard)
        
        # 終了条件
        if terminal:
            return None, None, evaluation
        
        if maximizing_player:  # Xプレイヤー
            best_evaluation = -20000
            best_move = (None, None)
            # 可能なムーブを回す
            for row in range(3):
                for column in range(3):
                    if board[row][column] == " ":
                        board[row][column] = "X"
                        _, _, evaluation = self.minimax(tictacboard, depth + 1, False)
                        board[row][column] = " "
                        if evaluation > best_evaluation:
                            best_evaluation = evaluation
                            best_move = (row, column)

            return best_move[0], best_move[1], best_evaluation

        else:  # Oプレイヤー
            best_evaluation = 20000
            best_move = (None, None)
            # 可能なムーブを回す
            for row in range(3):
                for column in range(3):
                    if board[row][column] == " ":
                        board[row][column] = "O"
                        _, _, evaluation = self.minimax(tictacboard, depth + 1, True)
                        board[row][column] = " "
                        if evaluation < best_evaluation:
                            best_evaluation = evaluation
                            best_move = (row, column)

            return best_move[0], best_move[1], best_evaluation


class HumanPlayer:
    def __init__(self, player_symbol, next_moveX=None, next_moveY=None):
        self.next_moveX = next_moveX
        self.next_moveY = next_moveY
        self.player_symbol = player_symbol
        self.player_name = "Human"
        self.incorrect_input_msg = "Incorrect value. Please enter a value between 1 and 3"

    def get_player_symbol(self):
        return self.player_symbol
    
    def get_player_name(self):
        return self.player_name

    def get_next_move(self, tictacboard):
        loop_not_break = True
        board = tictacboard.get_board()
        while loop_not_break:
            # x input
            while True:
                x_input = input("Enter x(1-3): ")
                try:
                    x_input = int(x_input)-1
                    if x_input > 2 or x_input < 0:
                        print(f"incorrect x,please enter a value between 1 and 3")
                    else:
                        break

                except ValueError:
                    print("input numbers only please")

            # y input
            while True:
                y_input = input("Enter y(1-3): ")
                try:
                    y_input = int(y_input)-1
                    if y_input > 2 or y_input < 0:
                        print(f"incorrect y, please enter a value between 1 and 3")
                    else:
                        break
                except ValueError:
                    print("input numbers only please")
            
            # 上書き防止
            if board[y_input][x_input] == " ":
                return x_input, y_input
            else:
                print("Not an empty square. Please enter your move again")


class RandomPlayer:
    def __init__(self, player_symbol,next_moveX=None, next_moveY=None):
        self.player_symbol = player_symbol
        self.player_name = "Random AI" 
    
    def get_player_symbol(self):
        return self.player_symbol
    
    def get_player_name(self):
        return self.player_name
    
    def get_next_move(self, tictacboard):
        the_board = tictacboard.get_board()
        while True:
            x = random.randrange(0, 2)
            y = random.randrange(0, 2)
            if the_board[y][x] == " ":
                return x, y
            else:
                continue


class Board:
    def __init__(self):
        self.board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # ボードの初期化(3x3),2次元リスト
        
    def get_board(self):
        return self.board
    
        # 盤の表示
    def display_board(self):
        output_row = "|"
        print("-------")
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.board[y][x] == SYMBOL_1:
                    output_row += "X" + "|"
                elif self.board[y][x] == SYMBOL_2:
                    output_row += "O" + "|"
                else:
                    output_row += " |"
            print(output_row)
            print("-------")
            output_row = "|"  
    
    def check_winner(self, player):
        for i in range(BOARD_SIZE):
            # 横検定
            if all([cell == player for cell in self.board[i]]):
                return True
            # 縦検定 
            if all([self.board[j][i] == player for j in range(BOARD_SIZE)]):  # yは固定で、xの値は(1-3)。
                return True
        # 斜め検定
        if(all(self.board[i][i] == player for i in range(3)) or 
           all(self.board[i][2-i] == player for i in range(3))):
            return True

    def check_tie(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == " ":
                    return False
                
        return True
                

def play_the_board(player_1, player_2):
    # 各プレイヤーは必ずget_next_move(),  get_player_symbol()関数をみつこと。
    players = [player_1, player_2]
    tictacboard = Board()
    the_board = tictacboard.get_board()
    turn = 0
    while True:
        # 順番ごとにプレイヤ交換、盤の表示
        current_player = players[turn % 2]
        player_symbol = current_player.get_player_symbol()
        player_name = current_player.get_player_name()

        tictacboard.display_board()
        # 次のムーブを獲得し、ボードに入力
        print(f"{player_symbol} player's turn")
        
        if player_name == "MiniMax AI":
            x, y, evaluation = current_player.get_next_move(tictacboard)
            the_board[y][x] = player_symbol
            print(f"Evaluation: {evaluation}")
            print(f"{player_name} player played x:{x+1}, y:{y+1} \n")

        else:
            x, y = current_player.get_next_move(tictacboard)
            the_board[y][x] = player_symbol
            print(f"{player_name} player played x:{x+1}, y:{y+1} \n")


        # 勝利検定
        if tictacboard.check_winner(player_symbol):
            tictacboard.display_board()
            print(f"Game over:{player_name} wins")
            break
        # 引き分け検定
        if tictacboard.check_tie():
            print("Draw!!")
            break
        turn += 1


if __name__ == "__main__":
    # player_1の手：X,player_2の手：O
    # インスタンスの初期化
    player_1 = MiniMaxPlayer(SYMBOL_1)  
    player_2 = RandomPlayer(SYMBOL_2)  
    game_board = Board()

    play_the_board(player_1, player_2)

