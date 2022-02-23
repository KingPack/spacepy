# Branch desatualizada va para o branch master

Branch [master](https://github.com/KingPack/spacepy)

Projeto desenvolvido e mantido por [KingPack](https://github.com/KingPack).

## Back-end Challenge 2021 - Space Flight News

Este é um desafio de programação back-end que consiste na replicação de uma API Restful baseada na API [Space Flight News](https://api.spaceflightnewsapi.net/v3/documentation).

## Tecnologias

- [Poetry](https://python-poetry.org/docs/)
- [Git](https://git-scm.com)
- [Python 3](https://www.python.org/downloads/)
- [IPython](https://ipython.org)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
- [Gunicorn](https://gunicorn.org)
- [Postgres](https://www.postgresql.org)
- [Heroku](heroku.com)
- [Docker](https://www.docker.com)
- [Portainer](https://www.portainer.io)
- [Flasgger](https://github.com/flasgger/flasgger)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
- [Schedule](https://schedule.readthedocs.io/en/stable/)

## Requisitos

### 1º Poetry

Para a instalação do  [Poetry](https://python-poetry.org/docs/)

### 2º Python 3

Você deve instalar a versão 3.9.10 ou maior do [Python](https://www.python.org/downloads/).

### 3º Git

Documentação  para instalação do [Git](https://git-scm.com/downloads).

### 4º Banco de dados

Tenha os dados para se conectar no banco de dados.

Após fazer o git clone do repositório, você deve criar um arquivo chamado [config.py](https://github.com/KingPack/spacepy#iniciando-o-banco-de-dados) e colocar as configurações do banco de dados.

## Instalação

Agora, vamos para a instalação do projeto.

Mas antes devemos verificar a se temos os requisitos necessarios para instalar e rodar o projeto.

### Poetry

Verifique se a sua versão do poetry está superior ou igual a 1.1.12.

```bash
poetry --version

# O retorno deve ser

Poetry version 1.1.12
```

### Python

Não podemos esquecer de averiguar a versão do Python que está sendo utilizada.

```bash
python3 --version

# O retorno deve ser

Python 3.9.10
```

## Git

Para verificar a versão do Git.

```bash
git --version

# retorno
 
git version 2.32.0
```

Entre no diretorio na qual vamos fazer o clone do nosso projeto.

```bash
# Veja se o diretorio está correto 

pwd

# E nesse diretorio que vou colocar meu projeto

/home/hendrek/Documents/GitHub/KingPack
```

Agora vamos fazer o clone do projeto.

```bash
# Fazendo o clone do projeto

git clone https://github.com/KingPack/spacepy.git

# Liste o diretorio para ver e entrar no projeto

ls | grep spacepy

# retorno 

spacepy

# Entre no repositorio

cd spacepy/
```

 \o/ Oba !!! nosso projeto esta aqui.

### 49% já feito

Se você chegou ate aqui sem erros, então já devemos estar preparados para inicializar o ambiente virtual do Poetry.

```bash
# comando para entrar no ambiente do poetry
poetry shell

# retorno
Creating virtualenv spacepy-oQYf1C9p-py3.9 in /home/hendrek/.cache/pypoetry/virtualenvs
Spawning shell within /home/hendrek/.cache/pypoetry/virtualenvs/spacepy-oQYf1C9p-py3.9
➜  spacepy git:(main) . /home/hendrek/.cache/pypoetry/virtualenvs/spacepy-oQYf1C9p-py3.9/bin/activate
```

Apos inicializar o o ambiente virutal vamos instalar e atualizar as dependencias do projeto.

```bash
poetry update
 
# Retorno 

Updating dependencies
Resolving dependencies... (5.4s)
```

Pode demorar um pouco para instalar todas as dependencias.
Então e só esperar um pouco.

## Criando nossos arquivos config.py

Observação: Por conter dados sigilosos , esses arquivos sempre devem estar no .gitignore.

No diretorio [/spacepy/spacepy/](https://github.com/KingPack/spacepy/tree/main/spacepy)  e [spacepy/scripts/](https://github.com/KingPack/spacepy/tree/main/scripts) vamos criar um arquivo chamado de 'config.py' e adicionar os dados do nosso banco de dados.

```bash
# Criando arquivo config.py
touch config.py

# Entrando no arquivo 
nano config.py
```

Lembra dos dados do seu banco de dados? É aqui onde iremos adicioná-los.
Com o editor aberto, insira os dados  do banco e salve-os.

```python
DB_HOST = 'localhost'
DB_PORT = 'porta'
DB_USER = 'usuario'
DB_PASS = 'root'
DB_DATA = 'postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATA}'
```

Agora vamos verificar se os dados persistiram no arquivo.

```bash
cat config.py

# Retorno
DB_HOST = 'localhost'
DB_PORT = 'porta'
DB_USER = 'usuario'
DB_PASS = 'root'
DB_DATA = 'postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATA}'
```

Se tudo deu certo então agora temos nosso banco de dados salvo e configurado.

## Populando nosso banco de dados

Com o nosso banco de dados configurado, está na hora de inserir alguns dados nele, certo ?

Então vamos utilizar o [cycle_db.py](https://github.com/KingPack/spacepy/blob/main/scripts/cycle_db.py).

Observação: Na primeira execução do codigo e normal que demore algumas horas ate que todos os artigos sejam inseridos no banco de dados, portanto, para evitar problemas futuros, aguarde até que o programa complete o seu primeiro ciclo.

```bash
# Iniciando o cliclo do banco de dados
python3 cycle_db.py

# O script vai pedir um horario para agendar as tarefas.

Qual horario de inicio?  exemplo: 10:00 (HH:MM) : 09:00

# Coloque como no exemplo para funcionar

```

Quando a adição de todos os artigos terminar, poderemos ver o resultado no bando de dados.

## Configuração do Flask

Agora vamos configurar nossa aplicação Flak.

Devemos exportar as variaveis no diretorio [raiz](https://github.com/KingPack/spacepy) do projeto.

```bash
# Verifique se esta no diretorio correto
pwd

# Retorno
/home/hendrek/Documents/Projects/spacepy
```

Agora vamos exportar nossas variaveis de ambiente para o Flask.

```bash

# Exportando o caminho do arquivo main.py para o FLASK_APP
export FLASK_APP=spacepy/main.py

# Exportando o tipo de ambiente que estamos trabalhando
export FLASK_ENV=development
```

## Inicialização localhost

Depois que inicializamos o banco de dados, já estamos preparados para iniciar a nossa aplicação em desenvolvimento local.

```bash
# Use o comando para inicializar a aplicação

flask run

# retorno

 * Serving Flask app 'spacepy/main.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Se tudo ocorreu perfeitamente, já conseguiremos acessar a nossa aplicação.

> Entre no link : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Ebaaaaaa \o/ estamos no ar !!!

Veja a [documentação](http://127.0.0.1:5000/documentation) do projeto.

Continue no [README.md](https://github.com/KingPack/spacepy/tree/main/spacepy) das rotas do spacepy.

## Info

> This is a challenge by [Coodesh](https://coodesh.com/)
