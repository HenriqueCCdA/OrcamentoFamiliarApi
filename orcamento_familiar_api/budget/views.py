from django.views.decorators.csrf import csrf_exempt

from orcamento_familiar_api.budget.facade import get_post, get_put_delete
from orcamento_familiar_api.budget.models import Despesa, Receita


@csrf_exempt
def receitas(request):
    return get_post(request, Receita)


@csrf_exempt
def receita(request, id):
    return get_put_delete(request, Receita, id)


@csrf_exempt
def despesas(request):
    return get_post(request, Despesa)


@csrf_exempt
def despesa(request, id):
    return get_put_delete(request, Despesa, id)
