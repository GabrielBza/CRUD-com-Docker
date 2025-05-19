-- Tabela Professor
CREATE TABLE IF NOT EXISTS Professor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    formacao VARCHAR(100)
);

INSERT INTO Professor (nome, formacao) VALUES
('Ana Costa', 'Matemática'),
('Bruno Lima', 'Física'),
('Carla Mendes', 'Química'),
('Daniel Rocha', 'História'),
('Eduarda Silva', 'Geografia'),
('Fernando Souza', 'Biologia');

-- Tabela Aluno
CREATE TABLE IF NOT EXISTS Aluno (
    matricula INTEGER PRIMARY KEY,
    nome VARCHAR(100),
    telefone VARCHAR(15),
    data_nascimento DATE
);

INSERT INTO Aluno (matricula, nome, telefone, data_nascimento) VALUES
(1001, 'Lucas Ribeiro', '11999990001', '2005-03-15'),
(1002, 'Mariana Lima', '11999990002', '2004-08-22'),
(1003, 'Pedro Alves', '11999990003', '2005-12-10'),
(1004, 'Sofia Martins', '11999990004', '2006-02-05'),
(1005, 'Rafael Costa', '11999990005', '2004-11-30'),
(1006, 'Isabela Rocha', '11999990006', '2005-06-25'),
(1007, 'Carlos Silva', '11999990007', '2005-07-10'),
(1008, 'Beatriz Santos', '11999990008', '2004-10-15'),
(1009, 'Gabriel Oliveira', '11999990009', '2005-04-20'),
(1010, 'Juliana Pires', '11999990010', '2004-12-11');

-- Tabela Disciplina
CREATE TABLE IF NOT EXISTS Disciplina (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao VARCHAR(200),
    fk_Professor_id INTEGER
);

INSERT INTO Disciplina (nome, descricao, fk_Professor_id) VALUES
('Matemática I', 'Introdução à Álgebra', 1),
('Física I', 'Mecânica Básica', 2),
('Química I', 'Conceitos Iniciais', 3),
('História Antiga', 'Sociedades Antigas', 4),
('Geografia Física', 'Formações Geográficas', 5),
('Biologia Celular', 'Estudo das Células', 6);

-- Tabela Prova
CREATE TABLE IF NOT EXISTS Prova (
    id SERIAL PRIMARY KEY,
    nota_max INTEGER,
    qtd_questoes INTEGER,
    data_criacao DATE,
    tipo VARCHAR(20),
    fk_Professor_id INTEGER,
    fk_Disciplina_id INTEGER
);

INSERT INTO Prova (nota_max, qtd_questoes, data_criacao, tipo, fk_Professor_id, fk_Disciplina_id) VALUES
(100, 10, '2024-03-01', 'Objetiva', 1, 1),
(80, 8, '2024-03-02', 'Dissertativa', 2, 2),
(90, 9, '2024-03-03', 'Mista', 3, 3),
(70, 7, '2024-03-04', 'Objetiva', 4, 4),
(85, 10, '2024-03-05', 'Mista', 5, 5),
(60, 6, '2024-03-06', 'Dissertativa', 6, 6),
(80, 9, '2024-03-07', 'Mista', 1, 1),
(75, 8, '2024-03-08', 'Objetiva', 2, 2);

-- Tabela Realizacao
CREATE TABLE IF NOT EXISTS Realizacao (
    id SERIAL PRIMARY KEY,
    fk_Prova_id INTEGER,
    fk_Aluno_matricula INTEGER,
    data DATE,
    nota_obtida NUMERIC DEFAULT NULL
);

-- Inserir realizações para cada aluno em cada disciplina
INSERT INTO Realizacao (fk_Prova_id, fk_Aluno_matricula, data, nota_obtida) VALUES
(1, 1001, '2024-04-01', 8.5), (2, 1001, '2024-04-02', 7.8), (3, 1001, '2024-04-03', 9.0), (4, 1001, '2024-04-04', 6.5), (5, 1001, '2024-04-05', 8.0), (6, 1001, '2024-04-06', 7.0),
(1, 1002, '2024-04-01', 8.8), (2, 1002, '2024-04-02', 7.5), (3, 1002, '2024-04-03', 8.5), (4, 1002, '2024-04-04', 6.0), (5, 1002, '2024-04-05', 7.8), (6, 1002, '2024-04-06', 7.2),
(1, 1003, '2024-04-01', 8.0), (2, 1003, '2024-04-02', 6.8), (3, 1003, '2024-04-03', 9.2), (4, 1003, '2024-04-04', 7.5), (5, 1003, '2024-04-05', 8.2), (6, 1003, '2024-04-06', 7.7),
(1, 1004, '2024-04-01', 7.0), (2, 1004, '2024-04-02', 6.5), (3, 1004, '2024-04-03', 7.8), (4, 1004, '2024-04-04', 8.0), (5, 1004, '2024-04-05', 7.2), (6, 1004, '2024-04-06', 7.4),
(1, 1005, '2024-04-01', 7.5), (2, 1005, '2024-04-02', 7.9), (3, 1005, '2024-04-03', 8.8), (4, 1005, '2024-04-04', 6.7), (5, 1005, '2024-04-05', 7.5), (6, 1005, '2024-04-06', 7.0),
(1, 1006, '2024-04-01', 9.0), (2, 1006, '2024-04-02', 8.5), (3, 1006, '2024-04-03', 9.1), (4, 1006, '2024-04-04', 8.0), (5, 1006, '2024-04-05', 8.3), (6, 1006, '2024-04-06', 8.8),
(1, 1007, '2024-04-01', 7.7), (2, 1007, '2024-04-02', 7.9), (3, 1007, '2024-04-03', 8.7), (4, 1007, '2024-04-04', 7.4), (5, 1007, '2024-04-05', 7.1), (6, 1007, '2024-04-06', 7.8),
(1, 1008, '2024-04-01', 8.5), (2, 1008, '2024-04-02', 7.3), (3, 1008, '2024-04-03', 8.0), (4, 1008, '2024-04-04', 6.5), (5, 1008, '2024-04-05', 7.8), (6, 1008, '2024-04-06', 6.9),
(1, 1009, '2024-04-01', 9.2), (2, 1009, '2024-04-02', 8.2), (3, 1009, '2024-04-03', 8.8), (4, 1009, '2024-04-04', 7.5), (5, 1009, '2024-04-05', 8.0), (6, 1009, '2024-04-06', 7.2),
(1, 1010, '2024-04-01', 8.3), (2, 1010, '2024-04-02', 7.9), (3, 1010, '2024-04-03', 8.6), (4, 1010, '2024-04-04', 8.2), (5, 1010, '2024-04-05', 7.6), (6, 1010, '2024-04-06', 8.1);


-- Adição de constraints (chaves estrangeiras)
DO $$
BEGIN
    ALTER TABLE Disciplina ADD CONSTRAINT FK_Disciplina_2
        FOREIGN KEY (fk_Professor_id) REFERENCES Professor(id) ON DELETE RESTRICT;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END$$;

DO $$
BEGIN
    ALTER TABLE Prova ADD CONSTRAINT FK_Prova_2
        FOREIGN KEY (fk_Professor_id) REFERENCES Professor(id) ON DELETE CASCADE;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END$$;

DO $$
BEGIN
    ALTER TABLE Prova ADD CONSTRAINT FK_Prova_3
        FOREIGN KEY (fk_Disciplina_id) REFERENCES Disciplina(id) ON DELETE CASCADE;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END$$;

DO $$
BEGIN
    ALTER TABLE Realizacao ADD CONSTRAINT FK_Realizacao_1
        FOREIGN KEY (fk_Prova_id) REFERENCES Prova(id) ON DELETE RESTRICT;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END$$;

DO $$
BEGIN
    ALTER TABLE Realizacao ADD CONSTRAINT FK_Realizacao_2
        FOREIGN KEY (fk_Aluno_matricula) REFERENCES Aluno(matricula) ON DELETE RESTRICT;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END$$;
