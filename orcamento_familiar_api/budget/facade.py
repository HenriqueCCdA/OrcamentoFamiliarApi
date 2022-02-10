from django.http import JsonResponse
from http import HTTPStatus
from django.db import IntegrityError


def save_in_db_with_restricion(obj_orm, data_in_request) -> JsonResponse:
    '''
    Salva no banco de dados com as retricoes

    param: obj_orm objeto que tentara se salvo no banco de dados
    param: data_in_request dicionario com os dados do request
    '''
    try:
        obj_orm.save()
        resp_json = JsonResponse(data=data_in_request, status=HTTPStatus.CREATED)
    # restriticion unique_together = ('descricao', 'mes',)
    except(IntegrityError):
        resp_json = JsonResponse(data={'error': 'Income already registered'},
                                 status=HTTPStatus.CONFLICT)

    return resp_json


def validation(model, data_in_request) -> str:
    '''
    Valida se existe algum campo faltando da requiscao

    param: model modelo
    param: data_in_request dicionario com os dados do request

    return: str com o dado faltando
    '''
    for key in model.required_fields():
        if key not in data_in_request:
            return f"'{key}' field is missing"

    return ''
