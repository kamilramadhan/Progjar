N = int(input().strip())
keyval = {}

for _ in range(N):
    key, val = input().split()
    keyval[key] = int(val)

K = input().strip()
print(keyval[K])