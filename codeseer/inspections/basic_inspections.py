import strsimpy

from codeseer.utils_for_repos import RepoHandler
from .inspection_tools.basic_tools import get_the_coeff_part
from .inspection_tools.general_tools import (
    inputs_preprocessing1,
    inputs_preprocessing2,
    get_the_name_of_link,
)


class BasicInspections:
    def __init__(self, repo_handler: RepoHandler):
        """
        We set the repository handler for the verification class,
        which this class will use to access the content on GitHub

        Parameters
        ----------
        repo_handler: object
            A pointer to the repository handler class
        """
        self.repo_handler = repo_handler

    def compare_files_levenstein(self, *file_inputs) -> dict[str, float]:
        """

        :param file_inputs:
        :return:
        """

        file_urls, file_names = zip(*file_inputs)
        result: dict[str, float] = {}
        files_count = len(file_urls)
        norm_levenstein = strsimpy.normalized_levenshtein.NormalizedLevenshtein()

        for i in range(files_count):
            for j in range(i + 1, files_count):
                result[f"{file_names[i]} to {file_names[j]}"] = (
                    1
                    - norm_levenstein.distance(
                        self.repo_handler.get_file_content(file_urls[i]),
                        self.repo_handler.get_file_content(file_urls[j]),
                    )
                )

        return result

    def compare_folders_levenstein(self, *folder_inputs) -> dict[str, float]:
        """

        :param folder_inputs:
        :return:
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

        for i in range(folders_count):
            count_of_files_from_cur_folder = len(file_links[i])
            for q in range(i + 1, folders_count):
                for j in range(count_of_files_from_cur_folder):
                    # add results for cur file from cur folder
                    result = {
                        **result,
                        **self.compare_files_levenstein(
                            file_links[i][j], *file_links[q]
                        ),
                    }

        return result

    def compare_files_with_folders_levenstein(
        self, file_inputs: list[str], folder_inputs: list[str]
    ) -> dict[str, float]:
        """

        :param file_inputs:
        :param folder_inputs:
        :return:
        """

        file_urls, file_names = zip(*file_inputs)
        folder_urls, folder_names = zip(*folder_inputs)

        result: dict[str, float] = {}

        for i in range(len(file_urls)):  # for each file
            for j in range(len(folder_urls)):  # for each folder
                for file in self.repo_handler.get_list_of_files_in_folder(
                    folder_urls[j], types_for_selection=[".py"]
                ):
                    link = file["url"]
                    result = {
                        **result,
                        **self.compare_files_levenstein(
                            (file_urls[i], file_names[i]),
                            (link, get_the_name_of_link(link)),
                        ),
                    }

        return result


class BasicResultsHandler(BasicInspections):
    _AVAILABLE_IDENTITY_INSPECTIONS_LIST = [
        "compare_files_levenstein",
        "compare_folders_levenstein",
        "compare_files_with_folders_levenstein",
    ]

    @inputs_preprocessing1
    def handle_compare_files_levenstein(self, *file_inputs) -> str:
        func_result = super().compare_files_levenstein(*file_inputs)

        part_to_report = """check using levenstein (comparing of files)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing1
    def handle_compare_folders_levenstein(self, *folder_inputs) -> str:
        func_result = super().compare_folders_levenstein(*folder_inputs)

        part_to_report = """check using levenstein (comparing of folders)\n"""
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report

    @inputs_preprocessing2
    def handle_compare_files_with_folders_levenstein(
        self, file_inputs: list[str], folder_inputs: list[str]
    ) -> str:

        func_result = super().compare_files_with_folders_levenstein(
            file_inputs, folder_inputs
        )

        part_to_report = (
            """check using levenstein (comparing of files with folders)\n"""
        )
        for compared_names, res_coeff in func_result.items():
            part_to_report += f"""<p>Similarity of {compared_names} is {get_the_coeff_part(res_coeff * 100)}</p>"""

        return part_to_report
