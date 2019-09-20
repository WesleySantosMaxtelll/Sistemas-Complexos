import numpy as np
import random
from statistics import mean
import matplotlib.mlab as mlab
import scipy
from scipy.stats import bernoulli
from math import sqrt
import matplotlib.pyplot as plt


taxa_lambda = 4
IT = 60
mi = 0.5
N = 10000


def Simula_Interv_Tempo(n, taxa_lambda, IT, mi):
    # Inicializa a lista de atendentes com tamanho n e as demais variáveis utilizadas
    tempdisp = [0 for _ in range(n)]
    x, y, k, tm, Tc, ct_cheg, r, w = 0, 0, 0, 0, 0, {}, 0, 0

    # Gera tempo de chegada do próximo cliente
    z  = np.random.exponential(1/taxa_lambda)

    # Enquanto o próximo cliente chegar dentro do intervalo máximo considerado
    while Tc+z <=IT:
        Tc += z
        k+=1
        ct_cheg[k] = Tc

        # Cria uma lista com os ids dos guiches que podem atender no tempo Tc
        idxdisp = [i for i in range(len(tempdisp)) if tempdisp[i] <= Tc]

        # Enquanto ouverem guiches livres e clientes esperando para serem atendidos
        while idxdisp and x<k:
            x +=1
            # Retira da lista o id do primeiro guiche disponível
            j = idxdisp.pop(0)
            # Gera o tempo que o cliente manterá o guiche ocupado quando começa seu atendimento
            a = np.random.exponential(1/mi)
            # Atualiza o tempo em que o guiche j ficará disponível
            tempdisp[j] = max(tempdisp[j], ct_cheg[x]) + a
            # atualiza o tempo máximo de espera se necessário
            tm = max(tm, (tempdisp[j] - ct_cheg[x]))

        r = max(0, k-x-1)
        pr = r/(r+n)

        # Gera a opçao de o cliente nao esperar na fila (se a fila estiver vazia este valor será
        # invariavelmente zero)
        s = np.random.binomial(1, pr)
        if s == 1:
            k -= 1
            y += 1

        # Gera o intervalo para a chegada do próximo cliente,
        # atualiza o comprimento da fila e a proporçao de clientes que desistiram de esperar
        z = np.random.exponential(1/taxa_lambda)
        r = k - x
        w = y / (x + y + r)

    return x, y, r, w, tm


def Simula_Repeticoes(n, taxa_lambda, IT, mi, N):
    # Inicialização dos vetores
    X, Y, R, W, TM= [], [], [], [], []

    for _ in range(N):
        x, y, r, w, tm  = Simula_Interv_Tempo(n, taxa_lambda, IT, mi)

        # Adiciona a nova iteração
        X.append(x)
        Y.append(y)
        R.append(r)
        W.append(w)
        TM.append(tm)

    return X, Y, R, W, TM


n = 2
while True:
    print('Testando {} simulaçoes com n = {}'.format(N, n))
    X, Y, R, W, TM = Simula_Repeticoes(n, taxa_lambda, IT, mi, N)
    print(sorted(W, reverse=True)[:int(len(W)*0.05)][-1])
    if sorted(W, reverse=True)[:int(len(W)*0.05)][-1] < 0.20:
        print('O melhor valor para n é {}'.format(n))
        exit()
    n +=1