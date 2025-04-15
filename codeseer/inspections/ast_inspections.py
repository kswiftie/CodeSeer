from codeseer.utils_for_repos import RepoHandler
from .inspection_tools.ast_tools import (
    get_the_coeff_part,
    generate_subtrees_hashes,
    build_ast,
)
from codeseer.inspections.inspection_tools.general_tools import (
    inputs_preprocessing1,
    inputs_preprocessing2,
    get_the_name_of_link,
)


class ASTInspections:
    def __init__(self, repo_handler: RepoHandler):
        """
        init func

        Parametrs
        ---------
        repo_handler: RepoHandler
            Instance of a class that can handle links from github
        """
        self.repo_handler = repo_handler

    def compare_files(self, *file_inputs) -> dict[str, float]:
        """
        A function for comparing the content between
        inputted files using AST.

        Args:
            file_inputs: list[tuple[str, str]]
                A list of pairs of links/codes and their names.

        Returns:
            result: dict[str, float]
                A dictionary in which the key is
                a string indicating the files being compared,
                and the value is the result of comparing files
                from the key.
        """

        files_links, files_names = zip(*file_inputs)
        files_hashes: list[list[str]] = []  # hashes of subgraphs for all files
        count_of_files = len(files_links)
        result: dict[str, float] = {}

        for i in range(count_of_files):
            files_hashes.append(
                generate_subtrees_hashes(
                    build_ast(self.repo_handler.get_file_content(files_links[i]))
                )
            )

        for i in range(count_of_files):
            for j in range(i + 1, count_of_files):
                count_of_sim_hashes = 0
                for hash_i in files_hashes[i]:
                    count_of_sim_hashes += min(
                        files_hashes[i].count(hash_i), files_hashes[j].count(hash_i)
                    )

                result[f"{files_names[i]}-{files_names[j]}"] = (
                    count_of_sim_hashes
                    / min(len(files_hashes[i]), len(files_hashes[j]))
                )

        return result

    def compare_folders(self, *folder_inputs) -> dict[str, float]:
        """
        A function for comparing the contents between
        all files in folders using AST.

        Args:
            file_urls: list[str]
                A list of links from the github pointing to the folders

        Returns
        -------
        result: dict[str, float]
            A dictionary in which the key is
            a string indicating the files being compared,
            and the value is the result of comparing files
            from the key.
            The results of comparing each file with each
            of the different folders will be written here.
        """

        folder_urls, folder_names = zip(*folder_inputs)

        result: dict[str, float] = {}
        file_links: list[list[tuple[str, str]]] = []
        count_of_folders = len(folder_urls)

        for folder_url in folder_urls:
            file_links.append([])
            for file in self.repo_handler.get_list_of_files_in_folder(
                folder_url, types_for_selection=[".py"]
            ):
                link = file["url"]
                file_links[-1].append((link, get_the_name_of_link(link)))

        # below each file from each folder is gonna be compared
        # to all each file from other folders
        for i in range(count_of_folders):
            count_of_files_from_cur_folder = len(file_links[i])
            for q in range(i + 1, count_of_folders):
                compared_folders = f"{folder_names[i]} to {folder_names[q]}"
                for j in range(count_of_files_from_cur_folder):
                    # results for cur file from cur folder
                    result = {
                        **result,
                        **self.compare_files(file_links[i][j], *file_links[q]),
                    }  # add to the result comparsions for cur file

        return result

    def compare_files_with_folders(
        self, file_inputs: list[str], folder_inputs: list[str]
    ) -> dict[str, float]:
        """
        This function compares inputted files with all files from inputted folders.

        Args:
            file_inputs: list[str]
                A list of links from the github pointing to the file

            folder_inputs: list[str]
                A list of links from the github pointing to the folder

        Returns:
            result: dict[str, float]
                A dictionary in which the key is
                a string indicating the files and folders being compared,
                and the value is the result of comparing files with folders.

                The results of comparing each file with each
                of the different folders will be written here.
        """

        file_urls, file_names = zip(*file_inputs)
        folder_urls, folder_names = zip(*folder_inputs)

        result: dict[str, float] = {}

        for i in range(len(file_urls)):  # for each file
            for j in range(len(folder_urls)):  # for each folder
                compared_file_with_folder = f"{file_names[i]} to {folder_names[j]}"
                count_of_files_in_cur_folder = 0
                for file in self.repo_handler.get_list_of_files_in_folder(
                    folder_urls[j], types_for_selection=[".py"]
                ):
                    count_of_files_in_cur_folder += 1
                    link = file["url"]

                    result = {
                        **result,
                        **self.compare_files(
                            (file_urls[i], file_names[i]),
                            (link, get_the_name_of_link(link)),
                        ),
                    }

        return result


class ASTResultsHandler(ASTInspections):
    _AVAILABLE_AST_INSPECTIONS_LIST = [
        "compare_files",
        "compare_folders",
        "compare_files_with_folders_standart",
    ]

    def __init__(self, repo_handler):
        super().__init__(repo_handler)

    @inputs_preprocessing1
    def handle_compare_files(self, *file_inputs) -> str:
        """
        A function to take processed results of inspection
        """
        func_result = super().compare_files(*file_inputs)

        part_to_report = """check using hash of ASTs (comparing of files)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing1
    def handle_compare_folders(self, *file_inputs) -> str:
        """
        A function to take processed results of inspection
        """

        func_result = super().compare_folders(*file_inputs)

        part_to_report = """check using hash of ASTs (comparing of folders)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing2
    def handle_compare_files_with_folders_standart(self, *file_inputs) -> str:
        """
        A function to take processed results of inspection
        """

        func_result = super().compare_files_with_folders(*file_inputs)

        part_to_report = (
            """check using hash of ASTs (comparing of files with folders)\n"""
        )
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report
