res = {}

def tribonacci(n):
    if (n == 1) or (n == 0):
        return 0
    if n == 2:
        return 1
    if n in res:
        return res[n]
    ans = tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3)
    res[n] = ans
    return ans

print(tribonacci(0))
print(tribonacci(1))
print(tribonacci(2))
print(tribonacci(6))
print(tribonacci(10))
print(tribonacci(33))