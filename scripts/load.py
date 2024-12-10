async def load_table(df, table_name, conn):
    """Carrega os dados em uma tabela do PostgreSQL."""
    if df.empty:
        print(f"Nenhum dado para carregar na tabela {table_name}.")
        return

    columns = df.columns.tolist()
    rows = df.to_records(index=False).tolist()

    query = f"""
    INSERT INTO {table_name} ({', '.join(columns)})
    VALUES ({', '.join(['$' + str(i+1) for i in range(len(columns))])})
    ON CONFLICT DO NOTHING
    """

    try:
        await conn.executemany(query, rows)
        print(f"Dados carregados na tabela {table_name}.")
    except Exception as e:
        print(f"Erro ao carregar dados na tabela {table_name}: {e}")
