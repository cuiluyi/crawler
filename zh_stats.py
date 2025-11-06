import re
from pathlib import Path

import jieba

from utils import compute_probability_distribution, compute_entropy
from zipf import plot_freq_rank, plot_probability_distribution


def extract_chinese_characters(text: str) -> list[str]:
    """
    Extract all Chinese characters (Unicode range U+4E00 to U+9FFF) from the input text.

    Args:
        text (str): Input text containing Chinese characters.

    Returns:
        list[str]: List of extracted Chinese characters.
    """
    return re.findall(r"[\u4e00-\u9fff]", text)


def chinese_character_stats(
    text: str,
    save_dir: Path,
) -> float:
    """
    Compute the probability distribution and entropy for Chinese characters in the text.

    Args:
        text (str): Input text.
    Returns:
        float: Entropy of the Chinese character distribution.
    """
    chars = extract_chinese_characters(text)
    plot_freq_rank(chars, save_dir / "char_freq_rank.png")

    probs = compute_probability_distribution(chars)
    plot_probability_distribution(
        probs,
        save_dir / "char_prob_dist.png",
        top_k=30,
    )

    entropy = compute_entropy(probs)
    return entropy
    # print(f"Character Entropy: {entropy:.4f} bits")


def chinese_word_stats(
    text: str,
    save_dir: Path,
) -> float:
    """
    Compute the probability distribution and entropy for Chinese words using Jieba tokenizer.

    Args:
        text (str): Input text.
    Returns:
        float: Entropy of the Chinese word distribution.
    """
    words = [w for w in jieba.lcut(text) if re.search(r'[\u4e00-\u9fff]', w)]
    plot_freq_rank(words, save_dir / "word_freq_rank.png")

    probs = compute_probability_distribution(words)
    plot_probability_distribution(
        probs,
        save_dir / "word_prob_dist.png",
        top_k=30,
    )

    entropy = compute_entropy(probs)
    return entropy
    # print(f"Word Entropy: {entropy:.4f} bits")
