import os, requests, base64


class RepoHandler:
    def __init__(self, token: str):
        """
        init

        Parameters
        ----------
        token: str
            GitHub user token for API requests
        """
        self.headers = {"Authorization": f"token {token}"}

    def get_file_info(self, file_url: str) -> tuple[str, int]:
        """

        :param file_url:
        :return:
        """
        response = requests.get(file_url, headers=self.headers)
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

    def get_list_of_files_in_folder(self, folder_url: str) -> list:
        """

        :param folder_url:
        :return:
        """

        response = requests.get(folder_url, headers=self.headers)
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

    def get_list_of_folders_in_folder(self, folder_url: str) -> list:
        """

        :param folder_url:
        :return:
        """
        response = requests.get(folder_url, headers=self.headers)
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
        response = requests.get(folder_url, headers=self.headers)
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
