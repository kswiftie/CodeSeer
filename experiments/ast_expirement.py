import os, pathlib
from codeseer import RepoHandler, ReportCompiler

my_handler = RepoHandler(open("./token.txt", "r").read())
r = ReportCompiler(my_handler)

DATASET = pathlib.Path(__file__).parent.parent / "dataset"


def walk_directory(directory_path):
    for problemname in os.listdir(directory_path):
        if problemname == "readme.md":
            continue
        inputs = []
        for solutiontype in os.listdir(directory_path / problemname):
            for filename in os.listdir(directory_path / problemname / solutiontype):
                full_path = directory_path / problemname / solutiontype / filename
                # if solutiontype == "non-plagiarized":
                #     inputs.append(
                #         (open(full_path, 'r', encoding="utf-8").read(), solutiontype + '-' + filename.strip(".py")))
                # else:
                if filename in ["02.py", "03.py"]:
                    continue
                inputs.append(
                    (open(full_path, "r", encoding="utf-8").read(), solutiontype)
                )

        r.make_report(
            f"./AST-expirement-results/{problemname}",
            {"ASTInspections": ["compare_files"]},
            *inputs,
        )


walk_directory(DATASET)
