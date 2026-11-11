
-- PROJETO 04
-- 05 | PERFIL FINANCEIRO E SCORE FICO


-- 1. Renda e valor medio por situacao

SELECT
    loan_status AS situacao_emprestimo,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(AVG(annual_inc), 2) AS renda_anual_media,
    ROUND(AVG(loan_amnt), 2) AS emprestimo_medio
FROM accepted_loans_sample
GROUP BY loan_status;


-- 2. Score FICO por situacao

SELECT
    loan_status AS situacao_emprestimo,
    ROUND(AVG(fico_range_low), 2) AS fico_medio,
    MIN(fico_range_low) AS menor_fico,
    MAX(fico_range_low) AS maior_fico
FROM accepted_loans_sample
GROUP BY loan_status;


-- 3. Contratos baixados por faixa de score FICO

SELECT
    CASE
        WHEN fico_range_low < 650 THEN 'Abaixo de 650'
        WHEN fico_range_low < 700 THEN '650 a 699'
        WHEN fico_range_low < 750 THEN '700 a 749'
        ELSE '750 ou mais'
    END AS faixa_fico,
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
WHERE fico_range_low IS NOT NULL
GROUP BY
    CASE
        WHEN fico_range_low < 650 THEN 'Abaixo de 650'
        WHEN fico_range_low < 700 THEN '650 a 699'
        WHEN fico_range_low < 750 THEN '700 a 749'
        ELSE '750 ou mais'
    END
ORDER BY MIN(fico_range_low);
