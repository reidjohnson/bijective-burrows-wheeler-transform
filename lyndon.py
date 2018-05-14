def factor(data):
    """Returns Lyndon factorization of data."""
    words = []
    while len(data) > 0:
        a = 0
        b = 1
        while b < len(data) and data[a] <= data[b]:
            if data[a] == data[b]:
                a += 1
            else:
                a = 0
            b += 1
        l = b - a
        while a >= 0:
            words.append(data[:l])
            data = data[l:]
            a -= l
    return words
