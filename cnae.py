from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from conexao import conectar_banco
from crud_cnae import inserir_dados
from crud_cnae import inserir_dados_hierarquia

def extrair_informacoes_link(link_completo, cnae, conexao):
    # Inicializar o navegador Chrome
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)

    # Abrir o link completo
    navegador.get(link_completo)

    WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Obter o conteúdo HTML da página
    html_content = navegador.page_source

    # Passar o conteúdo HTML para o BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrar a tabela de informações
    tabela_informacoes = soup.find('table', {'data-v-be12d62c': True})

    if tabela_informacoes:
        # Extrair as informações do tbody
        tbody = tabela_informacoes.find('tbody')
        if tbody:
            # Extrair as informações específicas
            informacoes = {}
            for tr in tbody.find_all('tr'):
                tipo = tr.find('td', {'class': 'type'}).text.strip()
                texto = tr.find('td', {'class': 'text'}).text.strip()
                informacoes[tipo] = texto

            # Inserir as informações na tabela hierarquia_da_atividade
            inserir_dados_hierarquia(conexao, cnae, informacoes.get('Divisão', ''), informacoes.get('Grupo', ''), informacoes.get('Classe', ''), informacoes.get('Subclasse', ''))

    # Fechar o navegador
    navegador.quit()

# Função principal para extrair e inserir os dados
def extrair_e_inserir():
    # Inicializar o navegador Chrome
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)

    # Abrir a página desejada
    navegador.get("https://www.contabilizei.com.br/contabilidade-online/cnae/")

    # Obter o conteúdo HTML da página
    html_content = navegador.page_source

    # Passar o conteúdo HTML para o BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    elemento_com_id = soup.find(id="tableCNAE")

    # Encontrando todas as linhas (<tr>) dentro do elemento com o ID
    linhas_da_tabela = elemento_com_id.find_all('tr')

    # Iterar sobre as linhas da tabela
    for linha in linhas_da_tabela:
        # Encontrar todas as células (<td>) na linha
        dados = linha.find_all('td')

        # Verificar se há dados suficientes
        if len(dados) >= 6:
            # Extrair os valores de cada célula
            cnae = dados[0].text.strip()
            descricao_principal = dados[1].text.strip()
            anexo = dados[2].text.strip()
            fator_r = dados[3].text.strip()
            aliquota = dados[4].text.strip()
            contabilizei = dados[5].text.strip()

            # Extrair o link completo da primeira célula (<td>) - código CNAE
            link_cnae = dados[0].find('a')['href']
            link_completo = f"https://www.contabilizei.com.br{link_cnae}"
            print("Link cane: ", link_completo)

            # Conectar ao banco de dados
            conexao = conectar_banco()

            # Inserir dados na tabela
            inserir_dados(conexao, cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei)

            # Extrair e inserir informações do link completo
            extrair_informacoes_link(link_completo,cnae, conexao)

            # Fechar a conexão
            conexao.close()

    # Fechar o navegador
    navegador.quit()

# Chamar a função para extrair e inserir os dados
extrair_e_inserir()
