-- 1. Criação da Tabela-Pai (Generalização)
-- Usamos SERIAL para auto-incrementar o ID (PK)
CREATE TABLE Usuario (
    IdUsuario SERIAL PRIMARY KEY,
    Login VARCHAR(100) NOT NULL UNIQUE, -- Login (ou email) deve ser único
    senha VARCHAR(255) NOT NULL, -- Senha (deve ser armazenada com hash)
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20)
);

-- 2. Tabela Cliente
CREATE TABLE Cliente (
    IdCliente SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE -- Email do cliente também deve ser único
);

-- 3. Tabela Caminhão
-- A placa é um texto (VARCHAR) e é a chave primária natural
CREATE TABLE Caminhao (
    placa VARCHAR(10) PRIMARY KEY,
    modeloDescricao VARCHAR(255),
    -- Criação da Chave Estrangeira (FK) para Cliente
    idCliente INT NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES Cliente(IdCliente)
    -- ON DELETE RESTRICT (Impede deletar um cliente que tenha caminhão)
    -- ON UPDATE CASCADE (Se o idCliente mudar, atualiza aqui)
    -- [cite: 2213-2214]
);

-- 4. Criação das Tabelas-Filhas (Especialização)
-- A PK de Tecnico é também a FK que referencia Usuario
CREATE TABLE Tecnico_Terceirizado (
    IdUsuario INT PRIMARY KEY,
    metaFaturamento NUMERIC(10, 2) NOT NULL DEFAULT 0, -- NUMERIC é o tipo correto para dinheiro [cite: 2167]
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario) ON DELETE CASCADE
    -- ON DELETE CASCADE: Se o Usuario for deletado, o Tecnico também é.
);

CREATE TABLE Colaborador_Interno (
    IdUsuario INT PRIMARY KEY,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario) ON DELETE CASCADE
    -- ON DELETE CASCADE: Se o Usuario for deletado, o Colaborador também é.
);

-- 5. Tabela Serviço (A tabela central)
CREATE TABLE Servico (
    IdServico SERIAL PRIMARY KEY,
    Data DATE NOT NULL, -- Tipo correto para Data [cite: 2168]
    hora TIME NOT NULL, -- Tipo correto para Hora
    descricao TEXT, -- TEXT para descrições longas [cite: 2169]
    valor NUMERIC(10, 2) NOT NULL,
    statusConciliacao VARCHAR(20) NOT NULL DEFAULT 'Pendente', -- Ex: 'Pendente', 'Confirmado'
    MesFaturamento DATE NOT NULL, -- Para controlar o rollover do RF10
    
    -- Chaves Estrangeiras (FKs)
    idTecnico INT NOT NULL,
    placaCaminhao VARCHAR(10) NOT NULL,
    idColaborador INT NULL, -- << IMPORTANTE: "NULL" permite valores nulos (serviço pendente)

    FOREIGN KEY (idTecnico) REFERENCES Tecnico_Terceirizado(IdUsuario),
    FOREIGN KEY (placaCaminhao) REFERENCES Caminhao(placa),
    FOREIGN KEY (idColaborador) REFERENCES Colaborador_Interno(IdUsuario)
);

-- 6. Tabela Histórico de Alteração (Auditoria)
CREATE TABLE Historico_Alteracao (
    idAlteracao SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- TIMESTAMP = Data + Hora [cite: 2168]
    descrMudanca TEXT NOT NULL,
    
    -- Chaves Estrangeiras (FKs)
    idUsuario INT NOT NULL,
    idServico INT NOT NULL,
    
    FOREIGN KEY (idUsuario) REFERENCES Usuario(IdUsuario),
    FOREIGN KEY (idServico) REFERENCES Servico(IdServico) ON DELETE CASCADE
    -- Se um Serviço for deletado, seu histórico de alteração é deletado junto.
);
