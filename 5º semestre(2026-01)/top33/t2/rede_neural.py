import torch
import torch.nn as nn
import math

class LSTManual(nn.Module):
    def __init__(self, tamanho_vocab, tamanho_oculto):
        super().__init__()
        self.tamanho_oculto = tamanho_oculto
        self.tamanho_vocab = tamanho_vocab
        
        # a gente precisa criar nossa propria matriz de embeddings tbm
        # pq o nn.Embedding eh uma camada pronta e nao pode usar
        self.embedding = nn.Parameter(torch.randn(tamanho_vocab, tamanho_oculto) * 0.1)
        
        # pesos pra juntar entrada (x) e estado oculto (h)
        # multiplicamos por std pra rede nao começar maluca e os gradientes explodirem
        std = 1.0 / math.sqrt(tamanho_oculto)
        
        self.w_f = nn.Parameter(torch.randn(tamanho_oculto * 2, tamanho_oculto) * std)
        self.b_f = nn.Parameter(torch.zeros(tamanho_oculto))
        
        self.w_i = nn.Parameter(torch.randn(tamanho_oculto * 2, tamanho_oculto) * std)
        self.b_i = nn.Parameter(torch.zeros(tamanho_oculto))
        
        self.w_c = nn.Parameter(torch.randn(tamanho_oculto * 2, tamanho_oculto) * std)
        self.b_c = nn.Parameter(torch.zeros(tamanho_oculto))
        
        self.w_o = nn.Parameter(torch.randn(tamanho_oculto * 2, tamanho_oculto) * std)
        self.b_o = nn.Parameter(torch.zeros(tamanho_oculto))
        
        # matriz pra transformar o estado oculto final na previsao da proxima palavra
        self.w_y = nn.Parameter(torch.randn(tamanho_oculto, tamanho_vocab) * std)
        self.b_y = nn.Parameter(torch.zeros(tamanho_vocab))

    def forward(self, x, h_prev, c_prev):
        # x vem com formato [tamanho_lote, tamanho_seq]
        tamanho_lote, tamanho_seq = x.shape
        
        # lista pra guardar as previsoes de cada passo de tempo da sequencia
        saidas = []
        
        h_t = h_prev
        c_t = c_prev
        
        # bptt: passa cada palavra da sequencia pela nossa lstm manual
        for t in range(tamanho_seq):
            # pega a palavra do tempo t e acha o embedding dela manualmente na matriz
            x_t = self.embedding[x[:, t]]
            
            # junta o x_t (entrada) com o h_t (estado anterior)
            xh = torch.cat([x_t, h_t], dim=1)
            
            # equacoes matematicas das portas da lstm usando multiplicacao de matriz (@)
            f_t = torch.sigmoid(xh @ self.w_f + self.b_f) # gate de esquecimento
            i_t = torch.sigmoid(xh @ self.w_i + self.b_i) # gate de entrada
            c_tilde = torch.tanh(xh @ self.w_c + self.b_c) # candidato a estado da celula
            
            c_t = f_t * c_t + i_t * c_tilde # atualiza o estado longo da celula
            
            o_t = torch.sigmoid(xh @ self.w_o + self.b_o) # gate de saida
            h_t = o_t * torch.tanh(c_t) # atualiza o estado oculto de curto prazo
            
            # calcula a previsao pra proxima palavra baseada no h_t atual
            y_t = h_t @ self.w_y + self.b_y
            saidas.append(y_t)
            
        # junta todas as saidas calculadas numa coisa so
        # formato final fica: [tamanho_lote, tamanho_seq, tamanho_vocab]
        saidas = torch.stack(saidas, dim=1)
        
        return saidas, h_t, c_t