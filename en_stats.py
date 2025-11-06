import re
from pathlib import Path

from utils import compute_probability_distribution, compute_entropy
from zipf import plot_freq_rank, plot_probability_distribution


def extract_english_letters(text: str) -> list[str]:
    """
    Extract all English letters (a-z, A-Z) from the input text and convert to lowercase.

    Args:
        text (str): Input text containing English letters.

    Returns:
        list[str]: List of extracted lowercase English letters.
    """
    return re.findall(r"[a-zA-Z]", text.lower())


def segment_english_words(text: str) -> list[str]:
    """
    Segment the input text into English words:
    - Convert to lowercase
    - Split on non-word characters (punctuation, spaces, etc.)
    - Filter words with length >= 2 (ignore single letters and empty)

    Args:
        text (str): Input text.

    Returns:
        list[str]: List of lowercase English words.
    """
    words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    return words


def english_letter_stats(
    text: str,
    save_dir: Path,
) -> float:
    """
    Compute the probability distribution and entropy for English letters in the text.

    Args:
        text (str): Input text.
    Returns:
        float: Entropy of the English letter distribution.
    """
    letters = extract_english_letters(text)
    plot_freq_rank(letters, save_dir / "letter_freq_rank.png")

    probs = compute_probability_distribution(letters)
    plot_probability_distribution(probs, save_dir / "letter_prob_dist.png")

    entropy = compute_entropy(probs)
    return entropy
    # print(f"Letter Entropy: {entropy:.4f} bits")


def english_word_stats(
    text: str,
    save_dir: Path,
) -> float:
    """
    Compute the probability distribution and entropy for English words in the text.

    Args:
        text (str): Input text.
    Returns:
        float: Entropy of the English word distribution.
    """
    words = segment_english_words(text)
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