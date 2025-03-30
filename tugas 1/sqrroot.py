import math
N = int(input())
result=math.sqrt(N)

if result.is_integer():
    print(int(result))
else:
    print("Not a perfect square")