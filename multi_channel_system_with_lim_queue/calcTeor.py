from math import *
#Расчет теоретических p и q

lamb = 3
mu = 4
n = 1
m = 4

down1 = 0

for k in range(0, n+1):
	down1 += ((lamb/mu)**k)/factorial(k)
	
down2 = 0

for r in range(1, m+1):
	down2 += ((lamb/mu)**(n+r))/(factorial(n)*n**r)
	
up = ((lamb/mu)**(n+m))/(factorial(n)*n**m)

q = up/(down1+down2)
p = 1 - q
print("q=%.6f"%q)
print("p=%.6f"%p)