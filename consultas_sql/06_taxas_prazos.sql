
-- PROJETO 04
-- 06 | TAXAS DE JUROS E PRAZOS


-- 1. Taxa de juros e parcela por situacao

SELECT
    loan_status AS situacao_emprestimo,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(AVG(int_rate), 2) AS juros_medios,
    ROUND(AVG(installment), 2) AS parcela_media
FROM accepted_loans_sample
GROUP BY loan_status;


-- 2. Distribuicao por prazo do emprestimo

SELECT
    term AS prazo_emprestimo,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_concedido,
    ROUND(AVG(int_rate), 2) AS juros_medios
FROM accepted_loans_sample
GROUP BY term
ORDER BY term;


-- 3. Contratos baixados por prazo

SELECT
    term AS prazo_emprestimo,
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
GROUP BY term
ORDER BY term;
