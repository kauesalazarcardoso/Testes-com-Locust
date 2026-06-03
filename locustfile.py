from locust import HttpUser, task, between

class SauceDemoUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def home(self):
        self.client.get("/")

    @task(4)
    def login(self):
        self.client.post(
            "/login",
            json={
                "username": "standard_user",
                "password": "secret_sauce"
            }
        )

    @task(8)
    def produtos(self):
        self.client.get("/inventory")

    @task(6)
    def adicionar_carrinho(self):
        self.client.post(
            "/cart/add",
            json={"product_id": 1}
        )

    @task(3)
    def visualizar_carrinho(self):
        self.client.get("/cart")

    @task(2)
    def checkout(self):
        self.client.post(
            "/checkout",
            json={
                "firstName": "Teste",
                "lastName": "Usuario",
                "postalCode": "12345"
            }
        )