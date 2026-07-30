Itch = open("07302019.NASDAQ_ITCH50", "rb")
counts = {}
n = 0
while True:
    prefix = Itch.read(2)
    if len(prefix) < 2: 
        break
    length = int.from_bytes(prefix, "big")
    message = Itch.read(length) 
    if length == 0 or len(message) < length:
        break 
    letter = chr(message[0])
    counts[letter] = counts.get(letter,0) + 1 
    n = n + 1
    if n >= 1000000:
        break
print(counts) 
