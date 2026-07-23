import boto3
import time
from extraction import ingest_ans_bronze


def run_athena_query(query_string, database, s3_output):
    query_string = query_string.strip()
    if not query_string:
        return

    client = boto3.client("athena", region_name="us-east-1")

    response = client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={"OutputLocation": s3_output},
    )

    query_execution_id = response["QueryExecutionId"]
    print(f"Executando query (ID: {query_execution_id})...")

    while True:
        status = client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(2)

    if state == "SUCCEEDED":
        print("Query executada com sucesso!")
    else:
        reason = status["QueryExecution"]["Status"].get(
            "StateChangeReason", "Erro desconhecido"
        )
        print(f"Falha na query: {reason}")
        print(f"Comando que falhou (amostra):\n{query_string[:200]}...")


def execute_sql_file(filepath, database_name, s3_results_path):
    print(f"\n--- Iniciando execução da camada: {filepath} ---")
    with open(filepath, "r", encoding="utf-8") as file:
        full_query = file.read()

    queries = []
    current_query = []
    in_single_quote = False
    in_double_quote = False

    for char in full_query:
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote

        if char == ";" and not in_single_quote and not in_double_quote:
            queries.append("".join(current_query))
            current_query = []
        else:
            current_query.append(char)

    if current_query:
        queries.append("".join(current_query))

    for query in queries:
        if query.strip():
            print("Enviando para o Athena...")
            run_athena_query(query, database_name, s3_results_path)


if __name__ == "__main__":
    s3_results_path = "s3://datalake-ans-nava/athena-results/"
    database_name = "case_ans_medallion"

    print("\n--- Iniciando Etapa 1: Extração e Ingestão ---")
    ingest_ans_bronze()  # <-- Chamando a extração primeiro

    print("\n--- Iniciando Etapa 2: Transformações Medallion ---")
    execute_sql_file("sql/bronze.sql", database_name, s3_results_path)
    execute_sql_file("sql/silver.sql", database_name, s3_results_path)
    execute_sql_file("sql/gold.sql", database_name, s3_results_path)

    print("\nPipeline executado com sucesso!")
