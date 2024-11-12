from codeseer import ReportsCompiler

r = ReportsCompiler(user_github_token="")

report = r.get_report_from_all_inspections(
    "https://api.github.com/repos/kswiftie/CodeSeer/contents",
    "https://api.github.com/repos/kswiftie/CodeSeer/contents",
)

print(report)
