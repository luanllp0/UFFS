-- 1. RF04: Cadastrar Novo Cliente
INSERT INTO Cliente (nome, telefone, email) 
VALUES ('Empresa Cliente Exemplo', '(49) 99999-8888', 'contato@exemplo.com');

-- 2. RF05: Cadastrar Novo Caminhão
INSERT INTO Caminhao (placa, modeloDescricao, idCliente) 
VALUES ('QJA-2025', 'Volvo FH 540', 1);

-- 3. RF06: Lançar Novo Serviço (Técnico)
INSERT INTO Servico 
    (Data, hora, descricao, valor, MesFaturamento, idTecnico, placaCaminhao) 
VALUES (
    '2025-11-17', '14:30:00', 'Troca de compressor e limpeza do sistema.', 650.00, 
    '2025-11-01', 2, 'QJA-2025'
);

-- 4. RF08: Listar Serviços Pendentes (Tela de Conciliação)
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

-- 5. RF08: Editar Serviço (Ação de Conciliação)
UPDATE Servico
SET 
    valor = 620.00,
    descricao = 'Troca de compressor e limpeza do sistema (ajuste de valor).'
WHERE IdServico = 1;

-- 6. RF08: Confirmar Serviço (Ação de Conciliação)
UPDATE Servico
SET 
    statusConciliacao = 'Confirmado',
    idColaborador = 1 
WHERE IdServico = 1;

-- 7. RF08: Excluir Serviço (Ação de Conciliação)
DELETE FROM Servico
WHERE IdServico = 4; 

-- 8. RF07: Consultar Serviços por Múltiplos Filtros
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

-- 9. RF12: Relatório de Desempenho Técnico
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

-- 10. RF10: Relatório de Metas e Excedentes
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

-- 11. RF11: Auditoria de Clientes (Subconsulta)
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
