
-- PROJETO 04
-- 08 | QUALIDADE DOS DADOS E RESUMO EXECUTIVO


-- 1. Verificacao de valores ausentes

SELECT
    COUNT(*) AS total_registros,
    SUM(CASE WHEN loan_amnt IS NULL
        THEN 1 ELSE 0 END) AS nulos_valor,
    SUM(CASE WHEN grade IS NULL
        THEN 1 ELSE 0 END) AS nulos_grade,
    SUM(CASE WHEN loan_status IS NULL
        THEN 1 ELSE 0 END) AS nulos_status,
    SUM(CASE WHEN annual_inc IS NULL
        THEN 1 ELSE 0 END) AS nulos_renda,
    SUM(CASE WHEN fico_range_low IS NULL
        THEN 1 ELSE 0 END) AS nulos_fico
FROM accepted_loans_sample;


-- 2. Verificacao de valores invalidos

SELECT
    COUNT(*) AS total_registros,
    SUM(CASE WHEN loan_amnt <= 0
        THEN 1 ELSE 0 END) AS emprestimos_invalidos,
    SUM(CASE WHEN annual_inc < 0
        THEN 1 ELSE 0 END) AS rendas_negativas,
    SUM(CASE WHEN int_rate < 0
        THEN 1 ELSE 0 END) AS taxas_negativas
FROM accepted_loans_sample;


-- 3. Consolidacao dos principais indicadores

SELECT
    COUNT(*) AS total_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_total_concedido,
    ROUND(AVG(loan_amnt), 2) AS emprestimo_medio,
    ROUND(AVG(int_rate), 2) AS juros_medios,
    SUM(
        CASE
            WHEN loan_status = 'Charged Off'
            THEN 1
            ELSE 0
        END
    ) AS contratos_baixados,
    ROUND(
        SUM(
            CASE
                WHEN loan_status = 'Charged Off'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS percentual_contratos_baixados
FROM accepted_loans_sample;
