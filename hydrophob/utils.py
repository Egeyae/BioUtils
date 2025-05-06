def compute_profile(seq, scale, window):
    profile = [None for _ in range(window//2)]
    residues = seq.get_sequence()
    size = len(residues)
    # print(window, scale, len(seq.get_sequence()), seq.get_sequence())
    for i in range(window//2, size-window//2):
        score = 0
        for j in range(-window//2, window//2, 1):
            # print("\t", scale.get(residues[i+j], 0))
            score += scale.get(residues[i+j], 0)
        profile.append(score / window)
        # print(score/window)

    profile.extend([None for _ in range(window//2)])
    return profile