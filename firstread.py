Itch = open("07302019.NASDAQ_ITCH50", "rb")
counts = {} 
n = 0 # We say n = 0 to make n exist for the later comparison
while True:
    prefix = Itch.read(2)
    if len(prefix) < 2: 
        break
    length = int.from_bytes(prefix, "big")
    message = Itch.read(length) 
    if length == 0 or len(message) < length:
        break 
    letter = chr(message[0])
    if letter == "P":
        shares = int.from_bytes(message[20:24], "big")
        stock = message[24:32].decode("ascii").rstrip() 
        price = int.from_bytes(message[32:36], "big")
        print(stock, shares, price)
    counts[letter] = counts.get(letter,0) + 1 
    n = n + 1
    if n >= 1000000:
        break
print(counts) 
