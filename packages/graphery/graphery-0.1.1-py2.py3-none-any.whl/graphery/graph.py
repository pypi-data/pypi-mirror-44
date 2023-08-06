"""
Graph generator file. Contains classes related to generating networkx graphs
for search algorithms.
"""
#import random
import networkx as nx
import numpy as np
# import matplotlib.pyplot as plt
# import pylab as plt
# import gdal
# from PIL import Image, ImageDraw
# import scipy.misc as smp
# import sys

# import argparse


class Graph:
    """
    Graph class for generating graphs with NetworkX

    """
    def __init__(self, cost_map=None, weight_var="weight", mode="manhattan", verbose=False):
        """
        Graph constructor

        Parameters
        ----------
        cost_map: optional, np.ndarray
            The base map to get graph weights.
        weight_var: optional, str
            Name of the weight variable in edges dictionaries.

        """
        self.verbose = verbose
        self.default_weight_name = weight_var
        self.rows = 0
        self.cols = 0
        self._graph = None
        self.mode = mode
        if self.verbose:
            print(self.__str__())

        self.navigation_graph_init(cost_map, self.mode)

    def __str__(self):
        infoline = []
        infoline.append("Graph on {}x{} map in {} mode.\n".format(self.cols, self.rows, self.mode))
        if self._graph is not None:
            infoline.append("   - {} nodes\n".format(len(self._graph.nodes)))
            infoline.append("   - {} edges\n".format(len(self._graph.edges)))

        infostr = ""
        infostr = infostr.join(infoline)

        return infostr

    @property
    def graph(self):
        """ Graph property getter """
        return self._graph

    def navigation_graph_init(self, cost_map, mode=""):
        """
        Set the internal graph using the shape of a rhombus. 4 nodes and
        12 vertix per pixel

        This process is performed ini three steps,
            1. Create a real empty directional graph.
            2. Generate the edges between nodes (in both senses)
                that will automatically generate missing nodes.
            3. Load a map of weight.

        Parameters
        ----------
        cost_map : cost map (weights)

        """
        if cost_map is not None and isinstance(cost_map, np.ndarray):
            self.rows = cost_map.shape[0]
            self.cols = cost_map.shape[1]

        #if self._graph is not None:
        #    # TODO clean the graph
        #    del self._graph


        if mode != "":
            self.mode = mode

        if self.mode == "diagonals":
            self._graph = nx.Graph()
            self.edge_generator(cost_map)
        else:
            self._graph = nx.DiGraph()
            self.edge_generator_grid(cost_map)

        return True


    def edge_generator(self, cost_map):
        """
        Generates the next structure for navigating each of the pixels.

        Graph generator for 1 pixel

        Composition: 4 path_nodes
                     6 edges

               2
               o
              /|\
           0 o-|-o 1
              \|/
               o
               3
        """
        cost = 0

        if self.verbose:
            print("Generating diagonal edges on {}x{} grid".format(self.cols, self.rows))

        # Edge weights, cost multiplicators, must be > 1.0
        # to avoid minimizing the heuristic distance
        weight_short = 1.0 + np.sqrt(2 * 0.5**2)
        weight_long = 2.0
        #random_weights = random.randint(0, 2) * 3+1

        coord_offset_struct = [
            (0.0, 0.5),
            (1.0, 0.5),
            (0.5, 0.0),
            (0.5, 1.0)
        ]

        edges_specs = [
            (0, 1, weight_long),
            (2, 3, weight_long),
            (0, 2, weight_short),
            (0, 3, weight_short),
            (1, 2, weight_short),
            (1, 3, weight_short)
        ]

        cel = []  # current edge list
        tcel = []

        for y_val, x_val in self.combinations(self.rows, self.cols):
            # numpy arrays are rows first, cols then.
            cost = cost_map[y_val][x_val]

            for edge_a, edge_b, edge_w in edges_specs:
                dx1, dy1 = coord_offset_struct[edge_a]
                dx2, dy2 = coord_offset_struct[edge_b]

                cel.append(((x_val + dx1, y_val + dy1),
                            (x_val + dx2, y_val + dy2),
                            {"weight": cost * edge_w}))

            if x_val == self.cols - 1:
                tcel.extend(cel)
                cel = []

        # Adding a bunch of edges with their dictionnaries
        # For the same data here is the benchmark adding 100 of edges:
        #  - add_edge():  120us
        #  - add_edges_from():  120us
        #  - add_weight_edges_from()  :  120us
        self._graph.add_edges_from(tcel)

        # Creating right vertex
        return True

    def update_cost_map(self, cost_map):
        """ Something """
        # load_map_grid copy
        pass

    def edge_generator_grid(self, cost_map):
        """
        Edge Generator Grid

        Parameters
        ----------
        cost_map :

        """
        edge_weight = 0
        #random_weights = random.randint(0, 2) * 3 + 1

        cel = []  # current edge list
        tcel = []

        for x_val, y_val in self.combinations(self.cols, self.rows):
            # edge_weight = self.rows * self.cols + cost_map[y_val][x_val]
            edge_weight = cost_map[y_val][x_val]
            if y_val == 0 and x_val == 0:
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val == (self.rows - 1)  and x_val == 0:
                cel.append(((x_val, y_val-1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val == 0  and x_val == (self.cols - 1):
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val == (self.rows - 1)  and x_val == (self.cols - 1):
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val-1), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val == 0 and x_val < (self.cols - 1):
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val == 0 and x_val < (self.cols - 1):
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val < (self.rows - 1)  and x_val == (self.cols - 1):
                cel.append(((x_val, y_val-1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val == (self.rows - 1)  and x_val < (self.cols - 1):
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val-1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))

            elif y_val < (self.rows - 1)  and x_val == 0:
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val-1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))

            else:
                cel.append(((x_val+1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val-1, y_val), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val+1), (x_val, y_val),
                            {"weight": edge_weight}))
                cel.append(((x_val, y_val-1), (x_val, y_val),
                            {"weight": edge_weight}))

            if y_val == self.rows - 1:
                tcel.extend(cel)
                cel = []

        self._graph.add_edges_from(tcel)

        if self.verbose:
            print(self._graph.edges)

        return True

    @staticmethod
    def add_node_information(graph, key, data):
        """
        Add other information to nodes other than weights for the edges. This
        will be an added key to the dictionary that contains the default graph
        information.

        Parameters
        ----------
        graph : nx.classes.graph.Graph or nx.classes.digraph.DiGraph()
            The graph which you would like to add extra information to at
            each node.
        key : str
            The key name of the information you want add.
        data : np.ndarray
            A 2x2 array that utilizes the row x col numbering of the node values
            to allow for easy transcribing of information from the array to the
            the graph node.

        Returns
        -------
        graph : nx.classes.graph.Graph or nx.classes.digraph.DiGraph()
            The graph that was passed to the function but now with the
            information desired at each node.

        """
        for node in graph.nodes():
            print("WARNING graph structure is not guaranteed: LINE HHH")
            graph[node][key] = data[node[0], node[1]]

        return graph

    @staticmethod
    def get_startend_gridmode(list_of_points):
        """
        Something
        """
        start_position_x = list_of_points[0][0]
        start_position_y = list_of_points[0][1]
        finish_position_x = list_of_points[1][0]
        finish_position_y = list_of_points[1][1]

        v_start = (start_position_x, start_position_y)
        v_end = (finish_position_x, finish_position_y)

        return v_start, v_end

    @staticmethod
    def dist(node_a, node_b):
        """
        This is the distance function using nodes positions to calculate
        euclidian distance

        :param node_a: node 1
        :param node_b: node 2
        """
        return np.sqrt(np.power(node_b[0] - node_a[0], 2) +
                       np.power(node_b[1] - node_a[1], 2))

    @staticmethod
    def fast_dist(node_a, node_b):
        """ Something """
        return np.abs(node_a[0] - node_b[0]) + np.abs(node_a[1] - node_b[1])

    def find_closest_node(self, position):
        """ Something """
        closest_node = (0.0, 0.0)
        closest_dist = self.fast_dist(closest_node, position)
        if self._graph is None:
            return closest_node

        for node in self._graph.nodes:
            cd_fd = self.fast_dist(node, position)
            if cd_fd < closest_dist:
                closest_dist = cd_fd
                closest_node = node

        return closest_node

    def a_star(self, initial_position, goal_position, dist=None,
               weight="weight"):
        """
        This is the function that returns the a_star route provided by
        NetworkX.

        Parameters
        ----------
        initial_position : tuple
            inital in the format (x1,y1)
        goal_position : tuple
            expected goal in the format (x1,y1)
        dist : optional, int
            default self.dist
        weight: optional, int
            defaut weight

        Returns
        -------
        [(x1,y1),(x2,y2)...

        """

        if self.verbose:
            print("Finding closest positions...")

        initial_position_c = self.find_closest_node(initial_position)
        if self.verbose:
            print(" - Start {} closest on the graph at {}:".format(
                initial_position, initial_position_c))

        goal_position_c = self.find_closest_node(goal_position)
        if self.verbose:
            print(" - Goal {} closest on the graph at {}:".format(
                goal_position, goal_position_c))

        if dist is None:
            v_dist = self.dist

        else:
            v_dist = dist

        result = []
        try:
            # Returns result as list of tuples.
            result = nx.astar_path(
                self._graph, initial_position_c, goal_position_c,
                v_dist, weight)

        except nx.NetworkXNoPath:
            print("No route found in graphery or graph is too big.")

        return result

    def a_start_length(self, initial_position, goal_position,
                       heuristic=None, weight='weight'):
        """
        This is the function that returns the a_star route provided by
        NetworkX.

        Parameters
        ----------
        initial_position : tuple
            inital in the format (x1,y1)
        goal_position : tuple
            expected goal in the format (x1,y1)
        heuristic : optional
            default self.dist
        weight : optional
            defaut weight

        Returns
        -------

        """
        try:
            # returns integral of pixel values along the optimal path
            result = nx.astar_path_length(
                self._graph, initial_position, goal_position,
                heuristic=heuristic, weight=weight)

        except nx.NetworkXNoPath:
            print("There is no route in GRID mode, " +
                  "therefore no length available.")

        return result

    @staticmethod
    def combinations(row, col):
        """ Returns iterable with tuples of all indices of a NxM matrix """
        for i in range(0, row):
            for j in range(0, col):
                yield (i, j)
