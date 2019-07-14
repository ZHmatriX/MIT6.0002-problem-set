###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:仲逊
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
from copy import deepcopy

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    inFile = open(filename, 'r')
    # cow: dict key:cow name(string), val:weight(int)
    cow = {}
    for line in inFile.readlines():
        #以逗号分割
        cow_weight=line.split(',')
        #姓名为key int(重量)为value
        cow[cow_weight[0]]=int(cow_weight[1])
    inFile.close()
    return cow

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    ans=[]
    #将cows按值从大到小排序成为新的字典
    ordered_cows=dict(sorted(cows.items(),key = lambda x:x[1],reverse = True))
    one_trans=limit  #一次运输的剩余质量
    one_list=[]      #一次运输的奶牛
    while(len(ordered_cows)>0):
        #拷贝一份新字典，防止del出问题
        tem_cow=ordered_cows.copy()
        for (key,val) in tem_cow.items():
            #如果一次运输的剩余质量足够就加上
            if val<=one_trans:
                one_trans=one_trans-val
                one_list.append(key)
                del ordered_cows[key]
        #一次运输的奶牛已经都在one_list中
        ans.append(one_list.copy())
        #重置一次运输的剩余质量和一次运输的奶牛
        one_trans=limit
        one_list.clear()
    return ans


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    valid_case=[]
    min_size=10**10
    #对于cows中元素的所有划分
    for partition in get_partitions(cows.items()):
        is_valid=True
        #如果该划分中所有列表中奶牛的质量和不超过limit则合法
        if(len(partition)<min_size):
            for kvlist in partition:
                if sum([kv[1] for kv in kvlist])>limit:
                    is_valid=False
                    break
        if len(partition)<min_size and is_valid:
            min_size=len(partition)
            valid_case=deepcopy(partition)
            
    ans=[]
    #按要求返回 每次运输奶牛的名称列表 组成的列表
    for case in valid_case:
        ans.append([kv[0] for kv in case])
    return ans
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cow=load_cows("ps1_cow_data.txt")
    start = time.time()
    print("greedy_cow_transport answer is:")
    print(greedy_cow_transport(cow))
    end = time.time()
    print("greedy_cow_transport time is ",end-start)

    start = time.time()
    print("\nbrute_force_cow_transport answer is:")
    print(brute_force_cow_transport(cow))
    end = time.time()
    print("brute_force_cow_transport time is ",end-start)
    
if __name__ == '__main__':
    compare_cow_transport_algorithms()