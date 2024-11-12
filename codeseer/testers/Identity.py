from codeseer.utils_for_repos import RepoHandler

"""
IC means identity check
"""


class IdentityInspection:
    """
    Class for the simplest checks of two repositories
    """

    def __init__(self, repo_handler):
        self.repo_handler = repo_handler

    def compare_sizes_in_folders(self, folder1_url: str, folder2_url: str):
        """
        Function compares the sizes of files and folders in repositories
        :return:
        """
        folder1_size, folder2_size = 0, 0

        folder1_folders = self.repo_handler.get_list_of_folders_in_folder(folder1_url)
        folder2_folders = self.repo_handler.get_list_of_folders_in_folder(folder2_url)

        for folder in folder1_folders:
            folder1_size += self.repo_handler.get_folder_size(folder["url"])

        for folder in folder2_folders:
            folder2_size += self.repo_handler.get_folder_size(folder["url"])

        return folder1_size, folder2_size

    def compare_names_in_folders(self, folder1_url: str, folder2_url: str):
        """
        Function compares the names of files and folders in repositories

        Returns
        -------
        result: float
            The Jacquard coefficient, which belongs from 0 to 1.
            The higher it is, the higher the similarity of names in the repository
        """

        # todo: add the translation of the names to the way they sound (Soundex) and then check

        folder1_files = set(
            [
                file["name"]
                for file in self.repo_handler.get_list_of_files_in_folder(folder1_url)
            ]
        )
        folder2_files = set(
            [
                file["name"]
                for file in self.repo_handler.get_list_of_files_in_folder(folder2_url)
            ]
        )

        if not folder1_files or not folder2_files:
            raise ValueError("Folders should not be empty")

        # The Jacquard coefficient
        return len(folder1_files & folder2_files) / len(folder1_files | folder2_files)

    def compare_content_in_files(self, file1_url: str, file2_url: str):
        """
        Function checks the lengths of the lines in the files and checks how identical they are

        :return:
        """

        # todo: Decide what to do with file sizes

        file1_content, file1_size = self.repo_handler.get_file_info(file1_url)
        file2_content, file2_size = self.repo_handler.get_file_info(file2_url)

        return len(file1_content), len(file2_content)

    def compare_content_in_repos(self, repo1_url: str, repo2_url: str):
        """
        Function checks the lengths of the lines in all files of repositories and checks how identical they are

        :return:
        """
        pass


class Identity_results_handler(IdentityInspection):
    AVAILABLE_IDENTITY_INSPECTIONS_LIST = [
        "handle_Identity_compare_sizes_in_folders_results",
        "handle_Identity_compare_names_in_folders",
        "handle_Identity_compare_content_in_repos",
    ]

    def handle_Identity_results(self, *repo_urls) -> str:
        res = ""
        for inspection in Identity_results_handler.AVAILABLE_IDENTITY_INSPECTIONS_LIST:
            res += getattr(self, inspection)(*repo_urls) + "\n\n"

        return res

    def handle_Identity_compare_sizes_in_folders_results(self, *repo_urls) -> str:
        a, b = super().compare_sizes_in_folders(*repo_urls)
        return f"The difference between project weights is {abs(a - b)}"

    def handle_Identity_compare_names_in_folders(self, *repo_urls) -> str:
        similarity_coeff = super().compare_names_in_folders(*repo_urls)
        return f"The contents of the names used in the projects match on {similarity_coeff * 100}%"

    def handle_Identity_compare_content_in_repos(self, *repo_urls) -> str:
        return ""
