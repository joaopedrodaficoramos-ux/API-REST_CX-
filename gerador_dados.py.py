import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializa o Faker para dados em Português do Brasil
fake = Faker('pt_BR')

def gerar_dados_cx(qtd_registros=1000):
    dados = []
    status_opcoes = ['Resolvido', 'Em Andamento', 'Escalado']
    
    for _ in range(qtd_registros):
        # Dados básicos do cliente e ticket
        ticket_id = fake.unique.random_number(digits=6)
        cliente = fake.company()
        data_abertura = fake.date_time_between(start_date='-6m', end_date='now')
        status = random.choices(status_opcoes, weights=[0.7, 0.2, 0.1])[0]
        
        # Simula o tempo de resolução em horas
        tempo_resolucao_horas = random.randint(1, 72)
        
        # Regra de negócio (A anomalia para você analisar depois):
        # Se demorou mais de 24h, o CSAT tende a ser menor.
        if tempo_resolucao_horas <= 24:
            csat = random.choices([4, 5], weights=[0.3, 0.7])[0]
        elif tempo_resolucao_horas <= 48:
            csat = random.choices([3, 4], weights=[0.6, 0.4])[0]
        else:
            csat = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
            
        # Adiciona o registro na lista
        dados.append({
            'TicketID': ticket_id,
            'Cliente': cliente,
            'DataAbertura': data_abertura.strftime("%Y-%m-%d %H:%M:%S"),
            'TempoResolucao_Horas': tempo_resolucao_horas,
            'Status': status,
            'CSAT': csat if status == 'Resolvido' else None
        })
        
    return pd.DataFrame(dados)

if __name__ == "__main__":
    print("Iniciando a geração de dados de CX...")
    df_cx = gerar_dados_cx(1000)
    
    # Salva os dados em um arquivo CSV
    nome_arquivo = 'base_cx_artemis.csv'
    df_cx.to_csv(nome_arquivo, index=False)
    print(f"Sucesso! Base de dados criada: {nome_arquivo}")
    print(df_cx.head()) # Mostra as 5 primeiras linhas no terminal
    