
import pandas as pd
import os
import sys
sys.path.append(".")
from crawlers.domain.aldo import Aldo
from crawlers.domain.amara import Amara
from crawlers.domain.ecori import Ecori
from crawlers.domain.fortlev import Fortlev
from crawlers.domain.ourolux import Ourolux
from crawlers.domain.solplace import Solplace

DIST_LIST = ['aldo','amara','ecori','fortlev','ourolux','solplace']

def main():
    # teste = ''
    # for dist in DIST_LIST:
    #     for _, _, arquivos in os.walk(f'crawlers/resultados-crawler/{dist}'):
    #         print(arquivos)
    #         for arquivo in arquivos:
    #             print(arquivo)
    #             if 'xlsx' in arquivo:
    #                 df = pd.read_excel(f'crawlers/resultados-crawler/{dist}/{arquivo}')
    #                 result = format(dist,df)
    #                 teste = result
    #             if 'csv' in arquivo:
    #                 df = pd.read_csv(f'crawlers/resultados-crawler/{dist}/{arquivo}')
    #                 result = format(dist,df)
    #                 teste = result
                    
    df = pd.read_excel(f'crawlers/resultados-crawler/aldo/aldo_produtos_2023-08-18.xlsx')
    result= format('aldo', df)
    for aldo in result[1:]:
        print("Nome:", aldo.nome)
        print("Descrição:", aldo.descricao)
        print("Preço:", aldo.preco)
        print("Data:", aldo.data)


                    
                    
def format(dist,arquivo):
    aldos = [Aldo]
    if dist == 'aldo':
        for _,row in arquivo.iterrows():
            aldo = Aldo(
                nome=row['Nome'],
                descricao=row['Descrição'],
                preco=row['Preço'],
                data=row['Data'])
            aldos.append(aldo)
        return aldos
    
    if dist == 'amara':
        amara = Amara(
            tipo=arquivo['tipo'],
            marca=arquivo['marca'],
            nome=arquivo['nome'],
            preco=arquivo['preço'],
            data=arquivo['data'])
        return amara

    if dist == 'ecori':
        ecori = Ecori(
            model_modulo=arquivo['Modelo Modulo'],
            port_modulo=arquivo['Pot Modulo'],
            model_inversor=arquivo['Modelo Inversor'],
            port_inversor=arquivo['Pot Inversor'],
            estrutura=arquivo['Estrutura'],
            preco=arquivo['Preco Kit'],
            data=arquivo['Data'])
        return ecori

    if dist == 'fortlev':
        fortlev = Fortlev(
            potencia=arquivo['potencia'],
            preco=arquivo['preco'],
            modulo=arquivo['modulo'],
            qtd_modulo=arquivo['qtd_modulo'],
            inversor=arquivo['inversor'],
            qtd_inversor=arquivo['qtd_inversor'],
            estrutura=arquivo['estrutura'],
            data=arquivo['data'])
        return fortlev
    
    if dist == 'ourolux':
        ourolux = Ourolux(
            potencia=arquivo['potencia'],
            preco=arquivo['preco'],
            modulo=arquivo['modulo'],
            qtd_modulo=arquivo['qtd_modulo'],
            inversor=arquivo['inversor'],
            qtd_inversor=arquivo['qtd_inversor'],
            data=arquivo['data'])
        return ourolux
    
    if dist == 'solplace':
        solplace = Solplace(
            produto=arquivo['produto'],
            preco=arquivo['preco'],
            inversor=arquivo['inversor'],
            modulo=arquivo['modulo'],
            data=arquivo['data'])
        return solplace
    
main()