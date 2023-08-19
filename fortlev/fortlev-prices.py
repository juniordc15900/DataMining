import requests
import pandas as pd
import json
import time, datetime
# ESSE TOKEN É RECEBIDO NO LOGIN.
# PEGUEI DA REQUISIÇÃO. (É SÓ ABRIR A ABA "REDES" DO CONSOLE E PROCURAR ALGUM POST,
# LÁ CONSTA O TOKEN EM "CABEÇALHOS DA REQUISIÇÃO")

def myRange(start,end,step):
    i = start
    while i < end:
        yield i
        i += step
    yield end


hoje = datetime.datetime.now()
hoje_string = f'{hoje.day}-{hoje.month}-{hoje.year}'

erros = {}
list_data = []
for y in myRange(1,7,1):


    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzZWE3MzU4OWQ1N2E1MjFiZTRiNWM5MiIsImVtYWlsIjoiYW5kcmUuYWJyYW50ZXNAZ3JlZW5lci5jb20uYnIiLCJuYW1lIjoiQW5kcmUiLCJpbnRlZ3JhdG9yIjoiNjNlYTczNTg5ZDU3YTUyMWJlNGI1YzkwIiwiaW1hZ2UiOiIiLCJtYWluSW50ZWdyYXRvciI6dHJ1ZSwiaWF0IjoxNjgzMDUxOTU2LCJleHAiOjE2ODMxMzgzNTZ9.fkAyTmrmdKyb0Kmx6qLoT54-1mYIjAAs1Amngcnl04U"
    HEADERS = {
        "x-access-token":TOKEN,
        "Content-Type": "application/json"
    }

    URL = f'https://api.fortlevsolar.app/project/all?page={y}&rowsPerPage=10&nextPage={y}&sort=financialResume.finalPrice&active=true&madeByGenerator='

    BODY = {
        'page': y,
        'rowsPerPage': '10',
        'nextPage': y,
        'sort': 'financialResume.finalPrice',
        'active': True,
        'madeByGenerator': ''
    }

    response = requests.get(URL, headers=HEADERS, json=BODY)
    dados = response.json()
    
    for i in myRange(0,9,1):
        try:
            preco = dados['docs'][i]["financialResume"]["finalPrice"]
            print(preco)
            potencia = dados['docs'][i]["systemPower"]
            print(potencia)
            modulo = dados['docs'][i]["components"]["modules"][0]["componentInfos"]["name"]
            print(modulo)
            inversor = dados['docs'][i]["components"]["inverters"][0]["componentInfos"]["name"]
            print(inversor)
            estrutura = dados['docs'][i]["components"]["layouts"][0]["surface"]["name"]
            print(estrutura)
            data_all = [hoje_string,preco,potencia,modulo,inversor, estrutura]
            list_data.append(data_all)
        except Exception as e:
                erros.update({i: e})
   


print(list_data)    
df = pd.DataFrame(list_data, columns=['Data','Preco','Potencia', 'Modelo Modulo','Modelo Inversor','Estrutura'])

df.to_excel(f'{hoje_string}.xlsx')