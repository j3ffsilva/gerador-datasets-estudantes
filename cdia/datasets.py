from cdia.colunas import *
from cdia.artefatos import Transformador, Gerador
import pandas as pd

class DatasetEstudantes:

    def criar(n_amostra):

        col_matricula = ColunaMatricula(n_amostra)
        col_idade = ColunaIdade(n_amostra)
        col_renda = ColunaRenda(n_amostra)
        col_cor = ColunaCor(n_amostra)
        col_motivacao = ColunaMotivacao(n_amostra)
        col_sexo = ColunaSexo(n_amostra)
        col_nome = ColunaNome(n_amostra, col_sexo.valores)
        col_endereco = MultiColunaEndereco(n_amostra)
        col_ano_curso = ColunaAnoCurso(n_amostra, col_idade.valores)
        col_escola = ColunaEscola(n_amostra, col_renda.valores)
        col_cod_curso = ColunaCurso(n_amostra)

        cols_correls = [
            col_idade,
            col_renda,
            col_motivacao,
        ]
        Transformador.correlacionar(cols_correls)

        lst_logs, lst_nums, lst_bairros, lst_cids, lst_ufs, lst_ceps = \
                                                            col_endereco.valores
        map_ = {}
        map_['matrícula'] = col_matricula.valores
        map_['nome'] = col_nome.valores
        map_['idade'] = col_idade.valores
        map_['renda'] = col_renda.valores
        map_['cor'] = col_cor.valores
        map_['sexo'] = col_sexo.valores
        map_['ano_curso'] = col_ano_curso.valores
        map_['escola'] = col_escola.valores
        map_['cod_curso'] = col_cod_curso.valores

        map_['logradouro'] = lst_logs
        map_['numero'] = lst_nums
        map_['bairro'] = lst_bairros
        map_['cidade'] = lst_cids
        map_['uf'] = lst_ufs
        map_['cep'] = lst_ceps

        # Atributo alvo
        map_['motivação'] = col_motivacao.valores

        return pd.DataFrame(map_)
