# 导入随机包
import copy
import math
import random

class RandomPlayer:
    """
    随机玩家, 随机返回一个合法落子位置
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color

    def random_choice(self, board):
        """
        从合法落子位置中随机选一个落子位置
        :param board: 棋盘
        :return: 随机合法落子位置, e.g. 'A1'
        """
        # 用 list() 方法获取所有合法落子位置坐标列表
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.random_choice(board)
        return action

class HumanPlayer:
    """
    人类玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color

    def get_move(self, board):
        """
        根据当前棋盘输入人类合法落子位置
        :param board: 棋盘
        :return: 人类下棋落子位置
        """
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player = "黑棋"
        else:
            player = "白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置
        while True:
            action = input(
                "请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。): ".format(player,
                                                                             self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")

import copy
class Node:
    def __init__(self,state,color,parent = None,action = None):
        self.visit = 0
        self.blackwin = 0
        self.whitewin = 0
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent
        self.action = action
        self.color = color

    def add_child(self,new_state,action,color):
        child_node = Node(new_state,parent=self,action = action,color=color)
        self.children.append(child_node)

    def if_fully_expanded(self):
        cnt_max = len(list(self.state.get_legal_actions(self.color)))
        print("cnt_max = ",cnt_max)
        cnt_now = len(self.children)
        print("cnt_now = ", cnt_now)
        if(cnt_max <= cnt_now):
            return True
        else:
            return False

class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color
    def if_terminal(self,state):
        # to see a state is terminal or not
        action_black = list(state.get_legal_actions('X'))
        action_white = list(state.get_legal_actions('O'))
        if(len(action_white) == 0 and len(action_black) == 0):
            return True
        else:
            return False

    def back_propagate(self,node,blackw,whitew):
        while(node is not None):
            node.visit+=1
            node.blackwin+=blackw
            node.whitewin+=whitew
            node = node.parent
        return 0

    def reverse_color(self,color):
        if(color == 'X'):
            return 'O'
        else:
            return 'X'

    def stimulate_policy(self,node):
        board = copy.deepcopy(node.state)
        color = copy.deepcopy(node.color)
        cnt = 0
        while not self.if_terminal(board):
            actions = list(node.state.get_legal_actions(color))
            if(len(actions)==0):
                #no way to go
                color = self.reverse_color(color)
            else:
                #have ways to go
                action = random.choice(actions)
                board._move(action,color)
                color = self.reverse_color(color)
            cnt+=1
            if cnt>20:
                break
        return board.count('X'),board.count('O')


    def ucb(self,node,uct_scalar=0.0):
        max = -float('inf')
        max_set=[]
        for c in node.children:
            exploit = 0
            if c.color == 'O':
                exploit = c.blackwin/(c.blackwin+c.whitewin)
            else:
                exploit = c.whitewin/(c.blackwin+c.whitewin)
            explore = math.sqrt(2.0*math.log(node.visit)/float(c.visit))
            uct_score = exploit+uct_scalar*explore
            if(uct_score==max):
                max_set.append(c)
            elif(uct_score>max):
                max_set=[c]
                max = uct_score
        if(len(max_set)==0):
            print("max_set is empty")
            print(len(node.children))
            node.state.display()
            return node.parent
        else:
            return random.choice(max_set)

    def expand(self,node):
        actions_available = list(node.state.get_legal_actions(node.color))
        actions_already = [c.action for c in node.children]
        if(len(actions_available)==0):
            return node.parent
        action = random.choice(actions_available)
        while action in actions_already:
            action=random.choice(actions_available)
        print(action)
        new_state = copy.deepcopy(node.state)
        new_state._move(action,node.color)
        new_state.display()
        new_color = self.reverse_color(node.color)
        node.add_child(new_state,action = action,color= new_color)
        return node.children[-1]

    def select_policy(self,node):
        while(not self.if_terminal(node.state)):
            if(len(list(node.state.get_legal_actions(node.color)))==0):
                return node;
            elif(not node.if_fully_expanded()):
                print("need to expand")
                new_node = self.expand(node)
                print("end of expand")
                return new_node
            else:
                print("fully expaned")
                node.state.display()
                print(len(node.children))
                print(list(node.state.get_legal_actions(node.color)))
                node = self.ucb(node)
        return node

    def MCTS_search(self,root,maxt = 100):
        #print("root state :")
        #root.state.display()
        for t in range(maxt):
            print("$$$$$$$$$$$$$$t = ",t)
            leave = self.select_policy(root)
            #print("leave state:")
            #leave.state.display()
            blackwin,whitewin = self.stimulate_policy(leave)
            self.back_propagate(leave,blackw=blackwin,whitew=whitewin)
        #print("root state :")
        #root.state.display()
        return self.ucb(root).action

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        action = None
        root_board = copy.deepcopy(board)
        root = Node(state=root_board,color=self.color)
        action = self.MCTS_search(root)

        # ------------------------------------------------------------------------

        return action

# 导入黑白棋文件
from game import Game

# 人类玩家黑棋初始化
black_player =  AIPlayer("X")

# AI 玩家 白棋初始化
white_player = RandomPlayer("O")

# 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
game = Game(black_player, white_player)

# 开始下棋
game.run()