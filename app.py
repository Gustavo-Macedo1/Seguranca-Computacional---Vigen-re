import streamlit as st
import pandas as pd
from modulos.criptografia import *
from modulos.descriptografia import descriptografar
from modulos.aaf import *
from modulos.auxiliares import *

st.caption("Autor: Gustavo de Oliveira Macedo")
st.caption("Matrícula: 211028515")
st.title("Criptografia Vigenère - Trabalho 1")
st.subheader("Bem-vindo(a) ao aplicativo de Criptografia Vigenère!")
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Criptografar**")
    texto_exemplo = "A Russia lancou na madrugada deste domingo o maior bombardeio com drones e misseis da guerra contra a Ucrania matando pelo menos nn pessoas e ferindo dezenas em horas de ataques a cidades e vilarejos por todo o pais disseram autoridades ucranianas O ataque ocorreu mesmo com a realizacao da maior troca de prisioneiros da guerra um raro momento de cooperacao entre ambas as nacoes"
    texto_plano = st.text_area("Digite o texto a ser cifrado:")
    chave = st.text_input("Digite a chave:", key="chave_criptografia")
    if st.button("Criptografar", type="primary"):
        if texto_plano and chave:
            texto_cifrado = criptografar(texto_plano, chave)
            st.success(f'Texto criptografado: {texto_cifrado}')
        else:
            st.error("Por favor, preencha todos os campos.")
with col2:
    st.markdown("**Descriptografar**")
    texto_cifrado = st.text_area("Digite o texto a ser decifrado:")
    chave = st.text_input("Digite a chave:", key="chave_descriptografia")
    if st.button("Descriptografar", type="primary"):
        if texto_cifrado and chave:
            texto_descriptografado = descriptografar(texto_cifrado, chave)
            st.success(f'Texto descriptografado: {texto_descriptografado}')
        else:
            st.error("Por favor, preencha todos os campos.")

st.divider()

st.subheader("Análise de Frequência")
texto_cifrado = st.text_area("Digite o texto cifrado para análise de frequência:")
lingua = st.selectbox("Selecione a língua:", ["Português", "Inglês"], index=0)

if lingua == "Português":
    lingua_code = "pt"
else:
    lingua_code = "en"

if texto_cifrado:
    aaf_streamlit(texto_cifrado, lingua_code)

st.divider()
