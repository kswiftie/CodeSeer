import ast, hashlib
import networkx as nx
from typing import Any


def get_subtree(tree: nx.DiGraph, root_id: int) -> nx.DiGraph:
    """
    Generates the subtree of inputted graph and from inputted node.
    It was written for undirected trees.

    Args:
        tree:
            The tree to get the subtree from.

        root_id:
            ID of the vertex to get the subtree from.

    Returns:
        The undirected subtree with root in root_id in inputted tree
    """

    descendants = nx.descendants(tree, root_id)
    subtree_nodes = descendants | {root_id}

    return tree.subgraph(subtree_nodes).copy()


def build_ast(code: str) -> nx.DiGraph:
    """
    Builds AST (abstract syntax tree) by inputted code.

    Args:
        code:
            The python code to build the AST from.

    Returns:
        AST. It is undirected.
    """

    graph = nx.DiGraph()

    def dfs(current_node: ast.AST, parent: Any = None):
        node_id = id(current_node)
        node_type = type(current_node).__name__
        graph.add_node(node_id, label=node_type)
        if parent is not None:
            graph.add_edge(id(parent), node_id)
        for child in ast.iter_child_nodes(current_node):
            dfs(child, current_node)

    dfs(ast.parse(code))

    return graph


def hash_tree(tree: nx.DiGraph, node: int) -> str:
    """
    Hashes the tree taking into account the features of the nodes.
    Each node is recorded with a unique id,
    but it also stores the name of the python operator.

    Args:
        tree:
            Undirected tree.
        node:
            ID of the current node.
    Returns:
        The string - hashed inputted tree.
    """

    node_hash = hashlib.sha256(str(tree.nodes[node]["label"]).encode()).hexdigest()

    children = nx.descendants(tree, node)

    child_hashes = [hash_tree(tree, child) for child in children]

    combined = node_hash + "".join(sorted(child_hashes))
    return hashlib.sha256(combined.encode()).hexdigest()


def generate_subtrees_hashes(tree: nx.DiGraph) -> list[str]:
    """
    Accepts a tree as input and returns a list of hashes of its subtrees.
    Subtrees are built only from certain nodes (they are written in available_roots).

    Args:
        tree:
            The tree to get the subtrees from.

    Returns:
        The list of the subtrees hashes for inputted tree.
    """
    avaliable_roots = ["FunctionDef", "For", "While", "If"]
    nodes = tree.nodes()
    res = []

    def dfs(cur_node_id: int):
        cur_node_data = tree.nodes[cur_node_id]

        if cur_node_data["label"] in avaliable_roots:
            res.append(hash_tree(get_subtree(tree, cur_node_id), cur_node_id))

        for child_id in tree.successors(cur_node_id):
            dfs(child_id)

    root = [x for x in nodes if tree.nodes[x]["label"] == "Module"][0]
    dfs(root)

    return res


def get_the_coeff_part(coeff: float | int) -> str:
    """
    The function that gives the color that depended on coefficient.

    Args:
        coeff:
            Coefficient of similarity.
    Returns:
        The .html part for this coefficient.
    """

    if coeff <= 50:
        return f"""<span class="green">{coeff}%</span>"""
    if coeff <= 80:
        return f"""<span class="orange">{coeff}%</span>"""
    return f"""<span class="red">{coeff}%</span>"""
