
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
    amaras = [Amara]
    ecoris = [Ecori]
    fortlevs = [Fortlev]
    ouroluxs = [Ourolux]
    solplaces = [Solplace]
    
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
        for _,row in arquivo.iterrows():
            amara = Amara(
                tipo=row['tipo'],
                marca=row['marca'],
                nome=row['nome'],
                preco=row['preço'],
                data=row['data'])
            amaras.append(amara)
        return amaras

    if dist == 'ecori':
        for _,row in arquivo.iterrows():
            ecori = Ecori(
                model_modulo=row['Modelo Modulo'],
                port_modulo=row['Pot Modulo'],
                model_inversor=row['Modelo Inversor'],
                port_inversor=row['Pot Inversor'],
                estrutura=row['Estrutura'],
                preco=row['Preco Kit'],
                data=row['Data'])
            ecoris.append(ecori)
        return ecori

    if dist == 'fortlev':
        for _,row in arquivo.iterrows():
            fortlev = Fortlev(
                potencia=row['potencia'],
                preco=row['preco'],
                modulo=row['modulo'],
                qtd_modulo=row['qtd_modulo'],
                inversor=row['inversor'],
                qtd_inversor=row['qtd_inversor'],
                estrutura=row['estrutura'],
                data=row['data'])
            fortlevs.append(fortlev)
        return fortlev
    
    if dist == 'ourolux':
        for _,row in arquivo.iterrows():
            ourolux = Ourolux(
                potencia=row['potencia'],
                preco=row['preco'],
                modulo=row['modulo'],
                qtd_modulo=row['qtd_modulo'],
                inversor=row['inversor'],
                qtd_inversor=row['qtd_inversor'],
                data=row['data'])
            ouroluxs.append(ourolux)
        return ourolux
    
    if dist == 'solplace':
        for _,row in arquivo.iterrows():
        
            solplace = Solplace(
                produto=row['produto'],
                preco=row['preco'],
                inversor=row['inversor'],
                modulo=row['modulo'],
                data=row['data'])
            solplaces.append(solplace)
        return solplace
    
main()