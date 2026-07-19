import pytest
from utils import ler_arquivo_sql

def test_ler_arquivo_sql_com_sucesso(tmp_path):
    arquivo_falso = tmp_path / "query_teste.sql"
    query_esperada = "SELECT * FROM camada_gold LIMIT 10;"
    
    arquivo_falso.write_text(f"   {query_esperada}  \n", encoding='utf-8')
    
    resultado = ler_arquivo_sql(str(arquivo_falso))
    
    assert resultado == query_esperada

def test_ler_arquivo_sql_arquivo_nao_encontrado():
    with pytest.raises(FileNotFoundError):
        ler_arquivo_sql("caminho_invalido.sql")