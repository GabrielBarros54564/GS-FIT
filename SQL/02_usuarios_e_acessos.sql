begin;

create table usuario (
    codigo_usuario int generated always as identity primary key,
    nome_usuario varchar(100) not null,
    email_usuario varchar(100) not null unique,
    senha_hash text not null
);

alter Table aluno
    add column codigo_usuario int not null REFERENCES usuario(codigo_usuario);
    add constraint uq_aluno_conta UNIQUE (codigo_usuario, codigo_aluno);

alter Table instrutor
    add column codigo_usuario int not null REFERENCES usuario(codigo_usuario);
    add constraint uq_instrutor_conta UNIQUE (codigo_usuario, codigo_instrutor);  r

alter TABLE treino
    add column codigo_usuario int not null REFERENCES usuario(codigo_usuario);
    add constraint fk_treinno_aluno_conta foreign key (codigo_usuario, codigo_aluno) references aluno(codigo_usuario, codigo_aluno),
    add constraint fk_treinno_instrutor_conta foreign key (codigo_usuario, codigo_instrutor) references instrutor(codigo_usuario, codigo_instrutor);

commit;
