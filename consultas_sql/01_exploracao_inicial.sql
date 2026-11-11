
-- PROJETO 04
-- 01 | EXPLORACAO INICIAL


-- 1. Quantidade total de emprestimos

SELECT
    COUNT(*) AS total_emprestimos
FROM accepted_loans_sample;


-- 2. Visualizacao dos primeiros registros

SELECT *
FROM accepted_loans_sample
LIMIT 5;


-- 3. Estrutura da tabela

PRAGMA table_info(accepted_loans_sample);


-- 4. Quantidade por situacao do emprestimo

SELECT
    loan_status AS situacao_emprestimo,
    COUNT(*) AS quantidade_emprestimos
FROM accepted_loans_sample
GROUP BY loan_status
ORDER BY COUNT(*) DESC;


-- 5. Percentual por situacao do emprestimo

SELECT
    loan_status AS situacao_emprestimo,
    COUNT(*) AS quantidade_emprestimos,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM accepted_loans_sample),
        2
    ) AS percentual_emprestimos
FROM accepted_loans_sample
GROUP BY loan_status
ORDER BY COUNT(*) DESC;
