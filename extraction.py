import requests
import zipfile
import io
import boto3  ## Upload CSV to S3

## Endpoint dataset.
url = "https://dadosabertos.ans.gov.br/FTP/PDA/informacoes_consolidadas_de_beneficiarios-024/202508/pda-024-icb-TO-2025_08.zip"
bucket_name = "datalake-ans-nava"  ## Salvar o dado extraido no S3
s3_prefix = "bronze/ans_beneficiarios/"

s3_client = boto3.client("s3")


def ingest_ans_bronze():
    print("Iniciando o download do arquivo ZIP da ANS...")
    response = requests.get(url)
    response.raise_for_status()

    print("Download concluído. Descompactando arquivo...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for file_name in z.namelist():
            print(f"Extraindo: {file_name}")

            with z.open(file_name) as extracted_file:
                s3_key = f"{s3_prefix}{file_name}"

                print(f"Realizando upload para: s3://{bucket_name}/{s3_key}")
                s3_client.upload_fileobj(extracted_file, bucket_name, s3_key)

    print("Ingestão bronze finalizada com sucesso!")


if __name__ == "__main__":
    ingest_ans_bronze()
