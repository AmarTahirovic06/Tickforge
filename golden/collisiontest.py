import zlib
from collections import Counter
symbols = [line.strip().encode() for line in open('top1000.txt')]

def to64(syms): 
    return int.from_bytes(syms.ljust(8, b' '), 'big')

def collisions(fn, bits):
    buckets = {}
    for s in symbols: 
        idx = fn(to64(s)) & ((1 << bits) - 1)
        buckets.setdefault(idx, []).append(s)
    clashes = {k: v for k, v in buckets.items() if len(v) > 1}
    return len(clashes), sum(len(v) for v in clashes.values())
def to_stripped(sym):
    return sym.rstrip()
vals = [(s, zlib.crc32(to64(s).to_bytes(8, 'big')) & 0x1FFFF) for s in symbols]
c = Counter(v for _, v in vals)
for s, v in vals: 
    if c[v] > 1:
        print(s,v)
