-- SCRIPT DE CRIAÇÃO E DADOS INICIAIS --

-- 1. Tabela Usuário 
CREATE TABLE Usuario (
    IdUsuario SERIAL PRIMARY KEY,
    Login VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    tipo VARCHAR(50) NOT NULL 
);

-- 2. Tabela Cliente
CREATE TABLE Cliente (
    IdCliente SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

-- 3. Tabela Caminhão
CREATE TABLE Caminhao (
    placa VARCHAR(10) PRIMARY KEY,
    modeloDescricao VARCHAR(255),
    idCliente INT NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES Cliente (IdCliente)
);

-- 4. Tabela Serviço
CREATE TABLE Servico (
    IdServico SERIAL PRIMARY KEY,
    Data DATE NOT NULL,
    hora TIME NOT NULL,
    descricao TEXT,
    valor NUMERIC(10, 2) NOT NULL,
    statusConciliacao VARCHAR(20) NOT NULL DEFAULT 'Pendente',
    MesFaturamento DATE NOT NULL,
    idTecnico INT NOT NULL,
    placaCaminhao VARCHAR(10) NOT NULL,
    idColaborador INT NULL,
    FOREIGN KEY (idTecnico) REFERENCES Usuario (IdUsuario),
    FOREIGN KEY (placaCaminhao) REFERENCES Caminhao(placa),
    FOREIGN KEY (idColaborador) REFERENCES Usuario(IdUsuario)
);

-- DADOS INICIAIS --

-- Usuários (Senha padrão: 123)
INSERT INTO Usuario (Login, senha, nome, telefone, tipo) VALUES
('admin@rodofrio.com', '123', 'Colaborador Admin', '(49) 91111-1111', 'Colaborador Interno'),
('sergio.tecnico@email.com', '123', 'Sérgio Peloso', '(49) 92222-2222', 'Tecnico Terceirizado');