from artefatos import Gerador, Transformador
from math import floor, ceil, log
from random import shuffle

class Coluna:

    def atualizar(self, correls):
        pass

class ColunaRenda(Coluna):

    def __init__(self, n_amostra):

        SAL_MIN = 1221.

        _classes = {
            0: {'min': 0.0, 'max': SAL_MIN / 2, 'perc': 0.038},
            1: {'min': (SAL_MIN / 2) + 0.01, 'max': SAL_MIN, 'perc': 0.226},
            2: {'min': SAL_MIN + 0.01, 'max': 2 * SAL_MIN, 'perc': 0.438},
            3: {'min': 2 * SAL_MIN + 0.01, 'max': 3 * SAL_MIN, 'perc': 0.149},
            4: {'min': 3 * SAL_MIN + 0.01, 'max': 5 * SAL_MIN, 'perc': 0.096},
            5: {'min': 5 * SAL_MIN + 0.01, 'max': 10 * SAL_MIN, 'perc': 0.037},
            6: {'min': 10 * SAL_MIN + 0.01, 'max': 20 * SAL_MIN, 'perc': 0.01},
            7: {'min': 20 * SAL_MIN + 0.01, 'max': 10 ** 6, 'perc': 0.004},
        }

        self.valores = Gerador.classes(n_amostra, _classes)
        self.min_ = min(self.valores)
        self.max_ = max(self.valores)
        self.n_amostra = n_amostra

    def atualizar(self, correls):
        vals = Transformador.rescale(correls, self.min_, self.max_)
        self.valores = [round(n, 2) for n in vals]

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

    def __init__(self, n_amostra):
        raiz = "RA55"
        self.valores = [f"{raiz}{self.__preencher_zeros(i)}{i}" \
                                                for i in range(1,n_amostra+1)]

    def __preencher_zeros(self, i):
        tam = len(str(i))
        return "0" * (6 - tam)
