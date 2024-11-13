from codeseer.inspections import Identity_results_handler
from codeseer.utils_for_repos import RepoHandler

f = Identity_results_handler(RepoHandler("*your_token*"))

print(f.handle_all_inspections_results())
