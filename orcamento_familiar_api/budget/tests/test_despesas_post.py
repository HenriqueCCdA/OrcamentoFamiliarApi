from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Despesa


def test_outcome_create(client, outcome_dict, url_base_outcome):
    '''
    POST: /api/v1/despesas/

    Testa se um receita foi criada
    '''

    outcome_json = json.dumps(outcome_dict)
    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    #  test status code 201 and application/json from response
    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    #  test if receita was correct save in db

    receita_db = Despesa.objects.filter(data=outcome_dict['data']).first()

    assert outcome_dict['descricao'] == receita_db.descricao
    assert outcome_dict['valor'] == str(receita_db.valor)
    assert outcome_dict['data'] == str(receita_db.data)


def test_outcome_with_missing_fields(client, outcome_dict, url_base_outcome):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando esta faltando um dos campos. Neste caso a receita não
    pode ser ser criada.
    '''

    for key in Despesa.required_fields():
        outcome_with_missing_fields = outcome_dict.copy()
        del outcome_with_missing_fields[key]
        outcome_json = json.dumps(outcome_with_missing_fields)

        response = client.post(url_base_outcome,
                               data=outcome_json,
                               content_type='application/json')

        error = json.loads(response.content)['error']

        assert response.status_code == HTTPStatus.BAD_REQUEST  # 400
        assert error == f"'{key}' field is missing"


def test_outcome_create_twice_in_a_row(client, outcome_dict, url_base_outcome):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas iguais. Neste caso
    a segunda receita não pode ser ser criada.
    '''

    outcome_json = json.dumps(outcome_dict)
    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'outcome already registered'

    assert Despesa.objects.count() == 1


def test_outcome_create_same_description_and_month(client, outcome_dict, url_base_outcome):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas com descricoes iguais e
    e com o mesmo mes. Neste caso a segunda receita não pode ser ser criada.
    '''

    outcome_json = json.dumps(outcome_dict)

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outcome_dict['data'] = '2022-01-01'
    outcome_json = json.dumps(outcome_dict)

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'outcome already registered'


def test_outcome_create_same_month_and_description_space_end(client, outcome_dict, url_base_outcome):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas iguais. Onde a discriação
    tem um espaço embrando a mais no final. Neste caso a segunda receita não pode ser ser
    criada.
    '''

    outcome_json = json.dumps(outcome_dict)

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outcome_dict['descricao'] = outcome_dict['descricao'] + ' '
    outcome_json = json.dumps(outcome_dict)

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'outcome already registered'


def test_outcome_create_same_description_day_and_year_but_other_month(client, outcome_dict, url_base_outcome):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas com a mesma descricao, dia e ano.
    Neste caso a segunda receita tem que ser criada.
    '''

    outcome_json = json.dumps(outcome_dict)

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outcome_dict['data'] = '2022-02-23'
    outcome_json = json.dumps(outcome_dict)

    response = client.post(url_base_outcome,
                           data=outcome_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outcome_list_db = Despesa.objects.all()
    assert len(outcome_list_db) == 2
