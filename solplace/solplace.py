import time, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


#Abre o Navegador, entra no site e clica para fazer Download
tempo_inicial = time.time()
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
chrome_options = webdriver.ChromeOptions()
driver.get("https://solplace.com.br/shop")
dados = {'Data':[],'Descrições':[],'Valores':[]}
erros = 0
tentativas = 0

hoje = datetime.datetime.now()
hoje_string = f'{hoje.day}-{hoje.month}-{hoje.year}'
while True:
    indice = 0
    n =len(driver.find_elements(By.XPATH,"//a[@itemprop='name']"))
    while indice < n:
        try:
            produto = driver.find_elements(By.XPATH,"//a[@itemprop='name']")[indice]
            nome = produto.text
            # link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(produto))
            # link.click()
            a = ActionChains(driver)
            a.move_to_element(produto).perform()
            quick_view = driver.find_element(By.XPATH,f"//*[@id='products_grid']/div/table/tbody/tr[{n}]/td/div/form/div[1]/button")
            quick_view.click()
            descricao = driver.find_element(By.XPATH,"//*[@id='product_details']/p").text
            valor = driver.find_element(By.XPATH,"//*[@id='product_details']/form/div/div[1]/h4[1]/span[1]/span").text
            dados["Valores"].append(valor)
            dados["Descrições"].append(descricao)
            dados["Data"].append(hoje_string)
            driver.back()
        except Exception as e:
            erros += 1
            print(f'Erro no Produto: {e}')
        finally:
            tentativas += 1
            indice += 1

    try:
       driver.find_element(By.XPATH,"//*[@id='wrap']/div[2]/div[1]/ul/li[9]/a").click()
    except:
        break

driver.quit()
 
# Dict to DataFrame
df = pd.DataFrame(dados)

#exporta o dataframe para um xlsx
df.to_excel(f'solplace/produtos-{hoje_string}.xlsx')
