SEPARATOR = ','
PATH = "./data/residues.csv"

data = []

with open(PATH) as f:
    for line in f.readlines():
        data.append(line.strip().split(SEPARATOR))


def _convert(r, col):
    for l in data:
        if r in l:
            return l[col]



def toSingleLetter(residue):
    return _convert(residue, 1)


def to3Letters(residue):
    return _convert(residue, 0)


def toAllLetters(residue):
    return _convert(residue, 2)
