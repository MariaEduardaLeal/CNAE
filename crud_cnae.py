def inserir_dados(conexao, cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei, link):
    cursor = conexao.cursor()

    try:
        # Verificar se os dados já existem no banco de dados com os mesmos valores
        sql_select = "SELECT * FROM tabela_cnae WHERE cnae = %s AND descricao_principal = %s AND anexo = %s AND fator_r = %s AND aliquota = %s AND contabilizei = %s"
        val_select = (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei)
        cursor.execute(sql_select, val_select)
        resultado = cursor.fetchone()

        if resultado:
            # Já existe um registro com os mesmos valores, não há necessidade de atualização
            print(f"Dados do CNAE {cnae} já estão iguais, não houve alteração.")
        else:
            # Inserir os dados na tabela
            sql = "INSERT INTO tabela_cnae (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei, link_hierarquia) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei, link)
            cursor.execute(sql, val)
            conexao.commit()
            print(f"Dados do CNAE {cnae} inseridos com sucesso.")

    except Exception as e:
        # Tratamento de exceção caso ocorra algum erro durante a execução do SQL
        print(f"Erro ao inserir dados do CNAE {cnae}: {e}")

    finally:
        # Fechar o cursor
        cursor.close()


def inserir_dados_hierarquia(conexao, cnae, divisao, grupo, classe, subclasse):
    cursor = conexao.cursor()

    # Verificar se o dado já existe na tabela
    cursor.execute("SELECT cnae FROM hierarquia_da_atividade WHERE cnae = %s", (cnae,))
    resultado = cursor.fetchone()

    if resultado:
        # Atualizar os dados na tabela
        sql = "UPDATE hierarquia_da_atividade SET divisao = %s, grupo = %s, classe = %s, subclasse = %s WHERE cnae = %s"
        val = (divisao, grupo, classe, subclasse, cnae)
        cursor.execute(sql, val)
        conexao.commit()
        print(f"Dados do CNAE {cnae} atualizados na tabela de hierarquia_da_atividade com sucesso.")
    else:
        # Inserir os dados na tabela
        sql = "INSERT INTO hierarquia_da_atividade (cnae, divisao, grupo, classe, subclasse) VALUES (%s, %s, %s, %s, %s)"
        val = (cnae, divisao, grupo, classe, subclasse)
        cursor.execute(sql, val)
        conexao.commit()
        print(f"Dados do CNAE {cnae} inseridos na tabela de hierarquia_da_atividade com sucesso.")

    # Fechar o cursor
    cursor.close()

def retornar_links_hierarquia(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT cnae, link_hierarquia FROM tabela_cnae")
    # Recuperar os resultados
    resultados = cursor.fetchall()
    return resultados