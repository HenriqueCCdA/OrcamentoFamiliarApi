from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Receita


# DELETE /api/v1/receitas/{id}

# URL_BASE = '/api/v1/receitas'


def test_delete_income(client, one_income, url_base):
    '''
    DELETE: /api/v1/receitas/{id}

    Testa o comportamento quando se tenta deletar uma receita existente. Neste a receita vai ser deletada.
    '''

    response = client.delete(f'{url_base}/{one_income.id}')

    income_response = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK

    assert 0 == len(Receita.objects.all())

    assert one_income.descricao == income_response['descricao']
    assert str(one_income.valor) == income_response['valor']
    assert str(one_income.data) == income_response['data']


def test_delete_income_doesnt_exist_id(client, one_income, url_base):
    '''
    DELETE: /api/v1/receitas/{id}

    Testa o comportamento quando se tenta deletar uma receita não existente. Neste nada ira acontecer.
    '''

    one_income.id += 1

    response = client.delete(f'{url_base}/{one_income.id}')

    income_response = json.loads(response.content)

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert f"id '{one_income.id}' does not exist" == income_response['error']
