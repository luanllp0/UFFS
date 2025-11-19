1. RF04: Cadastrar Novo Cliente
Objetivo: Permite ao colaborador interno registrar um novo cliente no banco de dados.
Complexidade: Comando DML de inserção.
SQL
INSERT INTO Cliente (nome, telefone, email) 
VALUES ('Empresa Cliente Exemplo', '(49) 99999-8888', 'contato@exemplo.com');

2. RF05: Cadastrar Novo Caminhão
Objetivo: Permite cadastrar um veículo e associá-lo imediatamente a um cliente existente através da chave estrangeira.
Complexidade: Inserção com integridade referencial.
SQL
INSERT INTO Caminhao (placa, modeloDescricao, idCliente) 
VALUES ('QJA-2025', 'Volvo FH 540', 1);

3. RF06: Lançar Novo Serviço (Técnico)
Objetivo: Permite ao técnico registrar um serviço realizado. O sistema define automaticamente o status como 'Pendente'.
Complexidade: Inserção com múltiplas chaves estrangeiras (Técnico e Caminhão).
SQL
INSERT INTO Servico 
    (Data, hora, descricao, valor, MesFaturamento, idTecnico, placaCaminhao) 
VALUES (
    '2025-11-17', '14:30:00', 'Troca de compressor e limpeza do sistema.', 650.00, 
    '2025-11-01', 2, 'QJA-2025'
);

4. RF08: Listar Serviços Pendentes (Tela de Conciliação)
Objetivo: Exibe para o Colaborador Interno todos os serviços que aguardam conferência, trazendo os nomes legíveis do técnico e do cliente em vez de apenas códigos.
Complexidade: Utilização de múltiplos JOINs entre 5 tabelas diferentes.
SQL
SELECT 
    s.IdServico, s.Data, s.descricao, s.valor,
    t_usuario.nome AS nome_tecnico,
    cli.nome AS nome_cliente, c.placa
FROM Servico s
JOIN Tecnico_Terceirizado t ON s.idTecnico = t.IdUsuario
JOIN Usuario t_usuario ON t.IdUsuario = t_usuario.IdUsuario
JOIN Caminhao c ON s.placaCaminhao = c.placa
JOIN Cliente cli ON c.idCliente = cli.IdCliente
WHERE s.statusConciliacao = 'Pendente'
ORDER BY s.Data;

5. RF08: Editar Serviço (Ação de Conciliação)
Objetivo: Permite ao colaborador corrigir informações (como valor ou descrição) de um serviço antes de aprová-lo.
Complexidade: Comando UPDATE direcionado a um registro específico.
SQL
UPDATE Servico
SET 
    valor = 620.00,
    descricao = 'Troca de compressor e limpeza do sistema (ajuste de valor).'
WHERE IdServico = 1;

6. RF08: Confirmar Serviço (Ação de Conciliação)
Objetivo: Finaliza o processo de conciliação, alterando o status para 'Confirmado' e registrando o ID do colaborador responsável pela aprovação.
Complexidade: Comando UPDATE com atualização de status e chave estrangeira.
SQL
UPDATE Servico
SET 
    statusConciliacao = 'Confirmado',
    idColaborador = 1 
WHERE IdServico = 1;

7. RF08: Excluir Serviço (Ação de Conciliação)
Objetivo: Permite ao colaborador remover do sistema um lançamento feito incorretamente ou em duplicidade.
Complexidade: Comando DELETE.
SQL
DELETE FROM Servico
WHERE IdServico = 4; 

8. RF07: Consultar Serviços por Múltiplos Filtros
Objetivo: Permite a busca avançada de histórico de serviços combinando filtros por cliente, técnico e período de datas.
Complexidade: JOINs combinados com cláusula WHERE composta e operadores lógicos (AND, BETWEEN).
SQL
SELECT 
    s.IdServico, s.Data, s.descricao, s.valor,
    u.nome AS nome_tecnico, c.nome AS nome_cliente
FROM Servico s
JOIN Caminhao cam ON s.placaCaminhao = cam.placa
JOIN Cliente c ON cam.idCliente = c.IdCliente
JOIN Tecnico_Terceirizado t ON s.idTecnico = t.IdUsuario
JOIN Usuario u ON t.IdUsuario = u.IdUsuario
WHERE 
    c.IdCliente = 1 
    AND s.idTecnico = 2 
    AND s.Data BETWEEN '2025-11-01' AND '2025-11-30';

9. RF12: Relatório de Desempenho Técnico
Objetivo: Gera um consolidado mostrando a quantidade de serviços realizados e o valor total gerado por cada técnico.
Complexidade: Uso de funções de agregação (COUNT, SUM) agrupadas (GROUP BY) por técnico.
SQL
SELECT 
    u.nome AS nome_tecnico,
    COUNT(s.IdServico) AS total_servicos_confirmados,
    SUM(s.valor) AS valor_total_confirmado
FROM Servico s
JOIN Tecnico_Terceirizado t ON s.idTecnico = t.IdUsuario
JOIN Usuario u ON t.IdUsuario = u.IdUsuario
WHERE s.statusConciliacao = 'Confirmado'
GROUP BY u.nome
ORDER BY valor_total_confirmado DESC;

10. RF10: Relatório de Metas e Excedentes
Objetivo: Aplica a regra de negócio de faturamento. Compara o total produzido pelo técnico com sua meta e calcula o valor excedente a ser pago no mês seguinte.
Complexidade: Cálculo aritmético dentro da projeção e uso da função GREATEST para evitar valores negativos.
SQL
SELECT 
    u.nome AS nome_tecnico,
    t.metaFaturamento,
    SUM(s.valor) AS total_faturado_mes,
    GREATEST(0, (SUM(s.valor) - t.metaFaturamento)) AS valor_excedente_proximo_mes
FROM Servico s
JOIN Tecnico_Terceirizado t ON s.idTecnico = t.IdUsuario
JOIN Usuario u ON t.IdUsuario = u.IdUsuario
WHERE 
    s.statusConciliacao = 'Confirmado' 
    AND s.MesFaturamento = '2025-11-01'
GROUP BY 
    u.nome, t.metaFaturamento;

11. RF11: Auditoria de Clientes (Subconsulta)
Objetivo: Identificar clientes que demandaram serviços de alto valor (acima de R$ 1.000,00) para fins de análise ou auditoria.
Complexidade: Utilização de Subconsulta aninhada na cláusula WHERE com o operador IN.
SQL
SELECT 
    c.nome, c.email, c.telefone
FROM 
    Cliente c
WHERE 
    c.IdCliente IN (
        SELECT cam.idCliente
        FROM Servico s
        JOIN Caminhao cam ON s.placaCaminhao = cam.placa
        WHERE s.valor > 1000 
    );




