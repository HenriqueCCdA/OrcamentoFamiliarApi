from http import HTTPStatus
import json

from orcamento_familiar_api.budget.models import Receita


def test_income_create(client, income_dict, url_base):
    '''
    POST: /api/v1/receitas/

    Testa se um receita foi criada
    '''

    income_json = json.dumps(income_dict)
    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    #  test status code 201 and application/json from response
    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    #  test if receita was correct save in db

    receita_db = Receita.objects.filter(data=income_dict['data']).first()

    assert income_dict['descricao'] == receita_db.descricao
    assert income_dict['valor'] == str(receita_db.valor)
    assert income_dict['data'] == str(receita_db.data)


def test_income_with_missing_fields(client, income_dict, url_base):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando esta faltando um dos campos. Neste caso a receita não
    pode ser ser criada.
    '''

    for key in Receita.required_fields():
        income_with_missing_fields = income_dict.copy()
        del income_with_missing_fields[key]
        income_json = json.dumps(income_with_missing_fields)

        response = client.post(url_base,
                               data=income_json,
                               content_type='application/json')

        error = json.loads(response.content)['error']

        assert response.status_code == HTTPStatus.BAD_REQUEST  # 400
        assert error == f"'{key}' field is missing"


def test_income_create_twice_in_a_row(client, income_dict, url_base):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas iguais. Neste caso
    a segunda receita não pode ser ser criada.
    '''

    income_json = json.dumps(income_dict)
    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'income already registered'

    assert Receita.objects.count() == 1


def test_income_create_same_description_and_month(client, income_dict, url_base):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas com descricoes iguais e
    e com o mesmo mes. Neste caso a segunda receita não pode ser ser criada.
    '''

    income_json = json.dumps(income_dict)

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income_dict['data'] = '2022-01-01'
    income_json = json.dumps(income_dict)

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'income already registered'


def test_income_create_same_month_and_description_space_end(client, income_dict, url_base):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas iguais. Onde a discriação
    tem um espaço embrando a mais no final. Neste caso a segunda receita não pode ser ser
    criada.
    '''

    income_json = json.dumps(income_dict)

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income_dict['descricao'] = income_dict['descricao'] + ' '
    income_json = json.dumps(income_dict)

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'income already registered'


def test_income_create_same_description_day_and_year_but_other_month(client, income_dict, url_base):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas com a mesma descricao, dia e ano.
    Neste caso a segunda receita tem que ser criada.
    '''

    income_json = json.dumps(income_dict)

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income_dict['data'] = '2022-02-23'
    income_json = json.dumps(income_dict)

    response = client.post(url_base,
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income_list_db = Receita.objects.all()
    assert len(income_list_db) == 2
