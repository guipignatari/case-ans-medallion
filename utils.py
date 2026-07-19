import os

def ler_arquivo_sql(caminho_arquivo: str) -> str:
    """Lê um arquivo .sql e retorna a query como string, pronta para o Athena."""
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Erro: O arquivo SQL '{caminho_arquivo}' não foi encontrado.")
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        return file.read().strip()