-- 1. USUÁRIOS (Pai da hierarquia)
-- (SERIAL PKs serão 1, 2, 3)
INSERT INTO Usuario (Login, senha, nome, telefone) VALUES
('admin@rodofrio.com', 'hash_senha_admin', 'Colaborador Interno Admin', '(49) 91111-1111'),
('sergio.tecnico@email.com', 'hash_senha_sergio', 'Sérgio Peloso', '(49) 92222-2222'),
('maria.tecnica@email.com', 'hash_senha_maria', 'Maria Silva', '(49) 93333-3333');

-- 2. CLIENTES
-- (SERIAL PKs serão 1, 2)
INSERT INTO Cliente (nome, telefone, email) VALUES
('Transportadora Zago', '(49) 94444-4444', 'contato@zago.com'),
('Friolog Cargas Refrigeradas', '(49) 95555-5555', 'logistica@friolog.com');

-- 3. COLABORADOR INTERNO (Filho de Usuário)
-- (Linka com Usuário 1)
INSERT INTO Colaborador_Interno (IdUsuario) VALUES (1);

-- 4. TÉCNICO TERCEIRIZADO (Filho de Usuário)
-- (Linka com Usuários 2 e 3)
INSERT INTO Tecnico_Terceirizado (IdUsuario, metaFaturamento) VALUES
(2, 5000.00), -- Meta de 5k para o Sérgio
(3, 3500.00); -- Meta de 3.5k para a Maria

-- 5. CAMINHÕES
-- (Linka com Clientes 1 e 2)
INSERT INTO Caminhao (placa, modeloDescricao, idCliente) VALUES
('AAA-1111', 'Scania R450', 1),          -- Caminhão 1 do Cliente 1
('BBB-2222', 'Mercedes-Benz Actros', 1), -- Caminhão 2 do Cliente 1
('CCC-3333', 'Volvo FH 540', 2);         -- Caminhão 1 do Cliente 2

-- 6. SERVIÇOS (O núcleo dos testes)
-- Vamos criar serviços para testar todas as suas consultas
-- (SERIAL PKs serão 1, 2, 3, 4, 5)

-- Serviços CONFIRMADOS para testar relatórios (RF10, RF12)
INSERT INTO Servico (Data, hora, descricao, valor, MesFaturamento, idTecnico, placaCaminhao, statusConciliacao, idColaborador) VALUES
('2025-11-05', '10:00:00', 'Revisão completa do sistema SLX', 2800.00, '2025-11-01', 2, 'AAA-1111', 'Confirmado', 1),
('2025-11-07', '14:30:00', 'Troca de compressor', 3000.00, '2025-11-01', 2, 'BBB-2222', 'Confirmado', 1),
('2025-11-06', '09:15:00', 'Conserto de vazamento de gás (valor alto)', 1200.00, '2025-11-01', 3, 'CCC-3333', 'Confirmado', 1),

-- Serviços PENDENTES para testar Conciliação (RF08)
('2025-11-10', '11:00:00', 'Troca de óleo e filtros', 500.00, '2025-11-01', 3, 'CCC-3333', 'Pendente', NULL),
('2025-11-11', '16:45:00', 'Reparo elétrico simples', 300.00, '2025-11-01', 2, 'AAA-1111', 'Pendente', NULL);
-- (O IdServico 5 será usado para testar o UPDATE e DELETE)

-- 7. HISTÓRICO DE ALTERAÇÃO
-- (Linka com Usuário 1 e Serviço 1)
INSERT INTO Historico_Alteracao (descrMudanca, idUsuario, idServico) VALUES
('Serviço confirmado pelo administrador.', 1, 1);

– testar meta mensal | prox mes
-- Adicionando serviços extras para a Maria (ID 3) ultrapassar a meta de 3500
INSERT INTO Servico (Data, hora, descricao, valor, MesFaturamento, idTecnico, placaCaminhao, statusConciliacao, idColaborador) VALUES
('2025-11-15', '08:00:00', 'Instalação de Thermo King', 2500.00, '2025-11-01', 3, 'CCC-3333', 'Confirmado', 1),
('2025-11-20', '13:30:00', 'Manutenção preventiva', 400.00, '2025-11-01', 3, 'CCC-3333', 'Confirmado', 1);


