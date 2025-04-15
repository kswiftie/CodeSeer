import tokenize, torch, math
from collections import Counter
from io import BytesIO

from pandas.core.window.doc import template_returns


def get_the_coeff_part(coeff: float | int) -> str:
    """
    The function that gives the color that
    depended on coefficient similarity.

    And returns it in format for html-report.
    """
    if coeff <= 50:
        return f"""<span class="green">{coeff}%</span>"""
    if coeff <= 80:
        return f"""<span class="orange">{coeff}%</span>"""
    return f"""<span class="red">{coeff}%</span>"""


def tokenize_code(code: str) -> tuple[set[str], Counter[str]]:
    """
    The function accepts a string containing python code
    as input and divides it into unique tokens,
    as well as counts the occurrence of each of them.
    Minor tokens (such as line breaks) are not considered.

    Args:
        code: str
            Python code.
    Returns:
        A pair (tuple) - set of tokens and
        Counter which takes into account the
        number of uses of each token in the code.
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


def cosine_between_tensors(tensor1: torch.Tensor, tensor2: torch.Tensor) -> float:
    """
    Represents two tensors as a one-dimensional vector,
    rewriting their values in order in a row,
    and then calculates the cosine of the angle between them.

    This function can apply certain functions
    to the cosine to get a better estimate of the similarity.
    """

    tensor1 = tensor1.flatten()
    tensor2 = tensor2.flatten()

    dot_product = torch.dot(tensor1, tensor2)

    norm1 = torch.norm(tensor1)
    norm2 = torch.norm(tensor2)

    if norm1 == 0 or norm2 == 0:
        raise ValueError("Inputs must be non-empty")

    cosine = dot_product / (norm1 * norm2)

    # similarity = torch.clamp(cosine * (cosine > 0), -1, 1)
    similarity = cosine * (cosine > 0)

    # f = lambda x: x * math.log(x + 1) / math.log(2)  # ITS NOT SO BAD
    # f = lambda x: 1 - (1 - x) ** 0.5  # THATS GOOD
    # f = lambda x: (math.cosh(x) - 1) / (math.cosh(1) - 1)
    return similarity / (len(tensor1) ** 0.5)


def cos_similarity_counter_modififed(
    counter1: Counter[str], counter2: Counter[str]
) -> float:
    """
    Cosine between two vectors of counter.
    Counters are represented as vectors.

    If one is shorter than the other,
    it is padded with zeros on the right.

    Then the cosine of the angle is calculated between them.
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
    norm1 = sum(v**2 for v in vec1) ** 0.5
    norm2 = sum(v**2 for v in vec2) ** 0.5

    # Calculating the angle between the vectors
    # 2 * norm1 * norm2 because coordinates of the vectors are always non-negative
    # so the cosine values are at [0, 1]
    return dot_product / (2 * norm1 * norm2) if norm1 and norm2 else 0


def euclidean_similarity(t1: torch.Tensor, t2: torch.Tensor) -> float:  # In testing
    """
    The Euclidean distance between L2-normalized vectors.

    This function can apply certain functions
    to the distance to get a better estimate of the similarity.
    """
    similarity = 1 - ((sum([(a - b) ** 2 for a, b in zip(t1, t2)]) ** 0.5) / 2)
    # f = lambda x: 1 - (1 - x) ** 0.5
    # f = lambda x: (math.cosh(x) - 1) / (math.cosh(1) - 1)
    return similarity


def get_normalized_embedding(code: str, model, device) -> torch.Tensor:
    """
    Builds embedding based on python code using UnixCoder.
    The result is an L2-normalized vector.
    """
    tokens_ids = model.tokenize([code], mode="<encoder-only>")
    source_ids = torch.Tensor(tokens_ids).to(device)
    _, embedding = model(source_ids)
    return torch.nn.functional.normalize(embedding.flatten(), p=2, dim=0)
