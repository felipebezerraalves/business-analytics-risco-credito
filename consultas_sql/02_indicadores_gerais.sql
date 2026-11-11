
-- PROJETO 04
-- 02 | INDICADORES GERAIS DA CARTEIRA


-- 1. Quantidade e valores dos emprestimos

SELECT
    COUNT(*) AS quantidade_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_total_concedido,
    ROUND(AVG(loan_amnt), 2) AS valor_medio_emprestimo,
    MIN(loan_amnt) AS menor_emprestimo,
    MAX(loan_amnt) AS maior_emprestimo
FROM accepted_loans_sample;


-- 2. Valor concedido por situacao

SELECT
    loan_status AS situacao_emprestimo,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_total_concedido,
    ROUND(AVG(loan_amnt), 2) AS valor_medio_emprestimo
FROM accepted_loans_sample
GROUP BY loan_status
ORDER BY SUM(loan_amnt) DESC;


-- 3. Participacao financeira por situacao

SELECT
    loan_status AS situacao_emprestimo,
    ROUND(SUM(loan_amnt), 2) AS valor_total_concedido,
    ROUND(
        SUM(loan_amnt) * 100.0 /
        NULLIF(
            (SELECT SUM(loan_amnt)
             FROM accepted_loans_sample),
            0
        ),
        2
    ) AS percentual_valor_concedido
FROM accepted_loans_sample
GROUP BY loan_status
ORDER BY SUM(loan_amnt) DESC;

