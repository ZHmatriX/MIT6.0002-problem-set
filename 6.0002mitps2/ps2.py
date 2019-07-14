# 6.0002 Problem Set 5
# Graph optimization
# Name:仲逊
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# 图的节点代表各个地点
# 图的边代表连接两个地点的直连路径(即不经过其他任何地点)
# 距离代表直连路径长度，total_distance就是距离
# outdoor_distance是直连路径的室外距离长度

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    res=Digraph()
    inFile = open(map_filename, 'r')
    for line in inFile.readlines():
        #以空格分割
        entry=line.split(' ')
        #如果图中没有这两个节点就加入 注意要用字符初始化Node对象
        if not res.has_node(Node(entry[0])):
            res.add_node(Node(entry[0]))
        if not res.has_node(Node(entry[1])):
            res.add_node(Node(entry[1]))
        
        #加入新的边 起点和终点为Node对象 总距离和室外距离要为int型
        res.add_edge(WeightedEdge(Node(entry[0]), Node(entry[1]), int(entry[2]), int(entry[3])))
    
    inFile.close()
    
    print("Loading map from file...")
    return res
# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# print(str(load_map("test.txt")))
# print(str(load_map("mit_map.txt")))

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
        
    path[0] = path[0] + [start]
    if not (digraph.has_node(Node(start)) and digraph.has_node(Node(end))): 
        raise ValueError("Graph doesn't have the node")
    if start == end: 
        return (path[0], path[1]) 
    
    for edge in digraph.get_edges_for_node(Node(start)): 
        #避免回路
        if str(edge.get_destination()) not in path[0]: 
            #要符合室外距离之和小于max_dist_outdoors
            if edge.get_outdoor_distance()+path[2]<=max_dist_outdoors:
                #判断是否需要更新路径，即判断路径是否为空或者有更短的路径
                if best_path == None or path[1]+edge.get_total_distance()<best_dist: 
                    #更新总距离和室外距离
                    tem_path=[path[0].copy(), path[1]+edge.get_total_distance(), path[2]+edge.get_outdoor_distance()]
                    #对更新了总距离和室外距离的路径递归调用函数，注意返回值是元组
                    new_path,new_dist = get_best_path(digraph, str(edge.get_destination()), end, 
                                                      tem_path, max_dist_outdoors, best_dist, best_path) 
                    #如果找到了就更新最佳路径和最佳距离
                    if new_path != None:
                        best_path = new_path 
                        best_dist = new_dist

    return (best_path, best_dist)

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """ 
    #调用get_best_path获取最短路径和最短距离
    short_path, short_dist=get_best_path(digraph,start,end,[[],0,0],max_dist_outdoors,0,None)
    
    #如果最短路不存在或者最短距离超过max_total_dist限制则抛异常
    #否则返回最短路径
    if short_path == None: 
        raise ValueError("unreachable destination")
    elif short_dist > max_total_dist: 
        raise ValueError("don't meet requirement")
    else: 
        return short_path
# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
