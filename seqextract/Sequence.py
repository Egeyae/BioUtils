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

    def load_from_fasta(self, data):
        data = data.split('\n')

        # TODO: better extraction of information from fasta
        self.info = data[0][1:]

        self._sequence = "".join(data[1:]).replace('\n', '')

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
            i += 1

        j = i
        while j < len(data):
            if not data[j].startswith('SEQRES'):
                break
            j += 1

        curr_chainid = data[i][11]
        while i < j:
            if curr_chainid != data[i][11]:
                self._sequence += "/"
                curr_chainid = data[i][11]
            s = data[i][19:]
            s = map(toSingleLetter, s.strip().split())
            self._sequence += "".join(s)
            i += 1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self._sequence

    def save_to_file(self, filepath):
        if self.outtype == "fasta":
            s = f">{self.info}\n{self._sequence}"
        else:
            s = self._sequence
        with open(filepath, "w") as f:
            f.write(s)

    def get_sequence(self):
        return self._sequence

    def __init__(self, data, outtype="raw", seqtype="p"):
        self.info = ""
        self._sequence = ""

        self.input_type = None
        self.data_type = None

        self.outtype = outtype
        if data:
            self.input_type = Sequence.find_input_type(data)
            self.data_type = seqtype

            match self.input_type:
                case "fasta":
                    self.load_from_fasta(data)
                case "pdb":
                    self.load_from_pdb(data)
                case "seq":
                    self._sequence = data.upper().replace("\n", "")
