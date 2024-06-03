import time
import random
import numpy as np
import sys
import time
import random
import numpy as np


sys.setrecursionlimit(1500)

def knapSackTD(Size, Val, Capa):
    hashtable = {}
    def topdown(capa, n):
        if capa <= 0 or n == 0:
            return 0
        if Size[n-1] > capa:
            hashtable[(capa,n)] = topdown(capa,n-1)
            return hashtable[(capa,n)]
        elif hashtable.get((capa,n)):
            return hashtable[(capa, n)]
        else:
            hashtable[(capa,n)] = max([topdown(capa,n-1), Val[n-1]+topdown(capa-Size[n-1], n-1)])
            return hashtable[(capa,n)]
    return topdown(Capa, len(Size))


def knapSackBU(Size,Val,Capa):
	NS = [[0 for x in range (Capa+1)] for y in range (len(Size)+1)]
	NS[0][0] = 0
	for i in range(len(Val)+1):
		for j in range(Capa+1):
			if i== 0 or j == 0:
				NS[i][j] = 0
			elif j >= Size[i-1]:
				NS[i][j] = max(NS[i-1][j], NS[i-1][j-Size[i-1]]+Val[i-1])
			else:
				NS[i][j] = NS[i-1][j]
	return NS[len(Val)][Capa]


def main():
    Val = []
    Size = []
    for i in range (900):
        Val.append(random.randint(100,999))
    for i in range (900):
        Size.append(random.randint(1,100))
    Capa = 2000
    start_time = time.time()
    print("Given Capacity: 2000; set of 900 objects")
    print("The max value is:", knapSackBU(Size,Val,Capa))
    print("Bottom Up: --- %s seconds ---" % round(time.time() - start_time, 4))
    start_time = time.time()
    print("The max value is:", knapSackTD(Size,Val,Capa))
    print("Top Down: --- %s seconds ---\n" % round(time.time() - start_time, 4))
    Val = []; Size = []
    for i in range (20):
        Val.append(random.randint(1,90)*1000000)
    for i in range (20):
        Size.append(random.randint(1,10)*1000000)
    Capa = 5000000
    start_time = time.time()
    print("Given Capacity: 500; set of 20 objects")
    print("The max value is:", knapSackBU(Size,Val,Capa))
    print("Bottom Up: --- %s seconds ---" % round(time.time() - start_time, 4))
    start_time = time.time()
    print("The max value is:", knapSackTD(Size,Val,Capa))
    print("Top Down: --- %s seconds ---\n" % round(time.time() - start_time, 4))
if __name__== "__main__" :
	main()
    
