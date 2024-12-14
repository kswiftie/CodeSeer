import os, shutil
from codeseer.utils_for_repos import RepoHandler
from .inspection_utils.ast_tools import AST, list_of_edges, adjacency_matrix


class ASTInspection:
    def __init__(self, repo_handler: RepoHandler):
        """
        init func

        Parametrs
        ---------
        repo_handler: RepoHandler
            Instance of a class that can handle links from github
        """
        self.repo_handler = repo_handler
        self.ast_tools = AST()

    def compare_ast_subgraphs_to_isomorphism_for_files(self, *file_urls: list[str], max_legth: int = 9) -> dict[
        str, float]:
        """
        A function that checks the AST subgraphs of code
        in given files for isomorphism

        Parametrs
        ---------
        file_urls: list[str]
            A list of links to files
            where you want to compare programs

        max_length: int
            The limit of max subgraph length
            If max_length == -1 then max length of subgraphs will be limited automaticly

        Returns
        -------
        res: dict[str, float]
            The key is the name of files and length of the subgraphs.
            The value is the percentage of isomorphic of the total
        """

        # In fact, the maximum number of isomorphic subgraphs
        # is the minimum of subgraphs for each tree

        os.makedirs("codeseertemp")

        results: dict[str, float] = {}

        start_length = 3
        file_urls_count = len(file_urls)

        # list of dictionaries where i-th dictionary corresponds to the i-th link
        # key - length of subgraphs, value - count of subgraphs of such length
        count_of_subgraphs = [dict() for _ in range(file_urls_count)]

        for url_id in range(file_urls_count):
            cur_folder = f"codeseertemp/file{url_id}"  # folder with graph for cur file
            # and for subgraphs of this graph
            os.makedirs(cur_folder)
            # get the graph and write it
            cur_graph = self.ast_tools.build_ast(self.repo_handler.get_file_info(file_urls[url_id])[0],
                                                 cur_folder + "/fullgraph",
                                                 adjacency_matrix)

            # now get the subgraphs
            for subgraph_length in range(start_length, max_legth + 1):
                cur_folder_subgraphs = f"codeseertemp/file{url_id}/subgraphs_length{subgraph_length}"  # folder for subgraphs
                os.makedirs(cur_folder_subgraphs)
                count_of_subgraphs[url_id][subgraph_length] = self.ast_tools.generate_subgraphs(cur_graph,
                                                                                                cur_folder_subgraphs,
                                                                                                subgraph_length)

        # could work long if u push many urls and
        # many lengths of subgraphs
        for url_id1 in range(file_urls_count):
            for url_id2 in range(url_id1 + 1, file_urls_count):
                # compare all subgraphs for two files
                for subgraph_length in range(start_length, max_legth + 1):
                    count_of_isomorphic_subgraphs = 0
                    (
                        cur_folder_subgraphs1,
                        cur_folder_subgraphs2
                    ) = (
                        f"codeseertemp/file{url_id1}/subgraphs_length{subgraph_length}/",
                        f"codeseertemp/file{url_id2}/subgraphs_length{subgraph_length}/"
                    )
                    # compare subgraphs for current length

                    # list of numbers of subgraphs that
                    # shouldnt be comparable anymore
                    dont_compare_graphs = []
                    for subgraph1_file_number in range(1, count_of_subgraphs[url_id1][subgraph_length]):
                        subgraph1 = self.ast_tools.read_graphs_from_dotfile(
                            cur_folder_subgraphs1 + f"subgraph_{subgraph1_file_number}.dot"
                        )  # get the subgraph

                        for subgraph2_file_number in range(1, count_of_subgraphs[url_id2][subgraph_length]):
                            if subgraph2_file_number in dont_compare_graphs:
                                continue

                            subgraph2 = self.ast_tools.read_graphs_from_dotfile(
                                cur_folder_subgraphs2 + f"subgraph_{subgraph2_file_number}.dot"
                            )  # get the subgraph

                            if self.ast_tools.check_isomorphism(subgraph1, subgraph2):
                                dont_compare_graphs.append(subgraph2_file_number)
                                count_of_isomorphic_subgraphs += 1
                                break

                    results[
                        f"{file_urls[url_id1]}--{file_urls[url_id2]}--{subgraph_length}"] = (
                            count_of_isomorphic_subgraphs /
                            (
                                    min(
                                        count_of_subgraphs[url_id1][subgraph_length],
                                        count_of_subgraphs[url_id2][subgraph_length]
                                    ) - 1
                            ))

        shutil.rmtree("codeseertemp")

        return results

    def compare_ast_subgraphs_to_isomorphism_for_files2(self, *file_urls: list[str], max_legth: int = 9) -> dict[
        str, float]:
        """
        SECOND VARIANT
        RAW
        IN TESING
        """
        shutil.rmtree("codeseertemp")
        os.makedirs("codeseertemp")

        results: dict[str, float] = {}

        start_length = 9
        file_urls_count = len(file_urls)

        # list of dictionaries where i-th dictionary corresponds to the i-th link
        # key - length of subgraphs, value - count of subgraphs of such length
        count_of_subgraphs = [dict() for _ in range(file_urls_count)]

        for url_id in range(file_urls_count):
            cur_folder = f"codeseertemp/file{url_id}"  # folder with graph for cur file
            # and for subgraphs of this graph
            os.makedirs(cur_folder)
            # get the graph and write it
            cur_graph = self.ast_tools.build_ast(self.repo_handler.get_file_info(file_urls[url_id])[0],
                                                 cur_folder + "/fullgraph",
                                                 adjacency_matrix)

            # now get the subgraphs
            for subgraph_length in range(start_length, max_legth + 1):
                cur_folder_subgraphs = f"codeseertemp/file{url_id}/subgraphs_length{subgraph_length}"  # folder for subgraphs
                os.makedirs(cur_folder_subgraphs)
                count_of_subgraphs[url_id][subgraph_length] = self.ast_tools.generate_subgraphs2(cur_graph,
                                                                                                 cur_folder_subgraphs)

        # could work long if u push many urls and
        # many lengths of subgraphs
        for url_id1 in range(file_urls_count):
            for url_id2 in range(url_id1 + 1, file_urls_count):
                # compare all subgraphs for two files
                for subgraph_length in range(start_length, max_legth + 1):
                    count_of_isomorphic_subgraphs = 0
                    (
                        cur_folder_subgraphs1,
                        cur_folder_subgraphs2
                    ) = (
                        f"codeseertemp/file{url_id1}/subgraphs_length{subgraph_length}/",
                        f"codeseertemp/file{url_id2}/subgraphs_length{subgraph_length}/"
                    )
                    # compare subgraphs for current length

                    # list of numbers of subgraphs that
                    # shouldnt be comparable anymore
                    dont_compare_graphs = []
                    for subgraph1_file_number in range(1, count_of_subgraphs[url_id1][subgraph_length]):
                        subgraph1 = self.ast_tools.read_graphs_from_dotfile(
                            cur_folder_subgraphs1 + f"subgraph_{subgraph1_file_number}.dot"
                        )  # get the subgraph

                        for subgraph2_file_number in range(1, count_of_subgraphs[url_id2][subgraph_length]):
                            if subgraph2_file_number in dont_compare_graphs:
                                continue

                            subgraph2 = self.ast_tools.read_graphs_from_dotfile(
                                cur_folder_subgraphs2 + f"subgraph_{subgraph2_file_number}.dot"
                            )  # get the subgraph

                            if self.ast_tools.check_isomorphism(subgraph1, subgraph2):
                                dont_compare_graphs.append(subgraph2_file_number)
                                count_of_isomorphic_subgraphs += 1
                                break

                    results[
                        f"{file_urls[url_id1]}--{file_urls[url_id2]}--{subgraph_length}"] = (
                            count_of_isomorphic_subgraphs /
                            (
                                    min(
                                        count_of_subgraphs[url_id1][subgraph_length],
                                        count_of_subgraphs[url_id2][subgraph_length]
                                    ) - 1
                            ))

        # shutil.rmtree("codeseertemp")

        return results

    def compare_ast_subgraphs_to_isomorphism_for_repos(self, max_legth: int = 9, *repo_urls: list[str]) -> dict[
        int, float]:
        """
        A function that checks the AST subgraphs of code
        in given repositories for isomorphism

        In fact, the maximum number of isomorphic subgraphs
        is the minimum of subgraphs for each tree

        Parametrs
        ---------
        repo_urls: list[str]
            A list of repositories or links to folders in repository
            where you want to compare programs

        max_length: int
            The limit of max subgraph length
            If max_length == -1 then max length of subgraphs will be limited automaticly

        Returns
        -------
        res: dict[int, float]
            The key is the length of the subgraphs.
            The value is the percentage of isomorphic of the total
        """

        start_length = 9

        # TBD

        return


class AST_results_handler(ASTInspection):
    _AVAILABLE_AST_INSPECTIONS_LIST = [
        "handle_ast_compare_ast_subgraphs_to_isomorphism_for_files"
    ]

    def __init__(self, repo_handler):
        super().__init__(repo_handler)

    def handle_all_inspections_results(self, *repo_urls) -> str:
        res = "AST Inspections Results:\n"
        for inspection in self._AVAILABLE_IDENTITY_INSPECTIONS_LIST:
            res += getattr(self, inspection)(*repo_urls) + "\n"

        return res

    def handle_ast_compare_ast_subgraphs_to_isomorphism_for_files(self, *repo_urls) -> str:
        return f""
