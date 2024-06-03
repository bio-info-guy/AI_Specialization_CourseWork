// C++ program to solve knapsack problem using 
// branch and bound 
#include <bits/stdc++.h> 
using namespace std; 

// Structure for Item which store weight and corresponding 
// value of Item 
struct Item 
{ 
  float weight;
  float size;
  int value;
  int index;
  int rank;
  struct Item * witem;
  struct Item *	sitem;
}; 

// Node structure to store information of decision 
// tree 
struct Node 
{ 
  // level --> Level of node in decision tree (or index 
  //			 in arr[] 
  // profit --> Profit of nodes on path from root to this 
  //		 node (including this node) 
  // bound ---> Upper bound of maximum profit in subtree 
  //		 of this node/ 
  int level, profit; 
  float weight, size, bound;
  vector<int> indices;
}; 

bool cmp(Item a, Item b)
{
  double r1 = std::min((double)a.value / a.weight, (double)a.value / a.size);
  double r2 = std::min((double)b.value / b.weight, (double)b.value / b.size);
  return r1 > r2;
}

// Comparison function to sort Item according to 
// val/weight ratio 
bool wcmp(Item a, Item b) 
{ 
  double r1 = (double)a.value / a.weight; 
  double r2 = (double)b.value / b.weight; 
  return r1 > r2; 
} 

bool scmp(Item a, Item b)
{
  double r1 = (double)a.value / a.size;
  double r2 = (double)b.value / b.size;
  return r1 > r2;
}

// Returns bound of profit in subtree rooted with u. 
// This function mainly uses Greedy solution to find 
// an upper bound on maximum profit. 
float bound(Node u, int n, int W, int S, Item arr[]) 
{ 
  // if weight or size overcomes the knapsack capacity, return 
  // 0 as expected bound 
  if (u.weight >= W || u.size >= S) 
    return 0; 
  
  // initialize bound on profit by current profit 
  float sprofit_bound = (float)u.profit;
  float wprofit_bound = (float)u.profit;
  // start including items from index 1 more to current 
  // item index 
  int j = u.level + 1; 
  int totweight = u.weight;
  int totsize = u.size;
  
  // checking index condition and knapsack capacity 
  
  // Find max item in terms of v/w
  Item* item = min_element(arr+j, arr+n, wcmp);
  // Greedily add largest v/w items that are in levels after j-1
  // In order to not sort each time
  // start from the largest item after j-1
  // pointer will lead to the next largest item and check if it's level is after j-1
  // This is confusing,, SLOPPY CODE
  while (item->witem != NULL)
    {
      if(item->rank < j)
	{
	  item = item->witem;
	  continue;
	}
      totweight += item->weight; 
      wprofit_bound += (float)item->value;
      if (item->witem != NULL)
	{

	  if(totweight + item->witem->weight >= W && item->witem->rank >= j)
	    {
	      wprofit_bound += ((float)W - totweight) * (float)item->witem->value /
		item->witem->weight;
	      break;
	    }
	  item = item->witem;
	}
      else{
	break;
	  }
    }
  //DO SAME FOR v/s to find greedy bound
  j = u.level + 1;
  item = min_element(arr+j, arr+n, scmp);
  while (item->sitem != NULL)
    {
      if(item->rank < j)
	{
        item = item->sitem;
        continue;
	}
      totsize += item->size;
      
      sprofit_bound += (float)item->value;
      if (item->sitem != NULL)
        {

          if(totsize + item->sitem->size >= S && item->sitem->rank >= j)
	    {
	      sprofit_bound += ((float)S - totsize) * (float)item->sitem->value /
		item->sitem->size;
	      break;
	    }
	  item = item->sitem;
	}else{
	break;
      }
    }
  return std::min(wprofit_bound, sprofit_bound); 
} 

// Returns maximum profit we can get with capacity W 
int multiknapsack(int W, int S, Item arr[], int n) 
{ 
  // sorting Item on basis of value per unit 
  // weight
  int maxProfit = 0;
  int j = 0;
  int threshold = 0;
  
  // sort array of items based on min(v/w, v/s)
  sort(arr, arr + n, cmp);
  for(int i = 0; i < n; i++){
    arr[i].rank = i;
  }
  
  // solving for a heuristic value for max profit to start bounding quicker
  float	next_size = std::min(arr[j].weight, arr[j].size);
  while(j < n && threshold + next_size <= W){
    threshold += next_size;
    maxProfit += arr[j].value;
    j++;
    next_size = std::max(arr[j].weight, arr[j].size);
  }
  // Following code is sloppy
  // in order to avoid sorting the array each time we calculate a bound
  // Pre-sort the array and remember the order using pointers in the item structure
  // create index vector of array items
  vector<int> index(n, 0);
  for (int i = 0 ; i != index.size() ; i++) {
    index[i] = i;
  }
  // sort index vectors by corresponding item's v/w
  sort(index.begin(), index.end(), [&](const int& a, const int& b) {
      return (wcmp(arr[a], arr[b]));
				   });
  // each item has a pointer that points to the smaller item in order of decreasing v/w
  for(int i = 0; i < n-1; i++){
    arr[index[i]].witem = &arr[index[i+1]];
  }
  // DO SAME thing with v/s
  sort(index.begin(), index.end(),
    [&](const int& a, const int& b) {
      return (scmp(arr[a], arr[b]));
    });
       
  for(int i = 0; i < n-1; i++){
    arr[index[i]].sitem = &arr[index[i+1]];
  }
  
  // make a stack for traversing the node 
  stack<Node> SS; 
  Node u, v, maxNode; 
  
  // dummy node at starting 
  u.level = -1; 
  u.profit = u.weight = u.size = 0; 
  SS.push(u); 
  
  // One by one extract an item from decision tree 
  // compute profit of all children of extracted item 
  // and keep saving maxProfit 
  printf("Starting max profit is: %d\n", maxProfit);
  while (!SS.empty()) 
    { 
      // Dequeue a node 
      u = SS.top(); 
      SS.pop(); 
      
      // If it is starting node, assign level 0 
      //if (u.level == -1) 
      //v.level = 0; 
      
      // If there is nothing on next level 
      if (u.level == n-1) 
	continue; 
      
      // Else if not last node, then increment level, 
      // and compute profit of children nodes. 
      v.level = u.level + 1; 
      
      // Without taking
      //the item in knapsack                                                                                                                                                                                                                                                                  
      v.weight = u.weight;
      v.size = u.size;
      v.profit = u.profit;
      v.indices = u.indices;
      v.bound = bound(v, n, W, S, arr);
      if (v.bound > maxProfit)
	SS.push(v);
      
      // Taking current level's item add current 
      // level's weight and value to node u's 
      // weight and value 
      v.weight = u.weight + arr[v.level].weight;
      v.size = u.size + arr[v.level].size;
      v.profit = u.profit + arr[v.level].value; 
      v.indices=u.indices;
      v.indices.push_back(arr[v.level].index);
      // If cumulated weight is less than W and size less than S 
      // profit is greater than previous profit, 
      // update maxprofit 
      if ((v.weight <= W && v.profit > maxProfit) && v.size <= S)
	{
	  maxNode = v;
	  maxProfit = v.profit;
	  //	  printf("%d\n", maxNode.indices[0]);
	}
      // Get the upper bound on profit to decide 
      // whether to add v to Q or not. 
      v.bound = bound(v, n, W, S, arr); 
      // If bound value is greater than profit, 
      // then only push into queue for further 
      // consideration 
      if (v.bound > maxProfit)
	{
	  //	printf("%f\n", v.bound);
	SS.push(v);
	}
    }
  printf("items stored are:\n");
  for(int i = 0; i != maxNode.indices.size(); i++){
    printf("%d\n", maxNode.indices[i]);
  }
  return maxProfit; 
} 

// driver program to test above function 
int main() 
{
  //READ IN csv FILE GENERATED BY MKSgenerator.py 
  std::ifstream infile("MKS_problem.csv");
  std::string line;
  getline(infile, line);
  int i = 0;
  int n, W, S;
  std::istringstream iss(line);
  iss >> n >> S >> W;
  Item arr[n];
  int S_factor = W / std::__gcd(S,W);
  int W_factor = S / std::__gcd(S,W);
  W = W*W_factor;
  S = S*S_factor;
  while (std::getline(infile, line))
    {

      	float w, s;
	int v, ind;
	std::istringstream in(line);
	in >> ind;
	in >> s;
	in >> w;
	in >> v;
	
	arr[i] = {w*W_factor,s*S_factor,v,ind};
	i++;
    }
  cout << W << " " << S << " " << n <<"\n";

  printf("Maximum possible profit = %d\n",  multiknapsack(W, S, arr, n)); 

	return 0; 
} 
