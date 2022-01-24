from http import HTTPStatus

import pytest
from model_bakery import baker
import json

from orcamento_familiar_api.budget.models import Receita


@pytest.fixture
def one_income(db):
    return baker.make(Receita)


@pytest.fixture
def five_incomes(db):
    return baker.make(Receita, 5)


@pytest.fixture
def response_incomes_get(client, db):
    return client.get('/api/v1/receitas')

# GET /api/v1/receitas


def test_income_list_type_and_status_code(one_income, response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa o estatos code e o tipo da repostas
    '''
    response = response_incomes_get

    assert response.status_code == HTTPStatus.OK
    assert response['content-type'] == 'application/json'


def test_income_list_none(response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa quando da há receitas no banco de dados
    '''
    response = response_incomes_get

    incomes = json.loads(response.content)['list']

    assert [] == incomes


def test_income_list_with_one(one_income, response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa quando quando uma receitas no banco de dados
    '''
    response = response_incomes_get

    first_income = json.loads(response.content)['list'][0]

    assert one_income.descricao == first_income['descricao']
    assert str(one_income.valor) == first_income['valor']
    assert str(one_income.data) == first_income['data']


def test_income_list_with_five(five_incomes, response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa quando quando mais de uma receitas no banco de dados
    '''
    response = response_incomes_get

    list_income = json.loads(response.content)['list']

    for expect, income in zip(five_incomes, list_income):
        assert expect.descricao == income['descricao']
        assert str(expect.valor) == income['valor']
        assert str(expect.data) == income['data']
