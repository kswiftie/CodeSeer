from codeseer import RepoHandler, ReportCompiler

# put ur GitHub token into token.txt
my_handler = RepoHandler(open("./token.txt", "r").read())
r = ReportCompiler(my_handler)

# put ur links here
links = [
    "https://github.com/kswiftie/CodeSeer/tree/main/dataset/add-one-row-to-tree/non-plagiarized",
    "https://github.com/kswiftie/CodeSeer/tree/main/dataset/add-one-row-to-tree/original",
    "https://github.com/kswiftie/CodeSeer/tree/main/dataset/add-one-row-to-tree/plagiarized",
]

r.make_report(
    "add-one-row-to-tree",
    {
        "BasicInspections": ["compare_folders_levenstein"],
        "TokenizationInspections": ["compare_folders_standart", "compare_folders_nn"],
        "ASTInspections": ["compare_folders"],
    },
    *links
)
