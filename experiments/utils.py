import os, pathlib
from codeseer import RepoHandler
from codeseer.inspections import (
    BasicInspections,
    TokenizationInspections,
    ASTInspections,
)  # This is needed to use globals()

DATASET = pathlib.Path(__file__).parent.parent / "dataset"


def get_inspection_results(
    repo_handler, inspection_class_name: str, inspection_name: str, *inputs
) -> dict[str, float]:
    inspection_class = globals()[inspection_class_name](repo_handler)

    return getattr(inspection_class, inspection_name)(*inputs)


def create_inputs(solutiontype1, solutiontype2) -> list[list[tuple[str, str]]]:
    res = []

    for taskname in os.listdir(DATASET):
        path1 = DATASET / taskname / solutiontype1
        path2 = DATASET / taskname / solutiontype2
        if taskname == "readme.md":
            continue
        cur_inputs = []
        for file in os.listdir(path1):
            cur_inputs.append(
                (
                    open(path1 / file, "r", encoding="utf-8").read(),
                    solutiontype1 + file * (file == "non-plagiarized.py"),
                )
            )
        for file in os.listdir(path2):
            cur_inputs.append(
                (
                    open(path2 / file, "r", encoding="utf-8").read(),
                    solutiontype2 + file * (file == "non-plagiarized.py"),
                )
            )

        res.append(cur_inputs)

    return res
