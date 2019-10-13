import numpy as np
import random
from statistics import mean
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

n = 5
taxa_lambda = 2
th = 2

IT = 50
N = 100000


def Simula_Interv_Tempo(n, th, taxa_lambda, IT ):
    tempdisp = np.zeros(n, dtype=int)
    x, y, Tr = 0, 0, 0
    z  = random.expovariate(taxa_lambda)

    while Tr+z <=IT:
        Tr = Tr + z
        idxdisp = [i for i in range(len(tempdisp)) if tempdisp[i] <= Tr]
        if len(idxdisp) > 0:
            lindisp = idxdisp[0]
            tempdisp[lindisp] = Tr + th
            x += 1
        else:
            y+=1

        z = random.expovariate(taxa_lambda)

    return x, y



def Simula_Repeticoes(n, th, taxa_lambda, IT, N):
    X = [0 for _ in range(N)]
    Y = [0 for _ in range(N)]

    for i in range(N):
        X[i], Y[i]  = Simula_Interv_Tempo(n, th, taxa_lambda, IT)

        if i%100==0:
            print(i)

    return X, Y


X, Y = Simula_Repeticoes(n, th, taxa_lambda, IT, N)

W = []
print(len(X))
for x, y in zip(X, Y):
    W.append(y/(x+y))
# print(Y)
# W = Y/(X+Y)

print([mean(X), mean(Y), mean(W)])

# Caso eu queira gerar os graficos em png
#grwidth = 700
#grheight = 400
#nmarq = paste('HistX_', n, '_', lambda, '_', th, '.png', sep='')
#png(filename=nmarq, width = grwidth, height = grheight, pointsize = 14)
#par(mai=c(1.2,1.3,1,0.2))
#

# par(mai=c(0.96, 0.82, 0.2, 0.2))
n, bins, patches = plt.hist(X, 100, facecolor='green', alpha=0.5)
plt.show()



n, bins, patches = plt.hist(Y, 100, facecolor='red', alpha=0.5)
plt.show()
n, bins, patches = plt.hist(W, 100, facecolor='blue', alpha=0.5)
plt.show()


iters = range(100, N+1, 100)
qtiter = len(iters)
mw = [0 for _ in range(qtiter)]

for i in range(qtiter):
    Natu = iters[i]
    mw[i] = sum(W[0:Natu+1])/Natu


plt.plot(iters, mw)
plt.ylabel('E(W)')
plt.xlabel('k')
plt.show()

