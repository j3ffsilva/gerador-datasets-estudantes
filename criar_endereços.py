from gerador_endereco import *
from time import sleep
import json
import random

def ler(arquivo):
    with open(arquivo, 'r') as f:
        return f.read()

def escrever(arquivo, conteudo):
    with open(arquivo, 'w') as f:
        f.write(conteudo)

def main():
    arquivo_final = "cdia3_22/data/endereços.json"
    todos_ceps = ler("cdia3_22/data/ceps.tsv").split('\n')

    for i in range(100):
        endereços_existentes = ler(arquivo_final)
        um_cep_qualquer = random.choice(todos_ceps)
        sleep(1)
        endereco_json = get_random_complete_address(um_cep_qualquer)
        endereco = json.dumps(endereco_json)

        conteudo_final = f"{endereços_existentes}\n{endereco}"
        escrever(arquivo_final, conteudo_final)

main()
