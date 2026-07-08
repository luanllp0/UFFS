import os
import struct
from array import array
from os.path import join

import numpy as np
import kagglehub

from rede_neural import RedeNeural


# Dataset MNIST usado no trabalho:
# https://www.kaggle.com/datasets/hojjatk/mnist-dataset
#
# Versão do kagglehub usada:
# kagglehub==0.3.12

# Download latest version
path = kagglehub.dataset_download("hojjatk/mnist-dataset")

print("Path to dataset files:", path)

#
# MNIST Data Loader Class
# https://www.kaggle.com/code/hojjatk/read-mnist-dataset
#
class MnistDataloader(object):
    def __init__(self, training_images_filepath,training_labels_filepath,
                 test_images_filepath, test_labels_filepath):
        self.training_images_filepath = training_images_filepath
        self.training_labels_filepath = training_labels_filepath
        self.test_images_filepath = test_images_filepath
        self.test_labels_filepath = test_labels_filepath
    
    def read_images_labels(self, images_filepath, labels_filepath):        
        labels = []
        with open(labels_filepath, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049, got {}'.format(magic))
            labels = array("B", file.read())        
        
        with open(images_filepath, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051, got {}'.format(magic))
            image_data = array("B", file.read())        
        images = [] 
        for i in range(size):
            img = np.array(image_data[i * rows * cols:(i + 1) * rows * cols])
            img = img.reshape(784)  # transforma a imagem 28x28 em um vetor de 784 posições
            img = img / 255.0 # normaliza valor de pixels de 0 .. 255 para 0 .. 1
            images.append(img)            
        return np.array(images), np.array(labels)  # transforma listas em arrays NumPy para usar na rede neural
    
    def load_data(self):
        x_train, y_train = self.read_images_labels(self.training_images_filepath, self.training_labels_filepath)
        x_test, y_test = self.read_images_labels(self.test_images_filepath, self.test_labels_filepath)
        return (x_train, y_train),(x_test, y_test)       
    
def transformar_one_hot(labels):
    y = np.zeros((labels.size, 10))  # cria matriz com uma linha por label e 10 colunas
    y[np.arange(labels.size), labels] = 1  # coloca 1 na coluna da classe correta
    return y 

def calcular_acuracia(y_real, y_previsto):
    # compara as previsões com as respostas corretas e calcula a média de acertos
    return np.mean(y_real == y_previsto)

# caminhos dos arquivos do dataset
input_path = path

training_images_filepath = join(input_path, "train-images.idx3-ubyte")
training_labels_filepath = join(input_path, "train-labels.idx1-ubyte")
test_images_filepath = join(input_path, "t10k-images.idx3-ubyte")
test_labels_filepath = join(input_path, "t10k-labels.idx1-ubyte")

# carrega o MNIST
mnist_dataloader = MnistDataloader(
    training_images_filepath,
    training_labels_filepath,
    test_images_filepath,
    test_labels_filepath
)

(X_train, y_train), (X_test, y_test) = mnist_dataloader.load_data()

# Prints usados apenas para verificar se os dados foram carregados corretamente
# print("X_train:", X_train.shape)
# print("y_train:", y_train.shape)
# print("X_test:", X_test.shape)
# print("y_test:", y_test.shape)

# transforma os labels para one-hot encoding
# Exemplo: 5 -> [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
y_train_one_hot = transformar_one_hot(y_train)
# y_test_one_hot = transformar_one_hot(y_test)

# Prints usados apenas para verificar se o one-hot encoding foi feito corretamente
# print("y_train_one_hot:", y_train_one_hot.shape)
# print("y_test_one_hot:", y_test_one_hot.shape)

# parâmetros do treinamento
# usa parte do conjunto de treino para reduzir o custo computacional
qtd_treino = 15000

# número de vezes que a rede passa pelo conjunto de treino
epocas = 500

# controla o tamanho dos ajustes feitos nos pesos durante o treinamento
taxa_aprendizado = 0.5

X_train_usado = X_train[:qtd_treino]
y_train_usado = y_train_one_hot[:qtd_treino]
y_train_labels_usado = y_train[:qtd_treino]

# cria a rede neural
rede = RedeNeural()


# treina a rede
historico_erro = rede.treinar(
    X_train_usado,
    y_train_usado,
    epocas=epocas,
    taxa_aprendizado=taxa_aprendizado
)


# avaliação no conjunto usado para treino
previsoes_treino = rede.prever(X_train_usado)
acuracia_treino = calcular_acuracia(y_train_labels_usado, previsoes_treino)


# avaliação no conjunto de teste
previsoes_teste = rede.prever(X_test)
acuracia_teste = calcular_acuracia(y_test, previsoes_teste)


print("\nResultados finais:")
print("Quantidade de imagens usadas no treino:", qtd_treino)
print("Épocas:", epocas)
print("Taxa de aprendizado:", taxa_aprendizado)
print("Acurácia no treino:", acuracia_treino)
print("Acurácia no teste:", acuracia_teste)

pasta_resultados = "resultados"
os.makedirs(pasta_resultados, exist_ok=True)

np.savetxt(os.path.join(pasta_resultados, "historico_erro.csv"), historico_erro, delimiter=",")
np.savetxt(os.path.join(pasta_resultados, "previsoes_teste.csv"), previsoes_teste, delimiter=",", fmt="%d")
np.savetxt(os.path.join(pasta_resultados, "y_teste.csv"), y_test, delimiter=",", fmt="%d")

with open(os.path.join(pasta_resultados, "resultados.txt"), "w") as arquivo:
    arquivo.write(f"Quantidade de imagens usadas no treino: {qtd_treino}\n")
    arquivo.write(f"Épocas: {epocas}\n")
    arquivo.write(f"Taxa de aprendizado: {taxa_aprendizado}\n")
    arquivo.write(f"Acurácia no treino: {acuracia_treino}\n")
    arquivo.write(f"Acurácia no teste: {acuracia_teste}\n")

print("\nArquivos salvos em:", pasta_resultados)
print("historico_erro.csv")
print("previsoes_teste.csv")
print("y_teste.csv")
print("resultados.txt")