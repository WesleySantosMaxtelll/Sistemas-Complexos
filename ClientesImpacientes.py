import numpy as np
import random
from statistics import mean
import matplotlib.mlab as mlab
import scipy
from scipy.stats import bernoulli
import matplotlib.pyplot as plt


n = 5
taxa_lambda = 2
IT = 50
mi = 0.5


def Simula_Interv_Tempo(n, taxa_lambda, IT, mi):
    tempdisp = np.zeros(n, dtype=int)
    x, y, k, tm, Tc, fila, ct_cheg = 0, 0, 0, 0, 0, [], {}
    z  = random.expovariate(taxa_lambda)

    while Tc+z <=IT:
        Tc += z
        k+=1
        ct_cheg[k] = Tc
        idxdisp = [i for i in range(len(tempdisp)) if tempdisp[i] <= Tc]
        while idxdisp and x<k:
            x +=1
            j = idxdisp.pop(0)
            a = random.expovariate(mi)
            tempdisp[j] = max(tempdisp[j], ct_cheg[x]) + a
            tm = max(tm, (tempdisp[j] - ct_cheg[x]))

        r = max(0, (k-1)-x)
        pr = r/(r+n)
        s = bernoulli.rvs(pr)
        if s == 1:
            k -= 1
            y += 1

        z = random.expovariate(taxa_lambda)
    r = k - x
    w = y / (x + y + r)

    return x, y, r, w, tm

def calcula_intervalo_confianca(data, confidence=0.98):

    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def Simula_Repeticoes(n, taxa_lambda, IT, mi):
    X, Y, R, W, TM, intervalos = [], [], [], [], [], []
    N = 100
    no = 0
    i = 0
    while True:
        for _ in range(no, N):
            x, y, r, w, tm  = Simula_Interv_Tempo(n, taxa_lambda, IT, mi)
            X.append(x)
            Y.append(y)
            R.append(r)
            W.append(w)
            TM.append(tm)

        print(i)
        intervalo = calcula_intervalo_confianca(W)
        intervalos.append(intervalo)
        if intervalo[2]-intervalo[1] < 0.005:
            print(W)
            break

        N+=100
        i+=1


    return X, Y, R, W, TM, N


X, Y, R, W, TM, N = Simula_Repeticoes(n, taxa_lambda, IT, mi)

# print([mean(X), mean(Y), mean(W), mean(TM), N])

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


iters = range(100, N+1, 10)
qtiter = len(iters)
mw = [0 for _ in range(qtiter)]
upw = [0 for _ in range(qtiter)]
dnw = [0 for _ in range(qtiter)]



for i in range(qtiter):
    Natu = iters[i]
    mw[i] = sum(W[0:Natu+1])/Natu
    # upw[i] = sum(IT[0:Natu + 1]) / Natu
    # dnw[i] = sum(IT[0:Natu + 1]) / Natu


plt.plot(iters, mw)
plt.ylabel('E(W)')
plt.xlabel('k')
plt.show()

print('Médias Finais')
print('\tX: {}'.format(mean(X)))
print('\tY: {}'.format(mean(Y)))
print('\tR: {}'.format(mean(R)))
print('\tTm: {}'.format(mean(TM)))

pr = len([x for x in TM if x >13])/len(TM)
print('\nA probabilidade de Tm ser maior que 13 é {}'.format(pr))