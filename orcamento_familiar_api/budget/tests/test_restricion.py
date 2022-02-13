from datetime import datetime
from decimal import Decimal

import pytest
from orcamento_familiar_api.budget.facade import check_restricion_create, check_restricion_update
from orcamento_familiar_api.budget.models import Receita


@pytest.fixture
def income_1():
    income_1 = {
        'descricao': 'Minha receita de Teste',
        'valor': '200.00',
        'data': '2022-01-23'
    }
    return income_1


@pytest.fixture
def income_2():
    income_2 = {
        'descricao': 'Minha receita de Teste 2',
        'valor': '100.00',
        'data': '2022-01-25'
    }
    return income_2


def test_restricion_to_create(db, income_1):

    date = datetime.fromisoformat(income_1['data'])
    income_db_1 = Receita(descricao=income_1['descricao'].strip(),
                          valor=Decimal(income_1['valor']),
                          data=date,
                          mes=date.month)
    income_db_1.save()

    income_2 = income_1.copy()
    income_2['valor'] = '100'

    date = datetime.fromisoformat(income_2['data'])
    income_db_2 = Receita(descricao=income_2['descricao'].strip(),
                          valor=Decimal(income_2['valor']),
                          data=date,
                          mes=date.month)

    assert not check_restricion_create(Receita, income_db_2)


def test_restricion_to_update_same_income(db, income_1):

    date = datetime.fromisoformat(income_1['data'])
    income_db_1 = Receita(descricao=income_1['descricao'].strip(),
                          valor=Decimal(income_1['valor']),
                          data=date,
                          mes=date.month)
    income_db_1.save()

    assert check_restricion_update(Receita, income_db_1)


def test_restricion_to_update_diferent_incomes(db, income_1, income_2):

    date = datetime.fromisoformat(income_1['data'])
    income_db_1 = Receita(descricao=income_1['descricao'].strip(),
                          valor=Decimal(income_1['valor']),
                          data=date,
                          mes=date.month)
    income_db_1.save()

    date = datetime.fromisoformat(income_2['data'])
    income_db_2 = Receita(descricao=income_2['descricao'].strip(),
                          valor=Decimal(income_2['valor']),
                          data=date,
                          mes=date.month)

    income_db_2.save()

    income_1['descricao'] = income_2['descricao']

    date = datetime.fromisoformat(income_1['data'])
    income_db_1 = Receita(descricao=income_1['descricao'].strip(),
                          valor=Decimal(income_1['valor']),
                          data=date,
                          mes=date.month)

    assert not check_restricion_update(Receita, income_db_1)
