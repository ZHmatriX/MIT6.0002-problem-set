###########################
# 6.0002 Problem Set 1b: Space Change
# Name:仲逊
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #声明大小为target_weight+1的dp数组，初始化为无穷
    #dp[i]代表 可容纳质量为i的飞船至少需要多少个蛋能凑齐
    dp=[10**18 for x in range(0, target_weight+1)]

    #对于egg_weight中存在的质量，只需要一个蛋就能凑齐，将他们置为1
    for egg in egg_weights:
        dp[egg]=1

    for i in range(1,target_weight+1):
        for egg in egg_weights:
            dp[i]=min(dp[i],10**18) if i<egg else min(dp[i],dp[i-egg]+1)

    return dp[target_weight]

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    egg_weights = (1, 3, 50, 90)
    n = 100
    print("Egg weights = (1, 3, 50, 90)")
    print("n = 100")
    print("Expected ouput: 2 (2 * 50 = 100)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 10, 20, 38)
    n = 60
    print("Egg weights = (1, 10, 20, 38)")
    print("n = 60")
    print("Expected ouput: 3 (3 * 20 = 60)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()