i = 0
maximum = float('-inf')  

while i < 3:
    number = int(input())
    if number > maximum:
        maximum = number  
    i += 1

print(maximum)
