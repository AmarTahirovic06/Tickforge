import zlib
def to64(s): return int.from_bytes(s.ljust(8, b' '), 'big')
print(zlib.crc32(to64(b'MU').to_bytes(8,'big')) & 0x1FFFF)
drop = {b'AVEX', b'JHX'}
symbols = [line.strip().encode() for line in open ('top1000.txt')]
symbols = [s for s in symbols if s not in drop]
def to64(syms): 
    return int.from_bytes(syms.ljust(8, b' '), 'big')
table = [0x3FF] * 131072
for n, s in enumerate(symbols): 
    idx = zlib.crc32(to64(s).to_bytes(8, 'big')) & 0x1FFFF
    table[idx] = n
with open('symbol_table.mem', 'w') as f:
    for entry in table: 
        f.write(f"{entry:03x}\n")

