import gzip
Itch = gzip.open("itch50_05_18.gz", "rb")
counts = {}
prev = {}
ring = {}
S = {}
S2 = {}
ptr = {}
filled = {}
clamps = 0
N = 128
n = 0  
fires4 = 0
trace = open("trace.txt", "w")
while True:
    prefix = Itch.read(2)
    if len(prefix) < 2: 
        break
    length = int.from_bytes(prefix, "big")
    message = Itch.read(length) 
    if length == 0 or len(message) < length:
        break 
    letter = chr(message[0]) 
    if letter == "P":                                       # Col 4 
        shares = int.from_bytes(message[20:24], "big")
        stock = message[24:32].decode("ascii").rstrip() 
        price = int.from_bytes(message[32:36], "big")
        if stock not in ring: 
            ring[stock] = [0] * 128
            S[stock], S2[stock], ptr[stock], filled[stock] = 0, 0, 0, 0
            prev[stock] = price
            continue 
        delta = (price - prev[stock]) // 4
        if delta > 32767:
            delta = 32767  
            clamps = clamps + 1 
        elif delta < -32768:
            delta = -32768
            clamps = clamps + 1  
        old = ring[stock][ptr[stock]]
        if filled[stock] >= 128:
            diff = 128 * delta - S[stock]  
            deviation = diff ** 2  
            variance = 128 * S2[stock] - S[stock] ** 2
            if variance < 0:
                print("NEGATIVE VARIANCE", stock, n)     
            if diff > 0: 
                direction = "+"
            else: 
                direction = "-"
                decision = 0
            if deviation > 4 ** 2 * variance:
                decision = 1 
                fires4 = fires4 + 1
            trace.write(f"{n},{stock},{decision},{direction}\n")                         
        if delta != 0:      
            S[stock] = S[stock] + delta - old
            S2[stock] = S2[stock] + delta**2 - old**2
            ring[stock][ptr[stock]] = delta
            ptr[stock] = (ptr[stock] + 1) % 128
        prev[stock] = price
        filled[stock] = filled[stock] + 1
    n = n + 1
print(fires4)
print("clamps", clamps)
