import math

def shorten(n):
    """Turn stupid long numbers into short numbers and letters!"""
    millnames = ['', 'k', 'M', ' B', ' T']
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])