import pytest
from model_bakery import baker

from orcamento_familiar_api.budget.models import Receita, Despesa

URL_BASE = '/api/v1/receitas'


@pytest.fixture
def url_base():
    return '/api/v1/receitas'


@pytest.fixture
def url_base_outgoing():
    return '/api/v1/despesas'


@pytest.fixture
def one_income(db):
    return baker.make(Receita)


@pytest.fixture
def five_incomes(db):
    return baker.make(Receita, 5)


@pytest.fixture
def income_dict(db):
    income_dict = {
        'descricao': 'Minha receita de Teste',
        'valor': '100.00',
        'data': '2022-01-23'
    }
    return income_dict


@pytest.fixture
def one_outgoing(db):
    return baker.make(Despesa)


@pytest.fixture
def five_outgoings(db):
    return baker.make(Despesa, 5)


@pytest.fixture
def outgoing_dict(db):
    outgoing_dict = {
        'descricao': 'Minha despesa de Teste',
        'valor': '100.00',
        'data': '2022-01-23'
    }
    return outgoing_dict
