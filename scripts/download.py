import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(dataset_name, download_path):
    """Baixa o dataset do Kaggle e descompacta no caminho especificado."""
    api = KaggleApi()
    api.authenticate()
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    print(f"Dataset {dataset_name} baixado com sucesso para {download_path}.")