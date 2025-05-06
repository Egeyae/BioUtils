SEPARATOR = '~'
PATH = "./data/scales.txt"
SCALES_FOLDER = "./data/scales/"


def get_all_scales():
    all_scales = {}
    with open(PATH) as f:
        for line in f.readlines():
            line = line.strip().split(SEPARATOR)
            all_scales[line[0]] = {"id": line[0], "name": line[1], "ref": line[2], "desc": line[3]}

    return all_scales

def get_scale_filename(scale_id):
    return SCALES_FOLDER + scale_id + '.scale'

def load_scale(scale_id):
    scale = {}
    with open(SCALES_FOLDER + scale_id + ".scale") as f:
        for line in f.readlines():
            line = line.strip().split(',')
            scale[line[0]] = float(line[1])
    return scale


def get_scale_name(scale_id):
    scales = get_all_scales()
    if scale_id not in scales.keys():
        return 'Unknown Scale'
    return scales[scale_id]["name"]


def get_scale_ids():
    all_scales = get_all_scales()
    ids = list(all_scales.keys())[1:]
    return ids


def show_scales():
    all_scales = get_all_scales()
    sizes = []
    for col in ["id", "name", "ref", "desc"]:
        sizes.append(max([len(x[col]) for x in all_scales.values()]))

    for v in all_scales.values():
        print(
            f"{v['id']:<{sizes[0]}}   | {v['name']:<{sizes[1]}}   | {v['ref']:<{sizes[2]}}   | {v['desc']:<{sizes[3]}}   |")
