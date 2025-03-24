from seqextract.Sequence import Sequence

def run(data, output_file, output_type, noprint=False):
    seq = Sequence(data, outtype=output_type)
    if output_file:
        seq.save_to_file(output_file)

    if not noprint:
        print(seq)
