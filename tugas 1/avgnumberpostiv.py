n = int(input())
positive_n = []
for i in range(n):
    number = int(input())
    if number >= 0:
        positive_n.append(number)

if len(positive_n) > 0:
    average = sum(positive_n) / len(positive_n)
    print(f"{average:.2f}")
else:
    print("No positive numbers")

    