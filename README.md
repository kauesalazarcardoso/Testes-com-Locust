# Testes de Performance com Locust

## Descrição

Este projeto foi desenvolvido para a disciplina de Testes e Qualidade de Software com o objetivo de avaliar o desempenho de uma aplicação web utilizando a ferramenta Locust.

O teste simula múltiplos usuários acessando o sistema simultaneamente, permitindo medir métricas como:

* Tempo de resposta;
* Throughput (requisições por segundo);
* Percentis de desempenho (p90 e p95);
* Comportamento da aplicação sob diferentes níveis de carga.

Foram modelados cenários representando ações comuns de usuários, como acesso à página inicial, autenticação, consulta de produtos, adição de itens ao carrinho e finalização de compras.

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
locust -f locustfile.py --host=https://example.com
```

Após executar o comando, abra o navegador em:

```text
http://localhost:8089
```

### Executar em modo headless

10 usuários:

```bash
locust -f locustfile.py --host=https://example.com --headless -u 10 -r 2 -t 1m
```

50 usuários:

```bash
locust -f locustfile.py --host=https://example.com --headless -u 50 -r 5 -t 1m
```

100 usuários:

```bash
locust -f locustfile.py --host=https://example.com --headless -u 100 -r 10 -t 1m
```

### Exportar resultados para CSV

```bash
locust -f locustfile.py --host=https://example.com --headless -u 50 -r 5 -t 1m --csv resultado_50
```

## Autor

Kaue Salazar Cardoso
