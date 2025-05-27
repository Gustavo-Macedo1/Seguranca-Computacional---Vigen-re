import streamlit as st
import pandas as pd
from modulos.auxiliares import *
from modulos.descriptografia import *
from modulos.criptografia import *
from matplotlib import pyplot as plt

def checa_coincidencias(texto1, texto2):
    coincidencias = 0
    len_texto = len(texto1)

    for i in range(len_texto):
        if texto1[i] == texto2[i]:
            coincidencias += 1

    return coincidencias

def len_chave(texto_cifrado):
    len_texto = len(texto_cifrado)
    texto_deslocado = texto_cifrado[:len_texto - 1]
    indice = 1
    coincidencias = []

    for i in range(len_texto - 1):
        coincidencias.append((checa_coincidencias(texto_cifrado[indice:], texto_deslocado)) / len_texto)
        texto_deslocado = texto_deslocado[:-1]
        indice += 1

    return coincidencias

def grafico_coincidencias(texto_cifrado):
    x = list(range(len(texto_cifrado) - 1))[:40]
    y = len_chave(texto_cifrado)[:40]

    return x, y


def cria_caixas(texto_cifrado, n=None):
    if n == None:
        n = int(input("Digite o tamanho da chave: "))
    rotulos = list(range(n))
    caixas = {}

    for rotulo in rotulos:
        caixas[rotulo] = []

    for i in range(len(texto_cifrado)):
        rotulo = i % n
        caixas[rotulo].append(texto_cifrado[i])

    return caixas

def prepara_caixa(caixa):
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    map = {}

    for letra in alfabeto:
        map[letra] = 0

    for letra in caixa:
        map[letra] += 1

    x = list(map.keys())
    y = list(map.values())

    return [x, y]

def mostra_caixa(caixas, i):
    caixa = caixas[i]
    x, y = prepara_caixa(caixa)

    plt.figure(figsize=(6, 1))
    plt.title("Frequência de letras na caixa atual")
    plt.xlabel("Letras")
    plt.ylabel("Frequência")
    plt.bar(x, y)
    plt.show()

def deslocar_esquerda(x, y):
    x1 = x[1:] + x[:1]
    y1 = y[1:] + y[:1]
    return (x1, y1)

def obtem_letra_chave(caixa, lingua):
    x, y = prepara_caixa(caixa)
    real = list(gerar_dicionario_freq(lingua).values())

    erro_final = 99999
    posicao = 0

    for i in range(25):
        erro = 0
        for j in range(25):
            erro += abs(y[j] - real[j])
        
        if erro < erro_final:
            erro_final = erro
            posicao = i
        
        _, y = deslocar_esquerda(x, y)

    return posicao

def obtem_chave(caixas, lingua):
    chave = ""
    for i in range(len(caixas)):
        chave += chr(ord('a') + obtem_letra_chave(caixas[i], lingua))
    return chave

def posicoes_espaco(texto):
    i = 0
    posicoes = []

    for caracter in texto:
        if caracter == " ":
            posicoes.append(i)
        i += 1

    return posicoes

def adicionar_espacos(texto, posicoes):
    for posicao in posicoes:
        texto = texto[:posicao] + " " + texto[posicao:]
    
    return texto

def aaf_streamlit(texto_cifrado, lingua):
    posicoes = posicoes_espaco(texto_cifrado)
    texto_cifrado = texto_cifrado.replace(" ", "")
    x, y = grafico_coincidencias(texto_cifrado)
    fig = pd.DataFrame({"Posição": x, "Coincidências": y}).set_index("Posição")
    st.bar_chart(fig)
    n = st.number_input("Tamanho estimado da chave:", min_value=1, max_value=20, value=None, key="tamanho_chave")
    if n != None:
        caixas = cria_caixas(texto_cifrado, n)
        chave = obtem_chave(caixas, lingua)
        descriptografado = descriptografar(texto_cifrado, chave)
        if descriptografado and caixas:
            st.markdown(f"**A chave é:** {chave}")
            st.markdown(f"**Texto descriptografado:** {adicionar_espacos(descriptografado, posicoes)}")
    
        return chave

def aaf(texto_cifrado, lingua):
    posicoes = posicoes_espaco(texto_cifrado)
    texto_cifrado = texto_cifrado.replace(" ", "")
    # fig = grafico_coincidencias(texto_cifrado)
    # st.pyplot(fig, clear_figure=True)
    caixas = cria_caixas(texto_cifrado)
    chave = obtem_chave(caixas, lingua)
    descriptografado = descriptografar(texto_cifrado, chave)
    print(f"A chave é: {chave}")
    print(f"Texto descriptografado: {adicionar_espacos(descriptografado, posicoes)}")
    
    return chave


### ------------ TESTE ------------ ###

# texto_exemplo = "A Russia lancou na madrugada deste domingo o maior bombardeio com drones e misseis da guerra contra a Ucrania matando pelo menos nn pessoas e ferindo dezenas em horas de ataques a cidades e vilarejos por todo o pais disseram autoridades ucranianas O ataque ocorreu mesmo com a realizacao da maior troca de prisioneiros da guerra um raro momento de cooperacao entre ambas as nacoes"
# key = "cachorro"
# cifrado = criptografar(texto_exemplo, key)
# descriptografado = descriptografar(cifrado, key)
# aaf(cifrado, "pt")