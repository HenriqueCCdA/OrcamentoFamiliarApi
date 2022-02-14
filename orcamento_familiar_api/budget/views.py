from decimal import Decimal
from json import loads
from http import HTTPStatus
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from orcamento_familiar_api.budget.facade import validation
from orcamento_familiar_api.budget.models import Despesa, Receita


@csrf_exempt
def receitas(request):

    if request.method == 'GET':

        income_list = [income.to_dict() for income in Receita.objects.all()]

        data = {'list': income_list}

        return JsonResponse(data=data)

    elif request.method == 'POST':
        dict_ = loads(request.body)

        error = validation(Receita, dict_)

        if not error:
            income = Receita.dict_to_model(dict_)

            if income.check_restriction_create():
                income.save()
                return JsonResponse(data=dict_, status=HTTPStatus.CREATED)
            else:
                return JsonResponse(data={'error': 'Income already registered'},
                                    status=HTTPStatus.CONFLICT)

        else:
            return JsonResponse(data={'error': error}, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse(data={}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
def receita(request, id):

    if request.method in ('GET', 'DELETE', 'PUT'):
        try:
            income = Receita.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse(data={'error': f"id '{id}' does not exist"},
                                status=HTTPStatus.NOT_FOUND)

        if request.method == 'DELETE':
            income.delete()
            return JsonResponse(data=income.to_dict(False))

        if request.method == 'PUT':
            dict_ = loads(request.body)

            error = validation(Receita, dict_)

            if not error:
                income.descricao = dict_['descricao'].strip()
                income.valor = Decimal(dict_['valor'])
                income.data = datetime.fromisoformat(dict_['data'])

                if income.check_restriction_update():
                    income.save()
                    return JsonResponse(data=dict_, status=HTTPStatus.OK)
                else:
                    return JsonResponse(data={'error': 'Income already registered'},
                                        status=HTTPStatus.CONFLICT)

        return JsonResponse(data=income.to_dict())

    return JsonResponse(data={}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
def despesas(request):

    outgoing_list = [outgoing.to_dict() for outgoing in Despesa.objects.all()]

    data = {'list': outgoing_list}

    return JsonResponse(data=data)
