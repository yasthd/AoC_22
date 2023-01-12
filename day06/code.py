SAMPLE = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

with open("input") as f:
    RAW = f.read().strip()

def process(signal: str, marker_len: int) -> int:
    for i in range(marker_len, len(signal)):
        window = signal[i-marker_len:i]
        if len(window) == len(set(window)):
            return i

print(process(RAW, 14))

