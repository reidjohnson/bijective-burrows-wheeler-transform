import argparse


def decode(data):
    """Implements inverse transformation to Bijective BWT."""
    t = construct_t(data)
    out = [None] * len(data)
    i = len(data) - 1
    for j in range(len(data)):
        if t[j] == -1:
            continue
        k = j
        while t[k] != -1:
            out[i] = data[k]
            i -= 1
            k_temp = t[k]
            t[k] = -1
            k = k_temp
    return ''.join(out)


def construct_t(data):
    t = [0] * len(data)
    counts = [0] * 65536  # Unicode code points
    for _, b in enumerate(data):
        counts[ord(b)] += 1
    cum_counts = [0] * 65536
    for i in range(1, 65536):
        cum_counts[i] = cum_counts[i - 1] + counts[i - 1]
    for i, b in enumerate(data):
        t[i] = cum_counts[ord(b)]
        cum_counts[ord(b)] += 1
    return t


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Decodes strings encoded with the Burrows-Wheeler transform.')
    parser.add_argument('STRING', type=str, help='Decode this string.')
    args = parser.parse_args()

    print(decode(args.STRING))
