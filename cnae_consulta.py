from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from conexao import conectar_banco
from crud_cnae import inserir_dados_cnae

# Função para extrair e inserir os dados
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

            # Conectar ao banco de dados
            conexao = conectar_banco()

            # Inserir dados na tabela
            inserir_dados_cnae(conexao, cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei)

            # Fechar a conexão
            conexao.close()

    # Fechar o navegador
    navegador.quit()

# Chamar a função para extrair e inserir os dados
extrair_e_inserir()