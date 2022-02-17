from http import HTTPStatus
import pytest
import json


@pytest.fixture
def response(client, url_base_outgoing, db):
    return client.get(url_base_outgoing)


# GET /api/v1/depesas

def test_outgoing_list_type_and_status_code(one_outgoing, response):
    '''
    GET: /api/v1/despesas

    Testa o estatos code e o tipo da repostas
    '''
    assert response.status_code == HTTPStatus.OK
    assert response['content-type'] == 'application/json'


def test_outgoing_list_none(response):
    '''
    GET: /api/v1/despesas

    Testa quando da há despesas no banco de dados
    '''

    outgoing = json.loads(response.content)['list']

    assert [] == outgoing


def test_outgoing_list_with_one(one_outgoing, response):
    '''
    GET: /api/v1/despesas

    Testa quando quando uma despesas no banco de dados
    '''

    first_outgoing = json.loads(response.content)['list'][0]

    assert one_outgoing.descricao == first_outgoing['descricao']
    assert str(one_outgoing.valor) == first_outgoing['valor']
    assert str(one_outgoing.data) == first_outgoing['data']


def test_outgoing_list_with_five(five_outgoings, response):
    '''
    GET: /api/v1/despesas

    Testa quando quando mais de uma despesas no banco de dados
    '''

    list_outgoing = json.loads(response.content)['list']

    for expect, outgoing in zip(five_outgoings, list_outgoing):
        assert expect.descricao == outgoing['descricao']
        assert str(expect.valor) == outgoing['valor']
        assert str(expect.data) == outgoing['data']
