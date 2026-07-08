import torch
import torch.nn as nn
import collections
import os
import kagglehub
from rede_neural import LSTManual

device = torch.device('cpu')

def carregar_dados(caminho):
    # abre o arquivo e le tudo
    with open(caminho, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    # troca quebra de linha por eos e divide as palavras
    palavras = texto.replace('\n', '<eos>').split()
    return palavras

def criar_vocabulario(palavras):
    # conta as palavras
    contador = collections.Counter(palavras)
    
    # ordena as que mais aparecem
    palavras_unicas = sorted(contador.keys(), key=contador.get, reverse=True)
    
    # dicionario pra numero e vice versa
    word2id = {palavra: i for i, palavra in enumerate(palavras_unicas)}
    id2word = {i: palavra for palavra, i in word2id.items()}
    
    return word2id, id2word

def texto_para_tensor(palavras, word2id):
    # transforma as palavras em ids
    ids = [word2id[p] for p in palavras]
    return torch.tensor(ids, dtype=torch.long, device=device)

def criar_lotes(dados, tamanho_lote, tamanho_seq):
    # calcula os lotes inteiros
    qtd_lotes = dados.size(0) // (tamanho_lote * tamanho_seq)
    
    # tira a sobra do final
    dados = dados[:qtd_lotes * tamanho_lote * tamanho_seq]
    dados = dados.view(tamanho_lote, -1)
    
    lotes = []
    # pega as sequencias e o alvo deslocado
    for i in range(0, dados.size(1) - tamanho_seq, tamanho_seq):
        x = dados[:, i : i + tamanho_seq]
        y = dados[:, i + 1 : i + tamanho_seq + 1] 
        lotes.append((x, y))
        
    return lotes

if __name__ == '__main__':
    caminho_base = kagglehub.dataset_download("aliakay8/penn-treebank-dataset")
    caminho = os.path.join(caminho_base, 'ptbdataset', 'ptb.train.txt')
    
    palavras = carregar_dados(caminho)
    word2id, id2word = criar_vocabulario(palavras)
    dados_tensor = texto_para_tensor(palavras, word2id)
    
    batch_size = 20
    seq_len = 30
    
    lotes = criar_lotes(dados_tensor, batch_size, seq_len)
    
    print(f"vocab: {len(word2id)}")
    print(f"batches: {len(lotes)}")
    
    tamanho_vocab = len(word2id)
    tamanho_oculto = 256 
    epocas = 5
    lr = 0.001
    
    # instancia o modelo
    modelo = LSTManual(tamanho_vocab, tamanho_oculto).to(device)
    
    # calcula o erro e atualiza os pesos
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(modelo.parameters(), lr=lr)
    
    # lista pra salvar o erro e plotar no notebook depois
    historico_erro = []
    
    for epoca in range(epocas):
        # zera a memoria da lstm a cada epoca
        h_estado = torch.zeros(batch_size, tamanho_oculto).to(device)
        c_estado = torch.zeros(batch_size, tamanho_oculto).to(device)
        
        erro_total = 0
        
        for i, (x, y) in enumerate(lotes):
            optimizer.zero_grad()
            
            # passa os dados na rede
            saidas, h_estado, c_estado = modelo(x, h_estado, c_estado)
            
            # detach pra rede nao tentar calcular o gradiente de todos os lotes 
            # anteriores juntos, senao da falta de memoria
            h_estado = h_estado.detach()
            c_estado = c_estado.detach()
            
            # arruma o formato da matriz pra calcular o erro
            saidas_flat = saidas.view(-1, tamanho_vocab)
            y_flat = y.reshape(-1)
            
            loss = criterion(saidas_flat, y_flat)
            loss.backward()
            optimizer.step()
            
            erro_total += loss.item()
            
            # printa o erro a cada 100 lotes 
            if i % 100 == 0:
                print(f"ep {epoca+1} | b {i} | loss: {loss.item():.4f}")
                
        erro_medio = erro_total / len(lotes)
        historico_erro.append(erro_medio)
        print(f"--> fim ep {epoca+1} | loss medio: {erro_medio:.4f}")
        
    # salva o historico de erro num txt pra usar no analise.ipynb dps
    with open('historico_erro.txt', 'w') as f:
        for erro in historico_erro:
            f.write(f"{erro}\n")
    print("historico salvo: historico_erro.txt")

    # inicio do teste com dados nao vistos
    print("testando o modelo...")
    caminho_teste = os.path.join(caminho_base, 'ptbdataset', 'ptb.test.txt')
    
    palavras_teste = carregar_dados(caminho_teste)
    
    # usa o .get() pra evitar erro caso o teste tenha alguma palavra nova (joga pro id 0)
    ids_teste = [word2id.get(p, 0) for p in palavras_teste]
    dados_teste_tensor = torch.tensor(ids_teste, dtype=torch.long, device=device)
    
    lotes_teste = criar_lotes(dados_teste_tensor, batch_size, seq_len)
    
    # coloca o modelo em modo de avaliacao e desliga o autograd 
    # pra nao gastar processamento atoa calculando derivada
    modelo.eval()
    erro_teste_total = 0
    
    with torch.no_grad():
        h_estado = torch.zeros(batch_size, tamanho_oculto).to(device)
        c_estado = torch.zeros(batch_size, tamanho_oculto).to(device)
        
        for x, y in lotes_teste:
            saidas, h_estado, c_estado = modelo(x, h_estado, c_estado)
            
            saidas_flat = saidas.view(-1, tamanho_vocab)
            y_flat = y.reshape(-1)
            
            loss = criterion(saidas_flat, y_flat)
            erro_teste_total += loss.item()
            
    erro_teste_medio = erro_teste_total / len(lotes_teste)
    import math
    perplexidade_teste = math.exp(erro_teste_medio)
    
    print(f"loss teste: {erro_teste_medio:.4f}")
    print(f"perplexidade teste: {perplexidade_teste:.4f}")
    
    # salva num txt separado pra gente jogar no notebook dps
    with open('resultado_teste.txt', 'w') as f:
        f.write(f"loss:{erro_teste_medio:.4f}\n")
        f.write(f"perplexidade:{perplexidade_teste:.4f}\n")