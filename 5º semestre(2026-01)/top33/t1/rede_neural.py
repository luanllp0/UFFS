import numpy as np  # numpy para fazer operações com vetores e matrizes em vez de números individuais


def relu(z):  # função ReLU para as camadas escondidas
    return np.maximum(0, z)  # se z for positivo mantém o valor; se for negativo vira 0


def derivada_relu(z):  # derivada da função ReLU
    return (z > 0).astype(float)  # se z > 0 retorna 1; se z <= 0 retorna 0


def softmax(z):  # função softmax para a camada de saída
    z = z - np.max(z, axis=1, keepdims=True)  # subtrai o maior valor de cada linha para evitar números muito grandes
    exp_z = np.exp(z)  # calcula e^z para cada valor da matriz
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)  # divide cada valor pela soma da linha, gerando probabilidades


def calcular_erro(y_real, y_previsto): # calcular erro entre resposta prevista e a correta    
    epsilon = 0.00000001  # evita log(0), que daria erro
    erro = -np.mean(np.sum(y_real * np.log(y_previsto + epsilon), axis=1)) # cross-entropy
    # y_real contem uma classe certa(1) e as demais erradas(0)
    # probabilidade alta na classe certa → erro pequeno // log 0,99 = -0,01
    # probabilidade baixa na classe certa → erro grande // log 0,01 = -4,60
    # o restante das probabilidades são desconsideradas pois o valor da classe errada é 0 (0*n = 0)
    # soma e faz média dos erros
    # quanto menor o resultado, melhor
    
    return erro


class RedeNeural:
    def __init__(self):
        # define uma semente fixa para os números aleatórios serem sempre os mesmos
        np.random.seed(4937)

        # w1, w2, w3 = pesos      b1, b2, b3 = bias

        # imagem de 784 pixels

        # pesos e bias da primeira camada: entrada 784 -> camada escondida 128
        self.W1 = np.random.randn(784, 128) * 0.01 # cria matriz de pesos 784x128, * 0.01 para os pesos começarem pequenos
        self.b1 = np.zeros((1, 128)) # cria um vetor com 128 bias zerados

        # pesos e bias da segunda camada: camada escondida 128 -> camada escondida 64
        self.W2 = np.random.randn(128, 64) * 0.01 # matriz de pesos 128x64
        self.b2 = np.zeros((1, 64)) # vetor de 64 bias

        # pesos e bias da saída: camada escondida 64 -> saída 10
        self.W3 = np.random.randn(64, 10) * 0.01 # matriz de pesos 64x10
        self.b3 = np.zeros((1, 10)) # vetor de 10 bias
        
    def forward(self, X):
        # primeira camada escondida
        self.z1 = np.dot(X, self.W1) + self.b1 # z1 =  x * w1 + b1
        self.a1 = relu(self.z1) # a1 = relu(z1)

        # segunda camada escondida
        self.z2 = np.dot(self.a1, self.W2) + self.b2 # z2 = a1 * w2 + b2
        self.a2 = relu(self.z2) # a2 = relu(z2)

        # camada de saída
        self.z3 = np.dot(self.a2, self.W3) + self.b3 # z3 = a2 * w3 + b3
        self.a3 = softmax(self.z3) # a3 = softmax(z3)

        return self.a3
    
    def backward(self, X, y_real, y_previsto): # calcula a mudança de pesos e de bias
        qtd_exemplos = X.shape[0]  # quantidade de imagens sendo treinadas no momento

        # erro da camada de saída
        dz3 = y_previsto - y_real # calcula o erro da saída
        dW3 = np.dot(self.a2.T, dz3) / qtd_exemplos # calcula a média de ajuste dos pesos w3
        # usa a saída da segunda camada escondida junto com o erro da saída para calcular o ajuste de W3
        db3 = np.sum(dz3, axis=0, keepdims=True) / qtd_exemplos # calcula ajuste de bias da saida
        # soma o erro de cada neurônio da saída para calcular o ajuste dos 10 bias

        # erro da segunda camada escondida
        da2 = np.dot(dz3, self.W3.T) # quanto do erro da saída veio da segunda camada
        # erro da saída * pesos da saída transposta
        dz2 = da2 * derivada_relu(self.z2) # erro só passa pelos neurônios que estavam ativos
        # erro da segunda camada escondida * 1 para neuronios ativos e * 0 para os inativos
        dW2 = np.dot(self.a1.T, dz2) / qtd_exemplos # ajuste dos pesos W2, que ligam a primeira camada escondida à segunda
        db2 = np.sum(dz2, axis=0, keepdims=True) / qtd_exemplos # ajuste de bias

        # erro da primeira camada escondida
        da1 = np.dot(dz2, self.W2.T) # quanto do erro da segunda camada escondida veio da primeira camada
        dz1 = da1 * derivada_relu(self.z1) # erro só passa pelos neurônios que estavam ativos
        dW1 = np.dot(X.T, dz1) / qtd_exemplos # ajuste dos pesos W1, que ligam a entrada à primeira camada escondida
        db1 = np.sum(dz1, axis=0, keepdims=True) / qtd_exemplos # ajuste de bias

        return dW1, db1, dW2, db2, dW3, db3
    
    def atualizar_pesos(self, dW1, db1, dW2, db2, dW3, db3, taxa_aprendizado):
        # taxa_aprendizado controla o tamanho da mudança dos pesos e bias

        # atualiza os pesos e bias da primeira camada
        self.W1 -= taxa_aprendizado * dW1 # peso atual - taxa * ajuste de pesocalculado
        self.b1 -= taxa_aprendizado * db1 # bias atual - taxa * ajuste de bias calculado

        # atualiza os pesos e bias da segunda camada
        self.W2 -= taxa_aprendizado * dW2 # atual - taxa * ajuste
        self.b2 -= taxa_aprendizado * db2 # atual - taxa * ajuste

        # atualiza os pesos e bias da camada de saída
        self.W3 -= taxa_aprendizado * dW3 # atual - taxa * ajuste
        self.b3 -= taxa_aprendizado * db3 # atual - taxa * ajuste

    def treinar(self, X, y, epocas, taxa_aprendizado):
        historico_erro = []  # guarda o erro de cada época para depois fazer gráfico

        for epoca in range(epocas):
            # faz a previsão da rede
            y_previsto = self.forward(X)

            # calcula o erro da previsão
            erro = calcular_erro(y, y_previsto)
            historico_erro.append(erro)

            # calcula os ajustes dos pesos e bias
            dW1, db1, dW2, db2, dW3, db3 = self.backward(X, y, y_previsto)

            # atualiza os pesos e bias usando os ajustes calculados
            self.atualizar_pesos(dW1, db1, dW2, db2, dW3, db3, taxa_aprendizado)

            # mostra o erro a cada 10 épocas
            if epoca % 10 == 0:
                print(f"Época {epoca} - Erro: {erro:.4f}")

        return historico_erro
    
    def prever(self, X):
        # faz o forward para obter as probabilidades da saída
        probabilidades = self.forward(X)

        # pega a posição com maior probabilidade em cada linha
        previsoes = np.argmax(probabilidades, axis=1) # retorna a posição do maior valor (previsão) por linha

        return previsoes