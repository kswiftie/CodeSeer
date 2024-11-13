from codeseer.utils_for_repos import RepoHandler

handler1 = RepoHandler("*your token*")


files = handler1.handle_github_url("https://github.com/kswiftie/CodeSeer")
print(files)
