import datetime
import json
from pathlib import Path
import time
from requests import request
from scrapy import Request
import scrapy
from scrapy.http import HtmlResponse
from browsercookie import chrome
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def get_modulo(driver):
    time.sleep(5)

    all_products = []
    
    product = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')))
    products = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a/article')
    products = [product.text.split('\n') for product in products]
    for product in products:
           all_products.append({'tipo':'modulo',
                                'marca':product[0],
                                'nome':product[1],
                                'preço':product[2],
                                'data':datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")})
    print('Modulo OK')
    return all_products


def get_inversor(driver):
    time.sleep(5)

    all_products = []
    
    script_js = "window.scrollBy(0, 200);"
    driver.execute_script(script_js)
    button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vtex-search-result-3-x-buttonShowMore .vtex-button")))
    button.click()
    while driver.current_url != 'https://app.amaranzero.com.br/inversor?page=6':
        script_js = "window.scrollBy(0, 200);"
        driver.execute_script(script_js)
        button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vtex-search-result-3-x-buttonShowMore .vtex-button")))
        button.click()
    product = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')))
    products = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a/article')
    products = [product.text.split('\n') for product in products]
    for product in products:
           all_products.append({'tipo':'inversor',
                                'marca':product[0],
                                'nome':product[1],
                                'preço':product[2],
                                'data':datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")})
    print('Inversor OK')
    return all_products
    

def get_microinversor(driver):
    time.sleep(5)


    all_products = []
    
    product = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')))
    products = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a/article')
    products = [product.text.split('\n') for product in products]
    for product in products:
           all_products.append({'tipo':'micro-inversor',
                                'marca':product[0],
                                'nome':product[1],
                                'preço':product[2],
                                'data':datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")})
    print('Micro-Inversor OK')
    return all_products
           
    

def get_estrutura(driver):
    time.sleep(5)

     
    all_products = []
    
    script_js = "window.scrollBy(0, 200);"
    driver.execute_script(script_js)
    button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vtex-search-result-3-x-buttonShowMore .vtex-button")))
    button.click()
    while driver.current_url != 'https://app.amaranzero.com.br/estrutura?page=12':
        script_js = "window.scrollBy(0, 200);"
        driver.execute_script(script_js)
        button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vtex-search-result-3-x-buttonShowMore .vtex-button")))
        button.click()
    product = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')))
    products = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a/article')
    products = [product.text.split('\n') for product in products]
    for product in products:
           all_products.append({'tipo':'estrutura',
                                'marca':product[0],
                                'nome':product[1],
                                'preço':product[2],
                                'data':datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")})
    print('Estrutura OK')
    return all_products
           
    

def get_acessorio(driver):
    time.sleep(5)

     
     
    all_products = []
    
    script_js = "window.scrollBy(0, 200);"
    driver.execute_script(script_js)
    button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vtex-search-result-3-x-buttonShowMore .vtex-button")))
    button.click()
    while driver.current_url != 'https://app.amaranzero.com.br/acessorio?page=4':
        script_js = "window.scrollBy(0, 200);"
        driver.execute_script(script_js)
        button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vtex-search-result-3-x-buttonShowMore .vtex-button")))
        button.click()
    product = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')))
    products = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a/article')
    products = [product.text.split('\n') for product in products]
    for product in products:
           all_products.append({'tipo':'acessorio',
                                'marca':product[0],
                                'nome':product[1],
                                'preço':product[2],
                                'data':datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")})
    print('Acessorio OK')
    return all_products

def get_stringbox(driver):
    time.sleep(5)


    all_products = []
    
    product = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')))
    products = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a/article')
    products = [product.text.split('\n') for product in products]
    for product in products:
           all_products.append({'tipo':'stringbox',
                                'marca':product[0],
                                'nome':product[1],
                                'preço':product[2],
                                'data':datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")})
    print('Stringbox OK')
    return all_products
    

def controller(driver,type):
    if type == 'modulo':
        return get_modulo(driver)
    elif type == 'inversor':
        return get_inversor(driver)
    elif type == 'microinversor':
        return get_microinversor(driver)
    elif type == 'estrutura':
        return get_estrutura(driver)
    elif type == 'acessorio':
        return get_acessorio(driver)
    elif type == 'stringbox':
        return get_stringbox(driver)