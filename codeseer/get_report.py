import datetime, os
from codeseer.inspections import (
    BasicResultsHandler,
    TokenizationResultsHandler,
    ASTResultsHandler,
)  # This is needed to use globals()

AVAILABLE_INSPECTIONS: dict[str, list[str]] = {
    "BasicInspections": [
        "compare_files_levenstein",
        "compare_folders_levenstein",
        "compare_files_with_folders_levenstein",
    ],
    "TokenizationInspections": [
        "compare_files_standart",
        "compare_folders_standart",
        "compare_files_nn",
        "compare_folders_nn",
        "compare_files_with_folders_standart",
        "compare_files_with_folders_nn",
    ],
    "ASTInspections": [
        "compare_files_hash",
    ],
}


def save_file(file_path: str, content: str) -> None:
    """
    Creates a file at the location specified inside the current directory.
    The file name must be included in the path.
    """
    directory = os.path.dirname(file_path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, "w") as file:
        file.write(content)


class ReportCompiler:

    def __init__(self, repo_handler: object):
        self.repo_handler = repo_handler

    def make_report(
        self, path: str = "./", inspections_to_do: dict[str, list[str]] = {}, *inputs
    ) -> None:
        """
        A function for creating reports.

        Args:
            inspections_to_do:
                This is a dictionary, where the key is a class of checks,
                and the values are a list of checks related to this class.

                There is no need to pass anything to this argument,
                then the program will run all the necessary checks on its own.
            path:
                The path to save the report.
                May include folders, must include the file name.
            inputs:
                The input data is in one of four formats -
                    str - GitHub link
                    str - code
                    tuple - (GitHub link, name for it)
                    tuple - (code, name for it).

                If you pass only a link or only a variable with a code,
                the program will independently give them names.

        Returns:
            Nothing. It only creates a report file.
        """

        report_heading = f"""<header>
    <h1>Analysis Report</h1>
    <p>{str(datetime.datetime.now()).split()[0]}</p>
</header>"""

        inspections_data: dict[str, str] = {
            "BasicInspectionsHeading": "",
            "BasicInspectionsContent": "",
            "TokenizationInspectionsHeading": "",
            "TokenizationInspectionsContent": "",
            "ASTInspectionsHeading": "",
            "ASTInspectionsContent": "",
        }

        style = """body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            color: #333;
        }

        header {
            text-align: center;
            padding: 15px;
            background-color: #ffffff;
            border-bottom: 1px solid #ddd;
        }

        h1 {
            font-size: 2em;
            color: #333;
            margin: 0;
        }

        h2, h3 {
            color: #444;
        }

        section {
            padding: 25px;
            margin: 15px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .sub-topic {
            background-color: #fafafa;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
        }

        .sub-topic h3 {
            margin-top: 0;
            font-size: 1.25em;
        }

        .sub-topic .content {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }

        footer {
            background-color: #ffffff;
            text-align: center;
            padding: 10px 0;
            border-top: 1px solid #ddd;
        }

        .link {
            color: #ffffff;
            background-color: #0056b3;
            text-decoration: none;
            padding: 2px 4px;
            border-radius: 4px;
            font-weight: normal;
            transition: background-color 0.3s;
        }

        .green {
            color: white;
            background-color: #28a745;
            padding: 2px 4px;
            border-radius: 4px;
        }

        .red {
            color: white;
            background-color: #dc3545;
            padding: 2px 4px;
            border-radius: 4px;
        }

        .orange {
            color: white;
            background-color: #fd7e14;
            padding: 2px 4px;
            border-radius: 4px;
        }
        .grey {
            background-color: #cccccc;
            padding: 2px 4px;
            border-radius: 4px;
        }"""

        head = f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Analysis report</title>

    <style>
        {style}
    </style>
</head>"""

        scripts = """<script>
function toggleContent(id) {
    var content = document.getElementById(id);
    if (content.style.display === "none" || content.style.display === "") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}
</script>"""

        def make_header(inspection_class_name):
            """
            Convert name of inspection class to .html format

            :return:
            """
            return f"""<h3 onclick="toggleContent('{inspection_class_name}')">{inspection_class_name}</h3>"""

        def assemble_block(inspection_class_name) -> str:
            """
            Collects headlines with content

            :return:
            """

            return (
                f"""
<section>
    <div class="sub-topic">
        {inspections_data[inspection_class_name + "Heading"]}
        <div id="{inspection_class_name}" class="content">
            {inspections_data[inspection_class_name + "Content"]}
        </div>
    </div>
</section>
            """
                if (inspections_data[inspection_class_name + "Heading"])
                and (inspections_data[inspection_class_name + "Content"])
                else ""
            )

        converter: dict[str, str] = {
            "BasicInspections": "BasicResultsHandler",
            "TokenizationInspections": "TokenizationResultsHandler",
            "ASTInspections": "ASTResultsHandler",
        }

        if not inspections_to_do:
            inspections_to_do = AVAILABLE_INSPECTIONS

        for inspection_class_name, list_of_inspections in inspections_to_do.items():
            inspections_data[inspection_class_name + "Heading"] = make_header(
                inspection_class_name
            )
            for inspection_name in list_of_inspections:
                inspection = globals()[converter[inspection_class_name]](
                    self.repo_handler
                )
                inspections_data[inspection_class_name + "Content"] += (
                    getattr(inspection, "handle_" + inspection_name)(*inputs) + "\n"
                )

        body = f"""
<body>
    {report_heading}

    {assemble_block("BasicInspections")}

    {assemble_block("TokenizationInspections")}

    {assemble_block("ASTInspections")}

<footer>
    <p>CodeSeer</p>
</footer>

</body>"""

        report_content = f"""<!DOCTYPE html>
<html lang="en">
{head}
{body}
{scripts}
</html>
"""

        if ".html" not in path:
            path += ".html"

        save_file(path, report_content)
