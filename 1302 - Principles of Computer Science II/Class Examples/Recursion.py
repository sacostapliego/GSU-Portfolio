#Example 1: Factorial
"""
def fac(n):
    #base
    if n ==0:
        return 1
    #recursion
    return n * fac(n-1)

print(fac(4))
"""

#Example 2: Fibonacci
"""
def fib(n):
    #base cases
    if n == 1:
        return 0
    if n == 2:
        return 1
    #recursion
    return fib(n-1) + fib(n-2)

print(fib(4))
"""
#Example 3: Better Fibonacci Recursion
"""
res = {}
def fib(n):
    #base cases
    if n == 1:
        return 0
    if n == 2:
        return 1
    if n in res:
        return res[n]
    #recursion
    ans = fib(n - 1) + fib(n - 2)
    res[n] = ans
    return ans
"""

#Example 4: GCD

def gcd(a, b):
    if a % b == 0:
        return b
    return gcd(b, a % b)

print(gcd(2342,7456))