from json import loads
from http import HTTPStatus
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from orcamento_familiar_api.budget.models import Despesa, Receita


@csrf_exempt
def receitas(request):

    if request.method == 'GET':
        income_list = Receita.objects.all()

        income_list = [{
                        'descricao': income.descricao,
                        'valor': income.valor,
                        'data': income.data
                      }
                      for income in income_list]

        data = {'list': income_list}

        return JsonResponse(data=data)

    elif request.method == 'POST':
        dict_ = loads(request.body)

        # validantion
        for key in Receita.required_fields():
            if key not in dict_:
                return JsonResponse(data={'error': f"'{key}' field is missing"},
                                    status=HTTPStatus.BAD_REQUEST)

        date = datetime.fromisoformat(dict_['data'])
        receita = Receita(descricao=dict_['descricao'].strip(),
                          valor=dict_['valor'],
                          data=dict_['data'],
                          mes=date.month)

        try:
            receita.save()
        # restriticion unique_together = ('descricao', 'mes',)
        except(IntegrityError):
            return JsonResponse(data={'error': 'Income already registered'},
                                status=HTTPStatus.CONFLICT)
        return JsonResponse(data=dict_, status=HTTPStatus.CREATED)

    return JsonResponse(data={})


def receita(request, id):

    try:
        income = Receita.objects.get(id=id)
    except(ObjectDoesNotExist):
        return JsonResponse(data={'error': f"id '{id}' does not exist"},
                            status=HTTPStatus.NOT_FOUND)

    dict_ = {
            'descricao': income.descricao,
            'valor': income.valor,
            'data': income.data
            }

    return JsonResponse(data=dict_)


@csrf_exempt
def despesas(request):
    outgoing_list = Despesa.objects.all()

    outgoing_list = [{
                      'descricao': outgoing.descricao,
                      'valor': outgoing.valor,
                      'data': outgoing.data
                     }
                     for outgoing in outgoing_list]

    data = {'list': outgoing_list}

    return JsonResponse(data=data)
