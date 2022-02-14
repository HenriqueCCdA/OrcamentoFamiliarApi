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
