from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os


def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', 'window-size=1000,800']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver


driver = iniciar_driver()
driver.get('https://www.amazon.com.br/s?k=monitor&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=U4U6K2Y7ZATD&sprefix=monitor%2Caps%2C522&ref=nb_sb_noss_2')
sleep(10)

while True:
    driver.execute_script('window.scrollTo(0, 10500);')
    sleep(6)

    titulos = driver.find_elements(
        By.XPATH, '//div[@class="a-section a-spacing-base"]//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]//span[@class="a-size-base-plus a-color-base a-text-normal"]')
    precos = driver.find_elements(
        By.XPATH, '//div[@class="a-section a-spacing-small puis-padding-left-small puis-padding-right-small"]//span[@class="a-price-whole"]')
    links = driver.find_elements(
        By.XPATH, '//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')

    with open('lista_monitores.csv', 'a', encoding='utf-8', newline='') as arquivo:
        for titulo, preco, link in zip(titulos, precos, links):
            if preco.text != ' ':
                link_processado = link.get_attribute('href')
                arquivo.write(
                    f'{titulo.text};{preco.text};{link_processado}{os.linesep}')

    try:
        botao_proximo = driver.find_element(
            By.CLASS_NAME, 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
        sleep(3)
        botao_proximo.click()
    except:
        print('Chegamos ao fim')
        break

driver.close()
