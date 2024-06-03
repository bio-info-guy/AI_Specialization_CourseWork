
# coding: utf-8

# In[6]:


from copy import deepcopy as copy
import numpy as np
import operator
class eightPuzzleAgent:
    
    def __init__(self, heuristic='manhattan', solution=np.array([[1,2,3],[4,5,6],[7,8,0]])):
        self.heuristic=self.manhattan if heuristic == 'manhattan' else self.displacement
        self.solution=solution
        self.history=[]
        self._nodes_expanded=0
        self._total_uniq_nodes=0
        self._total_nodes=0
        
        
    def manhattan(self, array):
        dist=0
        for i in [1,2,3,4,5,6,7,8]:
            horizontal=np.absolute(int(np.where(self.solution == i)[0]-np.where(array == i)[0]))
            vertical=np.absolute(int(np.where(self.solution == i)[1]-np.where(array == i)[1]))
            dist += horizontal+vertical
        return dist
            
    def displacement(self, array):
        return np.sum(np.int0((self.solution-array) != 0))
    
    def switchNumbers(self, node, i, j, k, l):
        newarray=copy(node.array)
        newarray[k, l], newarray[i, j] = newarray[i, j],  newarray[k, l]
        return newarray
    
    def clear_hist(self):
        self.history=[]
        
    def check_goal(self, node):
        if list(np.ndarray.flatten(node.array)) == list(np.ndarray.flatten(self.solution)):
            return True
        return False
    
    def check_hist(self, node):
        if list(np.ndarray.flatten(node.array)) in self.history:
            return True
        return False
    
    def generateChild(self, node): # expand a node into a list of its children nodes
        children=[]
        i, j = int(np.where(node.array == 0)[0]), int(np.where(node.array == 0)[1]) # find the empty square on the node's board matrix
        if i+1 <= 2:
            children.append(eightPuzzleNode(array=self.switchNumbers(node, i, j, i+1, j), parent=node, depth=node.depth+1))
        if i-1 >= 0:
            children.append(eightPuzzleNode(array=self.switchNumbers(node, i, j, i-1, j), parent=node, depth=node.depth+1))
        if j+1 <= 2:
            children.append(eightPuzzleNode(array=self.switchNumbers(node, i, j, i, j+1), parent=node, depth=node.depth+1))
        if j-1 <= 2:
            children.append(eightPuzzleNode(array=self.switchNumbers(node, i, j, i, j-1), parent=node, depth=node.depth+1))
        return children
    
    def output_result(self, node):
        arrays=[]
        while node != None:
            arrays.append(node)
            node=node.parent
        arrays.reverse()
        for i in range(len(arrays)):
            print('step number '+str(i)+' at depth '+str(arrays[i].depth)+': ')
            print(arrays[i].array)
        print('total number of nodes generated: '+str(self._total_nodes))
        print('total number of unique nodes generated: '+str(self._total_uniq_nodes))
        print('total number of nodes expanded: '+str(self._nodes_expanded))
    
    def AstarSolver(self, node):
        if self.check_goal(node):
            self.output_result(node)
            return 
        Frontier=[]
        if not self.check_hist(node):
            self.history.append(list(np.ndarray.flatten(node.array)))
        Frontier.append(node.set_cost(self.heuristic(node.array)))
        while len(Frontier) != 0:
            Frontier.sort(key=operator.attrgetter('cost')) # sort the frontier by the cost of the nodes 
            node=Frontier.pop(0) # chose the node with the lowest cost
            children=self.generateChild(node)
            self._nodes_expanded += 1
            self._total_nodes += len(children)
            newchildren=[]

            for i in range(len(children)):
                if self.check_goal(children[i]): # check if one of the expanded children is the solution
                    self.output_result(children[i])
                    return
                elif not self.check_hist(children[i]): # check if the children node has been seen before
                    newchildren.append(children[i])
                    self.history.append(list(np.ndarray.flatten(children[i].array))) # add the node's array to history
            self._total_uniq_nodes += len(newchildren) 
            for c in newchildren:
                Frontier.append(c.set_cost(self.heuristic(c.array)+node.depth)) # insert the new child nodes into the frontier

        
class eightPuzzleNode:
    
    def __init__(self, file=None, array=None, parent=None, depth=0):
        if np.any(array) != None:
            assert array.shape == (3,3), 'the input board is not 3 by 3'
            self.array=array
        else:
            a=[]
            for line in open(file):
                a.extend(list(line))
            a=np.array([int(i) for i in a]).reshape((3,3))
        self.parent=parent
        self.depth=depth

    def set_cost(self, cost):
        self.cost=cost
        return self


# ## solution for the examples provided by the TA:
# ** First example is: start from [[1,2,3],[7,4,5],[6,8,0]], end with [[1,2,3],[8,6,4],[7,5,0]] **

# ** with displacement **

# In[10]:


problem=np.array([[1,2,3],[7,4,5],[6,8,0]])
n=eightPuzzleNode(array=problem)
agent=eightPuzzleAgent(heuristic='displacement', solution=np.array([[1,2,3],[8,6,4],[7,5,0]]))
agent.AstarSolver(n)


# ** with manhattan distance **

# In[9]:


problem=np.array([[1,2,3],[7,4,5],[6,8,0]])
n=eightPuzzleNode(array=problem)
agent=eightPuzzleAgent(heuristic='manhattan', solution=np.array([[1,2,3],[8,6,4],[7,5,0]]))
agent.AstarSolver(n)


# ** Second example: start from [[2,8,1],[3,4,6],[7,5,0]], end with  [[3,2,1],[8,0,4],[7,5,6]] **

# ** with displacement **

# In[11]:


problem=np.array([[2,8,1],[3,4,6],[7,5,0]])
n=eightPuzzleNode(array=problem)
agent=eightPuzzleAgent(heuristic='displacement', solution=np.array([[3,2,1],[8,0,4],[7,5,6]]))
agent.AstarSolver(n)


# ** with manhattan distance **

# In[12]:


problem=np.array([[2,8,1],[3,4,6],[7,5,0]])
n=eightPuzzleNode(array=problem)
agent=eightPuzzleAgent(heuristic='manhattan', solution=np.array([[3,2,1],[8,0,4],[7,5,6]]))
agent.AstarSolver(n)

