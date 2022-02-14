from datetime import datetime
from decimal import Decimal
from orcamento_familiar_api.budget.models import Receita


def test_parser_dict_to_model(income_dict):
    income = Receita.dict_to_model(income_dict)

    assert income.descricao == income_dict['descricao']
    assert income.valor == Decimal(income_dict['valor'])
    assert income.data == datetime.fromisoformat(income_dict['data'])
