from tictactoe_minimax import MiniMaxPlayer
# 変数の初期化
BOARD_SIZE = 3

# プレイヤー
SYMBOL_1 = "X"
SYMBOL_2 = "O"

EMPTY_SLOT = " "  # 何もない状態

class HumanPlayer:
    def __init__(self, player_symbol, next_moveX=None, next_moveY=None):
        self.next_moveX = next_moveX
        self.next_moveY = next_moveY
        self.player_symbol = player_symbol
        self.incorrect_input_msg = "Incorrect value. Please enter a value between 1 and 3"

    def get_player_symbol(self):
        return self.player_symbol

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


class Board:
    def __init__(self):
        self.board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # ボードの初期化(3x3),2次元リスト
        # self.board = [['X', 'O', 'O'], 
        #               [' ', 'O', ' '], 
        #               [' ', 'X', 'X']] 
        
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
            # output_row += "\n"
            print(output_row)
            print("-------")
            output_row = "|"  # 新しい行に入るからまた空にする。
    
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
    players = [player_1, player_2]
    tictacboard = Board()
    the_board = tictacboard.get_board()
    turn = 0
    while True:
        current_player = players[turn % 2]
        player_symbol = current_player.get_player_symbol()
        tictacboard.display_board()
        print(f"{player_symbol} player's turn")
        x, y = current_player.get_next_move(tictacboard)
        the_board[y][x] = player_symbol
        print(f"{player_symbol} player played x:{x+1}, y:{y+1} \n")

        if tictacboard.check_winner(player_symbol):
            tictacboard.display_board()
            print(f"Game over:{player_symbol} wins")
            break
        
        if tictacboard.check_tie():
            print("Draw!!")
            break
        turn += 1


if __name__ == "__main__":
    # インスタンスの初期化
    player_1 = MiniMaxPlayer(SYMBOL_1)  # first player = "X"
    player_2 = MiniMaxPlayer(SYMBOL_2)  # second player = "O"
    game_board = Board()

    play_the_board(player_1, player_2)

