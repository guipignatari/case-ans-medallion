CREATE TABLE IF NOT EXISTS case_ans_medallion.silver_beneficiarios
WITH (
    format = 'PARQUET',
    external_location = 's3://datalake-ans-nava/silver/ans_beneficiarios/'
) AS
SELECT 
    CAST(cd_operadora AS INTEGER) AS codigo_operadora,
    TRIM(nm_razao_social) AS nome_operadora,
    TRIM(nm_municipio) AS municipio_operacao,
    TRIM(de_faixa_etaria) AS faixa_etaria,
    TRIM(de_segmentacao_plano) AS segmento_plano,
    TRIM(de_abrg_geografica_plano) AS abrangencia,
    CAST(qt_beneficiario_ativo AS INTEGER) AS qtde_beneficiarios_ativos
FROM case_ans_medallion.bronze_beneficiarios
WHERE cd_operadora IS NOT NULL 
  AND cd_operadora != ''
  AND cd_operadora != 'CD_OPERADORA'
