import os, requests, base64, re


class RepoHandler:
    def __init__(self, user_github_token: str):
        """
        init

        Parameters
        ----------
        user_github_token: str
            GitHub user token for API requests
        """
        self.headers = {"Authorization": f"token {user_github_token}"}

    def handle_github_url(self, url: str) -> str:
        """
        A function that converts a link to a project
        on GitHub into a request to the GitHub API.
        If the correct link is passed, nothing will happen to it.

        Parametrs
        ---------
        url: str
            Link to the project on GitHub

        Returns
        -------
        api_request: str
            Request to GitHub API
        """

        api_pattern = (
            r"https?://api.github.com/repos/([^/]+)/([^/]+)/contents/.*\?ref=([^&]+)"
        )
        if re.match(api_pattern, url):
            return url

        pattern = r"https?://github.com/([^/]+)/([^/]+)/(?:blob|tree)/([^/]+)/?(.*)"

        match = re.match(pattern, url)

        if not match:
            pattern_simple = r"https?://github.com/([^/]+)/([^/]+)/?$"
            match = re.match(pattern_simple, url)
            if match:
                user = match.group(1)
                repo = match.group(2)
                return f"https://api.github.com/repos/{user}/{repo}/contents/?ref=main"

            raise ValueError("Incorrect url")

        user = match.group(1)
        repo = match.group(2)
        branch = match.group(3)
        path = match.group(4) if match.group(4) else ""

        api_request = (
            f"https://api.github.com/repos/{user}/{repo}/contents/{path}?ref={branch}"
        )
        return api_request

    def get_file_info(self, file_url: str) -> tuple[str, int]:
        """
        The function accepts a link to the file as input
        and returns its contents as a string and its size

        Parametrs
        ---------
        file_url: str
            Link to the file to get information about

        Returns
        -------
        Result: tuple[str, int]
            A pair is the contents of the file and its size
        """

        response = requests.get(self.handle_github_url(file_url), headers=self.headers)
        try:
            file_info = response.json()
            file_content, file_size = (
                base64.b64decode(file_info["content"]).decode("utf-8"),
                file_info["size"],
            )
            return file_content, file_size
        except Exception as ex:
            # print(ex)
            return "", 0

    def get_list_of_files_in_folder(self, folder_url: str) -> list[dict[str, str]]:
        """
        The function accepts a link to a folder as input
        and returns a list of all files stored inside this folder.
        At the moment, the function will also return
        files located inside child folders.

        Parametrs
        ---------
        folder_url: str
            Link to the folder

        Returns
        -------
        Result: list[dict[str, str]]
            A list of files inside a given folder
        """

        response = requests.get(
            self.handle_github_url(folder_url), headers=self.headers
        )
        files_list = []

        try:
            response_info = response.json()
            if isinstance(response_info, dict):
                response_info = [response_info]
            for obj in response_info:
                if obj["type"] == "file":
                    files_list.append(obj)
                if obj["type"] == "dir":
                    files_list.extend(self.get_list_of_files_in_folder(obj["url"]))
        except Exception as ex:
            print(ex)

        return files_list

    def get_list_of_folders_in_folder(self, folder_url: str) -> list[dict[str, str]]:
        """

        :param folder_url:
        :return:
        """
        response = requests.get(
            self.handle_github_url(folder_url), headers=self.headers
        )
        folders_list = []

        try:
            response_info = response.json()
            if isinstance(response_info, dict):
                response_info = [response_info]
            for obj in response_info:
                if obj["type"] == "dir":
                    folders_list.append(obj)
                    folders_list.extend(self.get_list_of_folders_in_folder(obj["url"]))
        except Exception as ex:
            print(ex)

        return folders_list

    def get_folder_size(self, folder_url: str) -> float:
        """

        :param folder_url:
        :return:
        """
        response = requests.get(
            self.handle_github_url(folder_url), headers=self.headers
        )
        folder_size = 0.0

        try:
            response_info = response.json()
            if isinstance(response_info, dict):
                response_info = [response_info]
            for obj in response_info:
                if obj["size"] == 0:
                    folder_size += self.get_folder_size(obj["url"])
                else:
                    folder_size += obj["size"]
        except Exception as ex:
            print(ex)

        return folder_size
