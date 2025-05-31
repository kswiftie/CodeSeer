from utils import create_inputs
from codeseer import RepoHandler, ReportCompiler

# put ur GitHub token into token.txt
my_handler = RepoHandler(open("./token.txt", "r").read())
r = ReportCompiler(my_handler)

name, inputs = create_inputs()

links = ["https://github.com/kswiftie/CodeSeer/tree/main/dataset/add-one-row-to-tree/non-plagiarized",
         "https://github.com/kswiftie/CodeSeer/tree/main/dataset/add-one-row-to-tree/original",
         "https://github.com/kswiftie/CodeSeer/tree/main/dataset/add-one-row-to-tree/plagiarized"]

r.make_report(
    name + "with" + "add-one-row-to-tree",
    {
        "BasicInspections": ["compare_files_with_folders_levenstein"],
        "TokenizationInspections": ["compare_files_with_folders_standart", "compare_files_with_folders_nn"],
        "ASTInspections": ["compare_files_with_folders"],
    },
    inputs, links
)
