from cdia.artefatos import Gerador, Transformador
from math import floor, ceil, log
from random import shuffle, randint, choice
import json
import cdia.config as config

def ler(arquivo):
    with open(arquivo, 'r') as f:
        return f.read().split('\n')

class Coluna:

    def atualizar(self, correls):
        pass

class ColunaRenda(Coluna):
    SAL_MIN = 1221.
    CLASSES = {
        0: {'min': 0.0, 'max': SAL_MIN / 2, 'perc': 0.038},
        1: {'min': (SAL_MIN / 2) + 0.01, 'max': SAL_MIN, 'perc': 0.226},
        2: {'min': SAL_MIN + 0.01, 'max': 2 * SAL_MIN, 'perc': 0.438},
        3: {'min': 2 * SAL_MIN + 0.01, 'max': 3 * SAL_MIN, 'perc': 0.149},
        4: {'min': 3 * SAL_MIN + 0.01, 'max': 5 * SAL_MIN, 'perc': 0.096},
        5: {'min': 5 * SAL_MIN + 0.01, 'max': 10 * SAL_MIN, 'perc': 0.037},
        6: {'min': 10 * SAL_MIN + 0.01, 'max': 20 * SAL_MIN, 'perc': 0.01},
        7: {'min': 20 * SAL_MIN + 0.01, 'max': 10 ** 6, 'perc': 0.004},
    }

    def __init__(self, n_amostra):
        self.valores = Gerador.classes(n_amostra, ColunaRenda.CLASSES)
        self.min_ = min(self.valores)
        self.max_ = max(self.valores)
        self.n_amostra = n_amostra

    def atualizar(self, correls):
        vals = Transformador.rescale(correls, self.min_, self.max_)
        self.valores = [round(n, 2) for n in vals]

    def obter_nivel(renda):
        map_ = ColunaRenda.CLASSES
        for chave in map_.keys():
            if (renda >= map_[chave]['min'] and renda <= map_[chave]['max']):
                return chave

class ColunaIdade(Coluna):

    def __init__(self, n_amostra):

        classes_ = {
            0: {'min': 19, 'max': 19, 'perc': 0.355},
            1: {'min': 20, 'max': 20, 'perc': 0.29},
            2: {'min': 21, 'max': 21, 'perc': 0.16},
            3: {'min': 22, 'max': 25, 'perc': 0.13},
            4: {'min': 26 , 'max': 50, 'perc': 0.065},
        }

        self.valores = Gerador.classes(n_amostra, classes_)
        self.min_ = min(self.valores)
        self.max_ = max(self.valores)
        self.n_amostra = n_amostra

    def atualizar(self, correls):
        vals = Transformador.rescale(correls, self.min_, self.max_)
        self.valores = [int(n) for n in vals]


class ColunaCor(Coluna):

    def __init__(self, n_amostra):
        PERC_PRETOS = 0.14
        LEG_BRANCO, LEG_PRETO = 1, 2

        n_brancos = ceil(n_amostra * (1. - PERC_PRETOS))
        n_pretos = floor(n_amostra * PERC_PRETOS)

        assert(n_brancos + n_pretos == n_amostra)

        vals = []
        vals.extend([LEG_BRANCO] * n_brancos)
        vals.extend([LEG_PRETO] * n_pretos)
        shuffle(vals)
        self.valores = vals

class ColunaMotivacao(Coluna):

    def __init__(self, n_amostra):
        classes_ = {
            0: {'min': 0, 'max': 1, 'perc':  0.10},
            1: {'min': 2, 'max': 3, 'perc':  0.20},
            2: {'min': 4, 'max': 5, 'perc':  0.10},
            3: {'min': 6, 'max': 8, 'perc':  0.30},
            4: {'min': 9, 'max': 10, 'perc': 0.30},
        }
        self.valores = Gerador.classes(n_amostra, classes_)
        self.min_ = min(self.valores)
        self.max_ = max(self.valores)
        self.n_amostra = n_amostra

    def atualizar(self, correls):
        #vals = [log(n+1) for n in correls]
        #vals = Transformador.rescale(vals, self.min_, self.max_)
        #self.valores = [round(n) for n in vals]
        self.valores.reverse()

class ColunaMatricula(Coluna):
    QTDE_DIGITOS = 6
    RAIZ = "RA55"

    def __init__(self, n_amostra):
        self.valores = [f"{ColunaMatricula.RAIZ}{self.__preencher_zeros(i)}{i}" \
                                                for i in range(1,n_amostra+1)]

    def __preencher_zeros(self, i):
        tam = len(str(i))
        return "0" * (ColunaMatricula.QTDE_DIGITOS - tam)

class ColunaSexo(Coluna):
    LEG_M = 1
    LEG_F = 2

    def __init__(self, n_amostra, prop_M=.5, prop_F=.5):
        qtd_M, qtd_F = self._div(n_amostra, prop_M, prop_F)
        self.valores = []
        self.valores.extend([ColunaSexo.LEG_M] * qtd_M)
        self.valores.extend([ColunaSexo.LEG_F] * qtd_F)
        shuffle(self.valores)

    def _div(self, n_amostra, prop_M, prop_F):

        assert(prop_M + prop_F == 1.)

        qtd_M = int(n_amostra * prop_M)
        qtd_F = int(n_amostra * prop_F)

        # Se n_amostra for par
        if (qtd_M + qtd_F == n_amostra):
            return qtd_M, qtd_F
        else:
            sorteado = randint(0,1)
            qtd_M = qtd_M + sorteado
            qtd_F = qtd_F + 1 - sorteado
            return qtd_M, qtd_F

class ColunaNome(Coluna):
    LEG_M = ColunaSexo.LEG_M
    LEG_F = ColunaSexo.LEG_F

    def __init__(self, n_amostra, sexos=None):
        resources_dir = config.RESOURCES_DIR
        self.sobrenomes = ler(f'{resources_dir}sobrenomes.tsv')
        self.nomes_M = ler(f'{resources_dir}nomes-masculinos.tsv')
        self.nomes_F = ler(f'{resources_dir}nomes-femininos.tsv')
        self.valores = []
        if (sexos):
            for sexo in sexos:
                self.valores.append(self._gerar_um_nome(sexo))
        else:
            for i in range(n_amostra):
                sexo = randint(ColunaNome.LEG_M, ColunaNome.LEG_F)
                self.valores.append(self._gerar_um_nome(sexo))

    def _gerar_um_nome(self, sexo):
        nomes = self.nomes_M if (sexo == ColunaNome.LEG_M) else self.nomes_F
        nome_ = choice(nomes).title()
        qtd_sobrenomes = randint(1,3)
        sobrenome_ = ""
        for i in range(qtd_sobrenomes):
            sobrenome_ += f" {choice(self.sobrenomes).title()}"
        return f"{nome_}{sobrenome_}"

class MultiColunaEndereco(Coluna):

    def __init__(self, n_amostra):
        """
        """
        resources_dir = config.RESOURCES_DIR
        self.todos_enderecos = ler(f'{resources_dir}endereços.json')
        self.valores = []

        lst_logradouros = []
        lst_numeros = []
        lst_bairros = []
        lst_cidades = []
        lst_ufs = []
        lst_ceps = []

        for i in range(n_amostra):
            end = json.loads(choice(self.todos_enderecos))

            lst_logradouros.append( end['logradouro'] )
            lst_numeros.append( end['numero'] )
            lst_bairros.append( end['bairro'] )
            lst_cidades.append( end['cidade'] )
            lst_ufs.append( end['uf'] )
            lst_ceps.append( end['cep'] )

        self.valores = (
            lst_logradouros,
            lst_numeros,
            lst_bairros,
            lst_cidades,
            lst_ufs,
            lst_ceps,
        )

class ColunaAnoCurso(Coluna):

    def __init__(self, n_amostra, idades):
        IDADE_BASE = 16
        anos_cursos = []

        for idade in idades:
            if (idade <= IDADE_BASE):
                anos_cursos.append(1)
            elif (idade < 22):
                anos_cursos.append(idade % IDADE_BASE)
            elif (idade >= 22):
                anos_cursos.append(choice([1,2,3,4,5]))
        self.valores = anos_cursos

class ColunaEscola(Coluna):
    LEG_PUBL = 1
    LEG_PART = 2

    def __init__(self, n_amostra, rendas):

        self.valores = []
        for renda in rendas:
            nivel = ColunaRenda.obter_nivel(renda)
            if (nivel < 2):
                self.valores.append(ColunaEscola.LEG_PUBL)
            elif (nivel >= 2 and nivel <= 5):
                sorteado = choice([
                            ColunaEscola.LEG_PUBL, 
                            ColunaEscola.LEG_PART,
                            ColunaEscola.LEG_PART,
                ])
                self.valores.append(sorteado)
            elif (nivel > 5):
                self.valores.append(ColunaEscola.LEG_PART)
