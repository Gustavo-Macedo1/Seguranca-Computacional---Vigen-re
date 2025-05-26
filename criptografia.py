def gerar_tabua():
    tabua = {}
    alfabeto = "abcdefghijklmnopqrstuvwxyz"

    # Para cada letra do alfabeto, gera alfabeto deslocado
    for i in range (26):
        letra = alfabeto[i]
        tabua[letra] = alfabeto[i:] + alfabeto[:i]

    return tabua

# Por 'frase', denota-se 'texto plano'.

def criptografar(frase, chave):
    # Normalização inicial, deixando todos os caracteres em caixa baixa
    frase = frase.lower()
    chave = chave.lower()

    # Gerando dados iniciais para posterior processamento
    tabua = gerar_tabua()
    tamanho_frase, tamanho_chave = len(frase), len(chave) - 1
    posicao = 0
    texto_cifrado = ""


    for i in range(tamanho_frase):
        # Recomeça o loop quando ultrapassar o tamanho do texto
        if posicao > tamanho_chave:
            posicao = 0

        # Chave
        chave_atual = chave[posicao]
        letra_atual = frase[i]

        if letra_atual != " ":
            letra_cifrada = tabua[chave_atual][(ord(letra_atual) - ord('a'))]
        else:
            letra_cifrada = " "
            posicao -= 1
        texto_cifrado += letra_cifrada

        posicao += 1

    return texto_cifrado

### ------------ TESTE ------------- ###

# frase = "eu gosto de banana"
# chave = "banana"

# print(criptografar(frase, chave))