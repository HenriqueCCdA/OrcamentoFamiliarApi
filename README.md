# OrcamentoFamiliarApi

![](https://img.shields.io/github/last-commit/HenriqueCCdA/DesenvolvimentoWeb?style=plasti&ccolor=blue)
![](https://img.shields.io/badge/Autor-Henrique%20C%20C%20de%20Andrade-blue)

Criando o ambiente virtual

```console
python -m venv .venv --upgrade-deps
```

Instalando o pip-tools

```console
pip install pip-tools
```

Gerando o requirements.txt

```console
pip-compile .\requirements.in
pip-compile .\requirements-dev.in
```

Instalando a dependecias

```console
pip install -r .\requirements-dev.txt
```
