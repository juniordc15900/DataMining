from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime
import re
import pandas as pd
import sys
sys.path.append(".")

USERNAME = 'andre.abrantes@greener.com.br'
PASSWORD = '#Fortlev123'

TIME = time = datetime.today().strftime('%Y-%m-%d')


def get_driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def login(driver: WebDriver):
    driver.get('https://fortlevsolar.app/login')

    login_inputs = driver.find_elements(by=By.CSS_SELECTOR, value='input.q-field__native.q-placeholder')
    if len(login_inputs) != 2:
        raise Exception('Não foi possivel encontrar os campos do formulário de login.')
    
    for input in login_inputs:
        if input.get_attribute('type') == 'email':
            input.send_keys(USERNAME)
        if input.get_attribute('type') == 'password':
            input.send_keys(PASSWORD)
    
    submit_btn = driver.find_element(by=By.XPATH, value='//*[@id="q-app"]/div/div/div[2]/div/form/div[2]/button')
    submit_btn.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[1]/aside/div/div[2]/a[2]')))


def get_catalog_page(driver: WebDriver):
    catalog = driver.find_element(by=By.XPATH, value='//*[@id="q-app"]/div/div[1]/aside/div/div[2]/a[2]')
    catalog.click()

    WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.q-mb-md.col-xs-12.col-sm-6.col-md-4.col-lg-3')))


def get_generator_data(driver: WebDriver) -> list:
    generators = []

    for card_range in range(1, 80):
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.q-mb-md.col-xs-12.col-sm-6.col-md-4.col-lg-3')))
        if card_range > 10:
            for _ in range(card_range//10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

        try:
            card_detail = driver.find_element(by=By.XPATH, value=f'//*[@id="q-app"]/div/div[2]/div/div/div[4]/div[{card_range}]/div/div/div[4]/div')
            card_detail.click()
            
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="q-app"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div')))

            power = driver.find_element(by=By.XPATH, value='//*[@id="q-app"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div').text
            price = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[2]/div[3]/div[4]/div/div[1]').text
            module_description = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]').text
            module_quntity = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]').text
            module_quntity = re.findall(r'\d+', module_quntity)[0]
            inverter_description = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]').text
            inverter_quantity = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]').text
            inverter_quantity = re.findall(r'\d+', inverter_quantity)[0]
            structure = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/div/div[2]').text

            generator_data = {
                'potencia': power,
                'preco': price,
                'modulo': module_description,
                'qtd_modulo': module_quntity,
                'inversor': inverter_description,
                'qtd_inversor': inverter_quantity,
                'estrutura': structure,
                'data': TIME
            }
            generators.append(generator_data)

            driver.back()
            sleep(2)
            ok_btn = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/div/div[3]/button[2]')
            driver.execute_script("arguments[0].click();", ok_btn)
        except:
            break
    
    return generators

def save_data(generators_data: list):
    df = pd.DataFrame(generators_data)
    df.to_csv(f'resultados-crawler/fortlev/fortilevsolar-{TIME}.csv')


if __name__ == '__main__':
    driver = get_driver()
    login(driver)
    get_catalog_page(driver)
    generators = get_generator_data(driver)
    save_data(generators)

    driver.close()
