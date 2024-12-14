import re


def remove_comments(code: str) -> str:
    # perhaps not very well, because """ may not be used for docstring
    code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", "", code, flags=re.DOTALL)

    code = re.sub(r"#.*", "", code)

    return code.strip()
