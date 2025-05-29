def posicoes_espaco(texto):
    i = 0
    posicoes = []
    caracteres = []
    caracteres_especiais = " .,;:!?-"

    for caracter in texto:
        if caracter in caracteres_especiais:
            posicoes.append(i)
            caracteres.append(caracter)
        i += 1

    return posicoes, caracteres

def limpar_texto(texto):
    caracteres_especiais = " .,;:!?-"
    
    for caracter in caracteres_especiais:
        texto = texto.replace(caracter, "")

    return texto

def adicionar_espacos(texto, posicoes, caracteres):
    for posicao, caracter in zip(posicoes, caracteres):
        texto = texto[:posicao] + caracter + texto[posicao:]
    
    return texto


texto = "no ceu uma constelacao, escolhera o vencedor, brilhando nao se extringuira, ate cumprir sua missao."
texto_limpo = limpar_texto(texto)
posicoes, caracteres = posicoes_espaco(texto)
texto_com_caracteres = adicionar_espacos(texto_limpo, posicoes, caracteres)
print(posicoes)
print(caracteres)   
print(texto_limpo)
print(texto_com_caracteres)