from http import HTTPStatus
from django.db import transaction

import pytest
from model_bakery import baker
import json

from orcamento_familiar_api.budget.models import Receita


@pytest.fixture
def one_income(db):
    return baker.make(Receita)


@pytest.fixture
def five_incomes(db):
    return baker.make(Receita, 5)


@pytest.fixture
def response_incomes_get(client, db):
    return client.get('/api/v1/receitas')

# GET /api/v1/receitas


def test_income_list_type_and_status_code(one_income, response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa o estatos code e o tipo da repostas
    '''
    response = response_incomes_get

    assert response.status_code == HTTPStatus.OK
    assert response['content-type'] == 'application/json'


def test_income_list_none(response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa quando da há receitas no banco de dados
    '''
    response = response_incomes_get

    incomes = json.loads(response.content)['list']

    assert [] == incomes


def test_income_list_with_one(one_income, response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa quando quando uma receitas no banco de dados
    '''
    response = response_incomes_get

    first_income = json.loads(response.content)['list'][0]

    assert one_income.descricao == first_income['descricao']
    assert str(one_income.valor) == first_income['valor']
    assert str(one_income.data) == first_income['data']


def test_income_list_with_five(five_incomes, response_incomes_get):
    '''
    GET: /api/v1/receitas

    Testa quando quando mais de uma receitas no banco de dados
    '''
    response = response_incomes_get

    list_income = json.loads(response.content)['list']

    for expect, income in zip(five_incomes, list_income):
        assert expect.descricao == income['descricao']
        assert str(expect.valor) == income['valor']
        assert str(expect.data) == income['data']

# GET /api/v1/receitas/{id}


def test_income_by_id(client, five_incomes):
    '''
    GET: /api/v1/receitas/{id}

    Testa o retorno de uma receita especifica por id
    '''
    get_ids = [receita.id for receita in Receita.objects.all()]
    for i, id in enumerate(get_ids):
        response = client.get(f'/api/v1/receitas/{id}')
        income = json.loads(response.content)
        assert five_incomes[i].descricao == income['descricao']
        assert str(five_incomes[i].valor) == income['valor']
        assert str(five_incomes[i].data) == income['data']


def test_income_by_id_not_exist(client, income):
    '''
    GET: /api/v1/receitas/{id}

    Testa o retorno de uma receita especifica quando o id não existe
    '''
    response = client.get('/api/v1/receitas/2')
    content = json.loads(response.content)
    assert response.status_code == HTTPStatus.NOT_FOUND  # 404
    assert content['error'] == "id '2' does not exist"


# POST /api/v1/receitas


@pytest.fixture
def income(db):
    income = {
        'descricao': 'Minha receita de Teste',
        'valor': '100.00',
        'data': '2022-01-23'
    }
    return income


def test_income_create(client, income):
    '''
    POST: /api/v1/receitas/

    Testa se um receita foi criada
    '''

    income_json = json.dumps(income)
    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    #  test status code 201 and application/json from response
    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    #  test if receita was correct save in db

    receita_db = Receita.objects.filter(data=income['data']).first()

    assert income['descricao'] == receita_db.descricao
    assert income['valor'] == str(receita_db.valor)
    assert income['data'] == str(receita_db.data)


def test_income_with_missing_fields(client, income):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando esta faltando um dos campos. Neste caso a receita não
    pode ser ser criada.
    '''

    for key in Receita.required_fields():
        income_with_missing_fields = income.copy()
        del income_with_missing_fields[key]
        income_json = json.dumps(income_with_missing_fields)

        response = client.post('/api/v1/receitas',
                               data=income_json,
                               content_type='application/json')

        error = json.loads(response.content)['error']

        assert response.status_code == HTTPStatus.BAD_REQUEST  # 400
        assert error == f"'{key}' field is missing"


def test_income_create_twice_in_a_row(client, income):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas iguais. Neste caso
    a segunda receita não pode ser ser criada.
    '''

    income_json = json.dumps(income)
    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    with transaction.atomic():
        response = client.post('/api/v1/receitas',
                               data=income_json,
                               content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'Income already registered'

    assert Receita.objects.count() == 1


def test_income_create_same_description_and_month(client, income):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas com descricoes iguais e
    e com o mesmo mes. Neste caso a segunda receita não pode ser ser criada.
    '''

    income_json = json.dumps(income)

    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income['data'] = '2022-01-01'
    income_json = json.dumps(income)

    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'Income already registered'


def test_income_create_same_month_and_description_space_end(client, income):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas iguais. Onde a discriação
    tem um espaço embrando a mais no final. Neste caso a segunda receita não pode ser ser
    criada.
    '''

    income_json = json.dumps(income)

    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income['descricao'] = income['descricao'] + ' '
    income_json = json.dumps(income)

    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CONFLICT  # 409
    assert response['content-type'] == 'application/json'

    error = json.loads(response.content)['error']
    assert error == 'Income already registered'


def test_income_create_same_description_day_and_year_but_other_month(client, income):
    '''
    POST: /api/v1/receitas/

    Testa o comportamento quando se tenta criar duas receitas com a mesma descricao, dia e ano.
    Neste caso a segunda receita tem que ser criada.
    '''

    income_json = json.dumps(income)

    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income['data'] = '2022-02-23'
    income_json = json.dumps(income)

    response = client.post('/api/v1/receitas',
                           data=income_json,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response['content-type'] == 'application/json'

    income_list_db = Receita.objects.all()
    assert len(income_list_db) == 2
