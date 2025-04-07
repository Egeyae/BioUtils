import matplotlib.pyplot as plt
# from os import system
from seqextract import Sequence
from dotplot.utils import compute_dotplot

def run(data_a, data_b, output_file=None, show=True, window=1, overlap=True, seqtype='dna'):
    seq_a = Sequence(data_a, outtype='raw', seqtype=seqtype)
    seq_b = Sequence(data_b, outtype='raw', seqtype=seqtype)

    x, y = compute_dotplot(seq_a, seq_b, window=window, overlap=overlap)

    plt.plot(x, y)

    if output_file:
        plt.savefig(output_file)
    if show:
        plt.show()

# def gui():
    #    system("PYTHONPATH=$(pwd) streamlit run hydrophob/interface.py")