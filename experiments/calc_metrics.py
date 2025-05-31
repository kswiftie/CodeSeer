from utils import create_inputs, get_inspection_results
from codeseer import RepoHandler


class CalculateMetrics:
    def __init__(self, repo_handler):
        self.repo_handler = repo_handler
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0

    def calculate_results(
        self, inspection_class_name: str, inspection_name: str, limit: float = 0.8
    ) -> None:
        for inputs in create_inputs("original", "plagiarized"):
            res = list(
                get_inspection_results(
                    self.repo_handler, inspection_class_name, inspection_name, *inputs
                ).values()
            )[0]
            if res > limit:
                self.TP += 1
            else:
                self.FN += 1

        for inputs in create_inputs("original", "non-plagiarized"):
            res = list(
                get_inspection_results(
                    self.repo_handler, inspection_class_name, inspection_name, *inputs
                ).values()
            )[0]
            if res > limit:
                self.FP += 1
            else:
                self.TN += 1

        print(
            f"""
TP = {self.TP}
TN = {self.TN}
FP = {self.FP}
FN = {self.FN}
"""
        )

    def accuracy(self) -> float:
        return (self.TP + self.TN) / (self.TP + self.FN + self.TN + self.FP)

    def recall(self) -> float:
        return self.TP / (self.TP + self.FN)

    def precision(self) -> float:
        return self.TP / (self.TP + self.FP)

    def F(self) -> float:
        return 2 * (
            (self.precision() * self.recall()) / (self.precision() + self.recall())
        )


if __name__ == "__main__":
    my_handler = RepoHandler(open("./token.txt", "r").read())
    calculator = CalculateMetrics(my_handler)
    # calculator.calculate_results("TokenizationInspections", "compare_files_standart", 0.8)
    calculator.calculate_results("TokenizationInspections", "compare_files_nn", 0.8)
    # calculator.calculate_results("ASTInspections", "compare_files", 0.6)
    print(f"Accuracy: {calculator.accuracy()}")
    print(f"Recall: {calculator.recall()}")
    print(f"Precision: {calculator.precision()}")
    print(f"F: {calculator.F()}")
