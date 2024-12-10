import os
import pandas as pd
from datetime import datetime

def ensure_directory_exists(path):
    """Garante que o diretório especificado existe; caso contrário, cria."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Diretório {path} criado com sucesso.")
    else:
        print(f"Diretório {path} já existe.")

def log_message(message, log_file=None):
    """Registra uma mensagem no console ou em um arquivo de log."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    if log_file:
        with open(log_file, 'a') as file:
            file.write(formatted_message + "\n")

def validate_file(file_path):
    """Verifica se o arquivo especificado existe."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return True

def convert_date_columns(df, date_columns):
    """Converte colunas de data para o formato datetime e trata valores nulos."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
            df[col] = df[col].where(df[col].notnull(), None)
    return df
