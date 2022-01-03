import heapq
import json
import math
import sys
from Graph import Graph


class Utilities:

    def shortest_path(self, this_graph, id1: int, id2: int) -> (float, list):
        # Running dijkstr'a algorithm to get all weights of paths from the source node and also the parent dictionary
        # to reconstruct the shortest path
        dijkstraResult = self.dijkstra(this_graph, id1)
        dist = dijkstraResult[0]
        pointers = dijkstraResult[1]
        temp = id2
        path = []
        node = this_graph.nodes.get(id2)

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
    def dijkstra(self, graph: graph, src):
        # we introduce a new attribute to the nodes - weight, we will use this attribute to run Dijkstr'a algorithm
        # the reset function sets all the weight of the nodes in the graph to positive infinity
        self.d_prepare(graph=graph)

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
        graph.get_node(src).weight = 0

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
            for source_id in graph.all_out_edges_of_node(temp[1]).keys():
                if self.relax(graph ,temp[1], source_id):
                    distances[source_id] = graph.get_graph().get_all_v().get(source_id).weight
                    parents[source_id] = temp[1]
                if source_id not in visited.keys():
                    visited[source_id] = True
                    heapq.heappush(neighbours,
                                   (graph.get_graph().get_all_v().get(source_id).weight, source_id))

        return distances, parents


    # helper relax function for dijkstr'a algorithm,
    # For the edge from the vertex u to the vertex v, if d[u]+w(u,v)<d[v] is satisfied, update d[v] to d[u]+w(u,v)
    def relax(self, graph: graph ,src: int, dest: int) -> bool:
        src_weight = graph.get_all_v().get(src).weight
        destination_weight = graph.all_out_edges_of_node(src).get(dest)

        if graph.get_node(dest).weight <= src_weight + destination_weight:
            return False

        graph.get_node(dest).weight = src_weight + destination_weight
        return True


    # preparation function, sets all node weight to infinity
    def d_prepare(self, graph):
        for node in graph.get_all_v().values():
            node.weight = math.inf


    """
       This algorithm returns the center point of the graph, first we check if the graph is even strongly connected -
       otherwise it has no center node ( We do this by running DFS twice from the same node while transposing the graph )
       Then, we run dijkstr'a algorithm for each node to determine it's maximum distance and then return the minimum
       value related to said node - that is the center.
       """


    def centerPoint(self, graph) -> (int, float):
        # first, we make sure the graph is strongly connected
        if graph.is_connected():
            min_distance = sys.float_info.max
            node_id = -1

            for vertex in graph.get_all_v():
                curr_node = vertex
                max_distance = sys.float_info.min
                for node in graph.get_all_v():
                    if node == vertex:
                        continue
                    next_node = node
                    dijkstra = self.shortest_path(graph,curr_node, next_node)
                    tmp = dijkstra[0]

                    if dijkstra[0] is not float('inf'):
                        if tmp > max_distance:
                            max_distance = tmp
                        if tmp > min_distance:
                            break

                if min_distance > max_distance:
                    min_distance = max_distance
                    node_id = vertex

            return node_id, min_distance
        else:
            return None, float('inf')
