import pytest
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


def test_restriction_to_create(db, income_1):

    income_db_1 = Receita.dict_to_model(income_1)
    income_db_1.save()

    income_2 = income_1.copy()
    income_2['valor'] = '100'

    income_db_2 = Receita.dict_to_model(income_2)

    assert not income_db_2.check_restriction_create()


def test_restriction_to_update_same_income(db, income_1):

    income_db_1 = Receita.dict_to_model(income_1)

    income_db_1.save()

    assert income_db_1.check_restriction_update()


def test_restricion_to_update_diferent_incomes(db, income_1, income_2):

    income_db_1 = Receita.dict_to_model(income_1)
    income_db_1.save()

    income_db_2 = Receita.dict_to_model(income_2)
    income_db_2.save()

    income_1['descricao'] = income_2['descricao']
    income_db_1 = Receita.dict_to_model(income_1)

    assert not income_db_1.check_restriction_update()
