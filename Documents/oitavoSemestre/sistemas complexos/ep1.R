

# Simulacao de Sistema de atendimento

rm(list=ls())

n = 6
lambda = 2 # taxa de chegada é de lambda no intervalo estimado
th = 2

IT = 50 # tempo total (em minutos, horas etc.)
N = 20000 # número de simulações realizadas

# Simulacao de uma sequencia de requisicoes no intervalo de 
# tempo especificado
Simula_Interv_Tempo = function(n, th, lambda, IT ) {
  tempdisp = rep(0, n) # t do slide, passo 3
  x=y=0
  Tr = 0 # tempo de chegada da ultima requisicao
  z = rexp(1, lambda) # gera um elemento com taxa de chegada lambda
  
  # geracao de nova requisicao
  while (Tr+z <= IT) { # testa se a requisicao chegou dentro do intervalo considerado
    Tr = Tr+z
    idxdisp = which(tempdisp<=Tr)
    #browser()
    if (length(idxdisp)>0) { # Existe ao menos uma linha disponivel
      lindisp = idxdisp[1]
      tempdisp[lindisp] = Tr+th
      x = x+1
    } else { # Nenhuma linha disponivel; rejeita
      y = y+1
    }
    #print(tempdisp)
    #browser()
    z = rexp(1, lambda)
  }
  return(list(x=x, y=y))
}

Simula_Repeticoes = function(n, th, lambda, IT, N) {
  X = rep(0,N)
  Y = rep(0,N)
  for (i in 1:N) {
    Atendimentos = Simula_Interv_Tempo(n, th, lambda, IT) 
    #browser()
    X[i] = Atendimentos$x
    Y[i] = Atendimentos$y
    if (i%%100==0) print(i)
  }
  return(list(X=X, Y=Y))
}

MC_Atend = Simula_Repeticoes(n, th, lambda, IT, N)

X = MC_Atend$X
Y = MC_Atend$Y
W = Y/(X+Y)
print(c(mean(X), mean(Y), mean(W)))

# Caso eu queira gerar os graficos em png
#grwidth = 700
#grheight = 400
#nmarq = paste('HistX_', n, '_', lambda, '_', th, '.png', sep='')
#png(filename=nmarq, width = grwidth, height = grheight, pointsize = 14)
#par(mai=c(1.2,1.3,1,0.2))

par(mai=c(0.96, 0.82, 0.2, 0.2))
hist(X, 100)
#dev.off()

browser()

hist(Y, 100)
hist(W, 100, main='')

iters = seq(100, N, by=100)
qtiter = length(iters)
mw = rep(0, qtiter)

for (i in 1:qtiter) {
  Natu = iters[i]
  mw[i] = sum(W[1:Natu])/Natu
}

plot(iters, mw, type='l', xlab='k', ylab='E(W)', main='', ylim=c(min(mw)*0.99, max(mw)*1.01))





