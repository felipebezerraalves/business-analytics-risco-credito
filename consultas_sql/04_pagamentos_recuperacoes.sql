
-- PROJETO 04
-- 04 | PAGAMENTOS E RECUPERACOES


-- 1. Pagamentos por situacao do emprestimo

SELECT
    loan_status AS situacao_emprestimo,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(SUM(loan_amnt), 2) AS valor_concedido,
    ROUND(SUM(total_pymnt), 2) AS pagamentos_recebidos,
    ROUND(SUM(total_rec_prncp), 2) AS principal_recebido,
    ROUND(SUM(total_rec_int), 2) AS juros_recebidos,
    ROUND(SUM(recoveries), 2) AS recuperacoes
FROM accepted_loans_sample
GROUP BY loan_status;


-- 2. Percentual do principal recebido

SELECT
    loan_status AS situacao_emprestimo,
    ROUND(SUM(loan_amnt), 2) AS valor_concedido,
    ROUND(SUM(total_rec_prncp), 2) AS principal_recebido,
    ROUND(
        SUM(total_rec_prncp) * 100.0 /
        NULLIF(SUM(loan_amnt), 0),
        2
    ) AS percentual_principal_recebido
FROM accepted_loans_sample
GROUP BY loan_status;


-- 3. Diferenca entre principal concedido e recebido

SELECT
    loan_status AS situacao_emprestimo,
    ROUND(SUM(loan_amnt), 2) AS valor_concedido,
    ROUND(SUM(total_rec_prncp), 2) AS principal_recebido,
    ROUND(
        SUM(loan_amnt) - SUM(total_rec_prncp),
        2
    ) AS diferenca_principal
FROM accepted_loans_sample
GROUP BY loan_status;


