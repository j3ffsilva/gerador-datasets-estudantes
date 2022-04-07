from gerador_endereco import *

list_ceps, _ = get_list_ceps_bairros(estado='sp', municipio='são paulo')
for cep in list_ceps:
    print(cep)
