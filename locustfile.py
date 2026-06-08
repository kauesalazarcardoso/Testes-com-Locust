import random
from locust import HttpUser, task, between


class DummyJsonUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://dummyjson.com"

    @task(8)
    def listar_produtos(self):
        self.client.get("/products")

    @task(4)
    def login(self):
        self.client.post(
            "/auth/login",
            json={
                "username": "emilys",
                "password": "emilyspass"
            }
        )

    @task(6)
    def produto_especifico(self):
        produto_id = random.randint(1, 30)
        self.client.get(f"/products/{produto_id}", name="/products/[id]")

    @task(5)
    def adicionar_carrinho(self):
        self.client.post(
            "/carts/add",
            json={
                "userId": 1,
                "products": [
                    {"id": random.randint(1, 30), "quantity": 1}
                ]
            }
        )

    @task(3)
    def visualizar_carrinho(self):
        self.client.get("/carts/1")

    @task(2)
    def buscar_produto(self):
        self.client.get("/products/search?q=phone")
