from codeseer import ReportsCompiler
from codeseer.utils_for_repos import RepoHandler

r = ReportsCompiler(RepoHandler(user_github_token="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"))

report = r.get_report_from_inspections(
    "all",
    "https://github.com/kswiftie/CodeSeer/tree/main/codeseer/testers",
    "https://github.com/kswiftie/CodeSeer/tree/main/codeseer/testers",
)

print(report)
