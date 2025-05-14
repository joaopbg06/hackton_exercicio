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



orcamentos = {
    "setor":[],
    "mes":[],
    "ano":[],
    "valor_previsto":[],
    "valor_realizado":[],
}

try:
    proxima_tabela = WebDriverWait(driver, 5).until(
    ec.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Orçamentos']"))
        )
    driver.execute_script("arguments[0].click();", proxima_tabela)
    proxima_tabela.click()


    
except Exception as e:
    print('Erro ao tentear avançar para a proxima página', e)


try:
    WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.TAG_NAME, "tr"))
    )
    print('Elementos encontrados com sucesso')

except TimeoutException:
    print('Tempo de expera foi muito e tankei foi nothing')




orcamento = driver.find_elements(By.TAG_NAME, "tr")

for produto in orcamento:
    try:
        setor = produto.find_element(By.CLASS_NAME, "td_setor").text.strip()
        mes = produto.find_element(By.CLASS_NAME, "td_mes").text.strip()
        ano = produto.find_element(By.CLASS_NAME, "td_ano").text.strip()
        valor_previsto = produto.find_element(By.CLASS_NAME, "td_valor_previsto").text.strip()
        valor_realizado = produto.find_element(By.CLASS_NAME, "td_valor_realizado").text.strip()


        print(f"{setor} - {mes} - {valor_previsto}")

        orcamentos["setor"].append(setor)
        orcamentos['mes'].append(mes)
        orcamentos['ano'].append(ano)
        orcamentos['valor_previsto'].append(valor_previsto)
        orcamentos['valor_realizado'].append(valor_realizado)

    except Exception:
        print('Erro ao coletar dados: ', Exception)


driver.quit()

df = pd.DataFrame(orcamentos)
df.to_excel('./base/orcamentos.xlsx', index=False)


