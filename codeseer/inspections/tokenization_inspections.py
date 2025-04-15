import torch

from .inspection_tools.unixcoder import UniXcoder
from collections import Counter
from nltk.metrics.distance import edit_distance
from codeseer.utils_for_repos import RepoHandler

from .inspection_tools.tokenization_tools import (
    get_normalized_embedding,
    euclidean_similarity,
    get_the_coeff_part,
    tokenize_code,
    cos_similarity_counter_modififed,
    cosine_between_tensors,
)

from .inspection_tools.general_tools import (
    inputs_preprocessing1,
    inputs_preprocessing2,
    get_the_name_of_link,
)


class TokenizationInspections:
    def __init__(self, repo_handler: RepoHandler):
        """
        init func

        :param repo_handler:
        """
        self.repo_handler = repo_handler
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = UniXcoder("microsoft/unixcoder-base").to(self.device)

    def compare_files_standart(self, *file_inputs) -> dict[str, float]:
        """
        A function for comparing files using tokenization.
        This is a simplified version of the comparison.
        Tokens in files are counted here, vectors are built on them,
        and the cosine of the angle is located between them.

        Args:
            file_urls: list[str]
                A list of links from the github pointing to the file

        Returns:
            result: dict[str, float]
                A dictionary in which the key is
                a string indicating the files being compared,
                and the value is the result of comparing files
                from the key.
        """

        file_urls, file_names = zip(*file_inputs)

        result: dict[str, float] = {}
        # Stores tokens for each file
        file_tokens: list[set[str]] = []
        # Stores the number of uses of each token by files
        file_counters: list[Counter[str]] = []

        files_count = len(file_urls)

        for file_url in file_urls:
            cur_file_tokens, cur_file_counter = tokenize_code(
                self.repo_handler.get_file_content(file_url)
            )
            file_tokens.append(cur_file_tokens)
            file_counters.append(cur_file_counter)

        for i in range(files_count):
            for j in range(i + 1, files_count):
                if True:
                    lev_distance = edit_distance(
                        sorted(file_tokens[i]), sorted(file_tokens[j])
                    )
                    max_len = max(len(file_tokens[i]), len(file_tokens[j]))
                    similarity = 1 - (lev_distance / max_len)

                    result[f"{file_names[i]} to {file_names[j]}"] = similarity
                else:
                    result[f"{file_names[i]} to {file_names[j]}"] = (
                        cos_similarity_counter_modififed(
                            file_counters[i], file_counters[j]
                        )
                    )

        return result

    def compare_folders_standart(
            self, *folder_inputs
    ) -> dict[str, float]:
        """
        A function for comparing the contents between
        all files in folders using tokenization.
        This is a simplified version of the comparison.
        Tokens in files are counted here, vectors are built on them,
        and the cosine of the angle is located between them.

        Args:
            file_urls: list[str]
                A list of links from the github pointing to the folders

        Returns:
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

        # below im gonna compare each file from each folder
        # to all files from other folders (1 file - all files)
        for i in range(count_of_folders):
            count_of_files_from_cur_folder = len(file_links[i])
            for q in range(i + 1, count_of_folders):
                for j in range(count_of_files_from_cur_folder):
                    # add results for cur file from cur folder
                    result = {**result, **self.compare_files_standart(
                        file_links[i][j], *file_links[q]
                    )}
                    # we can just take a max from each
                    # step bc file should not look similar
                    # more than with 1 other file ig

        return result

    def compare_files_nn(self, *file_inputs) -> dict[str, float]:
        """
        A function for comparing content between files
        An important feature is the use of a neural network to
        obtain the results of this function.

        Parameters
        ---------
        file_urls: list[str]
            A list of links from the github pointing to the file

        Returns
        -------
        result: dict[str, float]
            A dictionary in which the key is
            a string indicating the files being compared,
            and the value is the result of comparing files
            from the key.
        """

        file_urls, file_names = zip(*file_inputs)

        files_count = len(file_urls)
        result: dict[str, float] = {}
        files_content: list[str] = []

        for file_url in file_urls:
            files_content.append(self.repo_handler.get_file_content(file_url))

        for i in range(files_count):
            for j in range(i + 1, files_count):
                emb1 = get_normalized_embedding(files_content[i], self.model, self.device)
                emb2 = get_normalized_embedding(files_content[j], self.model, self.device)
                if False:  # In testing
                    result[f"{file_names[i]} to {file_names[j]}"] = (
                        cosine_between_tensors(emb1, emb2)
                    )
                else:
                    result[f"{file_names[i]} to {file_names[j]}"] = (
                        euclidean_similarity(emb1, emb2)
                    )

        return result

    def compare_folders_nn(
            self, *folder_inputs
    ) -> dict[str, float]:
        """
        A function for comparing the contents between all files in folders
        An important feature is the use of a neural network to
        obtain the results of this function.

        Args:
            folder_inputs: list[str]
                A list of links from the github pointing to the folders

        Returns:
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
        folders_count = len(folder_urls)

        for folder_url in folder_urls:
            file_links.append([])
            for file in self.repo_handler.get_list_of_files_in_folder(
                    folder_url, types_for_selection=[".py"]
            ):
                link = file["url"]
                file_links[-1].append((link, get_the_name_of_link(link)))

        # below im gonna compare each file from each folder
        # to all files from other folders (1 file - all files)
        for i in range(folders_count):
            count_of_files_from_cur_folder = len(file_links[i])
            for q in range(i + 1, folders_count):
                for j in range(count_of_files_from_cur_folder):
                    # add results for cur file from cur folder
                    result = {**result, **self.compare_files_nn(
                        file_links[i][j], *file_links[q]
                    )}

        return result

    def compare_files_with_folders_standart(
            self, file_inputs: list[str], folder_inputs: list[str]
    ) -> dict[str, float]:
        """
        This function compares files with all files from folders.
        This is a simple version of the function.

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
                count_of_files_in_cur_folder = 0
                for file in self.repo_handler.get_list_of_files_in_folder(
                        folder_urls[j], types_for_selection=[".py"]
                ):
                    count_of_files_in_cur_folder += 1
                    link = file["url"]

                    result = {**result, **self.compare_files_standart(
                        (file_urls[i], file_names[i]),
                        (link, get_the_name_of_link(link)),
                    )}

        return result

    def compare_files_with_folders_nn(
            self, file_inputs: list[str], folder_inputs: list[str]
    ) -> dict[str, float]:
        """
        This function compares files with all files from folders.
        An important feature is the use of a neural network to
        obtain the results of this function.

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
                count_of_files_in_cur_folder = 0
                for file in self.repo_handler.get_list_of_files_in_folder(
                        folder_urls[j], types_for_selection=[".py"]
                ):
                    count_of_files_in_cur_folder += 1
                    link = file["url"]
                    result = {**result, **self.compare_files_nn(
                        (file_urls[i], file_names[i]),
                        (link, get_the_name_of_link(link)),
                    )}

        return result


class TokenizationResultsHandler(TokenizationInspections):
    _AVAILABLE_TOKENIZATION_INSPECTIONS_LIST = [
        "compare_files_standart",
        "compare_folders_standart",
        "compare_files_nn",
        "compare_folders_nn",
        "compare_files_with_folders_standart",
        "compare_files_with_folders_nn",
    ]

    @inputs_preprocessing1
    def handle_compare_files_standart(self, *file_inputs) -> str:
        """
        inputs may be str or tuple
        """

        func_result = super().compare_files_standart(*file_inputs)

        part_to_report = """check using tokens and levenstein (comparing of files)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing1
    def handle_compare_folders_standart(self, *folder_inputs) -> str:
        func_result = super().compare_folders_standart(*folder_inputs)

        part_to_report = """check using tokens and levenstein (comparing of folders)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing1
    def handle_compare_files_nn(self, *file_inputs) -> str:
        func_result = super().compare_files_nn(*file_inputs)

        part_to_report = """check using unixcoder (comparing of files)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing1
    def handle_compare_folders_nn(self, *folder_inputs) -> str:
        func_result = super().compare_folders_nn(*folder_inputs)

        part_to_report = """check using unixcoder (comparing of folders)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing2
    def handle_compare_files_with_folders_standart(
            self, file_inputs: list[str], folder_inputs: list[str]
    ) -> str:
        func_result = super().compare_files_with_folders_standart(file_inputs, folder_inputs)

        part_to_report = """check using tokens and levestein (comparing of files with folders)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing2
    def handle_compare_files_with_folders_nn(
            self, file_inputs: list[str], folder_inputs: list[str]
    ) -> str:
        func_result = super().compare_files_with_folders_nn(file_inputs, folder_inputs)

        part_to_report = """check using unixcoder (comparing of files with folders)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report
