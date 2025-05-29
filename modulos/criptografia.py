def gerar_tabua():
    tabua = {}
    alfabeto = "abcdefghijklmnopqrstuvwxyz"

    # Para cada letra do alfabeto, gera alfabeto deslocado
    for i in range (26):
        letra = alfabeto[i]
        tabua[letra] = alfabeto[i:] + alfabeto[:i]

    return tabua

def criptografar(texto_plano, chave):
    # Normalização inicial, deixando todos os caracteres em caixa baixa
    texto_plano = texto_plano.lower()
    chave = chave.lower()

    # Gerando dados iniciais para posterior processamento
    tabua = gerar_tabua()
    tamanho_texto_plano, tamanho_chave = len(texto_plano), len(chave) - 1
    posicao = 0
    texto_cifrado = ""
    caracteres_especiais = " .,;:!?-"

    # Loop para cifrar cada letra do texto plano
    for i in range(tamanho_texto_plano):
        # Recomeça o loop quando ultrapassar o tamanho do texto
        if posicao > tamanho_chave:
            posicao = 0

        # Atualiza valor das letras da chave e do texto plano
        chave_atual = chave[posicao]
        letra_atual = texto_plano[i]

        if letra_atual in caracteres_especiais:
            letra_cifrada = letra_atual
            posicao -= 1 # Ignora caracteres especiais na chave
        else:
            # Linha: chave_atual, Coluna: posição da letra atual    
            letra_cifrada = tabua[chave_atual][(ord(letra_atual) - ord('a'))] 

        texto_cifrado += letra_cifrada
        posicao += 1

    return texto_cifrado

### ------------ TESTE ------------- ###

# frase = "Enquanto as estrelas brilhavam no ceu, Marcos caminhava lentamente pela estrada." \
#         " Nao havia pressa, apenas o silencio da noite e o som distante de um rio. Pensava na vida," \
#         " nos sonhos esquecidos e nas palavras que nunca disse. Tudo parecia mais claro ali."
# chave = "sorvete"

# print(f'\nTexto cifrado: \n\n{criptografar(frase, chave)}\n\n')