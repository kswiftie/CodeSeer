from codeseer.testers import Identity_results_handler
from codeseer.utils_for_repos import RepoHandler

AVALAVLE_INSPECTIONS = ["Identity_inspection"]


class ReportsCompiler:
    def __init__(
        self, user_github_token: str = "", user_login: str = "", user_password: str = ""
    ):
        """
        init

        :param user_github_token:
        :param user_login:
        :param user_password:
        """
        if user_github_token:
            self.token = user_github_token

        elif user_login and user_password:  # now this is not available to use
            self.login = user_login
            self.password = user_password

        else:
            raise ValueError("authorization is required")

    def get_report_from_all_inspections(self, *repo_urls) -> str:
        """
        The function that will be called by the user.
        Accepts links to repositories and runs everything necessary to get a repository report

        :param repo_urls:

        :return:
        """
        if len(repo_urls) != 2:
            print("At the moment, only 2 repositories can be compared")
            return ""

        indentical_inspections_results = Identity_results_handler(
            RepoHandler(self.token)
        )
        return indentical_inspections_results.handle_Identity_results(*repo_urls)
