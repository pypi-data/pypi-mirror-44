"""
Graph generator file. Contains classes related to generating networkx graphs
for search algorithms.
"""
import random
import networkx as nx
import numpy as np
# import matplotlib.pyplot as plt
# import pylab as plt
# import gdal
# from PIL import Image, ImageDraw
# import scipy.misc as smp
# import sys

# import argparse


class GraphGenerator:
    """
    GraphGenerator Class


    """
    def __init__(self, width=600, height=600):
        print("Graph Generator: Init")
        self.width = width
        self.height = height
        self.DEBUG = False

    def graph_navigation_init(self, arr):
        """
        Set the internal graph using the shape of a rombus. 4 nodes and 12
        vertix per pixel.

        This process is performed in three steps,
            1. create the empty graph
            2. generate the edges between nodes (in both senses)
            3. Load a map of weight

        Parameters
        ----------
        arr : np.ndarray

        """
        rows = arr.shape[0]
        cols = arr.shape[1]

        image_size_in_pixels = rows * cols
        graph_size = ((rows * cols) * 6) + 9

        value_x = 3 + (6 * cols)
        value_y = (rows - 1) * ((value_x / 3) * 2)
        graph_size = value_x + value_y

        print("CLASS-Graph_generator: The size of the image is:", rows, cols,
              " this is a total of ", rows * cols,
              " pixels, the graph size is", graph_size)
        graph_walls = nx.empty_graph(int(graph_size), create_using=nx.DiGraph())
        graph_walls = self.edge_generator(graph_walls, rows, cols)
        graph_walls = self.load_map_2(graph_walls, rows, cols, arr)

        return graph_walls

    def graph_grid_init(self, arr):
        """
        Set the internal graph using the shape of a grid (one node per pixel).

        This process is performed in three steps,
            1. create the empty graph
            2. generate the edges between nodes (in both senses)
            3. Load a map of weight

        Nota bene:
            rows (height)
            cols (width)

        Parameters
        ----------
            arr : (navigation cost map)

        """
        height = arr.shape[0]
        width = arr.shape[1]
        image_size_in_pixels = width * height

        print("The size of the image is: x ", width,
              " y ", height,
              " this is a total of ", width * height,
              " pixels, the graph size is ", image_size_in_pixels)
        graph_walls = nx.empty_graph(image_size_in_pixels,
                                     create_using=nx.DiGraph())
        graph_walls = self.edge_generator_grid(graph_walls, height, width)
        graph_walls = self.load_map_grid(graph_walls, height, width, arr)

        return graph_walls

    def edge_generator(self, graph, height, width):
        """
        Generates the next structure for navigating each of the pixels.

        Graph generator for 1 pixel

        Composition: 4 path_nodes
                     6 edges


           o
         / | \
        o--|--o
         \ | /
           o

        Parameters
        ----------
        graph :
            something
        height :
            something
        width :
            something

        """
        size_height = height * 2  # get size of graph networkx
        size_width = width * 2
        print(height, width)
        print(size_height, size_width)
        print("")
        constant_weights = 0
        random_weights = random.randint(0, 2) * 3+1

        cel = []  # current edge list
        tcel = []
        for y_val, x_val in self.combinations(size_height, size_width):
            #print (x_val, y_val)
            if x_val % 2 == 1 and y_val % 2 == 0 and y_val != size_width - 1:
                cel.append(((x_val, y_val), (x_val-1, y_val+1),
                            {"weight":constant_weights}))
                cel.append(((x_val-1, y_val+1), (x_val, y_val),
                            {"weight":constant_weights}))

                cel.append(((x_val, y_val), (x_val+1, y_val+1),
                            {"weight":constant_weights}))
                cel.append(((x_val+1, y_val+1), (x_val, y_val),
                            {"weight":constant_weights}))

                cel.append(((x_val, y_val), (x_val, y_val+2),
                            {"weight":constant_weights}))
                cel.append(((x_val, y_val+2), (x_val, y_val),
                            {"weight":constant_weights}))

                #print graph.edges

            if y_val % 2 == 1:
                if x_val % 2 == 0:
                    if x_val + 1 < size_height:
                        cel.append(((x_val, y_val), (x_val+1, y_val+1),
                                    {"weight":constant_weights}))
                        cel.append(((x_val+1, y_val+1), (x_val, y_val),
                                    {"weight":constant_weights}))

                        cel.append(((x_val, y_val), (x_val+2, y_val),
                                    {"weight":constant_weights}))
                        cel.append(((x_val+2, y_val), (x_val, y_val),
                                    {"weight":constant_weights}))

                    #if (x_val > 0):
                        cel.append(((x_val+2, y_val), (x_val+1, y_val+1),
                                    {"weight":constant_weights}))
                        cel.append(((x_val+1, y_val+1), (x_val+2, y_val),
                                    {"weight":constant_weights}))
                #print graph.edges
            tcel.extend(cel)

            if x_val == size_width - 1:
                cel = []

        # Adding a bunch of edges with their dictionnaries
        # For the same data here is the benchmark adding 100 of edges:
        #  - add_edge():  120us
        #  - add_edges_from():  120us
        #  - add_weight_edges_from()  :  120us
        graph.add_edges_from(tcel)

        if self.DEBUG:
            print(graph.edges)

        #Creating righ vertix
        return graph

    def edge_generator_grid(self, graph, height, width, use_random_weights=False):
        """ Edge Generator Grid """
        size_height = height
        size_width = width
        print(height, width)
        print(size_height, size_width)
        print("")

        if use_random_weights:
            weights = random.randint(0, 2) * 3 + 1

        else:
            weights = 0

        #for y in range (0,size_height):
            #for x in range (0,size_height):

        cel = []  # current edge list
        tcel = []
        for x_val, y_val in self.combinations(width, height):
            if y_val == 0 and x_val == 0:
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))

            elif y_val == height - 1  and x_val == 0:
                cel.append(((x_val, y_val - 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))

            elif y_val == 0  and x_val == width - 1:
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))

            elif y_val == height - 1  and x_val == width - 1:
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val - 1), (x_val, y_val),
                            {"weight": weights}))

            elif y_val == 0 and x_val < width - 1:
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))

            elif y_val == 0 and x_val < width - 1:
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))

            elif y_val < height - 1  and x_val == width - 1:
                cel.append(((x_val, y_val - 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))

            elif y_val == height - 1  and x_val < width - 1:
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val - 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))

            elif y_val < height - 1 and x_val == 0:
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val - 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))

            else:
                cel.append(((x_val + 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val - 1, y_val), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val + 1), (x_val, y_val),
                            {"weight": weights}))
                cel.append(((x_val, y_val - 1), (x_val, y_val),
                            {"weight": weights}))

            if y_val == height - 1:
                tcel.extend(cel)
                cel = []

        graph.add_edges_from(tcel)

        if self.DEBUG:
            print(graph.edges)

        # Creating right vertix
        return graph

    def edge_generator_simple(self, graph, height, width, use_random_weights=False):
        """
        Generates the next structure for navigating each of the pixels

        Graph generator for 1 pixel

        Composition: 1 pixel
                     1 state


        o - o
        |   |
        o - o

        """
        size_height = height * 2
        size_width = width * 2
        print(height, width)
        print(size_height, size_width)
        print("")

        if use_random_weights:
            weights = random.randint(0, 2) * 3+1

        else:
            weights = 0

        for y_val, x_val in self.combinations(size_height, size_width):
            if x_val % 2 == 1 and y_val % 2 == 0 and y_val != size_width - 1:
                graph.add_edge((x_val, y_val), (x_val-1, y_val+1),
                               weight=weights)
                graph.add_edge((x_val-1, y_val+1), (x_val, y_val),
                               weight=weights)

                graph.add_edge((x_val, y_val), (x_val+1, y_val+1),
                               weight=weights)
                graph.add_edge((x_val+1, y_val+1), (x_val, y_val),
                               weight=weights)


                graph.add_edge((x_val, y_val), (x_val, y_val+2),
                               weight=weights)
                graph.add_edge((x_val, y_val+2), (x_val, y_val),
                               weight=weights)

                #print graph.edges

            if y_val % 2 == 1:
                if x_val % 2 == 0:
                    if x_val + 1 < size_height:
                        graph.add_edge((x_val, y_val), (x_val+1, y_val+1),
                                       weight=weights)
                        graph.add_edge((x_val+1, y_val+1), (x_val, y_val),
                                       weight=weights)

                        graph.add_edge((x_val, y_val), (x_val+2, y_val),
                                       weight=weights)
                        graph.add_edge((x_val+2, y_val), (x_val, y_val),
                                       weight=weights)

                    #if (x_val > 0):
                        graph.add_edge((x_val+2, y_val), (x_val+1, y_val+1),
                                       weight=weights)
                        graph.add_edge((x_val+1, y_val+1), (x_val+2, y_val),
                                       weight=weights)
                #print graph.edges

        if self.DEBUG:
            print(graph.edges)

        #Creating righ vertix
        return graph

    def load_map(self, graph, height, width, cost_map):
        """
        Loading a map to a graph map

        The cost map should have the weights for each node of the map.

        Parameters
        ----------
        graph_map : nx.graph.Graph
            pass
        height : int
            The height of the graph in nodes.
        width : int
            The width of the graph in nodes.
        cost_map: np.array
            A 2x2 array containing the weights for each node of the map.

        Returns
        -------
        graph : nx.graph.Graph
            The graph that was originally loaded, but with the added weights.

        """
        print("the width dimensions are ", width)
        print("the height dimensions are ", height)
        print("the dimensions are ", len(cost_map))

        constant_weight = 3.5
        v_weight = constant_weight

        v_x_edge_val = 0
        v_y_edge_val = 0

        height = height * 2

        for x_val, y_val in self.combinations(width, height):
            #print(x_val, y_val)
            #if (map[y_val][x_val]==1):
                #print("We are in the position X, y_val ", x_val, size_1 - y_val)
                #print("We are in the position", v_x_edge_val,v_y_edge_val)

            v_weight = cost_map[y_val][x_val]

            v_x_edge_val = (x_val * 2) + 1
            v_y_edge_val = ((height - y_val) * 2)
            graph.edges[(v_x_edge_val, v_y_edge_val),
                        ((v_x_edge_val - 1), v_y_edge_val + 1)]["weight"] = v_weight
            graph.edges[((v_x_edge_val - 1), v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val)]["weight"] = v_weight

            graph.edges[(v_x_edge_val + 1, v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val),
                        (v_x_edge_val + 1, v_y_edge_val + 1)]["weight"] = v_weight

            graph.edges[(v_x_edge_val, v_y_edge_val),
                        (v_x_edge_val, v_y_edge_val + 2)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val + 2),
                        (v_x_edge_val, v_y_edge_val)]["weight"] = v_weight


            graph.edges[(v_x_edge_val - 1, v_y_edge_val + 1),
                        (v_x_edge_val + 1, v_y_edge_val + 1)]["weight"] = v_weight
            graph.edges[(v_x_edge_val + 1, v_y_edge_val + 1),
                        (v_x_edge_val - 1, v_y_edge_val + 1)]["weight"] = v_weight


            graph.edges[(v_x_edge_val - 1, v_y_edge_val+1),
                        (v_x_edge_val, v_y_edge_val + 2)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val + 2),
                        (v_x_edge_val - 1, v_y_edge_val + 1)]["weight"] = v_weight


            graph.edges[(v_x_edge_val + 1, v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val + 2)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val + 2),
                        (v_x_edge_val + 1, v_y_edge_val + 1)]["weight"] = v_weight

        return graph

    def load_map_2(self, graph_map, height, width, map_description):
        """
        Loading a map to a graph map

        The map_description should have the weights for each node of the map.

        Parameters
        ----------
        graph_map : nx.graph.Graph
            pass
        height : int
            The height of the graph in nodes.
        width : int
            The width of the graph in nodes.
        map_description : np.array
            A 2x2 array containing the weights for each node of the map.

        Returns
        -------
        graph : nx.graph.Graph
            The graph that was originally loaded, but with the added weights.

        """
        graph = graph_map
        maps = map_description
        print("Loading Map:")
        print("Loading Map: the width dimensions are ", width)
        print("the height dimensions are ", height)
        print("the dimensions are (map) ", len(maps))
        print("the dimensions are (graph) ", len(graph))
        constant_weight = 3.5
        v_weight = constant_weight

        v_x_edge_val = 0
        v_y_edge_val = 0

        #height = height * 2
        height_1 = height -1
        for x_val, y_val in self.combinations(width, height):
            # print("the values in this case are x,y :", x_val, y_val)
            # if (map[y_val][x_val]==1):
                # print("We are in the position X, y ", x_val, size_1 - y_val)
                # print("We are in the position", v_x_edge_val, v_y_edge_val)

            v_weight = maps[y_val][x_val]

            v_x_edge_val = (x_val * 2) + 1
            v_y_edge_val = ((height_1 - y_val) * 2)
            #print("the values in this case are " +
            #      "v_x_edge_val,v_y_edge_val :",
            #      v_x_edge_val,  v_y_edge_val)
            graph.edges[(v_x_edge_val, v_y_edge_val),
                        (v_x_edge_val - 1, v_y_edge_val + 1)]["weight"] = v_weight
            graph.edges[(v_x_edge_val - 1, v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val)]["weight"] = v_weight

            graph.edges[(v_x_edge_val + 1, v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val),
                        (v_x_edge_val + 1, v_y_edge_val + 1)]["weight"] = v_weight

            graph.edges[(v_x_edge_val, v_y_edge_val),
                        (v_x_edge_val, v_y_edge_val + 2)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val + 2),
                        (v_x_edge_val, v_y_edge_val)]["weight"] = v_weight

            graph.edges[(v_x_edge_val - 1, v_y_edge_val + 1),
                        (v_x_edge_val + 1, v_y_edge_val + 1)]["weight"] = v_weight
            graph.edges[(v_x_edge_val + 1, v_y_edge_val + 1),
                        (v_x_edge_val - 1, v_y_edge_val + 1)]["weight"] = v_weight

            graph.edges[(v_x_edge_val - 1, v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val + 2)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val + 2),
                        (v_x_edge_val - 1, v_y_edge_val + 1)]["weight"] = v_weight

            graph.edges[(v_x_edge_val + 1, v_y_edge_val + 1),
                        (v_x_edge_val, v_y_edge_val + 2)]["weight"] = v_weight
            graph.edges[(v_x_edge_val, v_y_edge_val + 2),
                        (v_x_edge_val+1, v_y_edge_val+1)]["weight"] = v_weight

        return graph

    def load_map_grid(self, graph, height, width, cost_map):
        """
        Loading a map to a graph map

        The cost map should have the weights for each node of the map.

        Parameters
        ----------
        graph_map :
            networkx graph object
        height :
            Image height
        width :
            Image width.
        cost_map :
            Map containing the weights, navigation costs.

        """
        print("the width dimensions are ", width)
        print("the height dimensions are ", height)
        print("the dimensions are (map) ", len(cost_map))
        print("the dimensions are (graph) ", len(graph))
        print("Loading cost map...")
        constant_weight = 3.5
        v_weight = constant_weight

        for x_val, y_val in self.combinations(width, height):
            v_weight = 255 - cost_map[y_val][x_val]

            if y_val == 0 and x_val == 0:
                graph.edges[(x_val+1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val+1),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val == (height - 1) and x_val == 0:
                graph.edges[(x_val, y_val-1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val+1, y_val),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val == 0 and x_val == (width - 1):
                graph.edges[(x_val-1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val+1),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val == (height - 1) and x_val == (width - 1):
                graph.edges[(x_val-1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val-1),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val == 0 and x_val < (width - 1):
                graph.edges[(x_val+1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val+1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val-1, y_val),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val < (height - 1) and x_val == (width - 1):
                graph.edges[(x_val, y_val-1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val+1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val-1, y_val),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val == (height - 1) and x_val < (width - 1):
                graph.edges[(x_val-1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val-1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val+1, y_val),
                            (x_val, y_val)]["weight"] = v_weight

            elif y_val < (height - 1) and x_val == 0:
                graph.edges[(x_val+1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val-1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val+1),
                            (x_val, y_val)]["weight"] = v_weight

            else:
                graph.edges[(x_val+1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val-1, y_val),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val+1),
                            (x_val, y_val)]["weight"] = v_weight
                graph.edges[(x_val, y_val-1),
                            (x_val, y_val)]["weight"] = v_weight

        return graph

    @staticmethod
    def add_node_information(graph, key, data):
        """
        Add other information to nodes other than weights for the edges. This
        will be an added key to the dictionary that contains the default graph
        information.

        Parameters
        ----------
        graph : nx.classes.graph.Graph or nx.classes.digraph.DiGraph
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
        graph : nx.classes.graph.Graph or nx.classes.digraph.DiGraph
            The graph that was passed to the function but now with the
            information desired at each node.

        """
        for node in graph.nodes():
            graph[node][key] = data[node[0], node[1]]

        return graph

    def create_robot_graph(self, cost_map=None, number_of_nodes=None):
        """ Robot graph containing default state, time, and task. """
        if cost_map is None:
            row = int(np.sqrt(number_of_nodes))
            col = int(np.sqrt(number_of_nodes))

        elif number_of_nodes is None:
            row = cost_map.shape[0]
            col = cost_map.shape[1]

        else:
            row = self.height
            col = self.width

        graph = nx.grid_graph(dim=[col, row])
        graph.to_directed()

        if cost_map is None:
            for i, j in self.combinations(row, col):
                # Add edge weights
                for key in graph[i, j]:
                    if isinstance(key, tuple):
                        graph[i, j][key]["weight"] = 1

                # Assign time it takes to move to vertex and default task.
                graph[i, j]["t"] = 100  # minutes
                graph[i, j]["B"] = 0  # task

        else:
            for i, j in self.combinations(col, row):
                # Add edge weights
                for key in graph[i, j]:
                    if isinstance(key, tuple):
                        graph[i, j][key]["weight"] = cost_map[j, i]

                # Assign time it takes to move to vertex and default task.
                graph[i, j]["t"] = 100  # minutes
                graph[i, j]["B"] = 0  # task

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
    def get_startend_rombus_mode(list_of_points):
        """
        Something
        """
        if len(list_of_points) < 2:
            print("Not enough points provided")
            v_start = (0, 0)
            v_end = (100, 100)

        else:
            start_position_x = (list_of_points[0][0] * 2) + 1
            start_position_y = (list_of_points[0][1] * 2)
            finish_position_x = (list_of_points[1][0] * 2) + 1
            finish_position_y = (list_of_points[1][1] * 2)

            v_start = (start_position_x, start_position_y)
            v_end = (finish_position_x, finish_position_y)

        return v_start, v_end

    def dist(self, node_a, node_b):
        '''
        This is the distance function using nodes positions to calculate
        euclidian distance

        :param node_a: node 1
        :param node_b: node 2
        '''
        return np.sqrt(np.power(node_b[0] - node_a[0], 2) +
                       np.power(node_b[1] - node_a[1], 2))

    def a_star(self, graph, initial_position, goal_position, dist=None,
               weight="weight"):
        """ This is the function that returns the a_star route provided by networkx

            :param graph: a networkx graph
            :param initial_position: inital in the format (x1,y1)
            :param goal_position: expected goal in the format (x1,y1)
            :param dist: default self.dist
            :param weight: defaut weight

            : returns [(x1,y1),(x2,y2)...
        """
        if dist is None:
            v_dist = self.dist
        else:
            v_dist = dist

        try:
            # Returns result as list of tuples.
            result = nx.astar_path(graph, initial_position, goal_position,
                                   v_dist, weight)

        except nx.NetworkXNoPath:
            print("There is no route in GRID mode")

        return result

    @staticmethod
    def a_star_length(graph, initial_position, goal_position,
                      heuristic=None, weight='weight'):
        """
        This is the function that returns the A(star) route provided by
        NetworkX.

        Parameters
        ----------
        graph : nx.classes.graph.Graph or nx.classes.digraph.DiGraph
            A NetworkX graph.
        initial_position : float or int tuple
            Inital in the format (x1, y1)
        goal_position : float or int tuple
            Expected goal in the format (x1, y1)
        heuristic : Function (default: None)
            Pass
        weight : str (default: `weight`)
            Pass
        """
        try:
            # Returns integral of pixel values along the optimal path.
            result = nx.astar_path_length(graph, initial_position,
                                          goal_position, heuristic=heuristic,
                                          weight=weight)

        except nx.NetworkXNoPath:
            print("There is no route in GRID mode. No length available.")
            result = None

        return result

    @staticmethod
    def combinations(row, col):
        """ Returns iterable with tuples of all indices of a NxM matrix """
        for i in range(0, row):
            for j in range(0, col):
                yield (i, j)
