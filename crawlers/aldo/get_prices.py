import requests
import json
import pandas as pd
import time, datetime
from datetime import datetime
import sys
sys.path.append(".")
from aldo.adjust import adjust
from aldo.get_filtro import get_filtro

url = 'https://www.aldo.com.br/wcf/Produto.svc/getprodutosporsegmentonotlogin'
number_of_pages = 90
produtos = []
erros = {}

for i in range(number_of_pages):
    try:
        body = {
            "filtroAtributos":None,
            "offset":i,
            "filterId":get_filtro(),
            "orderby":"2"}
        response = requests.post(url,json=body)
        data = json.loads(response.content)
        infos = [{'Nome':p['psg_descricao'], 'Descrição':p['prd_descricao'],'Preço':p['prd_preco']} for p in data]
        produtos.extend(infos)
        print (i)
    except Exception as e:
        erros.update({i: e})


df = pd.DataFrame(produtos)

#exporta o dataframe para um xlsx
df.to_excel('aldo/aldo_produtos.xlsx')
adjust()
