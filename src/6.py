with open("input.txt", "r") as f:
    input = f.read().splitlines()[0]

def unique(u):
    return len(set(u)) == len(list(u))

for idx in range(len(input)):
    if unique(input[idx:idx+14]):
        print(idx+14)
        break
