from seqextract.Sequence import Sequence


def _overlap(window: int, overlap: bool):
    return window if overlap else 1

def compute_dotplot(seq_a: Sequence, seq_b: Sequence, window: int, overlap: bool) -> ([int], [int]):
    seq_a = seq_a.get_sequence()
    seq_b = seq_b.get_sequence()

    i = 0

    x, y = list(), list()

    while i < len(seq_a):
        j = 0
        while j < len(seq_b):
            if seq_a[i:i+window] == seq_b[j:j+window]:
                x.extend([k for k in range(i, i+window)])
                y.extend([k for k in range(j, j+window)])
            j += _overlap(window, overlap)
        i += _overlap(window, overlap)

    return x, y