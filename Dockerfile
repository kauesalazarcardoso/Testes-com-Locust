FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install locust

CMD ["locust", "-f", "locustfile.py", "--host=https://example.com"]
