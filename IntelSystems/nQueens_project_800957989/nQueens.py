
# coding: utf-8

# In[1]:


from copy import deepcopy as copy
import numpy as np
import sys
class nQueenMatrixAgent:
    
    def __init__(self, heuristic='conflicts', size=8, smart_init=True):
        self.heuristic=self.conflicts if heuristic == 'conflicts' else self.cost
        self.size=size
        self.smart_init=smart_init
        self.history=[]
    
    def initMatrix(self,custom=None):
        if custom:
            self.board=custom
        else:
            board=np.zeros((self.size,self.size))
            if self.smart_init:
                row_index=np.random.choice(np.arange(self.size), size=self.size, replace=False)
            else:
                row_index=np.random.choice(np.arange(self.size), size=self.size)
            for i in np.arange(self.size):
                board[row_index[i],i]=1
            self.board=board

            
    # Calculate number of conflicts overall or in a single position for a single queen            
    def conflicts(self, config, index=None):
        diag=0
        reverse_config=np.rot90(config)
        
        # if index is given then only calculate conflicts for queen at indexed position
        if index:
            row, col=index[0], index[1]
            return np.sum(config[row,:])+np.sum(config.diagonal(col-row))+np.sum(reverse_config.diagonal(row-(self.size-col-1)))
        
        #if no index is given then calculate total conflicts across the board
        for i in np.arange(-self.size, self.size+1):
            diag += np.sum(config.diagonal(i))*(np.sum(config.diagonal(i))-1)+np.sum(reverse_config.diagonal(i))*(np.sum(reverse_config.diagonal(i))-1)
        return (np.sum(np.sum(config, axis=1)*(np.sum(config, axis=1)-1))+diag)/2
        
        
    def cost(self, config):
        pass
    
    
    
    # Randomly choose a single queen each time to minimize conflict
    def updownMovesSingleQueen(self, config, sideways=False):
        columns=np.random.choice(np.arange(self.size), size=self.size, replace=False)
        for i in np.arange(self.size):
            col=columns[i]
            cost=np.zeros((self.size))
            index=np.argmax(config[:,col])
            original_cost=self.conflicts(config, index=(index, col))-3
            for j in np.arange(self.size):
                cost[j]=self.conflicts(config, index=(j, col))-original_cost
            cost[index]=1
            if np.min(cost) > 0:
                if i == self.size -1:
                    return False
                continue
            if np.min(cost) == 0 and not sideways:
                if i == self.size -1:
                    return False
                continue
            else:
                break
        moves=np.where(cost==np.min(cost))
        pick_move=np.random.randint(len(moves[0]))
        return moves[0][pick_move], col, np.min(cost)
     
    # Steepest Ascent Algorithm (if Sideways = True then it is steepest ascent with sideway moves allowed)
    def updownMoves(self, config, sideways=False):
        cost_matrix=np.zeros((self.size,self.size))
        for i in np.arange(self.size):
            index=np.argmax(config[:,i])
            original_cost=self.conflicts(config, index=(index, i))-3
            for j in np.arange(self.size):
                cost_matrix[j,i]=self.conflicts(config, index=(j, i))-original_cost
            cost_matrix[index,i]=1
        if np.min(cost_matrix) >0:
            return False
        if np.min(cost_matrix) == 0 and not sideways:
            return False
        moves=np.where(cost_matrix==np.min(cost_matrix))
        pick_move=np.random.randint(len(moves[0]))
        return moves[0][pick_move], moves[1][pick_move], np.min(cost_matrix)
    
    def clear_hist(self):
        self.history=[]
        
    def check_goal(self, board):
        if self.conflicts(board) == 0:
            return True
        return False
    
    def convertPath(self, history):
        path=[]
        for hist in history:
            real_board=[['.' for i in range(self.size)] for i in range(self.size)]
            for i in range(self.size):
                real_board[hist[i]][i] = 'Q'
            path.append(real_board)
        return path
    
    def HillClimbingSolver(self, sideways=False, random_restart=False, max_iteration=200, max_moves=1000, min_conflicts=False):
        move=self.updownMoves if not min_conflicts else self.updownMovesSingleQueen
        self.initMatrix()  
        
        iterations=1
        if random_restart:
            iterations=max_iteration

        if self.check_goal(self.board):
            return 1, self.convertPath([np.argmax(self.board, axis=0)]), 0, 0

        for i in range(iterations):
            if sideways:
                sd_moves=0
            board=copy(self.board)
            self.clear_hist()
            self.history.append(np.argmax(board, axis=0))
            num_moves=0
            new_move=move(board, sideways=sideways)
            while new_move and max_moves != 0:
                if sideways and new_move[2] == 0: # check if a sideway move was made and add one to sideway move
                    sd_moves +=1
                if sideways and sd_moves > 100: # only 100 consecutive sideway moves are allowed
                    break
                if new_move[2] < 0: # reset number of sideway moves if a better move was found 
                    sd_moves=0
                num_moves +=1
                old=np.argmax(board[:, new_move[1]])
                board[new_move[0], new_move[1]]=1
                board[old, new_move[1]]=0
                self.history.append(np.argmax(board, axis=0))
                if self.check_goal(board):
                    return 1, self.convertPath(self.history), i+1, num_moves
                new_move=move(board, sideways=sideways)
                max_moves -=1
            self.initMatrix()     
        return 0, self.history, i+1, num_moves
        


# In[2]:


def showBoard(board):
    for i in board:
        print(' '.join(list(i)))

def printHistory(history):
    for hist in history:
        for i in range(len(hist)):
            if i == 0:
                print('The First step (random config): \n')
                showBoard(hist[i])
                print('\n')
                
            elif i == len(hist)-1:
                print('the Final Config: \n')
                showBoard(hist[i])
                print('\n')
            else:
                print('Step number: '+str(i+1)+'\n')
                showBoard(hist[i])
                print('\n')
                
TOTAL_ROUNDS=100
size=int(sys.argv[1])
#size=8 # in the script this would be commented out and users can provide their own number: python nQueens.py num_queens
# steepest hill climb no sideway moves TEST
q=nQueenMatrixAgent(size=size)
history=[]
win_moves=[]
loss_moves=[]
wins=0
loss=0
for i in range(TOTAL_ROUNDS):

    result, hist, _, num_moves=q.HillClimbingSolver(sideways=False)
    if result:
        if len(history) <= 3:
            history.append(hist)
        win_moves.append(num_moves)
        wins +=1
    else:
        loss_moves.append(num_moves)
        loss +=1
print('RESULTS FOR NO SIDEWAY MOVES:')
print('success rate is: '+str(float(wins)/TOTAL_ROUNDS))
print('failure rate is: '+str(float(loss)/TOTAL_ROUNDS))
print('average number of moves for a win is: '+str(np.mean(win_moves)))
print('average number of moves for a loss is: '+str(np.mean(loss_moves)))
print('The following are the STEPS by 3 of the successful attempts: \n')
printHistory(history)
    
# steepest hill climb with sideway moves allowed TEST
history=[]
win_moves=[]
loss_moves=[]
wins=0
loss=0
for i in range(TOTAL_ROUNDS):
    result, hist, _, num_moves=q.HillClimbingSolver(sideways=True)
    if result:
        if len(history) <= 3:
            history.append(hist)
        win_moves.append(num_moves)
        wins +=1
    else:
        loss_moves.append(num_moves)
        loss +=1
print('RESULTS FOR SIDEWAY MOVES:')
print('success rate is: '+str(float(wins)/TOTAL_ROUNDS))
print('failure rate is: '+str(float(loss)/TOTAL_ROUNDS))
print('average number of moves for a win is: '+str(np.mean(win_moves)))
print('average number of moves for a loss is: '+str(np.mean(loss_moves)))
print('The following are the STEPS by 3 of the successful attempts: \n')
printHistory(history)
# random-restart hill climb with no sideway moves allowed TEST

restarts=[]
win_moves=[]
for i in range(100):
    result, hist, i, num_moves=q.HillClimbingSolver(sideways=False, random_restart=True, max_iteration=100000)
    if result:
        win_moves.append(num_moves)
        restarts.append(i)

print('RESULTS FOR RANDOM RESTART NO SIDEWAY MOVES:')
print('number of restarts used: '+str(np.mean(restarts)))
print('average number of moves needed is: '+str(np.mean(win_moves)))
print('\n')

# random-restart hill climb with sideway moves allowed TEST
restarts=[]
win_moves=[]
for i in range(100):
    
    result, hist, i, num_moves=q.HillClimbingSolver(sideways=True,random_restart=True, max_iteration=100000)
    if result:
        win_moves.append(num_moves)
        restarts.append(i)

print('RESULTS FOR RANDOM RESTART WITH SIDEWAY MOVES:')
print('number of restarts used: '+str(np.mean(restarts)))
print('average number of moves needed is: '+str(np.mean(win_moves)))


