from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Verifica a versão do seu google chrome e instala automaticamente o chromedriver correspondente
servico = Service(ChromeDriverManager().install())

# Criando instância do CHROMEDRIVER passando o chromedriver instalado automaticamente
navegador = webdriver.Chrome(service=servico)

# Abre a página desejada
navegador.get("https://www.contabilizei.com.br/contabilidade-online/cnae/")

# Obtendo o conteúdo HTML da página
html_content = navegador.page_source

# Passando o conteúdo HTML para o BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

elemento_com_id = soup.find(id="tableCNAE")

# Encontrando todas as linhas (<tr>) dentro do elemento com o ID
linhas_da_tabela = elemento_com_id.find_all('tr')

contador = 0

# Iterando sobre as linhas da tabela e imprimindo os dados
for linha in linhas_da_tabela:
    contador += 1  # Incrementa o contador em 1
    dados = linha.find_all('td')  # Encontrando todas as células da linha
    for dado in dados:
        print(dado.text.strip(), end=' ')  # Imprimindo o texto de cada célula
    print()  # Nova linha para separar cada linha da tabela

print('Contador: ', contador)

# Aguardando a entrada do usuário para fechar o navegador
input("Pressione Enter para fechar o navegador...")

# Fechando o navegador
navegador.quit()
