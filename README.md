# FastAPI Kafka

![](https://img.shields.io/badge/Python-v3.13-green) ![](https://img.shields.io/badge/FastAPI-v0.119-blue) 
![](https://img.shields.io/badge/Kafka-v3.7.0-black) ![](https://img.shields.io/badge/Faststream-v0.6.1-red)
![](https://img.shields.io/badge/Docker-blue) ![](https://img.shields.io/badge/UV-FF1493)


## Install
1. Change the environment variables `KAFKA_TOPIC`, `KAFKA_GROUP` in **deploy/.env** (or leave them as is for testing) 
2. `$ cd deploy && docker compose up -d`

## About
* Both **Producer** and **Consumer** are implemented for testing.  
* You can send messages through the Producer at the endpoint **POST /messages** with the body: `{"message": "test message"}`  
* The **Consumer** will receive the message and print it to the logs


**Swagger:** `127.0.0.1:8000/docs`  
**Kafka UI:** `127.0.0.1:8080`