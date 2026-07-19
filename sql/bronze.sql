CREATE EXTERNAL TABLE IF NOT EXISTS case_ans_medallion.bronze_beneficiarios (
    id_cmpt_movel STRING,
    cd_operadora STRING,
    nm_razao_social STRING,
    nr_cnpj STRING,
    modalidade_operadora STRING,
    sg_uf STRING,
    cd_municipio STRING,
    nm_municipio STRING,
    tp_sexo STRING,
    de_faixa_etaria STRING,
    de_faixa_etaria_reaj STRING,
    cd_plano STRING,
    tp_vigencia_plano STRING,
    de_contratacao_plano STRING,
    de_segmentacao_plano STRING,
    de_abrg_geografica_plano STRING, 
    cobertura_assist_plan STRING,
    tipo_vinculo STRING,
    qt_beneficiario_ativo STRING,
    qt_beneficiario_aderido STRING,
    qt_beneficiario_cancelado STRING,
    dt_carga STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ";",
   "quoteChar" = "\""
)
LOCATION 's3://datalake-ans-nava/bronze/ans_beneficiarios/'
TBLPROPERTIES ('skip.header.line.count'='1');
