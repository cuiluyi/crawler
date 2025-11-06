from pathlib import Path
from zh_stats import chinese_character_stats, chinese_word_stats
from en_stats import english_letter_stats, english_word_stats
from utils import process_text_in_parts

# english text analysis
en_file_path = Path("data/en/text.txt")
with open(en_file_path, "r", encoding="utf-8") as f:
    text = f.read()[:10000000]

figure_dir = Path("figures/en")
cumulative_texts = process_text_in_parts(text, n_parts=6)
for text in cumulative_texts:
    save_path = figure_dir / f"{len(text)}"
    save_path.mkdir(parents=True, exist_ok=True)
    letter_entropy = english_letter_stats(text, save_path)
    word_entropy = english_word_stats(text, save_path)

    log_path = save_path / "entropy_log.txt"
    with open(log_path, "w") as f:
        f.write(f"English Text Length: {len(text)}\n")
        f.write(f"English Letter Entropy: {letter_entropy:.4f} bits\n")
        f.write(f"English Word Entropy: {word_entropy:.4f} bits\n")


# chinese text analysis
zh_file_path = Path("data/zh/text.txt")
with open(zh_file_path, "r", encoding="utf-8") as f:
    text = f.read()[:10000000]

figure_dir = Path("figures/zh")
cumulative_texts = process_text_in_parts(text, n_parts=6)
for text in cumulative_texts:
    save_path = figure_dir / f"{len(text)}"
    save_path.mkdir(parents=True, exist_ok=True)
    char_entropy = chinese_character_stats(text, save_path)
    word_entropy = chinese_word_stats(text, save_path)

    log_path = save_path / "entropy_log.txt"
    with open(log_path, "w") as f:
        f.write(f"Chinese Text Length: {len(text)}\n")
        f.write(f"Chinese Character Entropy: {char_entropy:.4f} bits\n")
        f.write(f"Chinese Word Entropy: {word_entropy:.4f} bits\n")