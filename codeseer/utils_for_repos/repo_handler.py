import os, requests, base64, re, ast, functools
from codeseer.inspections.inspection_tools.general_tools import remove_comments


def is_valid_python_code(code: str) -> bool:
    """
    Verifies that the inputted code is valid
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def allow_python_code(func):
    """
    Since RepoHandler was written to work with links,
    it will return an error when receiving the code.

    This decorator checks that the entered code is correct
    and skips it past the RepoHandler functions.
    """

    @functools.wraps(func)
    def wrapper(self, input):
        if is_valid_python_code(input):
            return input
        return func(self, input)

    return wrapper


class RepoHandler:
    def __init__(self, user_github_token: str):
        self.headers = {"Authorization": f"token {user_github_token}"}

    @allow_python_code
    def handle_github_url(self, url: str) -> str:
        """
        A function that converts a link to a project
        on GitHub into a request to the GitHub API.
        If the correct link is passed, nothing will happen to it.

        Args:
            url:
                Link on the GitHub.

        Returns:
            Request to GitHub API.
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

    @allow_python_code
    def get_file_content(self, file_url: str) -> str:
        """
        The function accepts a link to the file as input
        and returns its contents.

        Args:
            file_url:
                Link to the file to get information about.

        Returns:
            The contents of the file.
        """

        response = requests.get(self.handle_github_url(file_url), headers=self.headers)
        try:
            file_info = response.json()
            file_content = base64.b64decode(file_info["content"]).decode("utf-8")
            return remove_comments(file_content)
        except Exception as ex:
            print(f"ERROR: {ex}")
            quit()

    def get_list_of_files_in_folder(self, folder_url: str, types_for_selection: list[str] = [".py"]) -> list[
        dict[str, str]]:
        """
        The function accepts a link to a folder as input
        and returns a list of all files stored inside this folder.
        At the moment, the function will also return
        files located inside child folders.

        Args:
            folder_url:
                Link to the folder.
            types_for_selection:
                List of file extensions to consider.

        Returns:
            A list of files inside a given folder.
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
                    if types_for_selection and f".{obj["name"].split('.')[-1]}" in types_for_selection:
                        files_list.append(obj)
                # if obj["type"] == "dir": I guess it is wrong
                #     files_list.extend(self.get_list_of_files_in_folder(obj["url"]))
        except Exception as ex:
            print(f"ERROR: {ex}")
            quit()

        return files_list

    def get_list_of_folders_in_folder(self, folder_url: str) -> list[dict[str, str]]:
        """
        Returns the list of folders in folder by the entered url
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
            print(f"ERROR: {ex}")
            quit()

        return folders_list
