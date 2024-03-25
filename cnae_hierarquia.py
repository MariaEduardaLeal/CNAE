from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from conexao import conectar_banco
from crud_cnae import retornar_links_hierarquia
from crud_cnae import inserir_dados_hierarquia
import time

def receber_link_hierarquia():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    conexao = conectar_banco()

    retorno = retornar_links_hierarquia(conexao)

    for cnae, link_hierarquia in retorno: 
        print("CNAE:", cnae) 
        print("Link:", link_hierarquia) 
        navegador.get(link_hierarquia)
        WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        html_content = navegador.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        informacoes = {}
        tentativas = 10
        for _ in range(tentativas):
            try:
                tbody = soup.find('tbody', id='hierarchy-body')
                if tbody is None:
                    raise AttributeError("Elemento tbody não encontrado")

                for tr in tbody.find_all('tr'):
                    tipo = tr.find('td', class_='type').text.strip()
                    texto = tr.find('td', class_='text').text.strip()
                    informacoes[tipo] = texto

                    inserir_dados_hierarquia(conexao, cnae, informacoes.get('Divisão', ''), informacoes.get('Grupo', ''), informacoes.get('Classe', ''), informacoes.get('Subclasse', ''))
                break
            except AttributeError as e:
                print(f"Erro: {e}")
                print("Tentando novamente...")
                time.sleep(5)

        print(informacoes)

    navegador.quit()
    conexao.close()

receber_link_hierarquia()
