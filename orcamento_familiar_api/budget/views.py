from django.http import JsonResponse

from orcamento_familiar_api.budget.models import Despesa, Receita


def receitas(request):
    income_list = Receita.objects.all()

    income_list = [{
                    'descricao': income.descricao,
                    'valor': income.valor,
                    'data': income.data
                   }
                   for income in income_list]

    data = {'list': income_list}

    return JsonResponse(data=data)


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
