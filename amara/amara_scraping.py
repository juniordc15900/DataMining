import time
import csv
from datetime import datetime
import sys
sys.path.append(".")
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from controller import controller



result = []
    
def get_products(driver,wait,url):
    driver.get(url)
    products = controller(driver,url[30:])
    return products


def get_driver() -> WebDriver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        return driver



#selenium LOGIN
inicio = time.time()
driver = get_driver()
driver.get('https://app.amaranzero.com.br/login?returnUrl')
wait = WebDriverWait(driver, 10)

email = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/div/section/div/div[2]/div/div[2]/div/div/form/div[1]/label/div/input')))
password =  wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/div/section/div/div[2]/div/div[2]/div/div/form/div[2]/div/label/div/input')))


email.send_keys('andre.abrantes@greener.com.br')
password.send_keys('#123Amara')
password.send_keys(Keys.RETURN)
print('Login Efetuado')

time.sleep(5)


urls = [
        # 'https://app.amaranzero.com.br/inversor',
        'https://app.amaranzero.com.br/modulo',
        # 'https://app.amaranzero.com.br/microinversor',
        # 'https://app.amaranzero.com.br/estrutura',
        # 'https://app.amaranzero.com.br/acessorio',
        # 'https://app.amaranzero.com.br/stringbox'
]
for url in urls:
    print(f'Raspando de: {url}')
    response = get_products(driver,wait,url)
    result.append(response)

result = [item for sublist in result for item in sublist]
print('Raspagem Executada com sucesso')
print(f'RESULTADO: {result}\n Quantidade de produtos raspados: {len(result)}')
fim = time.time()
print(f'Tempo de execução: {fim-inicio}')

df = pd.DataFrame.from_dict(result)
print(f'DATA FRAME: {df}')
data = datetime.today().strftime('%Y-%m-%d')

df.to_excel(f'resultados-crawler/amara/amara_{data}.csv')