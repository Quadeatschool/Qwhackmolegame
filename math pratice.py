# def fun1(n):
#     if n==0:
#         return 5
#     return fun1(n-1) + 3*n

# print(f"{fun1(10)}")

# def fun2(n):
#     if n==0:
#         return 1
#     return n**3 + fun2(n-1)

# print(f"{fun2(10)}")

# def fun3(n):
#     if n==0:
#         return 1
#     if n==1:
#         return 3
#     return fun3(n-1) * fun3(n-2)

# print(f"{fun3(10)}")

# def fun4(n):
#     if n==0:
#         return 1
#     if n==1:
#         return 5
#     return fun4(n-1) + (fun4(n-2)**2)

# print(f"{fun4(10)}")


# for int in range(1,53):
#     print(int)

# ------------------------------------

def gcd(x,y): 
    for n in range(min(x,y),1,-1):
        if x % n == 0 and y % n == 0:
            return n
    return 1


# def lcm(x, y):
#     for n in range(max(x,y), x*y):
#         if n % x == 0 and n % y == 0:
#             return n 
#     return x*y

# def lcm(x, y):
#     for n in range(x*y, max(x,y),-1):
#         if n % x == 0 and n % y == 0:
#             return n 
#     return x*y

def lcm(x, y):
    return (x*y) / gcd(x,y)

# def lcm(x, y):
#     for n in range(min(x,y), max(x,y)+1):
#         if n % x == 0 and n %y == 0:
#             return n 
#     return max(x,y)
    
print(f'{gcd(64, 91)}')

print(f'{lcm(64, 91)}')
