import functools, ast, re


def remove_comments(code: str) -> str:
    """
    Removes comments from the code,
    including docstring and all that goes after this -
    if __name__ == "__main__":

    Args:
        code:
            Python code.
    Returns:
        Cleared python code.
    """

    def dfs(node):
        """
        Modified dfs with removal of nodes corresponding to comments.
        It is using module ast.
        """
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant) and isinstance(
                    node.value.value, str
            ):
                return None

        for child in ast.iter_child_nodes(node):
            result = dfs(child)
            if result is None:
                node.body = [stmt for stmt in node.body if stmt != child]

        return node

    tree = ast.parse(code)

    dfs(tree)

    result_code = ast.unparse(tree)
    if "if __name__ == '__main__':" in result_code:
        return result_code[: result_code.index("if __name__ == '__main__':")]

    if """if __name__ == "__main__":""" in result_code:
        return result_code[: result_code.index("""if __name__ == "__main__":""")]

    return result_code


def api_to_github_url(api_request: str) -> str:
    """
    The function translates the API request to GitHub into a link to GitHub

    Args:
        api_request:
            Api request to GitHub

    Returns:
        string - the link on GitHub
    """

    pattern = r"https://api\.github\.com/repos/([^/]+)/([^/]+)/contents/(.*)"

    match = re.match(pattern, api_request)
    if match is None:
        raise ValueError("Invalid API request passed to the function")

    owner = match.group(1)
    repo = match.group(2)
    path = match.group(3)

    github_url = f"https://github.com/{owner}/{repo}/blob/main/{path}"
    return github_url


def get_the_name_of_link(link: str) -> str:
    """
    Makes the link a little more readable
    and returns it as a part of the html-report.
    """
    processed_link = link.lstrip("https://api.github.com/repos/").rstrip("?ref=main")
    return f"""<a href="{api_to_github_url(link)}" class="link">{processed_link}</a>"""


def get_the_color_for_the_name(name: str) -> str:
    """Returns the file name inside the html report"""
    return f"""<span class="grey">{name}</span>"""


def inputs_preprocessing1(func):
    """
    It is used for the following checks:
    - Comparisons between folders,
    - Comparisons between folders.

    The verification function can accept different input data, namely:
    - str -- GitHub link
    - str -- str variable with the code in it
    - tuple -- str variable with the code in it and name for it
    - tuple -- GitHub link with name for it

    This decorator converts all input data to a single format -
    tuple: (link | code, name)
    """

    @functools.wraps(func)
    def wrapper(self, *inputs):
        processed_inputs = []
        codes_number = 1
        for inp in inputs:
            if isinstance(inp, str):
                if "https" in inp:
                    processed_inputs.append((inp, get_the_name_of_link(inp)))
                    continue
                processed_inputs.append(
                    (
                        remove_comments(inp),
                        get_the_color_for_the_name(f"InputtedCode{codes_number}"),
                    )
                )
                codes_number += 1
                continue

            if "https" in inp[0]:
                processed_inputs.append((inp[0], get_the_color_for_the_name(inp[1])))
                continue
            processed_inputs.append(
                (remove_comments(inp[0]), get_the_color_for_the_name(inp[1]))
            )
        return func(self, *processed_inputs)

    return wrapper


def inputs_preprocessing2(func):
    """
    It is used for the following checks:
    - Comparisons between files and folders.

    The verification function can accept different input data, namely:
    - str -- GitHub link
    - str -- str variable with the code in it
    - tuple -- str variable with the code in it and name for it
    - tuple -- GitHub link with name for it

    This decorator converts all input data to a single format -
    tuple: (link | code, name)
    """

    @functools.wraps(func)
    def wrapper(self, file_inputs, folder_inputs):
        processed_file_inputs = []
        codes_number = 1
        for inp in file_inputs:
            if isinstance(inp, str):
                if "https" in inp:
                    processed_file_inputs.append((inp, get_the_name_of_link(inp)))
                    continue
                processed_file_inputs.append(
                    (
                        remove_comments(inp),
                        get_the_color_for_the_name(f"InputtedCode{codes_number}"),
                    )
                )
                codes_number += 1
                continue

            if "https" in inp[0]:
                processed_file_inputs.append(
                    (inp[0], get_the_color_for_the_name(inp[1]))
                )
                continue
            processed_file_inputs.append(
                (remove_comments(inp[0]), get_the_color_for_the_name(inp[1]))
            )

        processed_folder_inputs = []
        for inp in folder_inputs:
            if isinstance(inp, str):
                processed_folder_inputs.append((inp, get_the_name_of_link(inp)))
                continue

            processed_folder_inputs.append((inp[0], get_the_color_for_the_name(inp[1])))

        return func(self, processed_file_inputs, processed_folder_inputs)

    return wrapper
