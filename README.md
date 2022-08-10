# Question Management
Um simples projeto de gerenciamento de perguntas, para inserção de perguntas e respostas, facilitando o treinamento de um chatbot (ainda decidindo) Rasa, botpress.. etc.

## Descrição

O projeto conta com uma página de login, necessária autenticação para uso (maior segurança). Uma página para cadastro de usuários, e uma página para o cadastro de 
perguntas e respostas. Um usuário administrador, para controlar as perguntas e respostas, validando as que estiverem boas o suficientes para serem inseridas no 
treinamento, e usuários comuns que fazem a inserção dessas perguntas e respostas de maneira simplificada.

## Getting Started

### Dependencias

* Python 3.6 ou acima.
* flask
* flask-login
* flask-sqlalchemy
* PostgreSQL, MySQL ou SQLite (decidindo)

### Instalação

* Basta baixar o projeto, instalar as dependências (Python, Flask .. etc) que o ambiente estará preparado.
```
pip install flask
pip install flask-login
pip install flask-sqlalchemy
```

### Executando

* Execute o arquivo main.py, que abrirá o servidor (como indica abaixo), e cole o link http no navegador (como indica na 6ª linha abaixo).
```
* Serving Flask app 'website' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 504-658-042
```

## Ajuda

Alguns problemas comuns ocorrem quando não se tem o python rodando corretamente, problemas com path.

## Autores

Pedro Henrique
(https://github.com/pedromaia1218)

Davi Freire
(https://github.com/Dvfreii)


## Histórico de versões

* 0.2
    * Autenticação.
    * Cadastro de novos usuários (somente por um administrador).
    * Cadastro de QnA para o banco de dados (perguntas e respostas).
    * Visualizar todas as QnAs do seu setor.
* 0.1
    * Esqueleto básico do projeto.

## Referências
