CREATE TABLE IF NOT EXISTS aluno (
    codigo_aluno INT GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    data_nascimento DATE NOT NULL,
    endereco VARCHAR(200) NOT NULL,
    CONSTRAINT pk_aluno PRIMARY KEY (codigo_aluno),
    CONSTRAINT uq_cpf_aluno UNIQUE (cpf)
);

CREATE TABLE IF NOT EXISTS instrutor (
    codigo_instrutor INT GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    cref VARCHAR(20) NOT NULL,
    cpf CHAR(11) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    especialidade VARCHAR(80) NOT NULL,
    endereco VARCHAR(200) NOT NULL,
    CONSTRAINT pk_instrutor PRIMARY KEY (codigo_instrutor),
    CONSTRAINT uq_cref_instrutor UNIQUE (cref),
    CONSTRAINT uq_cpf_instrutor UNIQUE (cpf)
);

CREATE TABLE IF NOT EXISTS treino (
    codigo_treino INT GENERATED ALWAYS AS IDENTITY,
    descricao TEXT NOT NULL,
    objetivo VARCHAR(50) NOT NULL,
    duracao_minutos INT NOT NULL,
    codigo_aluno INT NOT NULL,
    codigo_instrutor INT NOT NULL,
    CONSTRAINT pk_treino PRIMARY KEY (codigo_treino),
    CONSTRAINT fk_treino_aluno FOREIGN KEY (codigo_aluno)
        REFERENCES aluno (codigo_aluno)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_treino_instrutor FOREIGN KEY (codigo_instrutor)
        REFERENCES instrutor (codigo_instrutor)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_duracao_minutos CHECK (duracao_minutos > 0)
);