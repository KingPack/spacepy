# Branch desatualizada va para o branch master

Branch [master](https://github.com/KingPack/spacepy)

Este é um desafio de programação back-end onde consiste em replicar uma API Restful baseada na API [Space Flight News](https://api.spaceflightnewsapi.net/v3/documentation).

## Back-end Challenge 2021 - Space Flight News

## Tecnologias

- [Poetry](https://python-poetry.org/docs/)
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

 Para a instalação do --> [Poetry](https://python-poetry.org/docs/) <--

### 2º Python 3

Você deve instalar a versão 3.9.10 ou maior do [Python](https://www.python.org/downloads/).

### 2º Banco de dados

Tenha os dados para se conectar no banco de dados.

Apos fazer o git clone do repositorio, você deve criar um arquivo chamado config.py e colocar as configurações do banco de dados.

## Instalação

Então vamos para a instação do projeto. 

### Poetry
Veja se sua versão do poetry está superior ou igual a 1.1.12.
```bash
poetry --version

# O retorno deve ser

Poetry version 1.1.12
```

### Python
Não podemos esquecer de ver a versão do Python

```bash
python3 --version

# O retorno deve ser

Python 3.9.10
```

## Git

Quase esqueci que vamos usar Git, então precisamos instalar ele tambem. 

```bash
sudo apt install git

# Veja qual e a versão do Git

git --version

# retorno
 
git version 2.32.0
```
###
#
Apos a instalação do Git vamos para o diretorio na qual vamos fazer o clone do projeto.

Abra um terminal no diretorio na qual vamos usar.

```bash
# Veja se o diretorio está correto 

pwd

# retorno desejado

/home/hendrek/Documents/GitHub/KingPack
```

Agora vamos para o Git

```bash
# Fazendo o clone do projeto

git clone https://github.com/KingPack/spacepy.git

# Liste o diretorio para ver e entrar no projeto

ls | grep spacepy

# retorno 

>>> spacepy

# Entre no repositorio

cd spacepy/Space_Flight/

# \o/ Oba !!! nosso projeto esta aqui.
```
### 49 % já feito.

Se você chegou ate aqui, então ja devemos esta preparado para inicializar o ambiente virtual do Poetry.

```bash
# Então vamos la

# comando para entrar no ambiente do poetry
poetry shell

# retorno
Virtual environment already activated: /home/....

# Se você estiver no modo shell rode o comando

poetry update

# Pode demorar um pouco para instalar todas as dependencias 

```
## 

Já chegamos tão longe, e ate agora nao iniciamos nossa aplicação !!!

Não seja por isso.

```bash
# entre no modulo space_flight

cd space_flight/

# confirme se estamos no diretorio certo

pwd

# retorno
/home/hendrek/Documents/GitHub/KingPack/spacepy/Space_Flight/space_flight/

# Verifique se temos o arquivo app.py e wsgi.py usando o comando de listagem

# Para iniciar nossa aplicação temos algumas maneiras de fazer isso

```
##
### Iniciando o banco de dados

Não podemos esquecer de inicializar nosso banco de dados e popular ele, então pra isso temos o arquivo [cycle_db.py](https://github.com/KingPack/spacepy/blob/main/Space_Flight/cycle_db.py) 
e [insert_data.py](https://github.com/KingPack/spacepy/blob/main/Space_Flight/space_flight/insert_data.py).

O arquivo cycle_db.py e o maravilhoso script que vai fazer a atualização do banco de dados a cada determinado tempo. 
[hacker]. Você pode esta entrando dentro do script e mudar para o tempo que lhe convem.

### Mas e o arquivo insert_data.py ???

Bom ele e quem e o manda chuva em tudo por aqui, pois contem o script para verificar na api externa os dados do artigo, validar e inserir no banco de dados. Então e recomendado não mexer nele por hora.


### Criando nosso arquivo config.py

obs: Lembrando que esse arquivo contem dados sigilosos então sempre deve estar no .gitignore.

Ao lado dos arquivos app.py e insert_data.py vamos criar um arquivo chamado de 'config.py' e vamos adicionar os dados do nosso banco de dados.

```bash
# Criando arquivo config.py
touch config.py

# Entrando no arquivo 
nano config.py
```
Lembra dos dados do seu banco de dados? E aqui que onde vamos adicionar eles.


Com o editor aberto vamos inserir essas dados e salvar:


```python

DB_HOST = 'localhost'
DB_PORT = 'porta'
DB_USER = 'usuario'
DB_PASS = 'root'
DB_DATA = 'postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATA}'


```

Agora temos nosso banco de dados salvo e configurado.

## Populando nosso banco

Agora que temos nosso banco de dados configurado, esta na hora de inserir alguns dados nele não e ?

Então vamos la usar o cycle_db.py

obs: Talvez demore um pouco ou horas então espere todos os artigos serem inseridos no banco de dados  para evitar problemas !!


```bash
# Iniciando o cliclo do banco de dados
python3 cycle_db.py


# O script vai pedir um horario para agendar as tarefas.

Qual horario de inicio?  exemplo: 10:00 (HH:MM) : 

# Coloque como no exemplo para funcionar

```

Quando terminar a adição de todos os artigos poderemos ver o resultado.



## Inicialização localhost

Depois que inicializamos o banco de dados ja devemos esta pronto para iniciar nossa aplicação, então vamos para o terminal novamente !

```bash
# Use o comando para inicializar a aplicação

poetry run python3 app.py

# retorno

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Se tudo ocorreu certo então ja podemos acessar nossa aplicação.

Entre no link : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Ebaaaaaa \o/ estamos no ar !!!

Veja a [documentação](http://127.0.0.1:5000/documentation) do projeto.



## Info
>  This is a challenge by [Coodesh](https://coodesh.com/)