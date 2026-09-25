from fastapi import FastAPI, HTTPException
import pandas as pd
import json

app = FastAPI(
    title="API Ártemis - Motor de CX",
    description="API para consumo de dados operacionais e de Customer Experience",
    version="1.0.0"
)

# Carregando os dados em memória (Simulando nosso banco de dados)
try:
    df_cx = pd.read_csv("base_cx_artemis.csv")
    # Preenchendo valores nulos (chamados não resolvidos não têm CSAT)
    df_cx = df_cx.fillna("N/A") 
    # Convertendo o dataframe para um dicionário para facilitar o envio via API
    dados_mock = df_cx.to_dict(orient="records")
except FileNotFoundError:
    dados_mock = []
    print("Aviso: Arquivo base_cx_artemis.csv não encontrado. Rode o gerador de dados primeiro.")

@app.get("/")
def home():
    return {"mensagem": "API Ártemis online. Acesse /docs para ver a documentação."}

@app.get("/tickets")
def listar_tickets(limit: int = 10):
    """
    Retorna uma lista de tickets. O parâmetro 'limit' controla a quantidade (paginação básica).
    """
    return {"total_exibido": limit, "dados": dados_mock[:limit]}

@app.get("/tickets/{ticket_id}")
def buscar_ticket(ticket_id: int):
    """
    Busca um ticket específico pelo seu ID.
    """
    for ticket in dados_mock:
        if ticket["TicketID"] == ticket_id:
            return ticket
    
    raise HTTPException(status_code=404, detail="Ticket não encontrado.")

@app.get("/kpis/resumo")
def resumo_operacional():
    """
    Retorna os principais indicadores (KPIs) calculados na hora.
    Esta é a visão de negócio que a diretoria quer ver!
    """
    if df_cx.empty:
         raise HTTPException(status_code=404, detail="Sem dados para calcular KPIs.")

    # Filtra apenas os resolvidos para calcular o CSAT médio
    df_resolvidos = df_cx[df_cx['Status'] == 'Resolvido'].copy()
    df_resolvidos['CSAT'] = pd.to_numeric(df_resolvidos['CSAT'], errors='coerce')
    
    csat_medio = df_resolvidos['CSAT'].mean()
    tempo_medio_resolucao = df_cx['TempoResolucao_Horas'].mean()
    
    return {
        "volume_total_tickets": len(df_cx),
        "csat_medio_geral": round(csat_medio, 2),
        "tempo_medio_resolucao_horas": round(tempo_medio_resolucao, 2)
    }