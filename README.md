# startup-back

Para começar crie duas copias do arquivo `.env.example`, modifique o nome de uma delas para `.env`
 e da outra para `.container.env`, no arquivo `.container.env` remova a linha com a variavel `PG_PORT`
 e modifique a variável `PG_HOST` para `"db_postgres"`.

Por fim para rodar o backend use esse comando `docker compose up`.
