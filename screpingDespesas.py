# pip install selenium

# módulo para controlar o navegador web
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações de avançar(o mover do mouse, clique/arrasta)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explícita até uma condição seja satisfeita(ex: que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

#Condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# trabalhar com dataframe
import pandas as pd

#uso de funções relacionada ao tempo
import time 

#uso para tratamento de exceção
from selenium.common.exceptions import TimeoutException


chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path) #navegador controlado pelo Selenium
options = webdriver.ChromeOptions() #configurar as opções do navegador
options.add_argument('--disable-gpu') #evita possíveis erros gráficos
options.add_argument('--window-size=1920,1080') #defini uma resolução fixa
options.add_argument('--headless') # ativa o modo headless (sem abrir o navegador)


driver = webdriver.Chrome(service=service, options=options)


url_base = 'https://masander.github.io/AlimenticiaLTDA-financeiro/'
driver.get(url_base)
time.sleep(5) 


despesas = {
    "id_despesas":[], 
    'data':[], 
    'tipo':[],
    'setor':[],
    'valor':[],
    'fornecedor':[],
    }



try:
    WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.TAG_NAME, "tr"))
    )
    print('Elementos encontrados com sucesso')

except TimeoutException:
    print('Tempo de expera foi muito e tankei foi nothing')
    
despesa = driver.find_elements(By.TAG_NAME, "tr")

for produto in despesa:
    try:
        id_despesas = produto.find_element(By.CLASS_NAME, "td_id_despesa").text.strip()
        data = produto.find_element(By.CLASS_NAME, "td_data").text.strip()
        tipo = produto.find_element(By.CLASS_NAME, "td_tipo").text.strip()
        setor = produto.find_element(By.CLASS_NAME, "td_setor ").text.strip()
        valor = produto.find_element(By.CLASS_NAME, "td_valor ").text.strip()
        fornecedor = produto.find_element(By.CLASS_NAME, "td_fornecedor ").text.strip()


        print(f"{id_despesas} - {tipo} - {valor}")

        despesas["id_despesas"].append(id_despesas)
        despesas['data'].append(data)
        despesas['tipo'].append(tipo)
        despesas['setor'].append(setor)
        despesas['valor'].append(valor)
        despesas['fornecedor'].append(fornecedor)

    except Exception:
        print('Erro ao coletar dados: ', Exception)


df = pd.DataFrame(despesas)
df.to_excel('./base/despesas.xlsx', index=False)

