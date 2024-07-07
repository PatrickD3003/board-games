# Mazeクラスの作成
class Maze:
    """
    迷路を読み込んで、書き込むためのクラス
    """
    def __init__(self, path):
        self.maze_sheet = []
        self.path = path
        self.start_goal_pos = []
        self.board_data = []
        self.path_cost_data = []

    # スタートの情報を保存
    def get_start_pos(self):
        return tuple(self.start_goal_pos[0])
    
    def get_goal_pos(self):
        return tuple(self.start_goal_pos[1])
    
    def get_path_cost_data(self):
        return self.path_cost_data

    def get_board_data(self):
        return self.board_data
    
    def initialize_maze(self):
        self.read_maze_file()
        self.separate_sheet()
        self.manipulate_sheet()
        self.process_path_cost_data()

    def read_maze_file(self):
        """
        迷路の情報をファイルから読み込み,要らない情報を削除する処理
        """
        with open(self.path, 'r') as file:
            self.raw_sheet = file.readlines()  # 生の情報を読み取る
            for row in range(len(self.raw_sheet)):
                self.maze_sheet.append([i.strip(",") for i in self.raw_sheet[row] if i not in ['\n'," ", ","]])
    
    def separate_sheet(self):
        """
        #と$で区切られたリストを三つのリストに分割する処理
        """
        index = 0
        mark = 0
        while (index < len(self.maze_sheet)):
            if "#" in self.maze_sheet[index] or "$" in self.maze_sheet[index]:
                mark += 1
                index += 1
                continue
            if mark == 0:
                self.board_data.append(self.maze_sheet[index])
            elif mark == 1:
                self.start_goal_pos.append([int(i) for i in self.maze_sheet[index]])
            elif mark == 2:
                self.path_cost_data.append([int(i) for i in self.maze_sheet[index]])
            index += 1
    
    def manipulate_sheet(self):
        """
        保存した迷路の情報をint型に変換し、スタートとゴール座標の追加
        壁(W) -> 1に変換する.
        """
        # 壁を1に変換、strからint型に変換
        for row in range(len(self.board_data)):
            for column in range(len(self.board_data[row])):
                if self.board_data[row][column] == 'W':
                    self.board_data[row][column] = WALL_SYMBOL 
        # スタートとゴールの情報の追加
        start_row, start_column = self.start_goal_pos[0]
        goal_row, goal_column = self.start_goal_pos[1]
        self.maze_sheet[start_row][start_column] = START_SYMBOL
        self.maze_sheet[goal_row][goal_column] = GOAL_SYMBOL
    def process_path_cost_data(self):
        if self.path_cost_data != []:
            self.path_cost_data = [[tuple(data[0:2]), tuple(data[2:4]), data[4]] for data in self.path_cost_data]

    def print_maze(self):
        """
        迷路情報をターミナルなどで出力する関数
        """
        print("Maze:")
        for i in self.board_data:
            print(" ".join(self.colorize_symbol(j) for j in i))

    def check_win(self, row, column):
        """
        現在の位置による勝利検定
        """
        if [row, column] == self.goal_pos:
            return True
        else:
            return False   
    
    def colorize_symbol(self, symbol):
        """
        迷路をわかりやすくするために、色付ける関数
        プレイヤー  ：黄色
        壁        ：青
        スタート   ：緑
        ゴール     ：赤
        """
        if symbol == PLAYER_SYMBOL:  
            return f"\033[33m{symbol}\033[0m"  # 黄
        elif symbol == WALL_SYMBOL:
            return f"\x1b[34m{symbol}\x1b[0m"  # 青
        elif symbol == START_SYMBOL:
            return f"\033[32m{symbol}\033[0m"  # 緑
        elif symbol == GOAL_SYMBOL:
            return f"\033[31m{symbol}\033[0m"  # 赤
        else:
            return symbol


class BfsNode:
    """
    探索きの実装
    parent  : 親ノード(探索木の中に上のノード)
    position: ノードが表している迷路の場所
    depth   : スタートノードからの距離（行動の数）
    """
    def __init__(self, position, parent=None, depth=0):
        self.position = position
        self.parent = parent
        self.depth = depth
    
    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def get_position(self):
        return self.position
    
    def get_depth(self):
        return self.depth


class BreadthFirstSearch:
    """
    BFSアルゴリズムは、現在の深さレベルのすべてのノードを
    次の深さレベルのノードに進む前に訪問します。
    """
    def __init__(self, maze_class, name):
        self.name = name
        # 迷路情報の初期化
        self.maze_class = maze_class
        self.maze_sheet = self.maze_class.get_board_data()
        self.maze_size_row, self.maze_size_column  = len(self.maze_sheet), len(self.maze_sheet[0])
        # クラスノードを使って、スタートとゴールのノード作成。
        self.start_node = BfsNode(self.maze_class.get_start_pos())
        self.goal_node = BfsNode(self.maze_class.get_goal_pos())
        # リストの初期化
        self.solution = []  # 結果を保存するリストの初期化
        self.frontier = [self.start_node]  # 発見されたが、まだ探索されていない全てのノードの集合
        self.visited = []  # 訪問済みのリスト
        # 最短ルート見つかるために使う辞書とリスト
        self.optimal_solution = []
        # コストの計算
        self.cost = 0
    
    def get_ai_name(self):
        return self.name
    
    def get_visited(self):
        return self.visited
    
    def start_algorithm(self):
        if self.solution == []:
            if self.breadth_first_search():
                self.backtrack_with_node()
            else:  
                return None, None
        path_cost = self.goal_node.get_depth()
        return self.optimal_solution, path_cost
    
    def breadth_first_search(self):
        # self.frontierが空ではなければ、ループ続く
        while self.frontier != []:
            # self.frontierをでキューし、self.solutionとself.visitedに値を保存する。
            parent_node = self.frontier.pop(0)  # self.frontierの最初の要素を取り出す
            # 勝利検定
            if self.is_goal_node(parent_node):
                self.solution.append(parent_node)
                self.goal_node = parent_node
                return True
            # 子ノードを探す
            if parent_node.get_position() not in self.visited:
                self.solution.append(parent_node)
                self.visited.append(parent_node.get_position())
                # 次のフロンティアを取得する
                child_node = self.find_next_frontier(parent_node)
                # next_frontierをself.frontierリストに追加する。
                self.frontier += child_node
        # 子ノードが全く見付かれない場合は、Falseを返す
        return False

    def is_goal_node(self, node):
        row, col = node.get_position()
        return self.maze_sheet[row][col] == GOAL_SYMBOL

    def find_next_frontier(self, pointed_node):
        pointed_coordinate = pointed_node.get_position()
        pointed_depth = pointed_node.get_depth()
        next_frontier = []  # 初期化
        # 指摘された位置(pointed_coordinate)の上下左右を確認し、
        direction_checker = [(0, +1), (0, -1), (+1, 0), (-1, 0)]
        pointed_row, pointed_column = pointed_coordinate[0], pointed_coordinate[1]
        for row_direction, column_direction in direction_checker:
            count_row = pointed_row + row_direction
            count_column = pointed_column + column_direction

            if self.is_within_bounds(count_row, count_column) and self.is_traversable(count_row, count_column):
                next_frontier_node = BfsNode([count_row, count_column], pointed_node, pointed_depth + 1)
                next_frontier.append(next_frontier_node)
        return next_frontier
    
    def is_within_bounds(self, row, col):
        return (0 <= row < self.maze_size_row) and (0 <= col < self.maze_size_column)
    
    def is_traversable(self, row, col):
        return self.maze_sheet[row][col] != WALL_SYMBOL and [row, col] not in self.visited

    def backtrack_with_node(self):
        current_pos = self.goal_node.get_position()
        self.optimal_solution = [current_pos]
        self.solution = self.solution[::-1]
        for node in self.solution:
            if node.get_position() == current_pos:
                if node.get_parent() is not None:
                    current_pos = node.get_parent().get_position()
                else:
                    continue
                self.optimal_solution.append(current_pos)
        self.optimal_solution = self.optimal_solution[::-1]
        

class DijkstraNode:
    """
    探索きの実装
    parent  : 親ノード(探索木の中に上のノード)
    position: ノードが表している迷路の場所
    cost : 経路コスト
    ノードを作成するとき、親ノードの経路コストと移動コストを合計し、クラスに保存。
    """
    def __init__(self, position, parent=None, cost=0):
        self.position = position
        self.parent = parent
        self.cost = cost
    
    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def get_position(self):
        return self.position
    
    def get_cost(self):
        return self.cost


class Dijkstra:
    """
    縁におけるコストが最も少ないノードを展開する。
    """
    def __init__(self, maze_class, name):
        self.name = name
        # 迷路情報の初期化
        self.maze_class = maze_class
        self.maze_sheet = self.maze_class.get_board_data()
        self.maze_size_row, self.maze_size_column  = len(self.maze_sheet), len(self.maze_sheet[0])
        # クラスノードを使って、スタートとゴールのノード作成。
        self.start_node = DijkstraNode(self.maze_class.get_start_pos())
        self.goal_node = DijkstraNode(self.maze_class.get_goal_pos())
        # リストの初期化
        self.solution = []  # 結果を保存するリストの初期化
        self.frontier = [self.start_node]  # 発見されたが、まだ探索されていない全てのノードの集合
        self.visited = []  # 訪問済みのリスト
        # 最短ルート見つかるために使う辞書とリスト
        self.optimal_solution = []
        # コストの計算
        self.cost_list = self.maze_class.get_path_cost_data()
        self.cost = 0
    
    def get_ai_name(self):
        return self.name
    
    def start_algorithm(self):
        # run the algorithm if the solution list is empty
        if self.solution == []:
            if self.dijkstra():
                self.backtrack_with_node()
            else:  # when the function return none
                return None, None
        path_cost = self.goal_node.get_cost()
        return self.optimal_solution, path_cost
    
    def dijkstra(self):
        # self.frontierが空ではなければ、ループ続く
        while self.frontier != []:
            # self.frontierをでキューし、self.solutionとself.visitedに値を保存する。
            lowest_cost_index = self.pick_lowest_cost()  # 一番低いコストを選ぶ
            dequeued_frontier = self.frontier.pop(lowest_cost_index)  
            # if the dequeued_frontier is equal to the goal node,
            if self.maze_sheet[dequeued_frontier.get_position()[0]][dequeued_frontier.get_position()[1]] == GOAL_SYMBOL:
                # append the selected node to the solution, break from the loop.
                self.solution.append(dequeued_frontier)
                self.goal_node = dequeued_frontier
                return True
            # if not, just append the selected node to the solution.
            elif dequeued_frontier.get_position() not in self.visited:
                self.solution.append(dequeued_frontier)
                self.visited.append(dequeued_frontier.get_position())
                # 次のフロンティアを取得する
                next_frontier = self.find_next_frontier(dequeued_frontier)
                # next_frontierをself.frontierリストに追加する。
                self.frontier += next_frontier
        # if theres no solution left, return False
        return False

    def pick_lowest_cost(self):
        """
        self.frontierリストの中から、コストが一番低いノードを選ぶ
        """
        lowest_cost = float('inf')
        lowest_cost_index = None

        for index, node in enumerate(self.frontier):
            node_cost = node.get_cost()
            if node_cost < lowest_cost:
                lowest_cost_index = index
                lowest_cost = node_cost
        return lowest_cost_index

    def find_next_frontier(self, pointed_node):
        pointed_coordinate = pointed_node.get_position()
        pointed_cost = pointed_node.get_cost()
        next_frontier = []  # 初期化
        # 指摘された位置(pointed_coordinate)の上下左右を確認し、
        direction_checker = [(0, +1), (0, -1), (+1, 0), (-1, 0)]
        pointed_row, pointed_column = pointed_coordinate[0], pointed_coordinate[1]
        for row_direction, column_direction in direction_checker:
            count_row = pointed_row + row_direction
            count_column = pointed_column + column_direction
            # 端ではないことの確認
            if (0 <= count_row < self.maze_size_row) and (0 <= count_column < self.maze_size_column):
                # 壁ではないこと＆訪問済みリストに入ってないことの確認
                if (self.maze_sheet[count_row][count_column] != WALL_SYMBOL) and ([count_row, count_column] not in self.visited):
                    next_frontier_coordinate = (count_row, count_column)
                    next_frontier_cost = self.get_next_frontier_cost(pointed_coordinate, next_frontier_coordinate)
                    next_frontier_node = DijkstraNode(next_frontier_coordinate, pointed_node, pointed_cost + next_frontier_cost)
                    next_frontier.append(next_frontier_node)
        return next_frontier

    def get_next_frontier_cost(self, pointed_coordinate, next_frontier_coordinate):
        """
        用意された経路コストのリストから、ノードのコストを取得する
        """
        for data in self.cost_list:
            if (data[0] == pointed_coordinate and data[1] == next_frontier_coordinate) or \
                (data[0] == next_frontier_coordinate and data[1] == pointed_coordinate):
                return data[2]
        print("no data found :(")

    def backtrack_with_node(self):
        current_pos = self.goal_node.get_position()
        self.optimal_solution = [current_pos]
        self.solution = self.solution[::-1]
        for node in self.solution:
            if node.get_position() == current_pos:
                if node.get_parent() is not None:
                    current_pos = node.get_parent().get_position()
                else:
                    continue
                self.optimal_solution.append(current_pos)
        self.optimal_solution = self.optimal_solution[::-1]
    

class greedyNode:
    """
    探索きの実装
    parent  : 親ノード(探索木の中に上のノード)
    position: ノードが表している迷路の場所
    depth   : スタートノードからの距離（行動の数）
    """
    def __init__(self, position, parent=None, depth=0):
        self.position = position
        self.parent = parent
        self.depth = depth
    
    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def get_position(self):
        return self.position
    
    def get_depth(self):
        return self.depth


class greedyBestFirstSearch:
    """
    greedy-BFSはヒューリスティック関数h(n)を使用して、
    現在のノードから目標までの直線距離を推定します。
    アルゴリズムは各可能な経路のコストを評価し、最も
    低いコストの経路を拡張します。このプロセスを目標に
    到達するまで繰り返します。
    """
    def __init__(self, maze_class, name):
        self.name = name
        # 迷路情報の初期化
        self.maze_class = maze_class
        self.maze_sheet = self.maze_class.get_board_data()
        self.maze_size_row, self.maze_size_column  = len(self.maze_sheet), len(self.maze_sheet[0])
        # クラスノードを使って、スタートとゴールのノード作成。
        self.start_node = greedyNode(self.maze_class.get_start_pos())
        self.goal_node = greedyNode(self.maze_class.get_goal_pos())
        # リストの初期化
        self.solution = []  # 結果を保存するリストの初期化
        self.frontier = [self.start_node]  # 発見されたが、まだ探索されていない全てのノードの集合
        self.visited = []  # 訪問済みのリスト
        # 最短ルート見つかるために使う辞書とリスト
        self.optimal_solution = []
        # コストの計算
        self.cost = 0
    
    def get_ai_name(self):
        return self.name
    
    def get_visited(self):
        return self.visited
    
    def start_algorithm(self):
        # run the algorithm if the solution list is empty
        if self.solution == []:
            if self.greedy_best_first_search():
                self.backtrack_with_node()
            else:  # when the function return none
                return None, None
        path_cost = self.goal_node.get_depth()
        return self.optimal_solution, path_cost
    
    def greedy_best_first_search(self):
        # self.frontierが空ではなければ、ループ続く
        while self.frontier != []:
            # self.frontierをでキューし、self.solutionとself.visitedに値を保存する。
            dequeued_frontier = self.heuristic(self.frontier)
            # if the dequeued_frontier is equal to the goal node,
            if self.is_goal_node(dequeued_frontier):
                # append the selected node to the solution, break from the loop.
                self.solution.append(dequeued_frontier)
                self.goal_node = dequeued_frontier
                return True
            # if not, just append the selected node to the solution.
            if dequeued_frontier.get_position() not in self.visited:
                self.solution.append(dequeued_frontier)
                self.visited.append(dequeued_frontier.get_position())
                # 次のフロンティアを取得する
                next_frontier = self.find_next_frontier(dequeued_frontier)
                # next_frontierをself.frontierリストに追加する。
                self.frontier += next_frontier
        # if theres no solution left, return False
        return False
    
    def heuristic(self, frontier_list):
        """
        return the node with the shortest manhattan distance
        from the frontier_list.
        """
        shortest_manhattan_value = float("inf")
        return_node = None
        for node in frontier_list:
            node_y, node_x = node.get_position()
            manhattan_value = self.get_manhattan_distance(node_y, node_x)
            if manhattan_value < shortest_manhattan_value:
                shortest_manhattan_value = manhattan_value
                return_node = node

        return return_node

    def get_manhattan_distance(self, row, column):
        """
        count the manhattan distance of a coordinate
        """
        goal_row, goal_column = self.goal_node.get_position()
        return abs(row-goal_row) + abs(column-goal_column)

    def is_goal_node(self, node):
        row, col = node.get_position()
        return self.maze_sheet[row][col] == GOAL_SYMBOL

    def find_next_frontier(self, pointed_node):
        pointed_coordinate = pointed_node.get_position()
        pointed_depth = pointed_node.get_depth()
        next_frontier = []  # 初期化
        # 指摘された位置(pointed_coordinate)の上下左右を確認し、
        direction_checker = [(0, +1), (0, -1), (+1, 0), (-1, 0)]
        pointed_row, pointed_column = pointed_coordinate[0], pointed_coordinate[1]
        for row_direction, column_direction in direction_checker:
            count_row = pointed_row + row_direction
            count_column = pointed_column + column_direction

            if self.is_within_bounds(count_row, count_column) and self.is_traversable(count_row, count_column):
                next_frontier_node = greedyNode([count_row, count_column], pointed_node, pointed_depth + 1)
                next_frontier.append(next_frontier_node)
        return next_frontier
    
    def is_within_bounds(self, row, col):
        return (0 <= row < self.maze_size_row) and (0 <= col < self.maze_size_column)
    
    def is_traversable(self, row, col):
        return self.maze_sheet[row][col] != WALL_SYMBOL and [row, col] not in self.visited

    def backtrack_with_node(self):
        current_pos = self.goal_node.get_position()
        self.optimal_solution = [current_pos]
        self.solution = self.solution[::-1]
        for node in self.solution:
            if node.get_position() == current_pos:
                if node.get_parent() is not None:
                    current_pos = node.get_parent().get_position()
                else:
                    continue
                self.optimal_solution.append(current_pos)
        self.optimal_solution = self.optimal_solution[::-1]


class aStarNode:
    """
    探索きの実装
    parent  : 親ノード(探索木の中に上のノード)
    position: ノードが表している迷路の場所
    cost : 経路コスト
    ノードを作成するとき、親ノードの経路コストと移動コストを合計し、クラスに保存。
    """
    def __init__(self, position, parent=None, cost=0, heuristic=0):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.f_cost = self.cost + self.heuristic
    
    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def get_position(self):
        return self.position
    
    def get_cost(self):
        return self.cost
    
    def get_f_cost(self):
        return self.f_cost


class aStar:
    """
    A*アルゴリズムは、移動コストg(n)とヒューリスティック関数h(n)の
    両方を評価します。総コストf(n) = g(n) + h(n)を用いて、最も低い
    コストのノードを選択し、目標ノードに到達するまで繰り返します。
    """
    def __init__(self, maze_class, name):
        self.name = name
        # 迷路情報の初期化
        self.maze_class = maze_class
        self.maze_sheet = self.maze_class.get_board_data()
        self.maze_size_row, self.maze_size_column  = len(self.maze_sheet), len(self.maze_sheet[0])
        # クラスノードを使って、スタートとゴールのノード作成。
        self.goal_node = aStarNode(self.maze_class.get_goal_pos())
        self.start_node = aStarNode(self.maze_class.get_start_pos(), None, 0, self.get_manhattan_distance(self.maze_class.get_start_pos()))
        # リストの初期化
        self.solution = []  # 結果を保存するリストの初期化
        self.frontier = [self.start_node]  # 発見されたが、まだ探索されていない全てのノードの集合
        self.visited = []  # 訪問済みのリスト
        # 最短ルート見つかるために使う辞書とリスト
        self.optimal_solution = []
        # コストの計算
        self.cost_list = self.maze_class.get_path_cost_data()
        self.cost = 0
    
    def get_ai_name(self):
        return self.name
    
    def start_algorithm(self):
        # run the algorithm if the solution list is empty
        if self.solution == []:
            if self.a_star():
                self.backtrack_with_node()
            else:  # when the function return none
                return None, None
        path_cost = self.goal_node.get_cost()
        return self.optimal_solution, path_cost
    
    def a_star(self):
        # self.frontierが空ではなければ、ループ続く
        while self.frontier != []:
            # self.frontierをでキューし、self.solutionとself.visitedに値を保存する。
            lowest_cost_index = self.pick_lowest_cost()  # 一番低いコストを選ぶ
            dequeued_frontier = self.frontier.pop(lowest_cost_index)  
            # if the dequeued_frontier is equal to the goal node,
            if self.maze_sheet[dequeued_frontier.get_position()[0]][dequeued_frontier.get_position()[1]] == GOAL_SYMBOL:
                # append the selected node to the solution, break from the loop.
                self.solution.append(dequeued_frontier)
                self.goal_node = dequeued_frontier
                return True
            # if not, just append the selected node to the solution.
            elif dequeued_frontier.get_position() not in self.visited:
                self.solution.append(dequeued_frontier)
                self.visited.append(dequeued_frontier.get_position())
                # 次のフロンティアを取得する
                next_frontier = self.find_next_frontier(dequeued_frontier)
                # next_frontierをself.frontierリストに追加する。
                self.frontier += next_frontier
        # 次の手が見つからない場合
        return False

    def pick_lowest_cost(self):
        """
        out of all the data available in self.frontier, 
        pick the one with the lowest score
        """
        lowest_cost = float('inf')
        lowest_cost_index = None
        for index, node in enumerate(self.frontier):
            node_f_cost = node.get_f_cost()
            if node_f_cost < lowest_cost:
                lowest_cost_index = index
                lowest_cost = node_f_cost
        return lowest_cost_index

    def find_next_frontier(self, parent_node):
        parent_coordinate = parent_node.get_position()
        parent_cost = parent_node.get_cost()
        next_frontier = []  # 初期化
        # 指摘された位置(pointed_coordinate)の上下左右を確認し、
        direction_checker = [(0, +1), (0, -1), (+1, 0), (-1, 0)]
        parent_row, parent_column = parent_coordinate[0], parent_coordinate[1]
        for row_direction, column_direction in direction_checker:
            child_row = parent_row + row_direction
            child_column = parent_column + column_direction
            # 端ではないことの確認
            if self.is_within_bound(child_row, child_column) and self.is_traversible(child_row, child_column):
                child_coordinate = (child_row, child_column)
                child_cost, child_heuristic = self.get_next_frontier_cost(parent_coordinate, child_coordinate)
                child_node = aStarNode(child_coordinate, parent_node, parent_cost + child_cost, child_heuristic)
                next_frontier.append(child_node)
        return next_frontier

    def is_within_bound(self, count_row, count_column):
        return (0 <= count_row < self.maze_size_row) and (0 <= count_column < self.maze_size_column)
    
    def is_traversible(self, count_row, count_column):
        return (self.maze_sheet[count_row][count_column] != WALL_SYMBOL) and ([count_row, count_column] not in self.visited)

    def get_next_frontier_cost(self, parent_coordinate, child_coordinate):
        """
        self.cost_list変数リストに基づいて、親座標から子座標への
        コスト値を取得します。
        """
        for data in self.cost_list:
            if (data[0] == parent_coordinate and data[1] == child_coordinate) or \
                (data[0] == child_coordinate and data[1] == parent_coordinate):
                heuristic_value = self.get_manhattan_distance(child_coordinate)
                return data[2], heuristic_value
        print("no data found :(")

    def get_manhattan_distance(self, child_coordinate):
        """
        マンハッタン距離（ヒューリスティック値)を計算する関数
        """
        row, column = child_coordinate
        goal_row, goal_column = self.goal_node.get_position()
        return abs(row-goal_row) + abs(column-goal_column)

    def backtrack_with_node(self):
        current_pos = self.goal_node.get_position()
        self.optimal_solution = [current_pos]
        self.solution = self.solution[::-1]
        for node in self.solution:
            if node.get_position() == current_pos:
                if node.get_parent() is not None:
                    current_pos = node.get_parent().get_position()
                else:
                    continue
                self.optimal_solution.append(current_pos)
        self.optimal_solution = self.optimal_solution[::-1]


def print_path(solution):
    """
    print the solution(coordinate path) to the terminal
    """
    solution = [list(i) for i in solution]
    print(f"Path to goal:")
    text = ""
    for coordinate in range(len(solution)):
        add_text = solution[coordinate] 
        text += f"{add_text}"
        if solution[coordinate] == solution[-1]:
            continue
        else:
            text += "->"
    print(text)
    print(f"Next AI move: {solution[0]} -> {solution[1]}")

def play_game(maze, AI_player):
    AI_name = AI_player.get_ai_name()
    # print: the maze initial state
    maze.print_maze()
    # start the BFS algorithm
    print(f"Starting {AI_name}...")
    solution, cost = AI_player.start_algorithm()
    if solution:
        print(f"{AI_name} success!!")
        print(f"Path cost: {cost}")
        # print the path
        print_path(solution)
    else:
        print(f"{AI_name} failed!! no solution found..")

if __name__ == "__main__":
    PLAYER_SYMBOL = "A"
    GOAL_SYMBOL = "G"
    START_SYMBOL = "S"
    WALL_SYMBOL = "1"
    EMPTY_SPACE_SYMBOL = "0"
    path1 = "maze1.txt"
    path2 = "maze2.txt"
    path3 = "maze-astar-test.txt"
    # test_maze1 = Maze(path1)
    # test_maze1.initialize_maze()
    # test_maze2 = Maze(path2)
    # test_maze2.initialize_maze()
    test_maze3 = Maze(path3)
    test_maze3.initialize_maze()
    # # さまざまなAIの初期化
    # bfs_AI = BreadthFirstSearch(test_maze1, "Breadth First Search")
    # dijkstra_AI = Dijkstra(test_maze2, "Dijkstra")
    # greedy_AI = greedyBestFirstSearch(test_maze1, "greedy best first search")
    a_star_AI = aStar(test_maze3, "A* Search")
    # ゲームの実行
    play_game(test_maze3, a_star_AI)
