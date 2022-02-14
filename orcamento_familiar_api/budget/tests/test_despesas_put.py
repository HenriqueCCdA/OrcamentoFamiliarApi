from decimal import Decimal
from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Despesa


def test_put_outcome(client, one_outcome, url_base_outcome):
    '''
    PUT: /api/v1/despesas/{id}

    Testa o comportamento quando se atualizar uma receita valida.
    Neste a receita tem que ser atualizada.
    '''

    one_outcome.valor = Decimal('300.00')

    outcome_json = json.dumps(one_outcome.to_dict(id_field=False))
    response = client.put(f'{url_base_outcome}/{one_outcome.id}',
                          data=outcome_json,
                          content_type='application/json')

    update_outcome = Despesa.objects.get(id=one_outcome.id)

    assert response.status_code == HTTPStatus.OK

    assert update_outcome.valor == one_outcome.valor


def test_put_outcome_does_not_exist(client, outcome_dict, url_base_outcome):
    '''
    PUT: /api/v1/despesas/{id}

    Testa o comportamento quando se atualizar uma receita que não existe.
    '''

    outcome_json = json.dumps(outcome_dict)
    response = client.put(f'{url_base_outcome}/{1}',
                          data=outcome_json,
                          content_type='application/json')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_put_outcome_to_violate_restriction(client, five_outcomes, url_base_outcome):
    '''
    PUT: /api/v1/despesas/{id}

    Testa o comportamento quando tem atualizar uma receita valida que ira violar a restricao
    de descrição e mes unicos. Neste a receita não pode ser atualizada.
    '''

    first_outcome_update = five_outcomes[0]
    first_outcome_update.descricao = five_outcomes[1].descricao
    first_outcome_update.data = five_outcomes[1].data

    outcome_json = json.dumps(first_outcome_update.to_dict(id_field=False))

    response = client.put(f'{url_base_outcome}/{first_outcome_update.id}',
                          data=outcome_json,
                          content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT
