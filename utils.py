import math
from collections import Counter


def compute_entropy(probs: dict[str, float]) -> float:
    """
    Compute the Shannon entropy (in bits) from a probability distribution.

    Args:
        probs (dict[str, float]): Probability distribution.

    Returns:
        float: The entropy value.
    """
    entropy = 0.0
    for p in probs.values():
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def compute_probability_distribution(items: list[str]) -> dict[str, float]:
    """
    Compute the empirical probability distribution from a list of items.

    Args:
        items (list[str]): List of items (e.g., characters or words).

    Returns:
        dict[str, float]: Dictionary mapping each unique item to its probability.
    """
    if not items:
        return {}

    counter = Counter(items)
    total_count = sum(counter.values())
    return {item: count / total_count for item, count in counter.items()}


def process_text_in_parts(
    text: str,
    n_parts: int = 6,
):
    """
    Split the text into n_parts roughly equal parts, and create cumulative prefixes.
    Args:
        text (str): The full text to be processed.
        n_parts (int): Number of parts to split the text into.
    Returns:
        list[str]: List of cumulative text prefixes.
    """
    part_length = len(text) // n_parts
    # Split the text into 6 roughly equal parts
    parts = [
        text[i * part_length : (i + 1) * part_length]
        for i in range(n_parts - 1)
    ]
    parts.append(text[(n_parts - 1) * part_length :])  # the last part

    # Create cumulative prefixes
    cumulative_texts = []
    for i in range(1, n_parts + 1):
        cumulative_texts.append("".join(parts[:i]))

    return cumulative_texts
