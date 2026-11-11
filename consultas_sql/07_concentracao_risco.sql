
-- PROJETO 04
-- 07 | CONCENTRACAO DO RISCO


-- 1. Valor concedido aos contratos baixados por grade

SELECT
    grade AS classificacao_risco,
    COUNT(*) AS total_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_concedido,
    ROUND(
        SUM(
            CASE
                WHEN loan_status = 'Charged Off'
                THEN loan_amnt
                ELSE 0
            END
        ),
        2
    ) AS valor_concedido_baixados
FROM accepted_loans_sample
GROUP BY grade
ORDER BY valor_concedido_baixados DESC;


-- 2. Concentracao financeira dos contratos baixados

SELECT
    grade AS classificacao_risco,
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
        NULLIF(
            (SELECT SUM(loan_amnt)
             FROM accepted_loans_sample
             WHERE loan_status = 'Charged Off'),
            0
        ),
        2
    ) AS percentual_concentracao
FROM accepted_loans_sample
GROUP BY grade
ORDER BY percentual_concentracao DESC;
