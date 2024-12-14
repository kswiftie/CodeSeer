from codeseer import ReportsCompiler
from codeseer.utils_for_repos import RepoHandler

github_token = open("../tmp_and_tests/token.txt").read()
r = ReportsCompiler(RepoHandler(user_github_token=github_token))

# report = r.get_report_from_inspections(
#     "all",
#     "https://github.com/kswiftie/CodeSeer/tree/main/codeseer/inspections",
#     "https://github.com/kswiftie/CodeSeer/tree/main/codeseer/inspections",
# )

report = r.get_report_from_inspections(
    "all",
    "link1",
    "link2"
)
print(report)
