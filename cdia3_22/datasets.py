from colunas import *
from artefatos import Transformador, Gerador
import pandas as pd

class DatasetEstudantes:

    def criar(n_amostra):

        col_idade = ColunaIdade(n_amostra)
        col_renda = ColunaRenda(n_amostra)
        col_cor = ColunaCor(n_amostra)
        col_motivacao = ColunaMotivacao(n_amostra)

        cols_correls = [
            col_idade,
            col_renda,
            col_motivacao,
        ]
        Transformador.correlacionar(cols_correls)

        map_ = {}
        map_['idade'] = col_idade.valores
        map_['renda'] = col_renda.valores
        map_['cor'] = col_cor.valores
        map_['motivação'] = col_motivacao.valores

        return pd.DataFrame(map_)
