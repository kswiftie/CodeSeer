from codeseer.inspections import Identity_results_handler, Tokenization_results_handler
from codeseer.utils_for_repos import RepoHandler


class ReportsCompiler:
    _AVAILABLE_INSPECTIONS: dict[str, list[str]] = {
        "Tokenization_results_handler": ["handle_Tokenization_compare_folders_content"],
        "Identity_results_handler": [
            "handle_Identity_compare_sizes_in_folders_results",
            "handle_Identity_compare_names_in_folders",
        ],
    }

    def __init__(self, repo_handler: object):
        """
        init
        """

        self.repo_handler = repo_handler

    def get_report_from_inspections(
        self, inspections_to_do: list[tuple[str, str]] | str = "all", *repo_urls
    ) -> str:
        """
        The function that will be called by the user.
        Accepts links to repositories and runs everything necessary to get a repository report

        :param repo_urls:

        :return:
        """

        if len(repo_urls) != 2:
            print("At the moment, only 2 repositories can be compared")
            return ""

        report = ""

        if inspections_to_do == "all":
            for (
                inspection_class_name,
                inspection_names,
            ) in self._AVAILABLE_INSPECTIONS.items():
                for inspection_name in inspection_names:
                    report += self.get_report_from_inspection(
                        inspection_class_name, inspection_name, *repo_urls
                    )

        elif isinstance(inspections_to_do, list):
            for inspection_class_name, inspection_name in inspections_to_do:
                report += self.get_report_from_inspection(
                    inspection_class_name, inspection_name, *repo_urls
                )

        return report

    def get_report_from_inspection(
        self, inspection_class_name: str, inspection_name: str, *repo_urls: list[str]
    ) -> str:
        inspection = globals()[inspection_class_name](self.repo_handler)
        return getattr(inspection, inspection_name)(*repo_urls) + "\n"
