import random
# 変数の初期化
# 盤のサイズ
BOARD_SIZE_Y = 6
BOARD_SIZE_X = 7

# プレイヤー
PLAYER_1 = 1
PLAYER_2 = 2

EMPTY_SLOT = " "

# プレイヤークラスの作成
class HumanPlayer:
    def __init__(self, player_no, next_movex=None, next_movey=None):
        self.next_movex = next_movex
        self.next_movey = next_movey
        self.player_no = player_no
        self.player_name = "Human Player"

    def get_player_no(self):
        return self.player_no
    

    def get_next_move(self, connectboard):
        board = connectboard.get_board()
        not_break = True
        while not_break:  
            while True:  
                chip = input("Enter column (1-7): ")
                try:
                    self.next_movex = int(chip)-1
                    if self.next_movex >= 0 and self.next_movex < BOARD_SIZE_X:
                        break
                except ValueError:
                    print("Incorrect value. Please enter a value between 1 and 7")

            self.next_movey = BOARD_SIZE_Y-1

            while True:
                if board[self.next_movey][self.next_movex] != EMPTY_SLOT:
                    if self.next_movey > 0:
                        self.next_movey -= 1
                    else:
                        print("this column is full. please pick another column")
                        break
                else:
                    not_break = False
                    break

class RandomAI:
    def __init__(self, player_no, next_movex=None, next_movey=None):
        self.next_movex = next_movex
        self.next_movey = next_movey
        self.player_no = player_no
        self.player_name = "Random AI"

    def get_player_no(self):
        return self.player_no

    def get_next_move(self,connectboard):
        board = connectboard.get_board()
        not_break = True
        while not_break : 
            self.next_movex = random.randrange(0, BOARD_SIZE_X)
            self.next_movey = BOARD_SIZE_Y-1
            while True:
                if board[self.next_movey][self.next_movex] != EMPTY_SLOT:
                    if self.next_movey > 0:
                        self.next_movey -= 1
                    else:
                        break
                else:
                    not_break = False
                    break

class MiniMaxAI:
    def __init__(self, player_no):
        self.player_no = player_no
        self.player_name = "MiniMax AI"
        self.player_depth = 0
    
    def get_player_no(self):
        return self.player_no
    
    # number 1 player is maximize, number 2 player is minimize
    def get_next_move(self, connectboard):
        if self.player_no == 1:
            x, y, _ = self.minimax(connectboard, 0, True)
            return x, y
        
        elif self.player_no == 2:
            x, y, _ = self.minimax(connectboard, 0, True)
            return x, y

    def get_player_depth(self):
        return self.player_depth
        
    def terminal_state_check(self, connectboard):
        if connectboard.check_winner(1):
            result = 2000
            return True, result
    
        if connectboard.check_winner(2):
            result = -2000
            return True, result
    
        if connectboard.check_tie():
            result = 0
            return True, result
    
        return False, 0# Return None if no terminal state is found
    
    def gravity_check(self, x_input, board):
        # loop through the bottom of y, check if the current board[y][x_input] is already filled of not, if yes y - 1
        for y_input in range(BOARD_SIZE_Y-1, -1, -1):
            if board[y_input][x_input] == EMPTY_SLOT:
                return y_input
        
        return None  # return None if theres no empty slot anymore in the current column
    
    def minimax(self, connectboard, depth, maximizing_player):
        # 変数の初期化
        board = connectboard.get_board()
        terminal, evaluation = self.terminal_state_check(connectboard)

        # 終了条件
        if terminal:
            return None, None, evaluation

        if maximizing_player:  # 1 is maximizing player
            best_evaluation = -20000
            best_move = (None, None)
            
            # iterate x position
            for x_pos in range(BOARD_SIZE_X):
                # make sure that y is always at the bottom of the board(gravity check)
                y_pos = self.gravity_check(x_pos, board)

                if y_pos is not None:  
                    board[y_pos][x_pos] = PLAYER_1
                    _, _, evaluation = self.minimax(connectboard, depth + 1, False)
                    board[y_pos][x_pos] = EMPTY_SLOT
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_move = (x_pos, y_pos)

            return best_move[0], best_move[1], best_evaluation
        
        else:  # 2 is minimizing player
            best_evaluation = 2000
            best_move = (None, None)
            # iterate x position
            for x_pos in range(BOARD_SIZE_X):
                # make sure that y is always at the bottom of the board(gravity check)
                y_pos = self.gravity_check(x_pos, board)

                if y_pos is not None:  
                    board[y_pos][x_pos] = PLAYER_2
                    _, _, evaluation = self.minimax(connectboard, depth + 1, True)
                    board[y_pos][x_pos] = EMPTY_SLOT
                    if evaluation < best_evaluation:
                        best_evaluation = evaluation
                        best_move = (x_pos, y_pos)

            return best_move[0], best_move[1], best_evaluation


class Board:
    def __init__(self):
        self.board = [[EMPTY_SLOT for i in range(BOARD_SIZE_X)]for i in range(BOARD_SIZE_Y)]  # # 盤の初期化
        # テスト用
        # self.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2]]

    def get_board(self):
        return self.board

    # 盤の表示
    def display_board(self):
        output_row = "|"
        print("---------------")
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == PLAYER_1:
                    output_row += "1" + "|"
                elif self.board[y][x] == PLAYER_2:
                    output_row += "2" + "|"
                else:
                    output_row += " |"
            # output_row += "\n"
            print(output_row)
            print("---------------")
            output_row = "|"  # 新しい行に入るからまた空にする。
        print(" 1 2 3 4 5 6 7")

    def check_winner(self, player):

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                # 横検定
                if x < len(self.board[y])-3:
                    if self.board[y][x] == player and self.board[y][x+1] == player and self.board[y][x+2] == player and self.board[y][x+3] == player:
                        return True
                # 縦検定
                if y < len(self.board)-3:
                    if self.board[y][x] == player and self.board[y+1][x] == player and self.board[y+2][x] == player and self.board[y+3][x] == player:
                        return True
                # 斜め(左上-右下)検定
                if x < len(self.board[y])-3 and y < len(self.board)-3:
                    if self.board[y][x] == player and self.board[y+1][x+1] == player and self.board[y+2][x+2] == player and self.board[y+3][x+3] == player:
                        return True
                #斜め検定(右上-左下)検定
                if y < len(self.board)-3 and 3<=x<len(self.board[y]):
                    if self.board[y][x] == player and self.board[y+1][x-1] == player and self.board[y+2][x-2] == player and self.board[y+3][x-3] == player:
                        return True
                    
    def check_tie(self):
        # return all(cell != " " for row in self.board for cell in row)
        for i in range(BOARD_SIZE_Y):
            for j in range(BOARD_SIZE_X):
                if self.board[i][j] == " ":
                    return False
        return True
            
    
def play_game(player_1, player_2):
    connect4 = Board()
    connect4_board = connect4.get_board()

    players = [player_1, player_2]
    move_count = 1

    connect4.display_board()

    while True:
        to_move = players[(move_count%2)-1]
        player_num = to_move.get_player_no()

        x, y = to_move.get_next_move(connect4)
        
        if x is not None and y is not None:
            connect4_board[y][x] = player_num
            move_count += 1
            connect4.display_board()

            if connect4.check_winner(player_num):
                print(f"player {to_move.player_no} wins!")
                break

            elif connect4.check_tie():
                    print("DRAW!")
                    break
        else:
            break
            

if __name__ == "__main__":
    player_1 = MiniMaxAI(PLAYER_1)
    player_2 = MiniMaxAI(PLAYER_2)
    play_game(player_1, player_2)