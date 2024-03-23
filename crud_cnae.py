def inserir_dados(conexao, cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei):
    cursor = conexao.cursor()
    sql = "INSERT INTO tabela_cnae (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (cnae, descricao_principal, anexo, fator_r, aliquota, contabilizei)
    cursor.execute(sql, val)
    conexao.commit()
    print(cursor.rowcount, "registro(s) inserido(s).")
    cursor.close()
