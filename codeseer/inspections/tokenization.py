import tokenize, math
from collections import Counter
from io import BytesIO
from codeseer.utils_for_repos import RepoHandler


class TokenizationInspection:
    def __init__(self, repo_handler: RepoHandler):
        """
        init func

        :param repo_handler:
        """
        self.repo_handler = repo_handler

    def tokenize_code(self, code: str) -> tuple[set[str], Counter[str]]:
        """
        The function accepts a string containing python code
        as input and divides it into unique tokens,
        as well as counts the occurrence of each of them.
        Minor tokens (such as line breaks) are not considered

        :param code:
        :return:
        """

        # Get code format from string to bytes
        code_in_bytes = BytesIO(code.encode("utf-8"))

        tokens = set()
        token_count: Counter[str] = Counter()

        for token in tokenize.tokenize(code_in_bytes.readline):
            if token.type in (tokenize.NAME, tokenize.STRING, tokenize.NUMBER):
                tokens.add(token.string)
                token_count[token.string] += 1

        return tokens, token_count

    def compare_files_content(self, *file_urls) -> float:
        # Stores tokens for each file
        file_tokens: list[set[str]] = []
        # Stores the number of uses of each token by files
        file_counters: list[Counter[str]] = []

        for file_url in file_urls:
            cur_file_tokens, cur_file_counter = self.tokenize_code(
                self.repo_handler.get_file_info(file_url)[0]
            )
            file_tokens.append(cur_file_tokens)
            file_counters.append(cur_file_counter)

        """
        This piece can be used to calculate the Jacquard coefficient.
        But perhaps this does not make sense, because the cosine similarity is already quite accurate.

        tokens_intersection = file_tokens[0]

        for i in range(1, len(file_tokens)):
            tokens_intersection = tokens_intersection.union(file_tokens[i])
        """

        # Now this function works only for 2 files
        return self.cos_similarity(file_counters[0], file_counters[1])

    def cos_similarity(self, counter1: Counter[str], counter2: Counter[str]) -> float:
        """
        At the moment, the function only works for two vectors

        Parametrs
        ---------
        counter1: Counter[str]
            First counter
        counter2: Counter[str]
            Second counter

        Returns
        -------
        Result: float
            The "angle" between the two counters.
            Defined from -1 to 1.
            The closer to 1, the more similar the tokenizations are,
            the closer to -1, the more different they are
        """

        # Set of all tokens
        all_tokens = set(counter1.keys()).union(set(counter2.keys()))

        # For tokens from all associations,
        # we set a value equal to the number of uses by the code of this token
        # If token not in code, the value is 0
        vec1 = [counter1[token] for token in all_tokens]
        vec2 = [counter2[token] for token in all_tokens]

        # Calculating the scalar product of the constructed vectors
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

        # Calculating their norms
        norm1 = math.sqrt(sum(v**2 for v in vec1))
        norm2 = math.sqrt(sum(v**2 for v in vec2))

        # Calculating the angle between the vectors
        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0

    def compare_folders_content(self, *folder_urls) -> float:
        """

        :param folder_urls:
        :return:
        """
        # Stores tokens for each file
        file_tokens: list[set[str]] = []
        # Stores the number of uses of each token by files
        file_counters: list[Counter[str]] = []

        for folder_url in folder_urls:
            folder_code = ""
            for file in self.repo_handler.get_list_of_files_in_folder(folder_url):
                folder_code += self.repo_handler.get_file_info(file["url"])[0]

            cur_file_tokens, cur_file_counter = self.tokenize_code(folder_code)
            file_tokens.append(cur_file_tokens)
            file_counters.append(cur_file_counter)

        # Now this function works only for 2 files
        return self.cos_similarity(file_counters[0], file_counters[1])


class Tokenization_results_handler(TokenizationInspection):
    _AVAILABLE_TOKENIZATION_INSPECTIONS_LIST = [
        "handle_Tokenization_compare_folders_content",
    ]

    def handle_all_inspections_results(self, *repo_urls) -> str:
        res = "Tokenization Inspection Results:\n"
        for inspection in self._AVAILABLE_TOKENIZATION_INSPECTIONS_LIST:
            res += getattr(self, inspection)(*repo_urls) + "\n\n"

        return res

    def handle_Tokenization_compare_files_content(self, *file_urls) -> str:
        cos_ = super().compare_files_content(file_urls[0], file_urls[1])
        return f"These codes converge to {cos_ * 100}%"

    def handle_Tokenization_compare_folders_content(self, *file_urls) -> str:
        cos_ = super().compare_folders_content(file_urls[0], file_urls[1])
        return f"These codes converge to {cos_ * 100}%"
