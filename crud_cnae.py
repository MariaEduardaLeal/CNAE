def inserir_dados(conexao, cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei, link):
    cursor = conexao.cursor()

    try:
        # Verificar se os dados já existem no banco de dados
        sql_select = "SELECT * FROM tabela_cnae WHERE cnae = %s AND aliquota = %s AND anexo = %s"
        val_select = (cnae, aliquota, anexo)
        cursor.execute(sql_select, val_select)
        resultado = cursor.fetchone()

        if resultado:
            # Atualizar os dados na tabela
            sql = "UPDATE tabela_cnae SET descricao_principal = %s, anexo = %s, fator_r = %s, aliquota = %s, contabilizei = %s WHERE cnae = %s"
            val = (descricao_principal, anexo, fator_r, aliquota, contabilizei, cnae)
            cursor.execute(sql, val)
            conexao.commit()
            print(f"Dados do CNAE {cnae} atualizados com sucesso.")
        else:
            # Inserir os dados na tabela
            sql = "INSERT INTO tabela_cnae (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei, link_hierarquia) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei, link)
            cursor.execute(sql, val)
            conexao.commit()
            print(f"Dados do CNAE {cnae} inseridos com sucesso.")

    except Exception as e:
        # Tratamento de exceção caso ocorra algum erro durante a execução do SQL
        print(f"Erro ao inserir/atualizar dados do CNAE {cnae}: {e}")

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


