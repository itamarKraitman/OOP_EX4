import heapq
import math
import sys
from collections import deque
from typing import List

from graph import Graph

'''
This class is used to perform various algorithms on the underlying directed weighted graph.
It supports these algorithms:
    * Depth-First Search
    * Dijkstr'a Shortest Path
    * Determining if a graph is strongly connected
    * Finding the center of the graph
    * TSP 
This class also plots the graph and displays it to the user using tkinter
'''


class GraphAlgo:

    def __init__(self, *args):
        if len(args) == 1:
            self.graph = args[0]
        else:
            self.graph = Graph()

    def get_graph(self):
        return self.graph

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        # Running dijkstr'a algorithm to get all weights of paths from the source node and also the parent dictionary
        # to reconstruct the shortest path
        dijkstraResult = self.dijkstra(id1)
        dist = dijkstraResult[0]
        pointers = dijkstraResult[1]
        temp = id2
        path = []
        node = self.graph.nodes.get(id2)

        if node.weight == (float(math.inf)):
            return float(math.inf), []

        # We insert all nodes in the correct order
        while temp != id1:
            path.insert(0, temp)
            temp = pointers.get(temp)

        # inserting the source node to the list and return the result
        path.insert(0, id1)
        return dist.get(id2), path

    # Dijkstra's shortest path algorithm, we
    def dijkstra(self, src):
        # we introduce a new attribute to the nodes - weight, we will use this attribute to run Dijkstr'a algorithm
        # the reset function sets all the weight of the nodes in the graph to positive infinity
        self.d_prepare()

        # initializing dictionaries & lists
        distances = {}
        parents = {}
        visited = {}
        neighbours = [(0, src)]

        # a distance from the node to itself is 0
        distances[src] = 0

        # the source pointer has no "parent"
        parents[src] = None
        visited[src] = True

        # setting the source node's weight to 0
        self.graph.get_node(src).weight = 0

        """
        The "classic" dijkstra implementation using python's built in priority queue library Dijkstra's algorithm 
        will initially start with infinite distances and will try to improve them step by step. Mark all nodes 
        unvisited. Create a set of all the unvisited nodes called the unvisited set. Assign to every node a distance 
        value: set it to zero for our initial node and to infinity for all other nodes. For the current node, 
        consider all of its unvisited neighbors and calculate their distances through the current node. Compare the 
        newly calculated distance to the current assigned value and assign the smaller one. When we are done 
        considering all of the unvisited neighbors of the current node, mark the current node as visited and remove 
        it from the unvisited set. A visited node will never be checked again. If the destination has been marked 
        visited, we are done, otherwise, keep going. 
        """

        while not len(neighbours) == 0:
            temp = heapq.heappop(neighbours)
            for source_id in self.graph.all_out_edges_of_node(temp[1]).keys():
                if self.relax(temp[1], source_id):
                    distances[source_id] = self.get_graph().get_all_v().get(source_id).weight
                    parents[source_id] = temp[1]
                if source_id not in visited.keys():
                    visited[source_id] = True
                    heapq.heappush(neighbours,
                                   (self.get_graph().get_all_v().get(source_id).weight, source_id))

        return distances, parents

    # helper relax function for dijkstr'a algorithm,
    # For the edge from the vertex u to the vertex v, if d[u]+w(u,v)<d[v] is satisfied, update d[v] to d[u]+w(u,v)
    def relax(self, src: int, dest: int) -> bool:
        src_weight = self.get_graph().get_all_v().get(src).weight
        destination_weight = self.get_graph().all_out_edges_of_node(src).get(dest)

        if self.graph.get_node(dest).weight <= src_weight + destination_weight:
            return False

        self.graph.get_node(dest).weight = src_weight + destination_weight
        return True

    # preparation function, sets all node weight to infinity
    def d_prepare(self):
        for node in self.get_graph().get_all_v().values():
            node.weight = math.inf

    """
    TSP algorithm to find optimal route between a group of nodes.
    algorithm runs in O(n^2 * 2^n)
    """

    # def tsp(self, node_lst: List[int]) -> (List[int], float):
    #     shortest_path_weight = sys.maxsize
    #     total_path_weight = 0
    #     minimum = 0
    #     path = []
    #     for i in range(len(node_lst)):
    #         for j in range(len(node_lst)):
    #             curr_path_weight = self.shortest_path(i, j)[0]
    #             if shortest_path_weight > curr_path_weight:
    #                 minimum = j
    #                 shortest_path_weight = curr_path_weight
    #             total_path_weight += shortest_path_weight
    #             path.append(self.shortest_path(i, minimum)[1])
    #             node_lst.pop(i)
    #     return path, total_path_weight
    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if node_lst is None or len(node_lst) == 0:
            return None

        nearest_neighbour = node_lst[0]
        path = []
        total_path_weight = 0

        # We keep going as long as there's more than 1 node in our list
        # One node is not enough to calculate TSP solution
        while len(node_lst) > 1:
            node_lst.remove(nearest_neighbour)
            min_length = math.inf
            temp_path = []
            for city in range(len(node_lst)):
                temp = self.shortest_path(nearest_neighbour, node_lst[city])
                if temp[0] == math.inf:
                    break
                if temp[0] < min_length:
                    min_length = temp[0]
                    temp_path = temp[1]
                    current_node = node_lst[city]

            if len(path) == 0:
                path.extend(temp_path)
            else:
                temp_path.pop(0)
                path.extend(temp_path)

            total_path_weight = total_path_weight + min_length
            nearest_neighbour = current_node

        return path, total_path_weight

    """
    This algorithm returns the center point of the graph, first we check if the graph is even strongly connected -
    otherwise it has no center node ( We do this by running DFS twice from the same node while transposing the graph )
    Then, we run dijkstr'a algorithm for each node to determine it's maximum distance and then return the minimum
    value related to said node - that is the center.
    """

    def centerPoint(self) -> int:
        # first, we make sure the graph is strongly connected
        if self.is_connected():
            min_distance = sys.float_info.max
            node_id = -1

            for vertex in self.get_graph().get_all_v():
                curr_node = vertex
                max_distance = sys.float_info.min
                for node in self.get_graph().get_all_v():
                    if node == vertex:
                        continue
                    next_node = node
                    dijkstra = self.shortest_path(curr_node, next_node)
                    tmp = dijkstra[0]

                    if dijkstra[0] is not float('inf'):
                        if tmp > max_distance:
                            max_distance = tmp
                        if tmp > min_distance:
                            break

                if min_distance > max_distance:
                    min_distance = max_distance
                    node_id = vertex

            return node_id
        else:
            # if no center is found, graph is not strongly connected
            return 0

    # A simple DFS implementation using a double-edged queue acting as a stack
    def DFS(self, v: int, b: bool):
        stack = deque()
        stack.append(self.graph.nodes.get(v))
        flag = True
        while flag:
            if stack:
                v = stack.pop()
                if self.graph.get_node(v.getKey()).getTag() == 1:
                    continue
                self.graph.get_node(v.getKey()).setTag(1)

                if b:
                    u = self.graph.all_out_edges_of_node(v.getKey())
                else:
                    u = self.graph.all_out_edges_of_rev_node(v.getKey())
                for e in u.keys():
                    if self.graph.get_node(e).getTag() == 0:
                        stack.append(self.graph.get_node(e))
            else:
                flag = False

    def is_connected(self) -> bool:
        self.graph.reset_tags()
        it = iter(self.graph.nodes)
        v = next(it)
        self.DFS(v, True)
        for node in it:
            if self.graph.get_node(node).getTag() == 0:
                return False

        it2 = iter(self.graph.nodes)
        self.DFS(v, False)
        for node2 in it2:
            if self.graph.get_node(node2).getTag() == 0:
                return False
        return True