import matplotlib.pyplot as plt
from seqextract import Sequence
from dotplot.utils import compute_dotplot

def run(data_a, data_b, output_file=None, show=True, window=1, overlap=True, seqtype='dna', tol=0.05):
    seq_a = Sequence(data_a, outtype='raw', seqtype=seqtype)
    seq_b = Sequence(data_b, outtype='raw', seqtype=seqtype)
    
    seq_a_str = seq_a.get_sequence()
    seq_b_str = seq_b.get_sequence()
    len_a = len(seq_a_str)
    len_b = len(seq_b_str)

    x, y = compute_dotplot(seq_a, seq_b, window=window, overlap=overlap)

    diag_x = []
    diag_y = []
    noise_x = []
    noise_y = []
    
    for xi, yi in zip(x, y):
        norm_x = xi / len_a
        norm_y = yi / len_b
        if abs(norm_x - norm_y) < tol:
            diag_x.append(xi)
            diag_y.append(yi)
        else:
            noise_x.append(xi)
            noise_y.append(yi)

    plt.figure(figsize=(8, 8))
    
    plt.scatter(diag_x, diag_y, color='black', s=10, label='Diagonal Matches')
    plt.scatter(noise_x, noise_y, color='red', s=10, alpha=0.5, label='Noise')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.title("Dotplot")
    plt.xlabel("Sequence A")
    plt.ylabel("Sequence B")
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300)
    if show:
        plt.show()
