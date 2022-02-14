import pytest
from model_bakery import baker

from orcamento_familiar_api.budget.models import Receita

URL_BASE = '/api/v1/receitas'


@pytest.fixture
def url_base():
    return URL_BASE


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
