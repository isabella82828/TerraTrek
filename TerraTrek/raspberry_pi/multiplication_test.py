from time import time as tic
def toc(st):
    return st-tic()

st = tic()
a = 100000000000//2
print(a)
dt = toc(st)
print(dt)

st = tic()
a = 100000000000>>1
print(a)
dt = toc(st)

print(dt)
