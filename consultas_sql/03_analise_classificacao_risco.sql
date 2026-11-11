
-- PROJETO 04
-- 03 | ANALISE POR CLASSIFICACAO DE RISCO


-- 1. Distribuicao da carteira por grade

SELECT
    grade AS classificacao_risco,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_total_concedido,
    ROUND(AVG(int_rate), 2) AS taxa_juros_media
FROM accepted_loans_sample
GROUP BY grade
ORDER BY grade;


-- 2. Percentual de contratos baixados por grade

SELECT
    grade AS classificacao_risco,
    COUNT(*) AS total_emprestimos,
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
    ) AS percentual_baixados
FROM accepted_loans_sample
GROUP BY grade
ORDER BY grade;


-- 3. Participacao financeira dos contratos baixados
-- dentro de cada classificacao de risco

SELECT
    grade AS classificacao_risco,
    ROUND(SUM(loan_amnt), 2) AS valor_total_concedido,
    ROUND(
        SUM(
            CASE
                WHEN loan_status = 'Charged Off'
                THEN loan_amnt
                ELSE 0
            END
        ),
        2
    ) AS valor_concedido_baixados,
    ROUND(
        SUM(
            CASE
                WHEN loan_status = 'Charged Off'
                THEN loan_amnt
                ELSE 0
            END
        ) * 100.0 /
        NULLIF(SUM(loan_amnt), 0),
        2
    ) AS percentual_valor_baixados
FROM accepted_loans_sample
GROUP BY grade
ORDER BY grade;

