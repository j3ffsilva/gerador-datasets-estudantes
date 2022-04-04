import numpy as np
from copy import copy
from scipy.stats import skewnorm
import statistics

linalg = np.linalg
np.random.seed(1)

class Gerador:

    def obter_cov(n):
        """
        """
        cov = []
        l = [(i+1)/10 for i in range(n)]
        for i in range(n):
            cov.append(copy(l))
        cov[0].reverse()
        return cov

    def correlacionados(n_var, n_amostra, nao_correls=None):
        """
        Gera n_var distribuições correlacionadas
        Args:
            n_var: Número de variáveis (colunas)
        """
        cov = Gerador.obter_cov(n_var)
        eigenvs = np.linalg.eigvalsh(cov)
        # Soma os valores negativos
        soma_negs = sum([n for n in eigenvs if n < 0])
        if (soma_negs < 0):
            raise Exception("COV com valores negativos")

        L = linalg.cholesky(cov)
        if (not nao_correls):
            nao_correls = np.random.standard_normal((n_var, n_amostra))
        medias = [1 for n in range(n_var)]
        correls = np.dot(L, nao_correls) + np.array(medias).reshape(n_var, 1)
        return correls

    def assimetricos(a, n_amostra):
        return skewnorm.rvs(a, size=n_amostra)

    def aleatoriosint(min_, max_, n_amostra):
        return np.random.randint(min_, max_+1, n_amostra)

    def classes(n_amostra, classes_):
        n_classes = len(classes_)
        distrib = []
        for k in range(n_classes):
            min_ = classes_[k]['min']
            max_ = classes_[k]['max']
            qtde = round(n_amostra * classes_[k]['perc'])
            distrib.extend(np.random.randint(min_, max_+1, qtde))

        while (len(distrib) > n_amostra):
            k = np.random.randint(0, len(distrib), 1)[0]
            distrib.pop(k)

        menor = classes_[0]['min']
        maior = classes_[n_classes-1]['max']
        while (len(distrib) < n_amostra):
            sorteado = np.random.randint(menor, maior+1, 1)[0]
            distrib.append(sorteado)

        return distrib

# ==============================================================================
class Transformador:

    def coefs(dist, novo_min, novo_max):
        """
        Encontra os coeficientes para reescalar a distribuição
        Args:
            dist: Uma distribuição. Ex: [1,5,10]
            novo_min: o novo mínimo da distribuição reescalada
            novo_max: o novo máximo da distribuição reescalada
        Retorna
            A: o quociente multiplicador de cada elemento da distribuição
            b: o fator a ser somado após a múltiplicação
        """
        velho_min, velho_max = min(dist), max(dist)
        A = np.array([[velho_min, 1], [velho_max, 1]])
        b = np.array([float(novo_min), float(novo_max)])
        return np.linalg.solve(A, b)

    def rescale(dist, novo_min, novo_max):
        a, b = Transformador.coefs(dist, novo_min, novo_max)
        return [a * x + b for x in dist]

    def normalizar(dist):
        min_, max_ = min(dist), max(dist)
        return [(x - min_) / (max_ - min_) for x in dist]

    def padronizar(dist):
        s = statistics.stdev(dist)
        m = statistics.mean(dist)
        return [(x - m) / s for x in dist]

    def correlacionar(colunas):
        n_vars = len(colunas)
        nao_correls = []
        for col in colunas:
            nao_correls.append(col.valores)
            n_amostra = col.n_amostra

        correls = Gerador.correlacionados(n_vars, n_amostra, nao_correls)

        for i in range(n_vars):
            col = colunas[i]
            col.atualizar(correls[i])
