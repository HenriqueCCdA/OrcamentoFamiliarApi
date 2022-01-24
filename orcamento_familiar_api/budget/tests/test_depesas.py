from http import HTTPStatus

import pytest
from model_bakery import baker

import json

from orcamento_familiar_api.budget.models import Despesa


@pytest.fixture
def one_outgoing(db):
    return baker.make(Despesa)


@pytest.fixture
def five_outgoing(db):
    return baker.make(Despesa, 5)


@pytest.fixture
def response_outgoing_get(client, db):
    return client.get('/api/v1/despesas')


# GET /api/v1/depesas

def test_outgoing_list_type_and_status_code(one_outgoing, response_outgoing_get):
    '''
    GET: /api/v1/despesas

    Testa o estatos code e o tipo da repostas
    '''
    response = response_outgoing_get

    assert response.status_code == HTTPStatus.OK
    assert response['content-type'] == 'application/json'


def test_outgoing_list_none(response_outgoing_get):
    '''
    GET: /api/v1/despesas

    Testa quando da há despesas no banco de dados
    '''
    response = response_outgoing_get

    outgoing = json.loads(response.content)['list']

    assert [] == outgoing


def test_outgoing_list_with_one(one_outgoing, response_outgoing_get):
    '''
    GET: /api/v1/despesas

    Testa quando quando uma despesas no banco de dados
    '''
    response = response_outgoing_get

    first_outgoing = json.loads(response.content)['list'][0]

    assert one_outgoing.descricao == first_outgoing['descricao']
    assert str(one_outgoing.valor) == first_outgoing['valor']
    assert str(one_outgoing.data) == first_outgoing['data']


def test_outgoing_list_with_five(five_outgoing, response_outgoing_get):
    '''
    GET: /api/v1/despesas

    Testa quando quando mais de uma despesas no banco de dados
    '''
    response = response_outgoing_get

    list_outgoing = json.loads(response.content)['list']

    for expect, outgoing in zip(five_outgoing, list_outgoing):
        assert expect.descricao == outgoing['descricao']
        assert str(expect.valor) == outgoing['valor']
        assert str(expect.data) == outgoing['data']
