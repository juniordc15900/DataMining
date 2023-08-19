from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime
import pandas as pd
import sys
sys.path.append(".")


TIME = time = datetime.today().strftime('%Y-%m-%d')


def get_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


def get_shop_page(driver: WebDriver):
    driver.get('https://solplace.com.br/shop#')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.carousel-inner')))


def get_generator_data(driver: WebDriver) -> list:
    generators = []

    pages = driver.find_elements(by=By.CSS_SELECTOR, value='li.page-item')
    print(f"Paginas: {pages}")
    pages_qtd = len(pages) - 3

    for page in range(pages_qtd):
        print(f'Pagina {page}')

        products = driver.find_elements(by=By.CSS_SELECTOR, value='td.oe_product.oe_image_full')

        for product in products:
            ActionChains(driver).move_to_element(product).perform()
            sleep(2)
            quick_view_btn = product.find_element(by=By.CSS_SELECTOR, value=('button.btn.btn-primary.rounded-circle.font-weight-bold.py-2.tp-product-quick-view-action.tp-product-quick-view-large-btn.text-truncate'))
            driver.execute_script("arguments[0].click();", quick_view_btn)

            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.text-truncate')))

            product_name = driver.find_element(by=By.CSS_SELECTOR, value='h3.text-truncate').text
            price = driver.find_element(by=By.CSS_SELECTOR, value='h4.oe_price_h4.css_editable_mode_hidden').text
            full_description = driver.find_element(by=By.XPATH, value='//*[@id="product_details"]/p').text.split('\n')
            full_description = [description.lower() for description in full_description]
            inverter = list(filter(lambda item: 'inversor' in item, full_description))[0]
            module = list(filter(lambda item: 'módulo' in item, full_description))[0]

            data = {
                'produto': product_name,
                'preco': price,
                'inversor': inverter,
                'modulo': module,
                'data': TIME
            }

            generators.append(data)

            close_btn = driver.find_element(by=By.CSS_SELECTOR, value='button.close')
            close_btn.click()

        next_page = driver.find_element(by=By.XPATH, value='//*[@id="wrap"]/div[2]/div[5]/ul/li[9]/a')
        if page < pages_qtd - 1:
            driver.execute_script("arguments[0].click();", next_page)

    return generators


def save_data(generators_data: list):
    df = pd.DataFrame(generators_data)
    df.to_csv(f'resultados-crawler/solplace/solplace-{TIME}.csv')


if __name__ == '__main__':
    driver = get_driver()
    get_shop_page(driver)
    generators = get_generator_data(driver)
    save_data(generators_data=generators)
    driver.close()
