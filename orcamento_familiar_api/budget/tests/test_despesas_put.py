from decimal import Decimal
from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Despesa


def test_put_outgoing(client, one_outgoing, url_base_outgoing):
    '''
    PUT: /api/v1/despesas/{id}

    Testa o comportamento quando se atualizar uma receita valida.
    Neste a receita tem que ser atualizada.
    '''

    one_outgoing.valor = Decimal('300.00')

    outgoing_json = json.dumps(one_outgoing.to_dict(id_field=False))
    response = client.put(f'{url_base_outgoing}/{one_outgoing.id}',
                          data=outgoing_json,
                          content_type='application/json')

    update_outgoing = Despesa.objects.get(id=one_outgoing.id)

    assert response.status_code == HTTPStatus.OK

    assert update_outgoing.valor == one_outgoing.valor


def test_put_outgoing_does_not_exist(client, outgoing_dict, url_base_outgoing):
    '''
    PUT: /api/v1/despesas/{id}

    Testa o comportamento quando se atualizar uma receita que não existe.
    '''

    outgoing_json = json.dumps(outgoing_dict)
    response = client.put(f'{url_base_outgoing}/{1}',
                          data=outgoing_json,
                          content_type='application/json')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_put_outgoing_to_violate_restriction(client, five_outgoings, url_base_outgoing):
    '''
    PUT: /api/v1/despesas/{id}

    Testa o comportamento quando tem atualizar uma receita valida que ira violar a restricao
    de descrição e mes unicos. Neste a receita não pode ser atualizada.
    '''

    first_outgoing_update = five_outgoings[0]
    first_outgoing_update.descricao = five_outgoings[1].descricao
    first_outgoing_update.data = five_outgoings[1].data

    outgoing_json = json.dumps(first_outgoing_update.to_dict(id_field=False))

    response = client.put(f'{url_base_outgoing}/{first_outgoing_update.id}',
                          data=outgoing_json,
                          content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT
