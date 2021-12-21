import math
import random
import othello
import game

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):
    
    
    def __init__(self):
        super().__init__()
        
    def choose_move(self, state):
        self.a=[]
        # generate the list of moves:
        moves = state.generateMoves()
        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
            self.a.append(i)
        if len(self.a)>0:
            response = random.choice(self.a)
            print("Random move:",response)
            return moves[int(response)]
        else:
            pass 


class MinimaxAgent(game.Player):
     
    def __init__(self,depht_or_time):
        self.depth = depht_or_time
        super().__init__()
    def score(self,board1,player1):
        x1= 0
        boardSize = 8
        for i in range(boardSize):
            for j in range(boardSize):
                if board1[i][j] =='O':
                    x1+= 1
                if board1[i][j] =='X':
                    x1-= 1
        return x1
    def minmaxtree(self, state, depth):
        value, move =self.max(state,depth)
        return move

    def max(self, state, depth, Move=None):
        val=999
        moves = state.generateMoves()
        if len(moves)==0:
            return [self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move]
        if depth == 0:
            return [self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move]

        for i, move in enumerate(moves):
            state1 = state.applyMoveCloning(move)
            v2 , a2=self.min(state1,depth-1,Move=i)
            if v2>=val:
                val,move=v2,i
            else:
                val,move=999,i
        return val,move

    def min(self, state, depth,Move=None):
        val=-999
        moves = state.generateMoves()
        if len(moves)==0:
            return self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move
        if depth == 0:
            return self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move

        for i, move in enumerate(moves):
            tempstate = state.applyMoveCloning(move)
            v2 , a2 =self.max(tempstate,depth-1,Move=i)
            if v2<=val:
                val,move=v2,i
            else:
                val,move=-999,i
        return val,move

    def choose_move(self, state):
        moves = state.generateMoves()
        if len(moves)>0:
            for i, action in enumerate(moves):
                print('{}: {}'.format(i, action))
            response = self.minmaxtree(state,self.depth)
            print(response)
            return moves[int(response)]
        else:
            pass

class AlphaBeta(game.Player):
    def __init__(self,depht_or_time):
        self.depth = depht_or_time
        super().__init__()
        
    def score(self,board1,player1):
        x1= 0
        boardSize = 8
        for i in range(boardSize):
            for j in range(boardSize):
                if board1[i][j] =='O':
                    x1+= 1
                if board1[i][j] =='X':
                    x1-= 1
        return x1
    
    def alphabeta(self, state, depth):
        return self.max(state,depth, [-9999,None], [9999,None])[-1]

    def max(self, state, depth,alpha, beta, Move=None):
        val=[9999,None]
        moves = state.generateMoves()
        if len(moves)==0:
            return [self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move]
        if depth == 0:
            return [self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move]

        for i, move in enumerate(moves):
            state1 = state.applyMoveCloning(move)
           
            min1 = self.min(state1, depth-1, alpha, beta, Move=i)
            if val[0] <= min1[0]:
                val = [min1[0],i]
            else:
                val = [val[0],i]
                
            if val[0] <= alpha[0]:
                return val
            beta = [beta[0],i] if val[0] >= beta[0] else val
        return val

    def min(self, state, depth, alpha, beta,Move=None):
        val=[-9999,None]
        moves = state.generateMoves()
        if len(moves)==0:
            return [self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move]
        if depth == 0:
            return [self.score(state.board,othello.PLAYER_NAMES[state.nextPlayerToMove]),Move]

        for i, move in enumerate(moves):
            state1 = state.applyMoveCloning(move)
            max1= self.max(state1, depth-1, alpha, beta, Move=i)
            if val[0] >= max1[0]:
                val = [max1[0],i]
            else:
                val = [val[0],i]
            if val[0] >= alpha[0]:
                return val
            beta = [beta[0],i] if val[0] <= beta[0] else val
        return val

    def choose_move(self, state):
        moves = state.generateMoves()
        if len(moves)>0:
            for i, action in enumerate(moves):
                print('{}: {}'.format(i, action))
            response = self.alphabeta(state,self.depth)
            print(response)
            return moves[int(response)]
        else:
            pass
