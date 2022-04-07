Gerador de Datasets
========

.. image:: https://img.shields.io/pypi/v/cdia3.svg
    :target: https://pypi.python.org/pypi/cdia3
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/kragniz/cookiecutter-pypackage-minimal.png
   :target: https://travis-ci.org/kragniz/cookiecutter-pypackage-minimal
   :alt: Latest Travis CI build status

Este projeto implementa um gerador de dados aleatórios para estudantes do ensino superior no Brasil.

Instalação
------------

Clone o repositório e instale com o pip::

  git clone git@github.com:j3ffsilva/gerador-datasets-estudantes.git
  cd gerador-datasets-estudantes/
  pip install .


Uso
-----

Para usar o gerador::

  from cdia.datasets import DatasetEstudantes
  n_amostra = 10

  #  O método criar retorna um DataFrame (Pandas)
  df = DatasetEstudantes.criar(n_amostra)

Authors
-------

Este projeto foi escrito por `Jeff <silvajo@pucsp.br>`_.
