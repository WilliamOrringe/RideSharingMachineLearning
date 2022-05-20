from shapely.geometry import shape
from shapely.ops import unary_union
import fiona
import networkx as nx
import itertools
from haversine import haversine

import networkx as nx

'''
    This module is Used to convert MultiDigraph to Simple Graph
    @input:     MultiDiGraph
    @Output:    Simple Graph
'''


class MultiDiToSimple:
    def __init__(self, G):
        self.G = G

    def convert_MultiDi_to_Simple(self):
        new_G = self.G.to_undirected()

        new_simple_graph = nx.Graph()
        for uv in new_G.edges:
            u_lat = uv[0][0]
            u_lon = uv[0][1]

            v_lat = uv[1][0]
            v_lon = uv[1][1]

            new_start = (u_lat, u_lon)
            new_end = (v_lat, v_lon)
            weight = new_G.get_edge_data(uv[0], uv[1])[0]['weight']
            if new_simple_graph.has_edge(new_start, new_end):
                continue
            else:
                new_simple_graph.add_edge(new_start, new_end, weight=weight)
        return new_simple_graph


"""
    This module is used to clean all the intermediate nodes from the MultiDiGraph
    1. All the intermediate nodes of degree 2 which is just a curve or bend in the graph will be removed

    @input:     MultiDiGraph
    @output:    MultiDiGraph
"""


class GraphSimplify:
    def __init__(self, G):
        self.G = G

    '''
        @input:     The MultiDigraph and the coordinate of node
        @output:    Returns bool

        This function check if the node is intermediate node or not. It get the list of the successors and predecessors of
        the node and check for node with degree one and isolated nodes.

        Return true if its the intermediate node of false if its not
    '''

    def is_intermediate_node(self, node):
        neighbours = set(list(self.G.predecessors(node)) + list(self.G.successors(node)))
        d = self.G.degree(node)

        if node in neighbours:
            return True
        elif self.G.in_degree(node) == 0 or self.G.out_degree(node) == 0:
            return True
        elif not (len(neighbours) == 2 and d == 2):
            return True
        else:
            return False

    '''
        @input:     The MultiDiGraph, start coord, list of non intermediate nodes, list of nodes in path
        @output:    Returns list of nodes in the path from the start coord to then end

        This function will iterate over all the successor of the start coordinate and check if it lies in the path
        If not then check if its the non intermediate node, if not then call this function again till you get the
        non intermediate node.

    '''

    def find_path(self, start_node, endnode_list, path):
        for successor in self.G.successors(start_node):
            if successor not in path:
                path.append(successor)
                if successor not in endnode_list:
                    path = self.find_path(successor, endnode_list, path)
                else:
                    return path

        if (path[-1] not in endnode_list) and (path[0] in self.G.successors(path[-1])):
            path.append(path[0])
        return path

    '''
        @input:     The MultiDigraph for simplifying and cleaning
        @output:    Returns cleaned and simplified MultiDigraph

        This function removed all the nodes which are of degree one and intermediate nodes. While removing the intermediate
        nodes it preserve the weight(distance) between edges by adding it to the new edges while removing intermediate node.
    '''

    def simplify_graph(self):
        non_intermediate_node = set()
        for node in self.G.nodes():
            if self.is_intermediate_node(node):
                non_intermediate_node.add(node)

        uncleaned_path = []
        for node in non_intermediate_node:
            for successor in self.G.successors(node):
                if successor not in non_intermediate_node:
                    path = self.find_path(successor, non_intermediate_node, path=[node, successor])
                    uncleaned_path.append(path)

        nodes_to_remove = []
        edges_to_build = []

        for path in uncleaned_path:
            nodes_to_remove.extend(path[1:-1])
            total_distance = 0
            for index in range(1, len(path)):
                total_distance += (self.G.get_edge_data(path[0], path[1])[0]['weight'])

            edges_to_build.append({'start': path[0], 'end': path[-1], 'distance': total_distance})

        self.G.remove_nodes_from(nodes_to_remove)

        for edge in edges_to_build:
            self.G.add_edge(edge['start'], edge['end'], weight=edge['distance'])

        return self.G

class GraphConvertor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

    '''
        @input:     The path of the shapefile which need to be converted to network
        @output:    Returns the MultiDigraph created from the shapefile

        This function read the shapefile of the road network and convert it into graph by iterating through the lat, lon
        from the shapefile.
    '''

    def shape_convertor(self):
        geoms = [shape(feature['geometry']) for feature in fiona.open(self.input_file)]
        res = unary_union(geoms)
        G = nx.MultiDiGraph()
        for line in res.geoms:
            for seg_start, seg_end in zip(list(line.coords), list(line.coords)[1:]):
                start = (round(seg_start[1], 6), round(seg_start[0], 6))
                end = (round(seg_end[1], 6), round(seg_end[0], 6))
                G.add_edge(start, end, weight=haversine(start, end))
        return G

    '''
        @input:     The Graph and the path

        This function read the Graph, iterate over the list of nodes in the graph and save it into file defined by path
    '''

    def create_vertex_file(self, g):
        vertex = g.nodes
        output = open(self.output_dir + '/vertex.csv', 'w')
        output.write('Unique Id; Longitude; Latitude\n')

        count = 1
        for v in vertex:
            output.write(str(count) + ';' + str(round(v[0], 6)) + ';' + str(round(v[1], 6)) + '\n')
            count += 1

    '''
        @input:     The Graph and directory

        This function writes the graph in form of shape file to the given directory
    '''

    def create_edges_vertex_shape(self, g):
        nx.write_shp(g, self.output_dir + '/New Shape/')

    '''
        @input:     The Graph and the path

        This function iterate over the edges of the graph and write it into the file defined by the path
    '''

    def create_edges_file(self, g):
        output = open(self.output_dir + '/edges.csv', 'w')
        output.write('Starting Coordinate; End Coordinate; True Distance(km) \n')

        for edge in g.edges:
            distance = g.get_edge_data(edge[0], edge[1])[0]['weight']
            start_coor = [round(elem, 6) for elem in list(edge[0])]
            end_coor = [round(elem, 6) for elem in list(edge[1])]
            output.write(str(start_coor) + ';' + str(end_coor) + ';' + str(distance) + '\n')

    '''
        @input:     path of the shape file and the output for saving clean network
        @output:    Cleaned network

        This function read the input shape file and convert it into network for cleaning. After converting it simplify the
        graph by calling simplify_graph() and write the cleaned network in form of shapefiles
    '''

    def graph_convertor(self):
        G = self.shape_convertor()
        print("Number of Nodes in the graph, ", len(G.nodes))
        simplify_graph = GraphSimplify(G)
        new_G = simplify_graph.simplify_graph()

        print("Number of Nodes after simplifying, ", len(new_G.nodes))
        self.create_vertex_file(new_G)
        self.create_edges_file(new_G)

        multiDi_to_simple = MultiDiToSimple(new_G)
        new_simple_graph = multiDi_to_simple.convert_MultiDi_to_Simple()
        self.create_edges_vertex_shape(new_simple_graph)

        return new_G
