from decimal import Decimal
from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Receita


def test_put_income(client, one_income, url_base):
    '''
    PUT: /api/v1/receitas/{id}

    Testa o comportamento quando se atualizar uma receita valida.
    Neste a receita tem que ser atualizada.
    '''

    one_income.valor = Decimal('300.00')

    income_json = json.dumps(one_income.to_dict(id_field=False))
    response = client.put(f'{url_base}/{one_income.id}',
                          data=income_json,
                          content_type='application/json')

    update_income = Receita.objects.get(id=one_income.id)

    assert response.status_code == HTTPStatus.OK

    assert update_income.valor == one_income.valor


def test_put_income_does_not_exist(client, income_dict, url_base):
    '''
    PUT: /api/v1/receitas/{id}

    Testa o comportamento quando se atualizar uma receita que não existe.
    '''

    income_json = json.dumps(income_dict)
    response = client.put(f'{url_base}/{1}',
                          data=income_json,
                          content_type='application/json')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_put_income_to_violate_restriction(client, five_incomes, url_base):
    '''
    PUT: /api/v1/receitas/{id}

    Testa o comportamento quando tem atualizar uma receita valida que ira violar a restricao
    de descrição e mes unicos. Neste a receita não pode ser atualizada.
    '''

    first_income_update = five_incomes[0]
    first_income_update.descricao = five_incomes[1].descricao
    first_income_update.data = five_incomes[1].data

    income_json = json.dumps(first_income_update.to_dict(id_field=False))

    response = client.put(f'{url_base}/{first_income_update.id}',
                          data=income_json,
                          content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT
