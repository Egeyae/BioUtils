import matplotlib.pyplot as plt
from os import system
from hydrophob.utils import compute_profile
from seqextract import Sequence

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