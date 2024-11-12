from codeseer import ReportsCompiler

r = ReportsCompiler(user_github_token="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")

report = r.get_report_from_all_inspections(
    "https://api.github.com/repos/kswiftie/CodeSeer/contents",
    "https://api.github.com/repos/kswiftie/CodeSeer/contents",
)

print(report)
