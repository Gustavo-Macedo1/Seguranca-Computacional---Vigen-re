def gerar_tabua():
    tabua = {}
    alfabeto = "abcdefghijklmnopqrstuvwxyz"

    # Para cada letra do alfabeto, gera alfabeto deslocado
    for i in range (26):
        letra = alfabeto[i]
        tabua[letra] = alfabeto[i:] + alfabeto[:i]

    return tabua

def descriptografar(frase_cifrada, chave):
    tabua = gerar_tabua()
    tamanho_frase, tamanho_chave = len(frase_cifrada), len(chave) - 1
    posicao = 0
    texto_decrifrado = ""

    for i in range(tamanho_frase):
        if posicao > tamanho_chave:
            posicao = 0

        letra_atual = frase_cifrada[i]
        chave_atual = chave[posicao]

        if letra_atual != " ":
            letra_real = chr(ord('a') + (tabua[chave_atual].index(letra_atual)))
        else:
            letra_real = " "
            posicao -= 1

        texto_decrifrado += letra_real

        posicao += 1

    return texto_decrifrado


### ----------- TESTE ------------ ###

# texto_cifrado = 'fu toftp dr bnnbnn'
# chave = 'banana'

# print(descriptografar(texto_cifrado, chave))