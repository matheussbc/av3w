CREATE DATABASE CinemaDB;

CREATE TABLE Filme (
    id_filme SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    genero VARCHAR(50),
    duracao INT,
    classificacao VARCHAR(20),
    sinopse TEXT
);

CREATE TABLE Sala (
    id_sala SERIAL PRIMARY KEY,
    nome_sala VARCHAR(50) NOT NULL,
    capacidade INT NOT NULL
);

CREATE TABLE Sessao (
    id_sessao SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    id_filme INT NOT NULL REFERENCES Filme(id_filme) ON DELETE CASCADE,
    id_sala INT NOT NULL REFERENCES Sala(id_sala) ON DELETE CASCADE
);

CREATE TABLE Cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cpf VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    telefone VARCHAR(30)
);

CREATE TABLE Ingresso (
    id_ingresso SERIAL PRIMARY KEY,
    valor DECIMAL(10,2) NOT NULL,
    forma_pagamento VARCHAR(30),
    id_sessao INT NOT NULL REFERENCES Sessao(id_sessao) ON DELETE CASCADE,
    id_cliente INT NOT NULL REFERENCES Cliente(id_cliente) ON DELETE CASCADE
);

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    senha_hash VARCHAR(255),
    tipo VARCHAR(20)
);

INSERT INTO Filme (titulo, genero, duracao, classificacao, sinopse) VALUES
('Matrix', 'Ficção Científica', 136, '16 anos', 'Um hacker descobre a verdade sobre sua realidade.'),
('Titanic', 'Romance', 195, '12 anos', 'Uma história de amor a bordo do Titanic.'),
('O Senhor dos Anéis, 'Fantasia', 178, '12 anos', 'Frodo inicia a jornada para destruir o Anel.');

INSERT INTO Sala (nome_sala, capacidade) VALUES
('Sala 1', 150),
('Sala 2', 100),
('Sala 3', 80);

INSERT INTO Sessao (data, horario, id_filme, id_sala) VALUES
('2025-11-25', '19:00', 1, 1),
('2025-11-25', '21:00', 2, 2),
('2025-11-26', '18:30', 3, 3);

INSERT INTO Cliente (nome, cpf, email, telefone) VALUES
('Ana', '12345678900', 'ana.x@email.com', '82999990001'),
('Carlos', '98765432100', 'carlos.x@email.com', '82999990002');

INSERT INTO Ingresso (valor, forma_pagamento, id_sessao, id_cliente) VALUES
(30.00, 'Cartão', 1, 1),
(25.00, 'Pix', 2, 2),
(20.00, 'Dinheiro', 3, 1);

INSERT INTO Usuario (username, senha_hash, tipo)
VALUES ('admin', encode(digest('admin123','sha256'),'hex'), 'admin');