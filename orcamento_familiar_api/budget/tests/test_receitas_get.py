from http import HTTPStatus
import json

import pytest
from orcamento_familiar_api.budget.models import Receita


@pytest.fixture
def response(client, url_base, db):
    return client.get(url_base)


def test_income_list_type_and_status_code(one_income, response):
    '''
    GET: /api/v1/receitas

    Testa o estatos code e o tipo da repostas
    '''

    assert response.status_code == HTTPStatus.OK
    assert response['content-type'] == 'application/json'


def test_income_list_none(response):
    '''
    GET: /api/v1/receitas

    Testa quando da há receitas no banco de dados
    '''

    incomes = json.loads(response.content)['list']

    assert [] == incomes


def test_income_list_with_one(one_income, response):
    '''
    GET: /api/v1/receitas

    Testa quando quando uma receitas no banco de dados
    '''

    first_income = json.loads(response.content)['list'][0]

    assert one_income.descricao == first_income['descricao']
    assert str(one_income.valor) == first_income['valor']
    assert str(one_income.data) == first_income['data']


def test_income_list_with_five(five_incomes, response):
    '''
    GET: /api/v1/receitas

    Testa quando quando mais de uma receitas no banco de dados
    '''

    list_income = json.loads(response.content)['list']

    for expect, income in zip(five_incomes, list_income):
        assert expect.descricao == income['descricao']
        assert str(expect.valor) == income['valor']
        assert str(expect.data) == income['data']

# GET /api/v1/receitas/{id}


def test_income_by_id(client, five_incomes):
    '''
    GET: /api/v1/receitas/{id}

    Testa o retorno de uma receita especifica por id
    '''
    get_ids = [receita.id for receita in Receita.objects.all()]
    for i, id in enumerate(get_ids):
        response = client.get(f'/api/v1/receitas/{id}')
        income = json.loads(response.content)
        assert five_incomes[i].descricao == income['descricao']
        assert str(five_incomes[i].valor) == income['valor']
        assert str(five_incomes[i].data) == income['data']


def test_income_by_id_not_exist(client, db):
    '''
    GET: /api/v1/receitas/{id}

    Testa o retorno de uma receita especifica quando o id não existe
    '''
    response = client.get('/api/v1/receitas/2')
    content = json.loads(response.content)
    assert response.status_code == HTTPStatus.NOT_FOUND  # 404
    assert content['error'] == "id '2' does not exist"
