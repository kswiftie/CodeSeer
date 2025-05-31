from utils import create_inputs
from codeseer import RepoHandler, ReportCompiler

# put ur GitHub token into token.txt
my_handler = RepoHandler(open("./token.txt", "r").read())
r = ReportCompiler(my_handler)

name, inputs = create_inputs()

r.make_report(
    name,
    {
        "BasicInspections": ["compare_files_levenstein"],
        "TokenizationInspections": ["compare_files_standart", "compare_files_nn"],
        "ASTInspections": ["compare_files"],
    },
    *inputs
)
