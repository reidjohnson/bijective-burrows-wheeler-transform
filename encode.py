import argparse

from lyndon import factor
from sa import suffix_array_ManberMyers


class Rot():
    def __init__(self, w, r):
        self.w = w  # index of Lyndon word
        self.r = r  # rotation of Lyndon word


def encode(data):
    """Implements Bijective Burrows-Wheeler Transform."""
    out = []
    factors = factor(data)
    rots = []
    for i, w in enumerate(factors):
        r = [None] * len(w)
        for j in range(len(w)):
            r[j] = Rot(i, j)
        rots.append(r)
    s_rot = sort_rot(factors, rots)
    out = [None] * len(data)
    for i, r in enumerate(s_rot):
        ri = r.r - 1
        if ri < 0:
            ri += len(factors[r.w])
        out[i] = factors[r.w][ri]
    return ''.join(out)


def less_rot(factors, i, j):
    wi = i.w
    ri = i.r
    li = len(factors[wi])
    wj = j.w
    rj = j.r
    lj = len(factors[wj])
    for k in range(li * lj):
        if factors[wi][ri] < factors[wj][rj]:
            return True
        elif factors[wi][ri] > factors[wj][rj]:
            return False
        ri += 1
        rj += 1
        if ri == li:
            ri = 0
        if rj == lj:
            rj = 0
    return False


def sort_factor(factors, rots):
    sa = suffix_array_ManberMyers(factors[rots[0].w])
    for i, s in enumerate(sa):
        rots[i].r = s


def sort_rot(factors, rots):
    word_count = 0
    for _, r in enumerate(rots):
        word_count += 1
        sort_factor(factors, r)
    return merge_rots(factors, rots)


def merge_rots(factors, rots):
    merged = []
    while len(rots) > 0:
        merged = merge_rot(factors, merged, rots[0])
        rots = rots[1:]
    return merged


def merge_rot(factors, a, b):
    la = len(a)
    lb = len(b)
    length = la + lb
    out = [None] * length
    i = 0
    j = 0
    k = 0
    while i < la and j < lb:
        if less_rot(factors, b[j], a[i]):
            out[k] = b[j]
            j += 1
        else:
            out[k] = a[i]
            i += 1
        k += 1

    if i < la:
        out[k:] = a[i:]
    elif j < lb:
        out[k:] = b[j:]
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Encodes strings using the Burrows-Wheeler transform.')
    parser.add_argument('STRING', type=str, help='Encode this string.')
    args = parser.parse_args()

    print(encode(args.STRING))
