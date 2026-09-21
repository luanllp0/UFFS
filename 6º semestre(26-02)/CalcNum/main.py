import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Área de calculo

# função do exercício 7
def calcular_funcao_financiamento(taxa_juros, saldo_devedor, prestacao_mensal, numero_parcelas):
    # Fórmula f(j) = [1 - (1 + j)^(-P)] / j - (Saldo_Devedor / Prestacao_Mensal) = 0
    lado_esquerdo = (1 - (1 + taxa_juros) ** (-numero_parcelas)) / taxa_juros
    lado_direito = saldo_devedor / prestacao_mensal
    return lado_esquerdo - lado_direito


def executar_metodo_bissecao(saldo_devedor, prestacao_mensal, numero_parcelas, limite_inferior, limite_superior, tolerancia):
    # f(a):
    valor_funcao_inferior = calcular_funcao_financiamento(limite_inferior, saldo_devedor, prestacao_mensal, numero_parcelas)
    # f(b):
    valor_funcao_superior = calcular_funcao_financiamento(limite_superior, saldo_devedor, prestacao_mensal, numero_parcelas)

    # se f(a) * f(b) >= 0: erro, a e b não tem sinais opostos
    if valor_funcao_inferior * valor_funcao_superior >= 0:
        messagebox.showerror("Erro de Intervalo", 
                             "A função f(j) deve ter sinais contrários no limite inferior e superior.")
        return None, []

    # cria histórico de iterações e começa com i = 0
    historico_iteracoes = []
    numero_iteracao = 0

    while True:
        # calcula ponto médio (Xn), f(Xn) e erro de f(Xn)
        ponto_medio = (limite_inferior + limite_superior) / 2.0
        valor_funcao_ponto_medio = calcular_funcao_financiamento(ponto_medio, saldo_devedor, prestacao_mensal, numero_parcelas)
        erro_imagem = abs(valor_funcao_ponto_medio) # erro = diferença entre f(x) e 0 em modulo, logo erro = |f(x)|

        # salva os valores da iteração no histórico
        historico_iteracoes.append({
            'iteracao': numero_iteracao,
            'limite_inferior': limite_inferior,
            'limite_superior': limite_superior,
            'ponto_medio': ponto_medio,
            'valor_funcao': valor_funcao_ponto_medio,
            'erro': erro_imagem
        })

        # se erro < ε: termina
        if erro_imagem < tolerancia:
            break

        # calcula f(a)
        valor_funcao_inferior = calcular_funcao_financiamento(limite_inferior, saldo_devedor, prestacao_mensal, numero_parcelas)
        # se f(a) * f(x) < 0 (sinais opostos)
        if valor_funcao_inferior * valor_funcao_ponto_medio < 0: # 
            # f(x) substitui f(b)
            limite_superior = ponto_medio
        # sef(x) e f(a) tem mesmo sinal
        else:
            # f(x) substitui f(a)
            limite_inferior = ponto_medio

        # i = i+1 (próxima iteração)
        numero_iteracao += 1

    return ponto_medio, historico_iteracoes

# área de interface

# função executada ao clicar em calcular
def ao_clicar_calcular():
    try:
        # entradas: PV, E, PM, P, ε ,a, b
        preco_a_vista = float(entry_preco_vista.get().replace(',', '.'))
        valor_entrada = float(entry_entrada.get().replace(',', '.'))
        prestacao_mensal = float(entry_parcela.get().replace(',', '.'))
        numero_parcelas = int(entry_num_parcelas.get())
        tolerancia = float(entry_tolerancia.get().replace(',', '.'))
        limite_inferior = float(entry_lim_inf.get().replace(',', '.'))
        limite_superior = float(entry_lim_sup.get().replace(',', '.'))
    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, preencha todos os campos com números válidos.")
        return

    saldo_devedor = preco_a_vista - valor_entrada # SD = PV - E

    #tratamento de erros
    if saldo_devedor <= 0:
        messagebox.showerror("Erro Financeiro", "O saldo devedor deve ser maior que zero (Preço à vista > Entrada).")
        return

    #tratamento de erros
    if prestacao_mensal * numero_parcelas <= saldo_devedor:
        messagebox.showwarning("Aviso Financeiro", "A soma das parcelas é menor ou igual ao saldo devedor (não há juros cobrados).")
        return

    # com todas as entradas e verificação de erros, executa o programa
    taxa_juros, historico = executar_metodo_bissecao(
        saldo_devedor, prestacao_mensal, numero_parcelas, limite_inferior, limite_superior, tolerancia
    )

    if taxa_juros is None:
        return

    # Limpar caixa de texto
    area_texto.delete("1.0", tk.END)

    # Formatar Resultados
    saida = []
    saida.append("=" * 80)
    saida.append(f"DADOS DO FINANCIAMENTO:")
    saida.append(f"Saldo Devedor: R$ {saldo_devedor:,.2f} | Parcelamento: {numero_parcelas}x de R$ {prestacao_mensal:,.2f}")
    saida.append("=" * 80 + "\n")

    saida.append("--- TABELA DE ITERAÇÕES (MÉTODO DA BISSEÇÃO) ---")
    saida.append(f"{'Iter.':<6} | {'Lim. Inf.':<10} | {'Lim. Sup.':<10} | {'Ponto Médio':<12} | {'f(m)':<12} | {'Erro |f(m)|':<12}")
    saida.append("-" * 75)

    for item in historico:
        saida.append(
            f"{item['iteracao']:<6} | {item['limite_inferior']:<10.6f} | {item['limite_superior']:<10.6f} | "
            f"{item['ponto_medio']:<12.6f} | {item['valor_funcao']:<12.6f} | {item['erro']:<12.6f}"
        )

    taxa_mensal = taxa_juros * 100

    saida.append("\n" + "=" * 80)
    saida.append("RESUMO FINAL DOS RESULTADOS:")
    saida.append("=" * 80)
    saida.append(f"• Taxa Mensal de Juros: {taxa_mensal:.4f}% ao mês")
    saida.append(f"• Saldo Devedor Financiado: R$ {saldo_devedor:,.2f}")
    saida.append(f"• Valor Total Pago nas Parcelas: R$ {(prestacao_mensal * numero_parcelas):,.2f}")
    saida.append(f"• Total de Juros Pagos: R$ {(prestacao_mensal * numero_parcelas) - saldo_devedor:,.2f}")
    saida.append(f"• Total de Iterações Necessárias: {len(historico)}")
    saida.append("=" * 80)

    area_texto.insert(tk.END, "\n".join(saida))


# Criar a Janela Principal
janela = tk.Tk()
janela.title("Calculadora de Financiamento - Método da Bisseção")
janela.geometry("820x680")
janela.resizable(True, True)

# Frame de Entradas
frame_entradas = ttk.LabelFrame(janela, text=" Parâmetros do Financiamento ", padding=10)
frame_entradas.pack(fill="x", padx=15, pady=10)

# Layout das Entradas
# valores padrão
campos = [
    ("Preço à Vista (R$):", "312000", 0, 0),
    ("Entrada (R$):", "91051.90", 0, 2),
    ("Prestação Mensal (R$):", "26000", 1, 0),
    ("Número de Parcelas (meses):", "12", 1, 2),
    ("Tolerância de Erro (ex: 0.01):", "0.01", 2, 0),
    ("Limite Inferior 'a' (ex: 0.0001):", "0.0001", 3, 0),
    ("Limite Superior 'b' (ex: 0.50):", "0.50", 3, 2),
]

entries = {}
for rotulo, padrao, linha, col in campos:
    lbl = ttk.Label(frame_entradas, text=rotulo)
    lbl.grid(row=linha, column=col, sticky="w", padx=5, pady=4)
    ent = ttk.Entry(frame_entradas, width=20)
    ent.insert(0, padrao)
    ent.grid(row=linha, column=col+1, sticky="w", padx=5, pady=4)
    entries[rotulo] = ent

entry_preco_vista = entries["Preço à Vista (R$):"]
entry_entrada = entries["Entrada (R$):"]
entry_parcela = entries["Prestação Mensal (R$):"]
entry_num_parcelas = entries["Número de Parcelas (meses):"]
entry_tolerancia = entries["Tolerância de Erro (ex: 0.01):"]
entry_lim_inf = entries["Limite Inferior 'a' (ex: 0.0001):"]
entry_lim_sup = entries["Limite Superior 'b' (ex: 0.50):"]

# Botão de Cálculo
btn_calcular = ttk.Button(janela, text="CALCULAR", command=ao_clicar_calcular)
btn_calcular.pack(fill="x", padx=15, pady=5)

# Frame de Saída de Resultados
frame_saida = ttk.LabelFrame(janela, text=" Tabela de Iterações e Resumo ", padding=10)
frame_saida.pack(fill="both", expand=True, padx=15, pady=10)

area_texto = scrolledtext.ScrolledText(frame_saida, font=("Courier", 9), wrap=tk.NONE)
area_texto.pack(fill="both", expand=True)

janela.mainloop()
