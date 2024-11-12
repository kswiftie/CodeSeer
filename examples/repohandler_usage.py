from codeseer.utils_for_repos import RepoHandler

handler1 = RepoHandler("*your token*")

files = handler1.get_list_of_files_in_folder(
    "https://api.github.com/repos/kswiftie/CodeSeer/contents/"
)
print(*files, sep="\n")
