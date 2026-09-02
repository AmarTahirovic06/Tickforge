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
wraps_S = 0
wraps_S2 = 0
def wrap_signed (value, bits):
    masked = value & ((1 << bits) - 1) 
    if masked >= 1 << (bits -1):
        masked = masked - (1 << bits) 
    return masked 
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
    if letter == "P":
        shares = int.from_bytes(message[20:24], "big")
        stock = message[24:32].decode("ascii").rstrip()
        price = int.from_bytes(message[32:36], "big")

        # First sighting of this symbol: initialise its state and record
        # the price. No delta exists yet, so skip the rest.
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

        # The value leaving the window. Read before the write overwrites it,
        # because the O(1) update needs it: S += new - old.
        old = ring[stock][ptr[stock]]

        
        if filled[stock] >= 128:
            
            diff = 128 * delta - S[stock]
            deviation = diff ** 2

            # Cauchy-Schwarz guarantees this is never negative.
            # If it fires, it's an overflow or stale-entry bug, not data.
            variance = 128 * S2[stock] - S[stock] ** 2
            if variance < 0:
                print("NEGATIVE VARIANCE", stock, n)

            # Direction from the sign of diff, before the square destroys it.
            # One flip-flop in hardware.
            if diff > 0:
                direction = "+"
            else:
                direction = "-"

            # k = 4. Measured fire rate 0.21% excluding zero-deltas --
            # selective enough to be a signal, frequent enough for a
            # meaningful Phase 4 latency histogram.
            decision = 0
            if deviation > 4 ** 2 * variance:
                decision = 1
                fires4 = fires4 + 1

            trace.write(f"{n},{stock},{decision},{direction}\n")
        if delta != 0:
            raw = S[stock] + delta - old
            S[stock] = wrap_signed(raw, 23)
            if S[stock] != raw:
                wraps_S = wraps_S + 1
            raw = S2[stock] + delta**2 - old**2
            S2[stock] = wrap_signed(raw, 39)
            if S2[stock] != raw:
                wraps_S2 = wraps_S2 + 1
            ring[stock][ptr[stock]] = delta
            ptr[stock] = (ptr[stock] + 1) % 128
            filled[stock] = filled[stock] + 1

        # Outside the zero-delta gate: prev tracks price on every trade,
        # regardless of whether the delta was zero or clamped.
        prev[stock] = price

    # Counts all messages, not just trades.             # K = 4 15,755
    n = n + 1
print("wraps_S", wraps_S)
print("wraps_S2", wraps_S2)
print(fires4)
print("clamps", clamps)
trace.close()                                   