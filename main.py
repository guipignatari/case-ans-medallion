import boto3
import time

def run_athena_query(query_string, database, s3_output):
    client = boto3.client('athena', region_name='us-east-1')
    
    response = client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': s3_output}
    )
    
    query_execution_id = response['QueryExecutionId']
    print(f"Executando query (ID: {query_execution_id})...")
    
    while True:
        status = client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)
        
    if state == 'SUCCEEDED':
        print("Query executada com sucesso!")
    else:
        reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Erro desconhecido')
        print(f"Falha na query: {reason}")

if __name__ == "__main__":
    s3_results_path = 's3://datalake-ans-nava/athena-results/'
    database_name = 'case_ans_medallion'
    
    print("Lendo script da camada Bronze...")
    with open('sql/bronze.sql', 'r', encoding='utf-8') as file:
        bronze_query = file.read()
        
    print("Enviando comando para o AWS Athena...")
    run_athena_query(bronze_query, database_name, s3_results_path)

    print("Lendo script da camada Silver...")
    with open('sql/silver.sql', 'r', encoding='utf-8') as file:
        silver_query = file.read()
        
    print("Enviando comando de transformação (Silver) para o AWS Athena...")
    run_athena_query(silver_query, database_name, s3_results_path)
