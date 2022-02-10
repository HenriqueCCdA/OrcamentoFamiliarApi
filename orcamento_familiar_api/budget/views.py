from json import loads
from http import HTTPStatus
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from orcamento_familiar_api.budget.facade import save_in_db_with_restricion, validation
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
            date = datetime.fromisoformat(dict_['data'])
            receita = Receita(descricao=dict_['descricao'].strip(),
                              valor=dict_['valor'],
                              data=dict_['data'],
                              mes=date.month)

            resp_json = save_in_db_with_restricion(receita, dict_)

            return resp_json
        else:
            return JsonResponse(data={'error': error}, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse(data={})


def receita(request, id):

    try:
        income = Receita.objects.get(id=id)
    except(ObjectDoesNotExist):
        return JsonResponse(data={'error': f"id '{id}' does not exist"},
                            status=HTTPStatus.NOT_FOUND)

    return JsonResponse(data=income.to_dict())


@csrf_exempt
def despesas(request):

    outgoing_list = [outgoing.to_dict() for outgoing in Despesa.objects.all()]

    data = {'list': outgoing_list}

    return JsonResponse(data=data)
