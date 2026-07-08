class Automato:
    def __init__(self):
        self.alfabeto = set()         # Ex: {'a', 'b', 'c', '0', '1'} - conjunto, apenas para eliminar repetições
        self.estados = set()          # Ex: {'q1', 'q2', 'q3', 'q4'}
        self.estado_inicial = 'S'     # O estado de partida
        self.estados_finais = set()   # Ex: {'q2', 'q4'}
        self.transicoes = {}          # Ex: 'S': {'a': ['q1', 'q4'], 'e': ['q3', 'q2']}; 'q2': {'b': ['q2']} - dicionário para criar "gavetas dentro de gavetas"
        self.contador = 1             # contador de estados

    def gerar_novo_estado(self):
        nome_estado = f"q{self.contador}"  # cria o nome do estado (q1, q2, ...)
        self.contador += 1 # incrementa o contador p/ criar o prox
        self.estados.add(nome_estado)   # add ao conjunto de estados
        return nome_estado  # retorna o nome do estado criado
    
    def adicionar_transicao(self, origem, simbolo, destino):
        self.alfabeto.add(simbolo) # adciona o simbolo ao conjunto do alfabeto
        if origem not in self.transicoes: # Se o estado de origem ainda não existe nas transições, criamos o espaço dele
            self.transicoes[origem] = {}
            
        if simbolo not in self.transicoes[origem]: # Se o símbolo ainda não existe na origem, criamos um conjunto vazio para ele
            self.transicoes[origem][simbolo] = set()
            
        self.transicoes[origem][simbolo].add(destino) # Adicionamos o destino na transição
        
#----------------------------#

def ler_arquivo_entrada(nome_arquivo):
    tokens = []       # Lista para guardar as palavras soltas
    gramaticas = []   # Lista para guardar as regras de gramáticas
    
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:  # with open fecha o arquivo automaticamente após o uso
        linhas = arquivo.readlines()
        
        for linha in linhas:
            linha_limpa = linha.strip() # .strip() remove espaços em branco e quebras de linha (\n) do início e do fim

            if not linha_limpa: # Ignora linhas vazias
                continue
                
            if '::=' in linha_limpa: # Se tiver ::=
                gramaticas.append(linha_limpa) # É gramática
                # EX: gramaticas = ['<S> ::= a<A> | e<A>']

            else:   # Se não tem
                tokens.append(linha_limpa) # É um token
                # EX: tokens = ['se', 'entao']

    return tokens, gramaticas

#----------------------------#

def carregar_tokens_no_afnd(automato, lista_tokens):
    for palavra in lista_tokens: # para cada palavra (ex: 'entao')
        estado_atual = automato.estado_inicial # começa com estado inicial S
        
        for letra in palavra: # para cada letra da palavra (ex: 'e')
            proximo_estado = automato.gerar_novo_estado() # cria um novo estado (ex: proximo_estado = q1)
            
            automato.adicionar_transicao(estado_atual, letra, proximo_estado) # salva a transição (ex 'S': {'e':['q1'])
            
            estado_atual = proximo_estado # avança o estado para avançar a letra (ex: estado_atual =q1)
            # vai para a prox letra
            
        automato.estados_finais.add(estado_atual) # quando acaba as letras, a ultima é um estado final

#----------------------------#

def carregar_gramaticas_no_afnd(automato, lista_gramaticas):
    # dicionario q "traduz" a gramática p/ automato
    mapa_gr = {'<S>': automato.estado_inicial} # adiciona o estado inicial <S> ao mapa como S
    
    # 1º Passo: Descobrir todos os estados da gramática antes de criar as rotas (ex: add ao mapa '<A>':'q1')
    for regra in lista_gramaticas: # para cada linha
        lado_esquerdo = regra.split('::=')[0].strip() # Pega o que está antes do ::= (estados)
        if lado_esquerdo not in mapa_gr: # se o que está no lado esquerdo não está no mapa (ex: <A>)
            mapa_gr[lado_esquerdo] = automato.gerar_novo_estado() # adiciona o lado esquerdo ao mapa, com o novo estado (ex: q1, q2, qn, ...)

    # 2º Passo: Criar as transições (as flechas do autômato)
    for regra in lista_gramaticas: # para cada linha
        partes = regra.split('::=') # partes[0] = parte esquerda(estados), partes[1] = parte direita(transições)
        lado_esquerdo = partes[0].strip() # limpa os espaços em branco
        estado_origem = mapa_gr[lado_esquerdo] # define o estado de origem (mapa do lado esquerdo, ex se lado esquerdo = <S>, vai ser S; se for <A>, vai ser o q1)
        
        producoes = partes[1].split('|') # separa o lado direito(produções) pelo '|'
        
        for prod in producoes: # para cada produção (ex: a<A>, &, ....)
            prod = prod.strip() # limpa os espaços em branco
            
            if prod == '&':  # se for epsilon transição
                automato.estados_finais.add(estado_origem) # adiciona o estado de origem aos estados finais
                
            elif '<' in prod: # se for não terminal (ex: a<A>)
                indice_corte = prod.find('<') # encontra o indice que separa o terminal do proximo estado
                letra_terminal = prod[:indice_corte].strip() # Pega o 'a'
                proximo_estado_gr = prod[indice_corte:].strip() # Pega o '<A>'
                
                estado_destino = mapa_gr[proximo_estado_gr] # define o '<A>' como estado de destino
                automato.adicionar_transicao(estado_origem, letra_terminal, estado_destino) # add a transição (ex: 'S': {'a': ['q4']})
                
            else: # se for terminal(ex a)
                novo_estado_final = automato.gerar_novo_estado() # gera novo estado
                automato.estados_finais.add(novo_estado_final) # add ao conjunto de estados finais
                automato.adicionar_transicao(estado_origem, prod, novo_estado_final) # add a transição

#----------------------------#

def determinizar(afnd): # usamos fila como uma "lista de tarefas"
    afd = Automato() # cria o novo automato vazio
    afd.alfabeto = afnd.alfabeto.copy() # copia o alfabeto
    
    conjunto_inicial = {afnd.estado_inicial} # cria conjunto com o inicial do afnd
    
    def gerar_nome(conjunto):
        lista_ordenada = sorted(list(conjunto)) # ordena pra não ter diferença entre S,q1 e q1,S
        return ",".join(lista_ordenada) # une com virgula (ex: S,q1,q8)
        
    nome_inicial = gerar_nome(conjunto_inicial) # gera o nome do inicial
    afd.estado_inicial = nome_inicial # define o inicial do afd
    afd.estados.add(nome_inicial) # adciona aos estados
    
    fila_estados = [conjunto_inicial] # fila pra processar os conjuntos
    estados_visitados = [] # lista pra guardar os conjuntos ja processados
    
    while fila_estados: # enquanto tiver conjunto na fila
        estado_atual_conj = fila_estados.pop(0) # tira o primeiro da fila
        nome_atual = gerar_nome(estado_atual_conj) # pega o nome dele em string
        
        if estado_atual_conj in estados_visitados: # se ja visitou, pula
            continue
            
        estados_visitados.append(estado_atual_conj) # marca como visitado
        
        # verifica se o estado é final
        for sub_estado in estado_atual_conj: # pra cada parte do conjunto (cada estado)
            if sub_estado in afnd.estados_finais: # se uma parte era final no afnd
                afd.estados_finais.add(nome_atual) # o estado todo vira final no afd
                break # achou um final, já é o suficiente
                
        # constroi as novas transições
        for simbolo in afnd.alfabeto: # pra cada letra do alfabeto
            destinos_alcançados = set() # conjunto pra juntar os destinos
            
            for sub_estado in estado_atual_conj: # olha cada parte (estado) do conjunto de estados
                # se a parte tem transição com esse simbolo
                if sub_estado in afnd.transicoes and simbolo in afnd.transicoes[sub_estado]:
                    destinos_alcançados.update(afnd.transicoes[sub_estado][simbolo]) # junta todos os destinos de cada parte em destinos_alcançados
                    
            if destinos_alcançados: # se encontrou algum caminho
                nome_destino = gerar_nome(destinos_alcançados) # cria o nome do destino
                afd.estados.add(nome_destino) # adciona aos estados do afd
                
                # adciona a transição (agora só tem 1 destino por letra, confirmando o AFD)
                afd.adicionar_transicao(nome_atual, simbolo, nome_destino)
                
                if destinos_alcançados not in estados_visitados: # se é um destino novo
                    fila_estados.append(destinos_alcançados) # poe na fila pra processar depois
                    
    return afd

#----------------------------#

def minimizar(afd): # usamos fila 
    # 1. Passo: Remover Estados Inalcançáveis (varrendo do início pra frente)
    estados_alcancaveis = {afd.estado_inicial} # o inicial sempre é alcançável
    fila = [afd.estado_inicial] # fila pra explorar os caminhos
    
    while fila:
        estado_atual = fila.pop(0) # tira o primeiro da fila
        
        if estado_atual in afd.transicoes: # se ele tem flechas saindo dele (alcança algum outro estado)
            for simbolo, destinos in afd.transicoes[estado_atual].items(): # pra cada "rota" (o simbolo e o destino (estado))
                for destino in destinos:
                    if destino not in estados_alcancaveis: # se achei um estado novo
                        estados_alcancaveis.add(destino) # marco como alcançável
                        fila.append(destino) # jogo na fila pra ver pra onde ele vai
                        
    # 2. Passo: Remover Estados Mortos (verificando se chegam no final)
    estados_vivos = set() # conjunto pros estados úteis
    
    for estado in estados_alcancaveis: # para cada estado que podemos alcançar a partir de S
        # faz uma busca a partir do estado atual pra ver se acha algum final
        visitados = set() # conjunto dos visitados
        fila_busca = [estado] # fila
        chega_no_final = False
        
        while fila_busca: # enquanto a fila não estiver vazia
            atual = fila_busca.pop(0) # tira o primeiro elemento
            
            if atual in afd.estados_finais: # se o caminho bateu num estado final
                chega_no_final = True
                break # achou um final, ele não é morto, pode parar de buscar
                
            visitados.add(atual) # se não for final, marca que visitamos
            
            if atual in afd.transicoes: # se ele tem transições
                for destinos in afd.transicoes[atual].values():
                    for d in destinos: # para cada destino 
                        if d not in visitados and d in estados_alcancaveis: # só explora os válidos
                            fila_busca.append(d)
                            
        if chega_no_final: # se chega no final
            estados_vivos.add(estado) # salva o estado (vivo)
            
    # 3. Passo: Montar o novo AFD limpinho
    afd_min = Automato()
    afd_min.alfabeto = afd.alfabeto.copy()
    afd_min.estado_inicial = afd.estado_inicial
    afd_min.estados = estados_vivos # add apenas estados vivos (que são alcançaveis)
    
    for ef in afd.estados_finais: # copia os estados finais que são alcançaveis e vivos
        if ef in estados_vivos:
            afd_min.estados_finais.add(ef)
            
    for origem in estados_vivos: # recopia as transições só pros estados que sobraram
        if origem in afd.transicoes:
            for simbolo, destinos in afd.transicoes[origem].items():
                for destino in destinos:
                    if destino in estados_vivos:
                        afd_min.adicionar_transicao(origem, simbolo, destino)
                        
    return afd_min

#----------------------------#

def preencher_estado_erro(afd):
    estado_erro = "Erro"
    afd.estados.add(estado_erro)
    
    afd.estados_finais.add(estado_erro) # estado de erro é estado final
    
    # 1. Varre todos os estados e todos os símbolos do alfabeto
    # Usamos list(afd.estados) para não dar erro ao modificar o autômato enquanto lemos ele
    for estado in list(afd.estados): 
        for simbolo in afd.alfabeto:
            # Se a célula for vazia (não tem rota pra essa letra), aponta pro Erro 
            if estado not in afd.transicoes or simbolo not in afd.transicoes[estado]:
                afd.adicionar_transicao(estado, simbolo, estado_erro)
                
    # 2. Faz o estado de erro ficar num loop infinito para qualquer letra 
    for simbolo in afd.alfabeto:
        afd.adicionar_transicao(estado_erro, simbolo, estado_erro)
        
    return afd

#----------------------------#

def imprimir_tabela(automato, nome="Autômato"): # função para imprimir tabela de transições
    print(f"\n=== TABELA DE TRANSIÇÕES: {nome} ===")
    
    alfabeto = sorted(list(automato.alfabeto))
    
    def chave_ordenacao(estado):
        if estado == 'Erro': 
            return [999999] # Joga o estado de erro lá para o final da tabela
            
        numeros = []
        # Para estados fundidos no AFD (ex: 'q1,q8'), separamos pela vírgula
        for parte in estado.split(','):
            numero_texto = parte.replace('q', '').strip() # Tira o 'q' para sobrar só o número
            if numero_texto.isdigit():
                numeros.append(int(numero_texto)) # Converte para número matemático
        return numeros

    estados_ordenados = [automato.estado_inicial]
    outros_estados = sorted([e for e in automato.estados if e != automato.estado_inicial], key=chave_ordenacao)
    estados_ordenados.extend(outros_estados)
    
    largura_estado = max([len(e) for e in automato.estados]) + 2 
    
    largura_coluna = 6
    for estado in automato.estados:
        for simbolo in alfabeto:
            if estado in automato.transicoes and simbolo in automato.transicoes[estado]:
                tamanho_celula = len(",".join(automato.transicoes[estado][simbolo]))
                if tamanho_celula > largura_coluna:
                    largura_coluna = tamanho_celula + 2
    
    cabecalho = "δ".center(largura_estado) + "|" + "|".join([simbolo.center(largura_coluna) for simbolo in alfabeto])
    print(cabecalho)
    print("-" * len(cabecalho))
    
    for estado in estados_ordenados:
        nome_estado = f"*{estado}" if estado in automato.estados_finais else estado
        linha = nome_estado.center(largura_estado) + "|"
        
        celulas = []
        for simbolo in alfabeto:
            if estado in automato.transicoes and simbolo in automato.transicoes[estado]:
                destinos = automato.transicoes[estado][simbolo]
                texto_celula = ",".join(sorted(list(destinos), key=chave_ordenacao))
            else:
                texto_celula = "-"
                
            celulas.append(texto_celula.center(largura_coluna))
            
        linha += "|".join(celulas)
        print(linha)

#----------------------------#

meus_tokens, minhas_gramaticas = ler_arquivo_entrada('entrada.txt')

meu_afnd = Automato()
carregar_tokens_no_afnd(meu_afnd, meus_tokens)
carregar_gramaticas_no_afnd(meu_afnd, minhas_gramaticas)

meu_afd = determinizar(meu_afnd)
meu_afd_minimizado = minimizar(meu_afd)
meu_afd_completo = preencher_estado_erro(meu_afd_minimizado) # Aplica o estado de erro

imprimir_tabela(meu_afnd, "AFND")
imprimir_tabela(meu_afd, "AFD")
imprimir_tabela(meu_afd, "AFD Minimizado")
imprimir_tabela(meu_afd_completo, "AFD com estados de erro")