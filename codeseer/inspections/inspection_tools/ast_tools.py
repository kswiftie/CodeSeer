import ast, hashlib
import networkx as nx
from typing import Any

NODE_NORMALIZATION = {
    "For": "Loop",
    "AsyncFor": "Loop",
    "While": "Loop",
    "FunctionDef": "Func",
    "AsyncFunctionDef": "Func",
    "Lambda": "Func",  # Not sure.
    # "With": "With",
    "AsyncWith": "With",
    "IfExp": "If",
    "Compare": "BinOP",  # Not sure.
    # "Try": "Try",
    "TryStar": "Try",
    "Break": "Control",
    "Continue": "Control",
    "Pass": "Control",
    # "Import": "Import",
    "ImportFrom": "Import",
    "Return": "Flow",
    "Raise": "Flow",
    "Yield": "Flow",
    "YieldFrom": "Flow",
    "ListComp": "Comprehension",
    "SetComp": "Comprehension",
    "DictComp": "Comprehension",
    "GeneratorExp": "Comprehension",
    "Assign": "Assign",
    "AnnAssing": "Assign",
    "Attribute": "Access",
    "Subscript": "Access",
    # "BinOp": "BinOp",
    "UnaryOp": "BinOp",  # not sure
    "BoolOp": "BinOp",  # not sure
}


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


def get_branches(tree: nx.DiGraph, root_id: int) -> list[nx.DiGraph]:
    """
    Возвращает список всех подграфов-ветвей, исходящих от root_id.

    Args:
        tree: граф AST (ориентированное дерево)
        root_id: идентификатор корня

    Returns:
        Список подграфов (каждая ветка — поддерево от одного из потомков root_id)
    """
    branches = []
    for child_id in tree.successors(root_id):
        branch_nodes = nx.descendants(tree, child_id) | {child_id} | {root_id}
        subgraph = tree.subgraph(branch_nodes).copy()
        branches.append(subgraph)
    return branches


def build_ast(code: str) -> nx.DiGraph:
    """
    Builds AST (abstract syntax tree) from inputted code.

    Args:
        code: The Python code to build the AST from.

    Returns:
        AST as a directed graph.
    """

    graph = nx.DiGraph()
    cur_id = 0

    def dfs(current_node: ast.AST, parent_id=None):
        nonlocal cur_id
        node_id = cur_id
        cur_id += 1
        node_type = type(current_node).__name__
        graph.add_node(node_id, label=NODE_NORMALIZATION.get(node_type, node_type))

        if parent_id is not None:
            graph.add_edge(parent_id, node_id)
        for child in ast.iter_child_nodes(current_node):
            dfs(child, node_id)

    tree = ast.parse(code)
    dfs(tree)
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


def hash_tree_structure(tree: nx.DiGraph, root: int, parent: int | None = None) -> str:
    children = [n for n in tree.successors(root) if n != parent]

    child_hashes = [hash_tree_structure(tree, child, root) for child in children]

    child_hashes.sort()

    structure_str = "(" + "".join(child_hashes) + ")"

    return hashlib.sha256(structure_str.encode("utf-8")).hexdigest()


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
    # avaliable_roots = {"FunctionDef", "ClassDef", "For", "While", "If", "Try", "With", "Expr"}
    avaliable_roots = {"FunctionDef", "ClassDef", "Loop", "If", "Try", "With", "Expr"}
    nodes = tree.nodes()
    res = []

    def dfs(cur_node_id: int):
        cur_node_data = tree.nodes[cur_node_id]

        if cur_node_data["label"] in avaliable_roots:
            res.extend(
                [
                    hash_tree(subtree, cur_node_id)
                    for subtree in get_branches(tree, cur_node_id)
                ]
            )
            # res.extend([hash_tree_structure(subtree, cur_node_id) for subtree in get_branches(tree, cur_node_id)])
            # res.append(hash_tree_structure(get_subtree(tree, cur_node_id), cur_node_id))

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

    if coeff <= 40:
        return f"""<span class="green">{coeff}%</span>"""
    if coeff <= 60:
        return f"""<span class="orange">{coeff}%</span>"""
    return f"""<span class="red">{coeff}%</span>"""
