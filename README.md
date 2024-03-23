# Projeto CNAE

Este projeto tem como objetivo extrair dados de uma página da web sobre Classificação Nacional de Atividades Econômicas (CNAE) e inseri-los em um banco de dados MySQL.

## Como funciona

O script `cnae.py` utiliza Selenium e BeautifulSoup para fazer scraping dos dados de uma página da web que lista informações sobre a CNAE. Ele então insere esses dados em um banco de dados MySQL usando a biblioteca mysql-connector-python.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter as seguintes bibliotecas Python instaladas via pip:

- Selenium: `pip install selenium`
- Webdriver Manager: `pip install webdriver-manager`
- BeautifulSoup: `pip install beautifulsoup4`
- mysql-connector-python: `pip install mysql-connector-python`

## Como executar

1. Clone o repositório para o seu ambiente local:

git clone https://github.com/seu-usuario/projeto-cnae.git


2. Execute o script `cnae.py`:

python cnae.py


Isso iniciará a extração de dados da página da web e inserção no banco de dados MySQL.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue se encontrar algum problema ou enviar um pull request com melhorias.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).


