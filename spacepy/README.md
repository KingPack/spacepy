# Sumario

Especificaçoes tecnicas para o pacote spacepy.

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
  
## Index
  
Rotas principal do projeto.
  
### / - [GET]

Na rota [http://localhost:5000](http://localhost:5000) sera rederenizado uma pagina HTML com a frase :

Back-end Challenge 🏅 2021 - Space Flight News

### /init/ - [GET]

Inicialização da rota [http://localhost:5000/init](http://localhost:5000/init) voce ira receber um json com os dados do banco de dados.

```json

// http://localhost:5000/init

{

"canceled_articles_db":  1822,

"canceled_articles_ext":  1822,

"canceled_articles_new":  0,

"end_articles_ext":  14008,

"end_articles_new":  100000,

"id":  5,

"init_articles_ext":  1,

"init_articles_new":  100000,

"last_update":  "2022-02-18 11:44:10.097879",

"total_articles_db":  14001,

"total_articles_ext":  12186,

"total_articles_new":  0

}

```

#### Informações /init

canceled_articles_db | Soma de todos os artigos cancelados no BD.

canceled_articles_ext | Soma dos artigos cancelados da API externa.

canceled_articles_new | Soma dos artigos criados na API local.

end_articles_ext | id do ultimo artigo publicado na API externa.

end_articles_new | id do ultimo artigo publicado na API externa

id | Chave PK da tabela

init_articles_ext | id inicial da API externa no DB.

init_articles_new | id inicial da API local no DB.

last_update | Horario que esses dados foram analisados.

total_articles_db | Quantidade de artigos salvos no BD.

total_articles_ext | Quantidade de artigos salvos no BD da API externa.

total_articles_new | Quantidade de artigos salvos no BD da API local.

## a

a
