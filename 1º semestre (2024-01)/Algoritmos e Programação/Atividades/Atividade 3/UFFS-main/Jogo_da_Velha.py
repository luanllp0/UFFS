ex = [[" 0,0 ", " 0,1 ", " 0,2 "], [" 1,0 ", " 1,1 ", " 1,2 "], [" 2,0 ", " 2,1 ", " 2,2 "]]
jogo = [ [ "", "", ""], ["", "", ""], ["", "", ""]]
jogador1 = True

def mostrar_jogo(jogo):		
    for l in range(0,3):
        for c in range(0,3):
            print(f'[{jogo[l][c]:^5}]', end='')
        print()

def mostrar_exemplo(exemplo):		
    for l in range(0,3):
        for c in range(0,3):
            print(f'[{exemplo[l][c]:^5}]', end='')
        print()

# tentei desta forma mas não estava funcionando:
# def verificar_vitoria(jogo):
    # for i in range (0,3):
    #     if str(jogo[i][0]) == str(jogo[i][1]) == str(jogo[i][2]) == "X" or "O":
    #         return True
    #     elif str(jogo[0][i]) == str(jogo[1][i]) == str(jogo[2][i]) == "X" or "O":
    #         return True
    # if str(jogo[0][0]) == str(jogo[1][1]) == str(jogo[2][2]) == "X" or "O":
    #     return True
    # elif str(jogo[0][2]) == str(jogo[1][1]) == str(jogo[2][0]) == "X" or "O":
    #     return True
    # else:
    #     return False
    # então coloquei todas as possibilidades dentro do mesmo for:

def verificar_vitoria(jogo):
    x = False
    for i in range (0,3):
        if jogo[i][0]  == "X" and jogo[i][1] == "X" and jogo[i][2] == "X" or jogo[i][0] == "O" and jogo[i][1] == "O" and jogo[i][2] == "O" or jogo[0][i]  == "X" and jogo[1][i] == "X" and jogo[2][i] == "X" or jogo[0][i]  == "O" and jogo[1][i] == "O" and jogo[2][i] == "O" or jogo[0][0] == "X" and jogo [1][1] == "X" and jogo[2][2] == "X" or jogo[0][0] == "O" and jogo [1][1] == "O" and jogo[2][2] == "O" or jogo[2][0] == "X" and jogo [1][1] == "X" and jogo[0][2] == "X" or jogo[2][0] == "O" and jogo [1][1] == "O" and jogo[0][2] == "O":
            x = True
    return(x)    

def verificar_velha(jogo):
    a = True
    for l in range(0,3):
        for c in range(0,3):
            if jogo[l][c] == "":
                a = False
    return(a)

print(f"\n\n                Bem vindo(a) ao Jogo da velha do Luan! \n\nPara jogar, os jogadores devem escolher a casa para colocar seu simbolo: (X)jogador_1 e (O)Jogador_2, alternando o jogador cada jogada.\n\nAbaixo está o mapeamento do tabuleiro para a seleção das casas:")
mostrar_exemplo(ex)

p1 = input("\nInsira o nome do jogador 1: \n")
p2 = input("\nInsira o nome do Jogador 2: \n")

while True:
    if verificar_velha(jogo) == True:
        print(f"\nDeu velha! nem {p1} nem {p2} ganharam.")
        break

    elif jogador1 == True:
        l, c = map(int, input(f"\n{p1} insira os valores das casas separados por espaço: \n").split())
        if jogo[l][c] != "":
            print(f"O espaço já está ocupado, selecione outro")
            continue
        else:
            jogo[l][c] = "X"
            jogador1 = False
            mostrar_jogo(jogo)
            if verificar_vitoria(jogo) == True:
                print(f"\nParabens {p1}, você venceu!")
                break

    elif jogador1 == False:
        l, c = map(int, input(f"\n{p2} insira os valores das casas separados por espaço: \n").split())
        if jogo[l][c] != "":
            print(f"O espaço já está ocupado, selecione outro")
            continue
        else:
            jogo[l][c] = "O"
            jogador1 = True
            mostrar_jogo(jogo)
            if verificar_vitoria(jogo) == True:
                print(f"\nParabens {p2}, você venceu!")
                break
    