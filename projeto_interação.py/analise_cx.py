import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar a base de dados
try:
    df = pd.read_csv("base_cx_artemis.csv")
except FileNotFoundError:
    print("Erro: O ficheiro base_cx_artemis.csv não foi encontrado.")
    exit()

# 2. Limpeza: Filtrar apenas tickets resolvidos e garantir que o CSAT é um número
df_resolvidos = df[df['Status'] == 'Resolvido'].copy()
df_resolvidos['CSAT'] = pd.to_numeric(df_resolvidos['CSAT'])

# 3. Engenharia de Dados: Criar categorias de SLA (Tempo de Resolução)
def categorizar_sla(horas):
    if horas <= 24:
        return "1. Até 24h (No Prazo)"
    elif horas <= 48:
        return "2. 24h a 48h (Atenção)"
    else:
        return "3. Mais de 48h (Crítico)"

df_resolvidos['Categoria_SLA'] = df_resolvidos['TempoResolucao_Horas'].apply(categorizar_sla)

# 4. Agrupamento Analítico: Calcular a média de CSAT por cada categoria de SLA
analise_csat = df_resolvidos.groupby('Categoria_SLA')['CSAT'].mean().reset_index()
analise_csat['CSAT'] = analise_csat['CSAT'].round(2)

print("\n--- RESULTADO DA ANÁLISE PARA A DIRETORIA ---")
print(analise_csat.to_string(index=False))
print("---------------------------------------------\n")

# 5. Visualização: Gerar e guardar um gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(analise_csat['Categoria_SLA'], analise_csat['CSAT'], color=['#2ca02c', '#ff7f0e', '#d62728'])
plt.title('Impacto do Tempo de Resolução na Satisfação do Cliente (CSAT)')
plt.xlabel('Janela de Tempo de Resolução')
plt.ylabel('Nota Média CSAT (1 a 5)')
plt.ylim(0, 5)

# Guardar a imagem na pasta para usarmos no GitHub depois
plt.savefig('grafico_csat_sla.png', bbox_inches='tight')
print("Sucesso! Gráfico 'grafico_csat_sla.png' guardado na tua pasta.")