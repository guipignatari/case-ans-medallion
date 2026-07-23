-- A) As 5 operadoras com maior número de beneficiários ativos --

CREATE TABLE IF NOT EXISTS case_ans_medallion.gold_top_operadoras
WITH (
    format = 'PARQUET',
    external_location = 's3://datalake-ans-nava/gold/top_operadoras/'
) AS
SELECT 
    nome_operadora,
    SUM(qtde_beneficiarios_ativos) AS total_beneficiarios
FROM case_ans_medallion.silver_beneficiarios
GROUP BY nome_operadora
ORDER BY total_beneficiarios DESC
LIMIT 5;

-- B) Qual é a faixa etária com mais beneficiários e quantos são? --

CREATE TABLE IF NOT EXISTS case_ans_medallion.gold_faixa_etaria
WITH (
    format = 'PARQUET',
    external_location = 's3://datalake-ans-nava/gold/faixa_etaria/'
) AS
SELECT 
    faixa_etaria,
    SUM(qtde_beneficiarios_ativos) AS total_beneficiarios
FROM case_ans_medallion.silver_beneficiarios
GROUP BY faixa_etaria
ORDER BY total_beneficiarios DESC
LIMIT 1;

-- C) Liste, de forma decrescente, a quantidade de beneficiários por município.
CREATE TABLE IF NOT EXISTS case_ans_medallion.gold_municipios
WITH (
    format = 'PARQUET',
    external_location = 's3://datalake-ans-nava/gold/municipios/'
) AS
SELECT 
    municipio_operacao,
    SUM(qtde_beneficiarios_ativos) AS total_beneficiarios
FROM case_ans_medallion.silver_beneficiarios
GROUP BY municipio_operacao
ORDER BY total_beneficiarios DESC;
