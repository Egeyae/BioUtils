from seqextract.Sequence import Sequence


def run(data, output_file=None, show=True, scale=None):
    seq = Sequence(data, outtype='raw', seqtype='p')
