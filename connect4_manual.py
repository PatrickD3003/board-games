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

    def get_next_move(self, board):
        loop_not_break = True  
        while loop_not_break:  
            while True:  
                input_x = int(input("Enter column (1-7): "))
                self.next_movex = int(input_x)-1
                if self.next_movex >= 0 and self.next_movex < BOARD_SIZE_X:
                    break
                else:
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
                    loop_not_break = False
                    break
    

# 盤の作成
def create_board():
    return [[EMPTY_SLOT for i in range(BOARD_SIZE_X)]for i in range(BOARD_SIZE_Y)]

# 盤の表示
def display_board(board):
    output_row = "|"
    print("---------------")
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == PLAYER_1:
                output_row += "1" + "|"
            elif board[y][x] == PLAYER_2:
                output_row += "2" + "|"
            else:
                output_row += " |"
        # output_row += "\n"
        print(output_row)
        print("---------------")
        output_row = "|"  # 新しい行に入るからまた空にする。
    print(" 1 2 3 4 5 6 7")

def check_winner(board, player_id):
    player = player_id.player_no
    for y in range(len(board)):
        for x in range(len(board[y])):
            # 横検定
            if x < len(board[y])-3:
                if board[y][x] == player and board[y][x+1] == player and board[y][x+2] == player and board[y][x+3] == player:
                    return True
            # 縦検定
            if y < len(board)-3:
                if board[y][x] == player and board[y+1][x] == player and board[y+2][x] == player and board[y+3][x] == player:
                    return True
            # 斜め(左上から右下への方向)の検定
            if x < len(board[y])-3 and y < len(board)-3:
                if board[y][x] == player and board[y+1][x+1] == player and board[y+2][x+2] == player and board[y+3][x+3] == player:
                    return True
            #斜め検定(右上から左下への方向)
            if y < len(board)-3 and 3<=x<len(board[y]):
                if board[y][x] == player and board[y+1][x-1] == player and board[y+2][x-2] == player and board[y+3][x-3] == player:
                    return True
                
def play_game():
    connect4_board = create_board()
    player_1 = HumanPlayer(PLAYER_1)
    player_2 = HumanPlayer(PLAYER_2)

    players = [player_1, player_2]
    move_count = 1

    display_board(connect4_board)

    while True:
        to_move = players[(move_count%2)-1]
        if to_move == player_1:
            print("First Player to move")
            player_1.get_next_move(connect4_board)
            x = player_1.next_movex
            y = player_1.next_movey
            connect4_board[y][x] = PLAYER_1
            move_count += 1
            display_board(connect4_board)
        else:
            print("Second Player to move")
            player_2.get_next_move(connect4_board)
            x = player_2.next_movex
            y = player_2.next_movey
            connect4_board[y][x] = PLAYER_2
            move_count += 1
            display_board(connect4_board)

        if check_winner(connect4_board, to_move):
            print(f"player {to_move.player_no} wins!")
            break

        elif move_count == (BOARD_SIZE_X * BOARD_SIZE_Y) + 1:
                print("DRAW!")
                break
            
play_game()