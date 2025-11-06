from collections import Counter
from typing import List, Optional, Dict

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号


def plot_freq_rank(
    items: List[str],
    save_path: Optional[str] = None,
    top_k: Optional[int] = None,
    figsize: tuple = (8, 10),
):
    """
    Plot frequency vs rank and log-log (log(rank) vs log(freq)) in one figure.

    Args:
        items: list of tokens (words or characters).
        top_k: if provided, plot only the top_k most frequent items.
        figsize: figure size (width, height).
        save_path: if provided, save the figure to this path (e.g., 'freq_rank.png').
    """
    # Count frequencies
    counter = Counter(items)
    # Sort by frequency descending
    sorted_pairs = counter.most_common()
    if top_k is not None:
        sorted_pairs = sorted_pairs[:top_k]

    freqs = np.array([p for _, p in sorted_pairs], dtype=np.float64)
    # ranks starting from 1
    ranks = np.arange(1, len(freqs) + 1, dtype=np.float64)

    # Prepare log values; avoid log(0) by filtering zeros
    nonzero_mask = freqs > 0
    log_ranks = np.log10(ranks[nonzero_mask])
    log_freqs = np.log10(freqs[nonzero_mask])

    # Create figure with two stacked subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

    # Linear-scale plot: rank vs freq
    ax1.plot(ranks, freqs, marker="o", linestyle="-", linewidth=1, markersize=3)
    ax1.set_xlabel("rank (r)")
    ax1.set_ylabel("frequency (f)")
    ax1.set_title("Frequency vs Rank")
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)

    # Log-log plot: log(rank) vs log(freq)
    ax2.plot(
        log_ranks,
        log_freqs,
        marker="o",
        linestyle="-",
        linewidth=1,
        markersize=3,
    )
    ax2.set_xlabel("log10(rank)")
    ax2.set_ylabel("log10(frequency)")
    ax2.set_title("Log-Log: log10(f) vs log10(r)")
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        # Close the figure to release memory and avoid too many open figures
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def plot_probability_distribution(
    prob_dict: Dict[str, float],
    save_path: Optional[str] = None,
    top_k: Optional[int] = None,
    figsize: tuple = (10, 6),
):
    """
    Plot a probability distribution bar chart.

    Args:
        prob_dict: A dictionary mapping each unique item to its probability (0 <= p <= 1).
        top_k: If provided, plot only the top_k items with highest probabilities.
        figsize: Figure size (width, height).
        save_path: If provided, save the figure to this path (e.g., 'prob_dist.png').
    """
    # Sort items by probability descending
    sorted_items = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
    if top_k is not None:
        sorted_items = sorted_items[:top_k]

    labels = [k for k, _ in sorted_items]
    probs = [v for _, v in sorted_items]

    # Create bar chart and get the figure object so we can close it later
    fig = plt.figure(figsize=figsize)
    plt.bar(range(len(probs)), probs, color="skyblue", edgecolor="black")

    # Set axis labels and title
    plt.xlabel("Items (sorted by probability)")
    plt.ylabel("Probability")
    plt.title("Probability Distribution")

    # Set x-axis tick labels (rotate if many)
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")

    # Add grid lines for readability
    plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    # Save figure if requested and close to free memory; otherwise show then close
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)
