import mysql.connector

def conectar_banco():
    conexao = mysql.connector.connect(
        host='localhost',
        database='cnae_teste',
        user='root',
        password='12345'
    )
    return conexao
