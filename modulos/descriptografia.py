from modulos.criptografia import gerar_tabua

def descriptografar(frase_cifrada, chave):
    tabua = gerar_tabua()
    tamanho_frase, tamanho_chave = len(frase_cifrada), len(chave) - 1
    posicao = 0
    texto_decrifrado = ""
    caracteres_especiais = " .,;:!?-"

    for i in range(tamanho_frase):
        if posicao > tamanho_chave:
            posicao = 0

        letra_atual = frase_cifrada[i]
        chave_atual = chave[posicao]

        if letra_atual in caracteres_especiais:
            letra_real = letra_atual
            posicao -= 1
        else:
            # Linha: chave_atual, Coluna: posição da letra atual
            letra_real = chr(ord('a') + (tabua[chave_atual].index(letra_atual)))

        texto_decrifrado += letra_real
        posicao += 1

    return texto_decrifrado


### ----------- TESTE ------------ ###

# texto_cifrado = 'cs iem oep gunknwaeiag ykrsrhwls d zknuyvdv, hrafzprjo fug hi kxlcfvyors, ult gamhlag waa eckheu'
# chave = 'pegasus'

# print(f'\nTexto decifrado: \n\n{descriptografar(texto_cifrado, chave)}\n')