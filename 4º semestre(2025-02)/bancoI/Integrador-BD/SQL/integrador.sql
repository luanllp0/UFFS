-- 1. Tabela Usuário
CREATE TABLE Usuario (
    IdUsuario SERIAL PRIMARY KEY,
    Login VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20)
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
    FOREIGN KEY (idCliente) REFERENCES Cliente(IdCliente)
);

-- 4. Tabelas Técnico Terceirizado e Colaborador Interno
CREATE TABLE Tecnico_Terceirizado (
    IdUsuario INT PRIMARY KEY,
    metaFaturamento NUMERIC(10, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario) ON DELETE CASCADE
);

CREATE TABLE Colaborador_Interno (
    IdUsuario INT PRIMARY KEY,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario) ON DELETE CASCADE
);

-- 5. Tabela Serviço
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
    FOREIGN KEY (idTecnico) REFERENCES Tecnico_Terceirizado(IdUsuario),
    FOREIGN KEY (placaCaminhao) REFERENCES Caminhao(placa),
    FOREIGN KEY (idColaborador) REFERENCES Colaborador_Interno(IdUsuario)
);

-- 6. Tabela Histórico de Alteração
CREATE TABLE Historico_Alteracao (
    idAlteracao SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descrMudanca TEXT NOT NULL,
    idUsuario INT NOT NULL,
    idServico INT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(IdUsuario),
    FOREIGN KEY (idServico) REFERENCES Servico(IdServico) ON DELETE CASCADE
);
