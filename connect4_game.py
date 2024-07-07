
class HumanPlayer:
    """
    人間のプレイヤークラス
    """
    def __init__(self, player_no, next_movex=None, next_movey=None):
        self.next_movex = next_movex
        self.next_movey = next_movey
        self.player_no = player_no
        self.player_name = "Human Player"

    def get_player_no(self):
        return self.player_no
    
    def get_next_move(self, to_move, connectboard):
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
                    return self.next_movex, self.next_movey, None

class RandomAI:
    """
    ランダムAIプレイヤークラス
    """
    def __init__(self, player_no, next_movex=None, next_movey=None):
        self.next_movex = next_movex
        self.next_movey = next_movey
        self.player_no = player_no
        self.player_name = "Random AI"

    def get_player_no(self):
        return self.player_no

    def get_player_name(self):
        return self.player_name

    def get_next_move(self, to_move, connectboard):
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
        return self.next_movex, self.next_movey, 0
    

class MiniMaxAI:
    """
    ミニマックスAIプレイヤークラス
    """
    def __init__(self, player_no):
        self.player_no = player_no
        self.player_name = "MiniMax AI"
        self.player_depth = 0
        self.max_search_depth = 5
    
    def get_player_no(self):
        return self.player_no

    def get_player_depth(self):
        return self.player_depth

    def get_player_name(self):
        return self.player_name
    
    def terminal_state_check(self, to_move, connectboard):
        if connectboard.check_winner(to_move):
            result = 20000000
            return True, result
    
        if connectboard.check_tie():
            result = 0
            return True, result
    
        return False, 0  # Return None if no terminal state is found
    

    def gravity_check(self, x_input, board):
        """
        重力効果をシミュレートするためのメソッド
        Connect4のチップはお互いに積み重なるため、底から確認する必要がある
        """
        for y_input in range(BOARD_SIZE_Y - 1, -1, -1):
            if board[y_input][x_input] == EMPTY_SLOT:
                return y_input
        
        return None  # 現在の列に空きスロットがない場合はNoneを返す
       
    def get_next_move(self, player_num, connectboard):
        x, y, evaluation = self.minimax(connectboard, 0, player_num, player_num)
        return x, y, evaluation

    def minimax(self, connectboard, depth, maximizing_player, to_move):
        # 変数の初期化
        board = connectboard.get_board()
        terminal, evaluation = self.terminal_state_check(to_move, connectboard)
        best_move = (None, None)
        # 最大化プレイヤーの初期評価値： -inf
        if maximizing_player == to_move:
            best_evaluation = -2000000000
        # 最小化プレイヤーの初期評価値： inf
        else:
            best_evaluation = 2000000000

        # 終了条件
        if terminal:
            if maximizing_player != to_move:
                evaluation = -evaluation
            
            return None, None, evaluation

        if depth == self.max_search_depth:
            eval_point = self.evaluation_point(connectboard)

            if maximizing_player == PLAYER_2:
                eval_point = -eval_point

            return None, None, eval_point

        # X位置を反復処理
        for x_pos in range(BOARD_SIZE_X):
            # 常に盤の底にyがあることを確認する(重力チェック)
            y_pos = self.gravity_check(x_pos, board)
            if y_pos is not None:  
                board[y_pos][x_pos] = to_move

                if to_move == PLAYER_1:
                    next_to_move  = PLAYER_2
                elif to_move == PLAYER_2:
                    next_to_move = PLAYER_1

                _, _, evaluation = self.minimax(connectboard, depth + 1, maximizing_player, next_to_move)
                
                board[y_pos][x_pos] = EMPTY_SLOT

                # 最大化プレイヤーのターンの場合
                if to_move == maximizing_player:
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_move = (x_pos, y_pos)
                # 最小化プレイヤーのターンの場合
                else:
                    if evaluation < best_evaluation:
                        best_evaluation = evaluation
                        best_move = (x_pos, y_pos)
                        
        return best_move[0], best_move[1], best_evaluation
    
    def evaluation_point(self, connectboard):
        """
        1. ボードのすべてのセルをチェック
        2. 空でない場合、
        3. 現在の位置から同じ色のコマが接続されているかを確認（横、縦、斜め）
        4. 評価ポイントを追加
        5. ループが終了したら、評価ポイントを返す
        """
        board = connectboard.get_board()
        eval_point = 0

        # ボードの全てのマスをループ
        for y in range(len(board)):
            for x in range(len(board[y])):
                # 空きマス出ない場合
                if board[y][x] != EMPTY_SLOT:
                    # プレイヤー１の場合、評価ポイントを加算
                    if board[y][x] == PLAYER_1:
                        eval_point += self.check_connections(connectboard, y, x, PLAYER_1)
                    # プレイヤー２の場合、評価ポイントを原産
                    elif board[y][x] == PLAYER_2:
                        eval_point -= self.check_connections(connectboard, y, x, PLAYER_2)
        return eval_point
    
    def check_connections(self, connectboard, starty, startx, player):
        """
        同じ色のコマの接続を確認するメソッド
        （横、縦、斜め）

        * 2つのコマの接続 = 10ポイント、3つのコマの接続 = 20ポイント
        """
        directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]  # 横、縦、斜め（左上ー右下）、斜め（右上ー左下）
        total_score = sum(self.check_direction(connectboard, starty, startx, player, dx, dy) for dx, dy in directions)
        return total_score

    def check_direction(self, connectboard, starty, startx, player, dx, dy):
        board = connectboard.get_board()
        count = 1
        score = 0
        x, y = startx + dx, starty + dy
        # 一方向のチェック
        while (self.is_whithin_bound(x, y) and self.is_player(board, x, y, player)):
            count += 1
            x += dx
            y += dy

        x, y = startx - dx, starty - dy
        # 逆方向のチェック
        while (self.is_whithin_bound(x, y) and self.is_player(board, x, y, player)):
            count += 1
            x -= dx
            y -= dy
        
        if count == 3:
            score += 20
        elif count == 2:
            score += 10

        return score

    def is_whithin_bound(self, x, y):
        return 0 <= x < BOARD_SIZE_X and 0 <= y < BOARD_SIZE_Y
    
    def is_player(self, board, x, y, player):
        return board[y][x] == player
     
    
class Board:
    def __init__(self):
        self.board = [[EMPTY_SLOT for i in range(BOARD_SIZE_X)]for i in range(BOARD_SIZE_Y)]  # # 盤の初期化

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
        rows = len(self.board)
        cols = len(self.board[0])
        
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                # 横検定
                if x < len(self.board[y]) - 3:
                    if self.board[y][x] == player and self.board[y][x + 1] == player and self.board[y][x + 2] == player and self.board[y][x + 3] == player:
                        return True
                # 縦検定
                if y < len(self.board) - 3:
                    if self.board[y][x] == player and self.board[y + 1][x] == player and self.board[y + 2][x] == player and self.board[y + 3][x] == player:
                        return True
                # 斜め(左上-右下)検定
                if x < len(self.board[y]) - 3 and y < len(self.board) - 3:
                    if self.board[y][x] == player and self.board[y + 1][x + 1] == player and self.board[y + 2][x + 2] == player and self.board[y + 3][x + 3] == player:
                        return True
                #斜め検定(右上-左下)検定
                if y < len(self.board)-3 and 3 <= x <len(self.board[y]):
                    if self.board[y][x] == player and self.board[y + 1][x - 1] == player and self.board[y + 2][x - 2] == player and self.board[y + 3][x - 3] == player:
                        return True
                    
    def check_tie(self):
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
        to_move = players[(move_count % 2 ) - 1]
        player_num = to_move.get_player_no()

        x, y, evaluation = to_move.get_next_move(player_num, connect4)

        if x is not None and y is not None:

            connect4_board[y][x] = player_num
            move_count += 1
            print(f"move {move_count}:{x+1} , evaluation: {evaluation}")
            connect4.display_board()

            if connect4.check_winner(player_num):
                print(f"player {to_move.player_no} wins!")
                break

            elif connect4.check_tie():
                print("DRAW!")
                break

            if to_move == player_1:
                print("First player to move")
            elif to_move == player_2:
                print("Second Player to move")

        else:
            print(f"NO MORE MOVES ON X AND Y")
            connect4.display_board()
            break
            

if __name__ == "__main__":
    import random
    # 変数の初期化
    # 盤のサイズ
    BOARD_SIZE_Y = 6
    BOARD_SIZE_X = 7

    # プレイヤー番号の定義
    PLAYER_1 = 1
    PLAYER_2 = 2

    # 空きますを表す文字
    EMPTY_SLOT = " "

    player_1 = HumanPlayer(PLAYER_1)
    player_2 = MiniMaxAI(PLAYER_2)
    play_game(player_1, player_2)