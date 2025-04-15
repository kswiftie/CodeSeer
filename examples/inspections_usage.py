from datasets import load_dataset
from codeseer import RepoHandler, ReportCompiler

ds = load_dataset(
    "HiggsBoson/CodeSemSim", split="train[:200]", cache_dir="./.cache"
)  # U will have to wait till it loads

code1, code2, code3 = "", "", ""

for row in ds["whole_func_string"]:
    code1 += row + "\n\n"

for row in ds["paraphrased_func_code_string"]:
    code2 += row + "\n\n"

for row in ds["perturbed_func_code_string"]:
    code3 += row + "\n\n"

# my_handler = RepoHandler(input()) # input your token here
my_handler = RepoHandler(open("./token.txt", "r").read())
r = ReportCompiler(my_handler)

r.make_report(
    "",
    {
        "BasicInspections": ["compare_files_levenstein"],
        "TokenizationInspections": ["compare_files_standart", "compare_files_nn"],
        "ASTInspections": ["compare_files_hash"],
    },
    (code1, "original"),
    (code2, "plagiarized"),
    (code3, "non-plagiarized"),
)
