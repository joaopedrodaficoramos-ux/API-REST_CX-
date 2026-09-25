Motor de Inteligência e API de CX

## 🎯 O Desafio de Negócio
Numa operação de Customer Experience (CX) de alto volume, foi identificada uma possível correlação entre o tempo de resolução de tickets de suporte (SLA) e a quebra no índice de satisfação do cliente (CSAT). 
Este projeto simula um ambiente de análise de dados avançado e a criação de uma API RESTful para centralizar, analisar e distribuir estes indicadores operacionais de forma escalável, apoiando a tomada de decisão das lideranças.

## 🛠️ Stack Tecnológica
* *Linguagem:* Python 3
* *Framework de API:* FastAPI e Uvicorn (Alta performance e documentação automatizada via Swagger UI)
* *Análise e Engenharia de Dados:* Pandas
* *Visualização de Dados:* Matplotlib
* *Geração de Dados Sintéticos:* Faker

## 📂 Arquitetura do Projeto
O repositório está estruturado com os seguintes módulos:
* gerador_dados.py: Script responsável por criar uma base de dados estruturada (base_cx_artemis.csv) com 1000 interações de clientes, injetando regras de negócio reais e anomalias estatísticas para análise.
* API.py: Motor da aplicação construído em FastAPI. Expõe endpoints de leitura (GET) para o consumo de KPIs em tempo real, como volume total da operação, CSAT médio geral e tempo médio de resolução.
* analise_cx.py: Script de análise exploratória que consome os dados em lote, aplica categorizações de SLA e gera visualizações comprovando a hipótese central do negócio.
