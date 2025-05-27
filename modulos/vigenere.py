from aaf import *

print("========= Teste de criptografia Vigenère =========\n\n")

texto_plano = input("Digite o texto a ser cifrado: ")
chave = input("Digite a chave: ")

print(f'Texto criptografado: {descriptografar(texto_plano, chave)} \n\n')

print("========= Teste de descriptografia Vigenère =========\n\n")

texto_cifrado = input("Digite o texto a ser decifrado: ")
chave = input("Digite a chave: ")

print(f'Texto descriptografado: {criptografar(texto_cifrado, chave)} \n\n')

print("========= Teste de ataque de análise de frequência Vigenère =========\n\n")

texto_cifrado = input("Digite o texto cifrado: ")
aaf(texto_cifrado, "pt")

print("\n\n========= Fim dos Testes - Vigenère =========")