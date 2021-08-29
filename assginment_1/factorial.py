print("factorial of number)-")

n=int(input("Enter number : "))
factorial=1
for item in range(1,n+1):
    factorial=factorial*item
print("{}! is {}".format(n,factorial))