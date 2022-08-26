# Write a python code to calculate the fatorial of a given number.
arr_fact = [1, 1]
def factorial(x):
    for n in range(2, x + 1):
        arr_fact.append(n*arr_fact[n - 1])
    print(arr_fact[x])

num = int(input("Enter the number whose factorial is to be found: "))
factorial(num)