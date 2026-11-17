BEGIN;

CREATE TABLE usuario (
    codigo_usuario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL
);

ALTER TABLE aluno
    ADD COLUMN codigo_usuario INT NOT NULL REFERENCES usuario (codigo_usuario),
    ADD CONSTRAINT uq_aluno_conta UNIQUE (codigo_usuario, codigo_aluno);

ALTER TABLE instrutor
    ADD COLUMN codigo_usuario INT NOT NULL REFERENCES usuario (codigo_usuario),
    ADD CONSTRAINT uq_instrutor_conta UNIQUE (codigo_usuario, codigo_instrutor);

ALTER TABLE treino
    ADD COLUMN codigo_usuario INT NOT NULL REFERENCES usuario (codigo_usuario),
    ADD CONSTRAINT fk_treino_aluno_conta FOREIGN KEY (codigo_usuario, codigo_aluno)
        REFERENCES aluno (codigo_usuario, codigo_aluno),
    ADD CONSTRAINT fk_treino_instrutor_conta FOREIGN KEY (codigo_usuario, codigo_instrutor)
        REFERENCES instrutor (codigo_usuario, codigo_instrutor);

COMMIT;
