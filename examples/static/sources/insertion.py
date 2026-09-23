def sort_values(values):
    out = list(values)
    for index in range(1, len(out)):
        incoming = out[index]
        position = index - 1
        while position >= 0 and out[position] > incoming:
            out[position + 1] = out[position]
            position -= 1
        out[position + 1] = incoming
    return out
