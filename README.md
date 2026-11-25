# Academia GS FIT

Desenvolvemos o GS FIT para a AV3 de LAB II a partir do nosso projeto de Banco de Dados. O sistema ajuda a organizar as fichas de treino de uma academia. Cada ficha registra o que um aluno vai fazer, qual é o objetivo do treino, quanto tempo ele deve durar e quem é o instrutor responsável.

A aplicação roda no terminal e foi escrita em Python. Os cadastros ficam em um banco PostgreSQL hospedado no Neon e podem ser consultados de novo quando o programa é reaberto.

## Como usar

No primeiro acesso, escolha **Cadastrar usuário** e informe nome, e-mail e senha. Depois, escolha **Entrar na conta**. Esse cadastro identifica quem está usando o sistema. Os alunos da academia são cadastrados depois do login, no menu **Alunos**.

O menu principal tem três opções:

- **Alunos** — permite cadastrar, listar, pesquisar, editar e excluir alunos. O cadastro pede nome, CPF, telefone, data de nascimento e endereço. A pesquisa aceita parte do nome e a listagem exibe os alunos em ordem alfabética.
- **Instrutores** — reúne os dados dos profissionais, incluindo CREF e especialidade. Pelo menu é possível cadastrar um instrutor, consultar a lista, atualizar os dados e excluir o registro.
- **Treinos** — permite montar e consultar as fichas. Para cadastrar uma ficha, informe a descrição, o objetivo, a duração em minutos e os códigos do aluno e do instrutor. A duração precisa ser maior que zero. Também é possível editar ou excluir um treino.

Por exemplo, para montar a primeira ficha da Ana, cadastre a aluna em **Alunos** e o instrutor em **Instrutores**. Consulte as listas para ver o código de cada um. Depois, entre em **Treinos → Cadastrar** e use esses códigos para registrar a ficha. Em **Treinos → Listar**, aparecem os nomes da aluna e do instrutor junto com a descrição, o objetivo e a duração.

## Como os cadastros se relacionam

Um aluno pode ter várias fichas, e um instrutor pode acompanhar vários alunos. Cada treino guarda o código de um aluno e o de um instrutor. Por isso, para excluir alguém que ainda aparece em uma ficha, primeiro é preciso excluir o treino ou editar o vínculo.

Cada conta gerencia seus próprios registros. O programa usa o código do usuário que fez login para filtrar as consultas, edições e exclusões. O banco também exige que o aluno e o instrutor escolhidos para um treino pertençam à mesma conta.

Na pesquisa de alunos, usamos `LIKE` para localizar o trecho digitado e `ORDER BY` para ordenar os nomes. Na listagem de treinos, o `INNER JOIN` reúne os dados da ficha com os nomes do aluno e do instrutor. Os valores digitados no terminal são enviados ao PostgreSQL como parâmetros. A senha da conta é armazenada como um hash gerado com bcrypt e verificada no login.

## Como executar no Linux

Na pasta do projeto, use Python 3.14 ou superior. No terminal, crie o ambiente virtual e instale as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Na primeira configuração, copie `.env.example` para `.env` e preencha `DATABASE_URL` com o endereço de conexão do seu PostgreSQL. Guarde o arquivo `.env` apenas na sua máquina, pois a URL pode conter a senha do banco.

Se estiver preparando um banco vazio, execute primeiro [01_esquema.sql](SQL/01_esquema.sql), que cria as tabelas de alunos, instrutores e treinos. Em seguida, execute [02_usuarios_e_acessos.sql](SQL/02_usuarios_e_acessos.sql), que cria as contas e vincula os registros a elas. Esses scripts fazem parte da configuração inicial. Com o banco já configurado, basta ativar o ambiente virtual e iniciar o aplicativo:

```bash
python main.py
```
