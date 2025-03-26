from seqextract.Sequence import Sequence
import matplotlib.pyplot as plt


def compute_profile(seq, scale, window):
    profile = []

    residues = seq.get_sequence()
    size = len(residues)

    for i in range(size):
        score = 0
        n = 0
        for j in range(-window//2, window//2+1, 1):
            if 0 <= i+j < size:
                score += scale[residues[i+j]]
                n += 1
        profile.append(score/n)
    return profile


def run(data, output_file=None, show=True, scale_values=None, window=3, scale=None):
    seq = Sequence(data, outtype='raw', seqtype='p')

    profile = compute_profile(seq, scale_values, window)

    plt.plot(profile)
    plt.ylabel('Score')
    plt.xlabel('Position')
    plt.title(f"Hydrophobic Profile / {scale=} / {window=} / Sequence = {seq.info}")
    plt.grid(True)

    if output_file:
        plt.savefig(output_file)
    if show:
        plt.show()
