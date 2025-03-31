def compute_profile(seq, scale, window):
    profile = []
    residues = seq.get_sequence()
    size = len(residues)
    for i in range(size):
        score = 0
        n = 0
        for j in range(-window//2, window//2+1, 1):
            if 0 <= i+j < size:
                score += scale.get(residues[i+j], 0)
                n += 1
        profile.append(score / n if n > 0 else 0)
    return profile