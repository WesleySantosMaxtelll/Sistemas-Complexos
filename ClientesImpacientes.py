import numpy as np
import random
from statistics import mean
import matplotlib.mlab as mlab
import scipy
from scipy.stats import bernoulli
from math import sqrt
import matplotlib.pyplot as plt


n = 5
taxa_lambda = 3
IT = 50
mi = 0.5


def Simula_Interv_Tempo(n, taxa_lambda, IT, mi):
    tempdisp = [0 for _ in range(n)]
    x, y, k, tm, Tc, ct_cheg, r, w = 0, 0, 0, 0, 0, {}, 0, 0
    z  = np.random.exponential(1/taxa_lambda)
    # print(z)
    while Tc+z <=IT:
        Tc += z
        # print('\nChegou cliente em {}'.format(Tc))
        k+=1
        ct_cheg[k] = Tc
        idxdisp = [i for i in range(len(tempdisp)) if tempdisp[i] <= Tc]
        # print('\tCaixas disponiveis: {}'.format(idxdisp))
        # print("\t\tComprimento da fila: {}".format(r))
        while idxdisp and x<k:
            x +=1
            j = idxdisp.pop(0)
            a = np.random.exponential(1/mi)
            # print('\t\tCliente {} Atendido no Caixa {} com tempo {}'.format(x, j, a))
            # print(ct_cheg)
            # print('j {}, x {}'.format(j, x))
            # print(tempdisp[j])
            tempdisp[j] = max(tempdisp[j], ct_cheg[x]) + a
            # print(ct_cheg[x])
            # print('\t\t\tCaixa estara disponivel em {}'.format(str(tempdisp[j])))
            tm = max(tm, (tempdisp[j] - ct_cheg[x]))
            # print('\tCaixas disponiveis: {}'.format(idxdisp))
        r = max(0, k-x-1)
        pr = r/(r+n)
        s = np.random.binomial(1, pr)
        if s == 1:
            # print('Cliente foi embora')
            k -= 1
            y += 1

        z = np.random.exponential(1/taxa_lambda)
        # print(z)
        r = k - x
        w = y / (x + y + r)

    return x, y, r, w, tm

def calcula_intervalo_confianca(data):
    dp = np.std(data)
    return 1.96*dp/sqrt(len(data))

def Simula_Repeticoes(n, taxa_lambda, IT, mi):
    X, Y, R, W, TM, intervalos, Wp = [], [], [], [0], [], [], []
    N = 100
    no = 0
    i = 0
    while True:
        for _ in range(no, N):
            x, y, r, w, tm  = Simula_Interv_Tempo(n, taxa_lambda, IT, mi)
            # print('x {}\ny {}\nr {}\nw {}\ntm {}'.format(x,y,r,w,tm))
            # exit(0)
            X.append(x)
            Y.append(y)
            R.append(r)
            W.append(w+W[-1])
            Wp.append(w)
            TM.append(tm)
            c = calcula_intervalo_confianca(Wp)
            intervalos.append(c)
        # print(i)
        # print(W)
        if 2*intervalos[-1] < 0.005:
            print(N)
            break

        N+=100
        i+=1

    return X, Y, R, W, TM, N


X, Y, R, Wp, TM, N = Simula_Repeticoes(n, taxa_lambda, IT, mi)

# print([mean(X), mean(Y), mean(W), mean(TM), N])

# Caso eu queira gerar os graficos em png
#grwidth = 700
#grheight = 400
#nmarq = paste('HistX_', n, '_', lambda, '_', th, '.png', sep='')
#png(filename=nmarq, width = grwidth, height = grheight, pointsize = 14)
#par(mai=c(1.2,1.3,1,0.2))
#

# par(mai=c(0.96, 0.82, 0.2, 0.2))
# n, bins, patches = plt.hist(X, 100, facecolor='green', alpha=0.5)
# plt.show()



n, bins, patches = plt.hist(TM, 100, facecolor='red', label='TM', alpha=0.5)
plt.ylabel('TM')
plt.xlabel('k')
plt.show()
n, bins, patches = plt.hist(Wp, 100, facecolor='blue', alpha=0.5)
plt.ylabel('W')
plt.xlabel('k')

plt.show()


iters = range(100, N+1, 100)
qtiter = len(iters)
mw = [0 for _ in range(qtiter)]
upw = [0 for _ in range(qtiter)]
dnw = [0 for _ in range(qtiter)]



for i in range(qtiter):
    Natu = iters[i]
    mw[i] = Wp[Natu]/Natu
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
print('\nA probabilidade de Tm ser maior que 13 é {}%'.format(100*pr))
