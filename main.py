import asyncio
import asyncpg
import os
from config.db_config import db_config
from scripts.download import download_dataset
from scripts.transformations import transform_datasets
from scripts.load import load_table

async def main():
    conn = await asyncpg.connect(**db_config)

    # Baixar o dataset
    download_path = "datasets/olist"
    download_dataset('olistbr/brazilian-ecommerce', download_path)

    # Carregar arquivos CSV
    data_files = {name: os.path.join(download_path, name) for name in os.listdir(download_path) if name.endswith('.csv')}

    # Transformar dados
    datasets = transform_datasets(data_files)

    # Carregar dados no banco
    for table_name, df in datasets.items():
        await load_table(df, table_name, conn)

    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())