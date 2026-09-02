import gzip
Itch = gzip.open("itch50_05_18.gz", "rb")
counts = {}
last = {}
over = {}
low = 0 
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
    if letter == "P":
        shares = int.from_bytes(message[20:24], "big")
        stock = message[24:32].decode("ascii").rstrip() 
        price = int.from_bytes(message[32:36], "big")
        previous = last.get(stock, None)   
        if previous is not None:
            delta = (price - previous) 
            if 0 < abs(delta) < 4:
                over[stock] = over.get(stock, 0) + 1
                low = low + 1
        last[stock] = price     
    counts[letter] = counts.get(letter,0) + 1 
    n = n + 1
    if n % 10000000 == 0:
        print(n)
print(counts)
print(over) 
print(low)
