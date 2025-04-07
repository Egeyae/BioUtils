from typing import Sequence, List, Tuple

def _overlap(window: int, overlap: bool) -> int:
    return 1 if overlap else window

def compute_dotplot(seq_a: Sequence, seq_b: Sequence, window: int, overlap: bool) -> Tuple[List[int], List[int]]:
    seq_a = seq_a.get_sequence()
    seq_b = seq_b.get_sequence()
    x, y = [], []

    i = 0
    while i + window <= len(seq_a):
        j = 0
        while j + window <= len(seq_b):
            if seq_a[i:i+window] == seq_b[j:j+window]:
                x.append(i)
                y.append(j)

            j += _overlap(window, overlap)

        i += _overlap(window, overlap)

    return x, y