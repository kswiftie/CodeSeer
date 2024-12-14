import os

from codeseer import ReportsCompiler
from codeseer.utils_for_repos import RepoHandler

report_compiler = ReportsCompiler(RepoHandler(input())) # input token

for problem_name in os.listdir("dataset"):
    report = report_compiler.get_report_from_inspections(
        "all",
        f"https://github.com/kswiftie/CodeSeer/tree/main/tests/dataset/{problem_name}/orig.py",
        f"https://github.com/kswiftie/CodeSeer/tree/main/tests/dataset/{problem_name}/plag.py")
    print(report)
