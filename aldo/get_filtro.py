import requests, json
def get_filtro():
    url = 'https://www.aldo.com.br/wcf/Produto.svc/getfiltrosporsegmento'
    body = {
        "slug":"energia-solar",
        "origem":"categoria",
        "filtroAtributos":None,
        "idAcionado":None,
        "filterId":None}
    response = requests.post(url,json=body)
    data = json.loads(response.content)
    filtro = data['FilterId']
    registros = data['TotalRegistros']
    print(f'filtro: {filtro}, itens: {registros}')
    return filtro
