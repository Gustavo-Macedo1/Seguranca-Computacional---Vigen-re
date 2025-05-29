import streamlit as st
import pandas as pd
from modulos.auxiliares import *
from modulos.descriptografia import *
from modulos.criptografia import *
from matplotlib import pyplot as plt


# -- Funções para análise de coincidências e descoberta do tamanho da chave --

### 1. Checa coincidências entre dois textos de mesmo tamanho
def checa_coincidencias(texto1, texto2):
    coincidencias = 0
    len_texto = len(texto1)

    for i in range(len_texto):
        if texto1[i] == texto2[i]:
            coincidencias += 1

    return coincidencias

### 2. Organiza os dados do eixo y para o gráfico de coincidências
def coincidencias_global(texto_cifrado):
    len_texto = len(texto_cifrado)
    texto_deslocado = texto_cifrado[:len_texto - 1]
    indice = 1
    coincidencias = []

    for i in range(len_texto - 1):
        coincidencias.append((checa_coincidencias(texto_cifrado[indice:], texto_deslocado)) / len_texto)
        texto_deslocado = texto_deslocado[:-1]
        indice += 1

    return coincidencias

### 3. Gera a figura do gráfico de coincidências
def grafico_coincidencias(texto_cifrado):
    x = list(range(len(texto_cifrado) - 1))[:40]
    y = coincidencias_global(texto_cifrado)[:40]

    return x, y

# -- Funções para descoberta da chave com base no tamanho (Parte 1) --

## 1. Cria caixas (uma para cada letra da chave) e distribui as letras do texto cifrado nelas
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

## 2. Prepara a caixa para visualização, contando a frequência de cada letra com um hashmap
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

## 3. Mostra a caixa atual em um gráfico de barras
def mostra_caixa(caixas, i):
    caixa = caixas[i]
    x, y = prepara_caixa(caixa)

    plt.figure(figsize=(6, 1))
    plt.title("Frequência de letras na caixa atual")
    plt.xlabel("Letras")
    plt.ylabel("Frequência")
    plt.bar(x, y)
    plt.show()

# -- Funções para descoberta da chave com base no tamanho (Parte 2) --

## 1. Desloca duas listas para a esquerda, simulando a rotação de uma distribuição de frequências
def deslocar_esquerda(x, y):
    x1 = x[1:] + x[:1]
    y1 = y[1:] + y[:1]
    return (x1, y1)

## 2. Obtem a letra da chave com base na caixa e na língua 
##    usando um coeficiente de similaridade rotativo
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

## 3. Obtem a chave completa, iterando sobre as caixas e concatenando as letras
def obtem_chave(caixas, lingua):
    chave = ""
    for i in range(len(caixas)):
        chave += chr(ord('a') + obtem_letra_chave(caixas[i], lingua))
    return chave

# -- Funções para tratamento de texto e caracteres especiais --

## 1. Identifica as posições e caracteres especiais no texto
def caracteres_especiais(texto):
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

## 2. Limpa o texto, removendo caracteres especiais
def limpar_texto(texto):
    caracteres_especiais = " .,;:!?-"
    
    for caracter in caracteres_especiais:
        texto = texto.replace(caracter, "")

    return texto

## 3. Adiciona os caracteres especiais de volta ao texto, nas posições originais
def adicionar_caracteres_especiais(texto, posicoes, caracteres):
    for posicao, caracter in zip(posicoes, caracteres):
        texto = texto[:posicao] + caracter + texto[posicao:]
    
    return texto

# -- Funções principais para a Análise de Frequência (AAF) --

## 1. Executa o fluxo de funções para análise de frequência no Streamlit
def aaf_streamlit(texto_cifrado, lingua):
    posicoes, caracteres = caracteres_especiais(texto_cifrado)
    texto_cifrado = limpar_texto(texto_cifrado)
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
            st.markdown(f"**Texto descriptografado:** {adicionar_caracteres_especiais(descriptografado, posicoes, caracteres)}")
    
        return chave

## 2. Executa o fluxo de funções para análise de frequência localmente
def aaf(texto_cifrado, lingua):
    posicoes, caracteres = caracteres_especiais(texto_cifrado)
    texto_cifrado = limpar_texto(texto_cifrado)
    # fig = grafico_coincidencias(texto_cifrado)
    # st.pyplot(fig, clear_figure=True)
    caixas = cria_caixas(texto_cifrado)
    chave = obtem_chave(caixas, lingua)
    descriptografado = descriptografar(texto_cifrado, chave)
    print(f"A chave é: {chave}")
    print(f"Texto descriptografado: {adicionar_caracteres_especiais(descriptografado, posicoes, caracteres)}")
    
    return chave


### ------------ TESTE ------------ ###

# texto_exemplo = "A Russia lancou na madrugada deste domingo o maior bombardeio com drones e misseis da guerra contra a Ucrania matando pelo menos nn pessoas e ferindo dezenas em horas de ataques a cidades e vilarejos por todo o pais disseram autoridades ucranianas O ataque ocorreu mesmo com a realizacao da maior troca de prisioneiros da guerra um raro momento de cooperacao entre ambas as nacoes"
# key = "cachorro"
# cifrado = criptografar(texto_exemplo, key)
# descriptografado = descriptografar(cifrado, key)
# aaf(cifrado, "pt")