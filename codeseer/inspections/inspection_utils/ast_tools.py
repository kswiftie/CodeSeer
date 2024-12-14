import ast
import networkx as nx
import os
from itertools import combinations

"""
AVAILABLE_AST_TYPES needs for tests bc
now im not sure what type to store ASTs is better
so im gonna try few of them
"""
AVAILABLE_AST_TYPES = ["list_of_edges", "adjacency_matrix"]
AVAILABLE_GRAPH_FILTERS = ["is_whole_function"]
list_of_edges, adjacency_matrix = "list_of_edges", "adjacency_matrix"
GRAPH_TYPE = nx.DiGraph


class AST:
    def __init__(self):
        """
        init func
        """

        self.data_created = set()

    def build_ast(self, code: str, output_file_name: str, returning_format: object) -> GRAPH_TYPE:
        """
        A function for building an AST based on the code provided by the program
        It is recommended to use only this function for building trees

        Parametrs
        --------
        code: str
            The code to use to build the AST

        returning_format: object
            The format in which the AST should be returned

        output_file_name: str
            The name for the file where AST will be saved

        Returns
        -------
        res_graph: GRAPH_TYPE
            AST built from the source code
        """

        if returning_format not in AVAILABLE_AST_TYPES:
            raise ValueError(f"returning_format must be in {AVAILABLE_AST_TYPES}")

        parsed_code = ast.parse(code)

        res_graph = nx.DiGraph()

        if returning_format == "list_of_edges":
            res_graph.add_edges_from(self.build_ast_list_of_edges(parsed_code))
        elif returning_format == "adjacency_matrix":
            return self.build_ast_adjacency_matrix(parsed_code)

        self.data_created.add(output_file_name)
        nx.drawing.nx_pydot.write_dot(res_graph, output_file_name + ".dot")

        return res_graph

    def build_ast_list_of_edges(self, node: object, parent: str | None = None) -> list[tuple[str, str]]:
        """
        Builds an abstract syntactic tree based
        on the program code in the list of edges format

        Parametrs
        ---------
        node: object
            Link to the node

        parent: str | None
            The name of the parent node

        Returns
        -------
        list[tuple[str, str]]
            Graph in the list of edges format
        """

        edges = []

        node_name = node.__class__.__name__  # name of cur node

        if parent is not None:
            edges.append((parent, node_name))
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):  # several children
                for item in value:
                    if isinstance(item, ast.AST):
                        edges.extend(self.build_ast_list_of_edges(item, node_name))
            elif isinstance(value, ast.AST):  # one child
                edges.extend(self.build_ast_list_of_edges(value, node_name))

        return edges

    def build_ast_adjacency_matrix(self, node: object) -> GRAPH_TYPE:
        """
        :param node:
        :return:
        """

        graph = nx.DiGraph()

        def dfs(node: object, parent: object | None = None):
            node_type = type(node).__name__  # Name of the node
            node_id = id(node)  # node ID

            graph.add_node(node_id, type=node_type)

            if parent is not None:
                parent_type = type(parent).__name__
                parent_id = id(parent)

                graph.add_edge(parent_id, node_id)

            for child in ast.iter_child_nodes(node):
                dfs(child, parent=node)

        dfs(node)

        return graph

    def get_subtree(self, graph: GRAPH_TYPE, root_id: int) -> GRAPH_TYPE:
        """

        :param root:
        :return:
        """

        descendants = nx.descendants(graph, root_id)
        subtree_nodes = descendants | {root_id}

        return graph.subgraph(subtree_nodes).copy()

    def compare_two_graphs_smart(self):
        # TBD
        # will be smart comparingn
        pass

    def check_isomorphism(self, graph1: GRAPH_TYPE, graph2: GRAPH_TYPE) -> bool:
        """
        Checking two graphs for isomorphism

        Parametrs
        ---------
        graph1: GRAPH_TYPE
            The first tree

        graph2: GRAPH_TYPE
            The second tree

        Returns
        -------
        bool
            True if the graphs are isomorphic False otherwise
        """
        if graph1.number_of_nodes() != graph2.number_of_nodes() or \
                graph1.number_of_edges() != graph2.number_of_edges():  # make program faster
            return False

        return nx.is_isomorphic(graph1, graph2)

    def is_input_node(self, node: str) -> bool:
        """
        Checking that the node is the input point to the function

        Parametrs
        ---------
        node: str
            Name of the node

        Returns
        -------
        bool
            Is the node the input point to the function
        """

        # todo: Extend the check so that something more than a function can be compared

        return True if node in ["FunctionDef"] else False

    def is_output_node(self, node: str) -> bool:
        """
        Checking that the node is the output point to the function

        Parametrs
        ---------
        node: str
            Name of the node

        Returns
        -------
        bool
            Is the node the output point to the function
        """

        # todo: Extend the check so that something more than a function can be compared
        return True if node in ["Return"] else False

    def is_whole_function(self, graph: GRAPH_TYPE) -> bool:
        """
        Filter for graphs
        Checks that the graph given at the input is
        logically an integral part of the program

        Parametrs
        ---------
        graph: GRARH_TYPE
            The graph that needs to be checked

        Returns
        -------
        bool
            True if it is an integral part False otherwise
        """

        input_nodes_count = len([node for node in graph.nodes if self.is_input_node(node)])
        output_nodes_count = len([node for node in graph.nodes if self.is_output_node(node)])

        nodes_count = len(graph.nodes())
        edges_count = len(graph.edges())

        return (input_nodes_count != 0 and
                output_nodes_count == input_nodes_count and
                nodes_count <= edges_count + 1)

    def generate_subgraphs(self, graph: GRAPH_TYPE, output_folder_path: str, length: int = 9,
                           filters: list[str] = AVAILABLE_GRAPH_FILTERS) -> int:
        """
        A function that writes all its subgraphs to a file according to a graph

        Parametrs
        ---------
        graph: GRAPH_TYPE
            The tree itself

        output_folder_path: str
            The name of folder where all the subgraphs will be saved

        length: int
            Length of subgraphs

        filters: list[str]
            Filters for subgraphs

        Returns
        -------
        int
            count of subgraphs
        """

        # avaliable_starts = ["FunctionDef", "For", "While", "If", "Assign", "Call"]
        avaliable_starts = ["FunctionDef", "For", "While", "If"]
        nodes = [x for x in graph.nodes() if x in avaliable_starts]
        subgraph_number = 1

        def dfs(current_node: str, path: list[str], current_length: int = 0):
            nonlocal subgraph_number
            if current_length == length:
                subgraph = graph.subgraph(path)
                if all(getattr(self, filter)(subgraph) for filter in AVAILABLE_GRAPH_FILTERS):
                    self.data_created.add(output_folder_path + f"/{subgraph_number}.dot")
                    nx.drawing.nx_pydot.write_dot(subgraph, output_folder_path + f"/subgraph_{subgraph_number}.dot")
                    subgraph_number += 1
                return

            for neighbor in graph.successors(current_node):  # list of adjacent nodes
                if neighbor not in path:
                    dfs(neighbor, path + [neighbor], current_length + 1)

        for start_node in nodes:
            dfs(start_node, [start_node])

        return subgraph_number

    def generate_subgraphs2(self, graph: GRAPH_TYPE, output_folder_path: str) -> int:
        """
        THIS IS THE 2 VARIATION OF SUBGRAPHS GENERATING IM GONNA TEST ALL OF THEM
        :return:
        """

        avaliable_roots = ["FunctionDef", "For", "While", "If"]
        subgraph_number = 1
        nodes = graph.nodes()

        def dfs(cur_node_id: int):
            nonlocal subgraph_number
            cur_node_data = graph.nodes[cur_node_id]

            if cur_node_data["type"] in avaliable_roots:
                subgraph = self.get_subtree(graph, cur_node_id)
                self.data_created.add(output_folder_path + f"/{subgraph_number}.dot")
                nx.drawing.nx_pydot.write_dot(subgraph, output_folder_path + f"/subgraph_{subgraph_number}.dot")
                subgraph_number += 1

            for child_id in graph.successors(cur_node_id):
                dfs(child_id)

        root = [x for x in nodes if graph.nodes[x]["type"] == "Module"][0]
        dfs(root)

        return subgraph_number

    def read_graphs_from_dotfile(self, filename: str) -> GRAPH_TYPE:
        """
        Reads graphs from files with the extension .dat and
        returns them in networkx format.Graph

        Parametrs
        ---------
        filename: str
            The file from which you want to read the graph

        Returns
        -------
        graph: GRAPH_TYPE
            Graph from the file in the desired format
        """

        return nx.drawing.nx_pydot.read_dot(filename)  # Stores the adjacency matrix in the format

    def delete_tmp_files(self):
        for file_path in self.data_created:
            os.remove(file_path)

        self.data_created = set()
