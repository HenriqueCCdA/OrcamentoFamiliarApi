from datetime import datetime
from decimal import Decimal
from http import HTTPStatus
from json import loads

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


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


def get_post(request, model):

    if request.method == 'GET':

        income_list = [income.to_dict() for income in model.objects.all()]

        data = {'list': income_list}

        return JsonResponse(data=data)

    elif request.method == 'POST':
        dict_ = loads(request.body)

        error = validation(model, dict_)

        if not error:
            income = model.dict_to_model(dict_)

            if income.check_restriction_create():
                income.save()
                return JsonResponse(data=dict_, status=HTTPStatus.CREATED)
            else:
                return JsonResponse(data={'error': f'{model.budget_type()} already registered'},
                                    status=HTTPStatus.CONFLICT)

        else:
            return JsonResponse(data={'error': error}, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse(data={}, status=HTTPStatus.BAD_REQUEST)


def get_put_delete(request, model, id):
    if request.method in ('GET', 'DELETE', 'PUT'):
        try:
            income = model.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse(data={'error': f"id '{id}' does not exist"},
                                status=HTTPStatus.NOT_FOUND)

        if request.method == 'DELETE':
            income.delete()
            return JsonResponse(data=income.to_dict(False))

        if request.method == 'PUT':
            dict_ = loads(request.body)

            error = validation(model, dict_)

            if not error:
                income.descricao = dict_['descricao'].strip()
                income.valor = Decimal(dict_['valor'])
                income.data = datetime.fromisoformat(dict_['data'])

                if income.check_restriction_update():
                    income.save()
                    return JsonResponse(data=dict_, status=HTTPStatus.OK)
                else:
                    return JsonResponse(data={'error': f'{model.budget_type()} already registered'},
                                        status=HTTPStatus.CONFLICT)

        return JsonResponse(data=income.to_dict())

    return JsonResponse(data={}, status=HTTPStatus.BAD_REQUEST)
