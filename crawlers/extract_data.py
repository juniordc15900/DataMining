
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

    for dist in DIST_LIST:
        for _, _, arquivos in os.walk(f'crawlers/resultados-crawler/{dist}'):
            print(arquivos)
            for arquivo in arquivos:
                print(arquivo)
                if 'xlsx' in arquivo:
                    df = pd.read_excel(f'crawlers/resultados-crawler/{dist}/{arquivo}')
                    print(df)
                if 'csv' in arquivo:
                    df = pd.read_csv(f'crawlers/resultados-crawler/{dist}/{arquivo}')
                    print(df)
main()