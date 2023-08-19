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
PASSWORD = '6TpFXT3uf@7Yab'

TIME = datetime.today().strftime('%Y-%m-%d')


def get_driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def login(driver: WebDriver):
    driver.get('https://ourolux.com.br/customer/account/login/')
    
    email_field = driver.find_element(by=By.XPATH, value='//*[@id="email"]')
    email_field.send_keys(USERNAME)
    password_field = driver.find_element(by=By.XPATH, value='//*[@id="pass"]')
    password_field.send_keys(PASSWORD)
    
    submit_btn = driver.find_element(by=By.XPATH, value='//*[@id="send2"]')
    submit_btn.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="custom.topnav"]/nav/ul/li[1]/a')))


def get_catalog_page(driver: WebDriver):
    catalog = driver.find_element(by=By.XPATH, value='//*[@id="custom.topnav"]/nav/ul/li[1]/a')
    ActionChains(driver).move_to_element(catalog).perform()
    sleep(1)

    catalog_link = driver.find_element(by=By.XPATH, value='//*[@id="custom.topnav"]/nav/ul/li[1]/div[2]/div/ul/li[2]/ul/li[1]/a')
    catalog_link.click()
    sleep(2)

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="layered-ajax-list-products"]/div')))


def get_generator_data(driver: WebDriver) -> list:
    generators = []

    page_info = driver.find_element(by=By.XPATH, value='//*[@id="toolbar-amount"]').text
    page_numbers = re.findall(r'\d', page_info)
    pages = [page_numbers[0], ''.join(page_numbers[1:-2]), ''.join(page_numbers[-2:])]
    # print(pages)
    qtd_pages = (int(pages[2]) // int(pages[1])) + 1
    # print(f'quantidade de paginas {qtd_pages}')
    qtd_itens = int(pages[1])
    # print(f'quantidade de items pp {qtd_itens}')


    for page in range(1, qtd_pages + 1):
        sleep(2)
        if page == qtd_pages:
            qtd_itens = (qtd_itens * qtd_pages) - int(pages[2])
        
        for item in range(1, qtd_itens + 1):
            try:
                print(f'item: {item}')
                product = driver.find_element(by=By.XPATH, value=f'//*[@id="layered-ajax-list-products"]/div/div[2]/div/ol/li[{item}]')
                price_info = product.find_element(by=By.CSS_SELECTOR, value='span.price').text
                price_numbers = re.findall(r'\d', price_info)
                price = float(''.join(price_numbers[:-2]) + '.' + ''.join(price_numbers[-2:]))

                product.click()
                sleep(1)

                power = driver.find_element(by=By.XPATH, value='//*[@id="product-attribute-specs-table"]/tbody/tr[4]/td').text
                module_description = driver.find_element(by=By.XPATH, value='//*[@id="bundle_content"]/table[1]/tbody/tr[1]/td').text
                module_quntity = driver.find_element(by=By.XPATH, value='//*[@id="bundle_content"]/table[1]/tbody/tr[3]/td[1]').text
                inverter_description = driver.find_element(by=By.XPATH, value='//*[@id="bundle_content"]/table[2]/tbody/tr[1]/td').text
                inverter_quantity = driver.find_element(by=By.XPATH, value='//*[@id="bundle_content"]/table[2]/tbody/tr[3]/td[1]').text

                generator_data = {
                    'potencia': power,
                    'preco': price,
                    'modulo': module_description,
                    'qtd_modulo': module_quntity,
                    'inversor': inverter_description,
                    'qtd_inversor': inverter_quantity,
                    'data': TIME
                }
                generators.append(generator_data)
            except Exception as e:
                # print(e)
                continue

            driver.back()
            sleep(2)
        
        next_page = driver.find_element(by=By.CSS_SELECTOR, value='li.item.pages-item-next')
        driver.execute_script("arguments[0].click();", next_page)

    return generators


def save_data(generators_data: list):
    df = pd.DataFrame(generators_data)
    df.to_csv(f'resultados-crawler/ourolux/ourolux_{TIME}.xlsx')


if __name__ == '__main__':
    driver = get_driver()
    login(driver)
    get_catalog_page(driver)
    generators = get_generator_data(driver)
    save_data(generators)

    driver.close()
