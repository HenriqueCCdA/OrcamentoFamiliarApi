from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Despesa


def test_outgoing_create(client, outgoing_dict, url_base_outgoing):
    '''
    POST: /api/v1/despesas/

    Testa se um receita foi criada
    '''

    outgoing_json = json.dumps(outgoing_dict)
    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    #  test status code 201 and application/json from response
    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    #  test if receita was correct save in db

    receita_db = Despesa.objects.filter(data=outgoing_dict['data']).first()

    assert outgoing_dict['descricao'] == receita_db.descricao
    assert outgoing_dict['valor'] == str(receita_db.valor)
    assert outgoing_dict['data'] == str(receita_db.data)


def test_outgoing_with_missing_fields(client, outgoing_dict, url_base_outgoing):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando esta faltando um dos campos. Neste caso a receita não
    pode ser ser criada.
    '''

    for key in Despesa.required_fields():
        outgoing_with_missing_fields = outgoing_dict.copy()
        del outgoing_with_missing_fields[key]
        outgoing_json = json.dumps(outgoing_with_missing_fields)

        response = client.post(url_base_outgoing,
                               data=outgoing_json,
                               content_type='application/json')

        error = json.loads(response.content)['error']

        assert response.status_code == HTTPStatus.BAD_REQUEST  # 400
        assert error == f"'{key}' field is missing"


def test_outgoing_create_twice_in_a_row(client, outgoing_dict, url_base_outgoing):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas iguais. Neste caso
    a segunda receita não pode ser ser criada.
    '''

    outgoing_json = json.dumps(outgoing_dict)
    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'outgoing already registered'

    assert Despesa.objects.count() == 1


def test_outgoing_create_same_description_and_month(client, outgoing_dict, url_base_outgoing):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas com descricoes iguais e
    e com o mesmo mes. Neste caso a segunda receita não pode ser ser criada.
    '''

    outgoing_json = json.dumps(outgoing_dict)

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outgoing_dict['data'] = '2022-01-01'
    outgoing_json = json.dumps(outgoing_dict)

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'outgoing already registered'


def test_outgoing_create_same_month_and_description_space_end(client, outgoing_dict, url_base_outgoing):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas iguais. Onde a discriação
    tem um espaço embrando a mais no final. Neste caso a segunda receita não pode ser ser
    criada.
    '''

    outgoing_json = json.dumps(outgoing_dict)

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outgoing_dict['descricao'] = outgoing_dict['descricao'] + ' '
    outgoing_json = json.dumps(outgoing_dict)

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'outgoing already registered'


def test_outgoing_create_same_description_day_and_year_but_other_month(client, outgoing_dict, url_base_outgoing):
    '''
    POST: /api/v1/despesas/

    Testa o comportamento quando se tenta criar duas despesas com a mesma descricao, dia e ano.
    Neste caso a segunda receita tem que ser criada.
    '''

    outgoing_json = json.dumps(outgoing_dict)

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outgoing_dict['data'] = '2022-02-23'
    outgoing_json = json.dumps(outgoing_dict)

    response = client.post(url_base_outgoing,
                           data=outgoing_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    outgoing_list_db = Despesa.objects.all()
    assert len(outgoing_list_db) == 2
