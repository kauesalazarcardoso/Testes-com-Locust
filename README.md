# Testes de Performance com Locust

## Descrição

Este projeto foi desenvolvido para a disciplina de Testes e Qualidade de Software com o objetivo de avaliar o desempenho de uma aplicação web utilizando a ferramenta Locust.

O sistema testado é o **DummyJSON** (`https://dummyjson.com`), uma API REST pública que simula um e-commerce com endpoints reais de autenticação, produtos e carrinho.

O teste simula múltiplos usuários acessando o sistema simultaneamente, permitindo medir métricas como:

* Tempo de resposta;
* Throughput (requisições por segundo);
* Percentis de desempenho (p90 e p95);
* Comportamento da aplicação sob diferentes níveis de carga.

### Cenários modelados

| Cenário | Método | Endpoint | Peso |
|---|---|---|---|
| Listar produtos | GET | /products | 8 |
| Login | POST | /auth/login | 4 |
| Produto específico | GET | /products/[id] | 6 |
| Adicionar ao carrinho | POST | /carts/add | 5 |
| Visualizar carrinho | GET | /carts/1 | 3 |
| Buscar produto | GET | /products/search?q=phone | 2 |

## Tecnologias Utilizadas

* Python 3
* Locust

## Como Executar

### Instalar dependências

```bash
pip install locust
```

### Executar com interface web

```bash
locust -f locustfile.py
```

Após executar o comando, abra o navegador em:

```text
http://localhost:8089
```

### Executar em modo headless

10 usuários:

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 1m
```

50 usuários:

```bash
locust -f locustfile.py --headless -u 50 -r 5 -t 1m
```

100 usuários:

```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 1m
```

### Exportar resultados para CSV

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 1m --csv resultados/carga_10
locust -f locustfile.py --headless -u 50 -r 5 -t 1m --csv resultados/carga_50
locust -f locustfile.py --headless -u 100 -r 10 -t 1m --csv resultados/carga_100
```

### Executar com Docker

```bash
docker-compose up
```

Após iniciar, abra o navegador em:

```text
http://localhost:8089
```

## Autor

Kaue Salazar Cardoso
