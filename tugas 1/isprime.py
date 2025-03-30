import math
N = int(input())
is_prime = False

if N <= 1:
    is_prime = False

else:
    is_prime = True
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            is_prime = False
            break

if is_prime:
    print("Prime")

else:
    print("Not Prime")