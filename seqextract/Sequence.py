from residues_convert import toSingleLetter


class Sequence:
    @staticmethod
    def find_input_type(data):
        """
        Tries to find the data type in the sequence.
        Various formats are supported.
        Assumes we gave it simply a sequence if no data type is found.
        :return: the data type.
        """
        if data.startswith('>'):
            return "fasta"
        elif data.startswith('HEADER'):
            return "pdb"
        else:
            return "seq"

    @staticmethod
    def find_data_type(data):
        # TODO: guess if it is DNA, RNA if possible OR Residues
        return "residues"

    def load_from_fasta(self, data):
        data = data.split('\n')

        # TODO: better extraction of information from fasta
        self.info = data[0]

        self.seq = "".join(data[1:]).replace('\n', '')

    def load_from_pdb(self, data):
        """
        ref: http://www.bmsc.washington.edu/CrystaLinks/man/pdb/part_35.html
        :param data:
        :return:
        """
        data = data.split('\n')

        i = 0
        while i < len(data):
            if data[i].startswith('SEQRES'):
                break

        j = i
        while j < len(data):
            if not data[j].startswith('SEQRES'):
                break

        for

    def __init__(self, data):
        self.input_type = Sequence.find_input_type(data)
        self.data_type = Sequence.find_data_type(data)
        self.info = ""
        self.seq = ""

        match self.input_type:
            case "fasta":
                self.load_from_fasta(data)
            case "pdb":
                self.load_from_pdb(data)
            case "seq":
                self.seq = data.upper()
