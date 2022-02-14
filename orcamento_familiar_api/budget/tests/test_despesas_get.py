from http import HTTPStatus
import pytest
import json


@pytest.fixture
def response(client, url_base_outcome, db):
    return client.get(url_base_outcome)


# GET /api/v1/depesas

def test_outcome_list_type_and_status_code(one_outcome, response):
    '''
    GET: /api/v1/despesas

    Testa o estatos code e o tipo da repostas
    '''
    assert response.status_code == HTTPStatus.OK
    assert response['content-type'] == 'application/json'


def test_outcome_list_none(response):
    '''
    GET: /api/v1/despesas

    Testa quando da há despesas no banco de dados
    '''

    outcome = json.loads(response.content)['list']

    assert [] == outcome


def test_outcome_list_with_one(one_outcome, response):
    '''
    GET: /api/v1/despesas

    Testa quando quando uma despesas no banco de dados
    '''

    first_outcome = json.loads(response.content)['list'][0]

    assert one_outcome.descricao == first_outcome['descricao']
    assert str(one_outcome.valor) == first_outcome['valor']
    assert str(one_outcome.data) == first_outcome['data']


def test_outcome_list_with_five(five_outcomes, response):
    '''
    GET: /api/v1/despesas

    Testa quando quando mais de uma despesas no banco de dados
    '''

    list_outcome = json.loads(response.content)['list']

    for expect, outcome in zip(five_outcomes, list_outcome):
        assert expect.descricao == outcome['descricao']
        assert str(expect.valor) == outcome['valor']
        assert str(expect.data) == outcome['data']
