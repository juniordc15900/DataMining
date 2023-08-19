import logging
import os
import requests
import pandas as pd
import json
import time, datetime
import sys
sys.path.append(".")

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ESSE TOKEN É RECEBIDO NO LOGIN.
# PEGUEI DA REQUISIÇÃO. (É SÓ ABRIR A ABA "REDES" DO CONSOLE E PROCURAR ALGUM POST,
# LÁ CONSTA O TOKEN EM "CABEÇALHOS DA REQUISIÇÃO")
def ecori():
    def myRange(start,end,step):
        i = start
        while i < end:
            yield i
            i += step
        yield end

    def get_driver() -> WebDriver:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()
            return driver

    hoje = datetime.datetime.now()
    hoje_string = f'{hoje.day}-{hoje.month}-{hoje.year}'
    driver = get_driver()
    driver.get('https://www.ecorionline.com.br/login')
    wait = WebDriverWait(driver, 10)
    email = wait.until(EC.presence_of_element_located((By.ID, 'email')))

    password = driver.find_element(By.ID, 'password')

    email.send_keys('andre.abrantes@greener.com.br')
    password.send_keys('123ecori')
    password.send_keys(Keys.RETURN)
    time.sleep(15)

    local_storage = driver.execute_script("return window.localStorage;")
    TOKEN = local_storage['user-token']
    HEADERS = {
        "Authorization":f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    URL = "https://www.ecorionline.com.br/graphql"
    BODY_1 = {
        "operationName":"ListarCustosKitFechadoDistribuidorAgrupado",
        "variables":
        {
            "input":
                {
                    "first":8000,
                    "offset":0,
                    "distribuidorId": 1,
                    "topologias": [
                                "microinversor",
                                "otimizador"
                                ],

                    "minPotenciaWp": None,
                    "maxPotenciaWp": None,
                    "nome": None

                }
        },
        "query":
            """query ListarCustosKitFechadoDistribuidorAgrupado($input: InputListarCustoKitFechadoDistribuidorAgrupado) {\n  listarCustosKitFechadoDistribuidorAgrupado(input: $input) {\n    id\n    codigo\n    nome\n    potenciaModulo\n    potenciaInversor\n    isHabilitado\n    custo {\n      id\n      custo\n    }\n  }\n}\n"""}




    response = requests.post(URL, headers=HEADERS, json=BODY_1)
    dados = response.json()

    new = pd.DataFrame.from_dict(dados)


    json_string = json.dumps(dados, indent = 4) 

    json_object_kit = json.loads(json_string)
    erros = {}
    id_vector = []
    for i in myRange(0,8500,1):
        
        try:
            ##print(json_object['data']['listarCustosKitFechadoDistribuidorAgrupado'][i]['id'])
            id_vector.append(json_object_kit['data']['listarCustosKitFechadoDistribuidorAgrupado'][i]['id'])
        except Exception as e:
            erros.update({i: e})
    
    


    list_data = []
    estrutura = []
    print(id_vector)

    for y in myRange(0,8500,1):
        try:
    
    

            for i in id_vector:
                estrutura = []
                if json_object_kit['data']['listarCustosKitFechadoDistribuidorAgrupado'][y]['id'] == i:
                    preco = json_object_kit['data']['listarCustosKitFechadoDistribuidorAgrupado'][y]['custo'][0]['custo']
                    pot_modulo = json_object_kit['data']['listarCustosKitFechadoDistribuidorAgrupado'][y]['potenciaModulo']
                    pot_inversor = json_object_kit['data']['listarCustosKitFechadoDistribuidorAgrupado'][y]['potenciaInversor']
                    
                
            
                else:
                    continue
                id_str = str(i)
                BODY_2 = {
                    "operationName": "VisualizarKitFechadoDistribuidor",
                    "variables": {
                        "id": i
                    },

                    "query":
                    """query VisualizarKitFechadoDistribuidor($id: ID!) {\n  visualizarKitFechadoDistribuidor(id: $id) {\n    id\n    nome\n    potenciaModulo\n    potenciaInversor\n    codigo\n    isHabilitado\n    isPermitidoCarport\n    isPermitidoCeramico\n    isPermitidoFibrocimento\n    isPermitidoLaje\n    isPermitidoShingle\n    isPermitidoMetalico\n    isPermitidoZipado\n    isPermitidoSolo\n    isPermitidoSemEstrutura\n    topologia\n    itens {\n      componente {\n        id\n        nome\n        grupoComponente {\n          id\n          nome\n        }\n      }\n      modulo {\n        id\n        modelo\n        fabricante\n      }\n      inversor {\n        id\n        modelo\n        fabricante\n      }\n      qtd\n    }\n  }\n}\n"""}

                
                

                response = requests.post(URL, headers=HEADERS, json=BODY_2)
                dados = response.json()

                json_string = json.dumps(dados, indent = 4) 

                json_object = json.loads(json_string)

                
                

                nome_kit = json_object['data']['visualizarKitFechadoDistribuidor']['nome']
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoCarport'] == True:
                    estrutura.append('Carport')
                    
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoCeramico'] == True:
                    estrutura.append('Ceramico')
                    
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoFibrocimento'] == True:
                    estrutura.append('Fibrocimento')
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoLaje'] == True:
                    estrutura.append('Laje')
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoShingle'] == True:
                    estrutura.append('Shingle')
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoMetalico'] == True:
                    estrutura.append('Metalico')
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoZipado'] == True:
                    estrutura.append('Zipado')
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoSolo'] == True:
                    estrutura.append('Solo')
                else :
                    continue
                if json_object['data']['visualizarKitFechadoDistribuidor']['isPermitidoSemEstrutura'] == True:
                    estrutura.append('Sem Estrutura')
                else :
                    continue


                #MODULO
                tipo = 'Modulo'
                modelo_modulo = json_object['data']['visualizarKitFechadoDistribuidor']['itens'][0]['modulo']['modelo']
                quantidade_modulo = json_object['data']['visualizarKitFechadoDistribuidor']['itens'][0]['qtd']
                data_modulo = [nome_kit,preco,tipo,modelo_modulo, quantidade_modulo]
                
            

                #INVERSOR
                tipo = 'Inversor'
                modelo_inversor=json_object['data']['visualizarKitFechadoDistribuidor']['itens'][2]['inversor']['modelo']
                quantidade_inversor = json_object['data']['visualizarKitFechadoDistribuidor']['itens'][2]['qtd']
                data_inversor = [nome_kit,preco,tipo,modelo_inversor,quantidade_inversor]
                
                estrutura=(','.join(estrutura))
                
                data_all = [hoje_string, modelo_modulo, pot_modulo,modelo_inversor, pot_inversor,estrutura,preco]
                
                list_data.append(data_all)
            
        except Exception as e:
            erros.update({i: e})



    logging.info(list_data)
    df = pd.DataFrame(list_data, columns=['Data','Modelo Modulo','Pot Modulo', 'Modelo Inversor','Pot Inversor','Estrutura','Preco Kit'])


    df.to_excel(os.path.join('resultados-crawler/ecori',f'ecori_{hoje_string}.csv'))
    driver.close()

ecori()