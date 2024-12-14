import sys
import time
from codeseer.inspections import ASTInspection
from codeseer.utils_for_repos import RepoHandler

sys.setrecursionlimit(2523000)

start = time.time()
github_token = open("../tmp_and_tests/token.txt").read()
r = ASTInspection(RepoHandler(user_github_token=github_token))

report = r.compare_ast_subgraphs_to_isomorphism_for_files2(
    "https://github.com/kswiftie/CodeSeer/blob/main/codeseer/utils_for_repos/repo_handler.py",
    "https://github.com/kswiftie/CodeSeer/blob/main/codeseer/utils_for_repos/repo_handler.py",
)

end = time.time()

print(report)
print()
print(f"Executing time: {end - start}")
