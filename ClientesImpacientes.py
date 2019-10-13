import numpy as np
from statistics import mean
from math import sqrt
import matplotlib.pyplot as plt

n = 5
taxa_lambda = 3
IT = 50
mi = 0.5


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

def calcula_intervalo_confianca(data):
    dp = np.std(data)
    return 1.96*dp/sqrt(len(data))

def Simula_Repeticoes(n, taxa_lambda, IT, mi):
    # Inicialização dos vetores
    X, Y, R, W, TM, ic_w, ic_tm = [], [], [], [], [], [], []

    # valor de N inicial
    N = 100
    # variável de iteração
    no = 0

    while True:
        # Calcula 100 vezes a cada rodada
        print(N)
        while no < N:
            no+=1
            x, y, r, w, tm  = Simula_Interv_Tempo(n, taxa_lambda, IT, mi)

            # Adiciona a nova iteração
            X.append(x)
            Y.append(y)
            R.append(r)
            W.append(w)
            TM.append(tm)
            c = calcula_intervalo_confianca(W)
            ic_w.append(c)
            c = calcula_intervalo_confianca(TM)
            ic_tm.append(c)

        # Verifica se a amplitude do último dado calculado é menor do que a restrição de 0.005
        # print(2*ic_w[-1])
        if 2*ic_w[-1] < 0.005:
            break

        # Incrementa em 100 para a próxima iteração
        N+=100

    return X, Y, R, W, TM, N, ic_w, ic_tm


X, Y, R, W, TM, N, ic_w, ic_tm = Simula_Repeticoes(n, taxa_lambda, IT, mi)



plt.hist(TM, 100, facecolor='red', label='TM', alpha=0.5)
plt.title('Histograma de TM')
plt.ylabel('TM')
plt.xlabel('k')
plt.show()


plt.hist(W, 100, facecolor='blue', alpha=0.5)
plt.title('Histograma de W')
plt.ylabel('W')
plt.xlabel('k')
plt.show()


# Gráfico de linha para W
iters = range(100, N)
qtiter = len(iters)

mw = [] # media acumulada de w
mu = [] # intervalo de confiança superior
md = [] # intervalo de confiança inferior

for i in range(qtiter):
    mw.append(sum(W[0:i+1])/(i+1))

for i, j in zip(mw, ic_w):
    mu.append(i+j)
    md.append(i-j)

plt.title('Gráfico de linha de W em funçao de K')
plt.plot(iters, mw, color='black')
plt.plot(iters, mu, '--', color='gray')
plt.plot(iters, md, '--', color='gray')
plt.ylabel('E(W)')
plt.xlabel('k')
# plt.ylim(md[-1]-0.1, mu[-1]+0.1)
plt.show()


# Gráfico de linha para TM

iters = range(100, N)
qtiter = len(iters)

mTm = [] # media acumulada de tm
mu = [] # intervalo de confiança superior
md = [] # intervalo de confiança inferior

for i in range(qtiter):
    mTm.append(sum(TM[0:i+1])/(i+1))

for i, j in zip(mTm, ic_tm):
    mu.append(i+j)
    md.append(i-j)

plt.title('Gráfico de linha de TM em funçao de K')
plt.plot(iters, mTm, color='black')
plt.plot(iters, mu, '--', color='gray')
plt.plot(iters, md, '--', color='gray')
plt.ylabel('E(TM)')
plt.xlabel('k')
# plt.ylim(10,13)
plt.show()



print('Médias Finais')
print('\tX: {}'.format(mean(X)))
print('\tY: {}'.format(mean(Y)))
print('\tR: {}'.format(mean(R)))
print('\tTm: {}'.format(mean(TM)))

pr = len([x for x in TM if x >13])/len(TM)
print('\nA probabilidade de Tm ser maior que 13 é {}%'.format(round(100*pr, 2)))


# Ordena W de forma decrescente, pegando os 5% maiores elementos,
# ws será o menor elemento dos 5% maiores.
ws = sorted(W, reverse=True)[:int(len(W)*0.05)][-1]

print('O valor de Ws para que p(W > Ws) < 5% é {}'.format(round(ws, 2)))