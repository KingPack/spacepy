
# Sumario

Especificaçoes tecnicas do pacote spacepy.

Rotas e Models.

## Rotas

- [Index](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [/ - [GET] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [/init - [GET] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
- [v1](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [/v1/ - [GET] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [v1/documentation](https://github.com/KingPack/spacepy/tree/main/spacepy)
- [Articles](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [v1/articles/ - [GET] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [v1/articles/ - [POST] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [v1/articles/id - [GET] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [v1/articles/id - [PUT] ](https://github.com/KingPack/spacepy/tree/main/spacepy)
	* [v1/articles/id - [DELETE] ](https://github.com/KingPack/spacepy/tree/main/spacepy)

## Rotas do projeto

Rotas principal do projeto.

### / - [GET]

Na rota [http://localhost:5000](http://localhost:5000) sera rederenizado uma pagina HTML com a frase :

Back-end Challenge 🏅 2021 - Space Flight News

### /init/ - [GET]

Inicialização da rota [http://localhost:5000/init](http://localhost:5000/init) voce ira receber um json com os dados do banco de dados.

Ao entrar nessa rota o aplicação irá inicializar a função [initialize_database()](https://github.com/KingPack/spacepy/blob/main/spacepy/insert_data.py#L43) no arquivo [insert_data.py](https://github.com/KingPack/spacepy/blob/main/spacepy/insert_data.py)

A função vai pegar os respectivos dados da [Spaceflight News API](https://api.spaceflightnewsapi.net/v3/documentation) (ultimo artigo criado), em seguida analisar os dados do banco de dados, salvar na tabela [data_api](https://github.com/KingPack/spacepy/blob/main/spacepy/models/article.py#L93) e retornar os dados em formato json.

```json
// http://localhost:5000/init

{
"id": 5,
"init_articles_ext": 1,
"init_articles_new": 100000,
"end_articles_ext": 14008,
"end_articles_new":  100000,
"total_articles_db": 14001,
"total_articles_ext": 12186,
"total_articles_new": 0
"canceled_articles_db": 1822,
"canceled_articles_ext": 1822,
"canceled_articles_new": 0,
"last_update": "2022-02-18 11:44:10.097879",
}
```

### Informações /init

Nome | Descrição
-------- | -----
id | Chave PK da tabela.
init_articles_ext | id inicial da API externa no DB.
init_articles_new | id inicial da API local no DB.
end_articles_ext | id do ultimo artigo publicado na API externa.
end_articles_new | id do ultimo artigo publicado na API interna.
total_articles_db | Quantidade de artigos salvos no BD.
total_articles_ext | Quantidade de artigos salvos no BD da API externa.
total_articles_new | Quantidade de artigos salvos no BD da API local.
canceled_articles_db | Soma de todos os artigos cancelados no BD.
canceled_articles_ext | Quantidade de artigos cancelados da API externa.
canceled_articles_new | Quantidade de artigos cancelados na API local.
last_update | Horario que esses dados foram gerados.

## Rota v1

Rota main v1 e a nossa Blueprint da aplicação, na sua versão 1.0, onde contem as demais rotas que manipulam nossos artigos.

### v1/ - [GET]

Retorna
