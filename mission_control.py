
import time
from rich import print

NOME_MISSAO = "MOSCOW - 4"
NOME_EQUIPE = "Equipe Lumos"

# Matriz principal: [temperatura, comunicacao, bateria, oxigenio, estabilidade]
# Ciclo 1 - Lançamento e estabilização inicial
# Ciclo 2 - Operação nominal
# Ciclo 3 - Primeiro distúrbio térmico
# Ciclo 4 - Queda de comunicação e energia
# Ciclo 5 - Crise operacional
# Ciclo 6 - Recuperação parcial
# Ciclo 7 - Segunda tentativa de recuperação
# Ciclo 8 - Estabilização emergencial

dados_missao = [
    [22, 95, 91, 97, 93],   # Ciclo 1 — lançamento estável
    [25, 88, 84, 95, 88],   # Ciclo 2 — operação normal
    [32, 70, 65, 92, 72],   # Ciclo 3 — alerta térmico
    [37, 45, 41, 88, 58],   # Ciclo 4 — energia e comunicação em queda
    [41, 25, 17, 76, 33],   # Ciclo 5 — crise crítica
    [38, 38, 22, 80, 42],   # Ciclo 6 — recuperação inicial
    [35, 52, 30, 83, 50],   # Ciclo 7 — sistemas parcialmente restaurados
    [29, 68, 45, 87, 65],   # Ciclo 8 — estabilização emergencial
]

# Lista de áreas monitoradas (alinhada às colunas da matriz)
areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional",
]


# ── Funções de análise por sensor ────────────────────────────

def analisar_temperatura(valor):
    # #Classifica a temperatura interna do módulo (°C).
    # NORMAL   : 18 °C a 30 °C
    # ATENÇÃO  : < 18 °C  ou  > 30 °C até 35 °C
    # CRÍTICO  : > 35 °C
    
    if valor < 18:
        return "ATENÇÃO", 1, "Temperatura baixa demais"
    elif valor <= 30:
        return "NORMAL", 0, "Temperatura estável"
    elif valor <= 35:
        return "ATENÇÃO", 1, "Temperatura elevada"
    else:
        return "CRÍTICO", 2, "Risco de superaquecimento"


def analisar_comunicacao(valor):
    # Classifica a qualidade do sinal de comunicação (%).
    # NORMAL   : >= 60 %
    # ATENÇÃO  : 30 % a 59 %
    # CRÍTICO  : < 30 %
    
    if valor < 30:
        return "CRÍTICO", 2, "Comunicação com a base em nível crítico"
    elif valor < 60:
        return "ATENÇÃO", 1, "Comunicação instável"
    else:
        return "NORMAL", 0, "Comunicação estável"


def analisar_bateria(valor):
    # Classifica o nível de bateria (%).
    # NORMAL   : >= 50 %
    # ATENÇÃO  : 20 % a 49 %
    # CRÍTICO  : < 20 %
    
    if valor < 20:
        return "CRÍTICO", 2, "Bateria em nível crítico"
    elif valor < 50:
        return "ATENÇÃO", 1, "Bateria abaixo do recomendado"
    else:
        return "NORMAL", 0, "Energia estável"


def analisar_oxigenio(valor):
    # Classifica o nível de oxigênio disponível (%).
    # NORMAL   : >= 90 %
    # ATENÇÃO  : 80 % a 89 %
    # CRÍTICO  : < 80 %

    if valor < 80:
        return "CRÍTICO", 2, "Oxigênio em nível crítico"
    elif valor < 90:
        return "ATENÇÃO", 1, "Oxigênio abaixo do ideal"
    else:
        return "NORMAL", 0, "Oxigênio adequado"


def analisar_estabilidade(valor):
    # Classifica a estabilidade geral dos sistemas (%).
    # NORMAL   : >= 70 %
    # ATENÇÃO  : 40 % a 69 %
    # CRÍTICO  : < 40 %
    
    if valor < 40:
        return "CRÍTICO", 2, "Estabilidade operacional crítica"
    elif valor < 70:
        return "ATENÇÃO", 1, "Estabilidade operacional reduzida"
    else:
        return "NORMAL", 0, "Estabilidade operacional adequada"


# ── Funções de avaliação de ciclo ────────────────────────────

def analisar_ciclo(ciclo):
    # Executa todas as análises de um ciclo e retorna lista de resultados.
    # Cada item: (label, valor, status, pontos, descricao)

    temp, com, bat, oxi, est = ciclo
    resultados = [
        ("Temperatura", f"{temp} °C", *analisar_temperatura(temp)),
        ("Comunicação", f"{com}%",    *analisar_comunicacao(com)),
        ("Bateria",     f"{bat}%",    *analisar_bateria(bat)),
        ("Oxigênio",    f"{oxi}%",    *analisar_oxigenio(oxi)),
        ("Estabilidade",f"{est}%",    *analisar_estabilidade(est)),
    ]
    return resultados


def calcular_risco_ciclo(resultados):
    # Soma os pontos de risco de um ciclo.
    return sum(r[3] for r in resultados)


def classificar_ciclo(pontuacao):
    # """Classifica o ciclo com base na pontuação total de risco.
    # 0-2  → MISSÃO ESTÁVEL
    # 3-5  → MISSÃO EM ATENÇÃO
    # 6-10 → MISSÃO CRÍTICA
    # """
    if pontuacao <= 2:
        return "MISSÃO ESTÁVEL"
    elif pontuacao <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


def gerar_recomendacao(resultados, classificacao):
    # Gera recomendação automática com base nos alertas do ciclo.

    criticos = [r[0] for r in resultados if r[2] == "CRÍTICO"]
    atencoes  = [r[0] for r in resultados if r[2] == "ATENÇÃO"]

    if classificacao == "MISSÃO ESTÁVEL":
        return "Manter operação normal e continuar monitoramento."

    recomendacoes = []
    mapa = {
        "Temperatura": "verificar controle térmico da missão",
        "Comunicação": "tentar restabelecer contato com a base",
        "Bateria":     "ativar modo de economia de energia",
        "Oxigênio":    "acionar protocolo de suporte à vida",
        "Estabilidade":"reduzir operações não essenciais",
    }

    for sensor in criticos:
        if sensor in mapa:
            recomendacoes.append(mapa[sensor].capitalize())

    if not recomendacoes and atencoes:
        return "Monitorar sistemas em atenção e preparar plano de contingência."

    if len(criticos) >= 3:
        return ("Ativar modo de segurança e priorizar suporte à vida, "
                "energia e comunicação.")

    return "; ".join(recomendacoes) + "." if recomendacoes else (
        "Monitorar sistemas em atenção e preparar plano de contingência.")


# ── Funções de análise global da missão ──────────────────────

def analisar_tendencia(riscos):
    # Compara o risco do primeiro e do último ciclo.

    if riscos[-1] > riscos[0]:
        return "A missão apresentou tendência de piora."
    elif riscos[-1] < riscos[0]:
        return "A missão apresentou tendência de melhora."
    else:
        return "A missão permaneceu estável em relação ao início."


def identificar_area_mais_afetada(todos_resultados):
    # Soma pontuação acumulada por área e retorna dict + área mais afetada.

    acumulado = {area: 0 for area in areas_monitoradas}
    indices = list(acumulado.keys())

    for resultados in todos_resultados:
        for i, resultado in enumerate(resultados):
            acumulado[indices[i]] += resultado[3]

    mais_afetada = max(acumulado, key=acumulado.get)
    return acumulado, mais_afetada


def calcular_medias():
    # Calcula a média de cada sensor ao longo de todos os ciclos.

    n = len(dados_missao)
    medias = {
        "temperatura":  sum(c[0] for c in dados_missao) / n,
        "comunicacao":  sum(c[1] for c in dados_missao) / n,
        "bateria":      sum(c[2] for c in dados_missao) / n,
        "oxigenio":     sum(c[3] for c in dados_missao) / n,
        "estabilidade": sum(c[4] for c in dados_missao) / n,
    }
    return medias


# ── Exibição do relatório ─────────────────────────────────────

def gerar_relatorio_final(riscos, todos_resultados):
    # Exibe o relatório consolidado da missão.

    medias         = calcular_medias()
    tendencia      = analisar_tendencia(riscos)
    acumulado, mais_afetada = identificar_area_mais_afetada(todos_resultados)

    risco_medio     = sum(riscos) / len(riscos)
    ciclo_mais_crit = riscos.index(max(riscos)) + 1
    qtd_criticos    = sum(1 for r in riscos if classificar_ciclo(r) == "MISSÃO CRÍTICA")
    risco_final_med = sum(riscos) / len(riscos)

    classificacao_final = classificar_ciclo(round(risco_medio))

    if classificacao_final == "MISSÃO ESTÁVEL":
        conclusao = ("A missão foi concluída com êxito. Todos os sistemas "
                     "operaram dentro dos parâmetros aceitáveis.")
    elif classificacao_final == "MISSÃO EM ATENÇÃO":
        conclusao = ("A missão apresentou instabilidade relevante durante a "
                     "operação. Apesar da tentativa de recuperação no último "
                     "ciclo, ainda existem sistemas em atenção e a equipe deve "
                     "manter o plano de contingência ativo.")
    else:
        conclusao = ("A missão enfrentou situação crítica. Recomenda-se revisão "
                     "completa dos sistemas antes de retomar operações plenas.")

    print("=" * 60)
    print("RELATÓRIO FINAL DA MISSÃO")
    print("=" * 60)
    time.sleep(5)
    

    print(f"Missão : {NOME_MISSAO}")
    print(f"Equipe : {NOME_EQUIPE}")
    print()
    print(f"[bold white]Quantidade de ciclos analisados: {len(dados_missao)}[/bold white]")
    print()
    print(f"[bold white]Média de temperatura  : {medias['temperatura']:.2f} °C [/bold white]")
    print(f"[bold white]Média de comunicação  : {medias['comunicacao']:.2f}% [/bold white]")
    print(f"[bold white]Média de bateria      : {medias['bateria']:.2f}% [/bold white]")
    print(f"[bold white]Média de oxigênio     : {medias['oxigenio']:.2f}% [/bold white]")
    print(f"[bold white]Média de estabilidade : {medias['estabilidade']:.2f}% [/bold white]")
    print()
    print(f"[bold white]Ciclo mais crítico      : Ciclo {ciclo_mais_crit} [/bold white]")
    print(f"[bold white]Maior pontuação de risco: {max(riscos)} [/bold white]")
    print(f"[bold white]Risco médio da missão   : {risco_medio:.2f} [/bold white]")
    print(f"[bold white]Ciclos críticos         : {qtd_criticos} [/bold white]")
    print()

    print("=" *65)
    print(f"\n[bold yellow]Tendência da missão:[/bold yellow]")
    print(f"[bold yellow]  {tendencia}[/bold yellow]\n")
    print("=" *65)
    print()

    print("Pontuação acumulada por área:")
    for area, pts in acumulado.items():
        print(f"  [bold yellow]{area}:[/bold yellow] [bold white]{pts} ponto(s)[/bold white]")
    print()
    print(f"[bold yellow]Área mais afetada:[/bold yellow]")
    print(f"  {mais_afetada}")
    print()
    print(f"[bold yellow]Classificação final da missão:[/bold yellow]")
    print(f"  {classificacao_final}")
    print()
    print("[bold yellow]Conclusão:[/bold yellow]")
    print(f"  {conclusao}")
    print("=" * 60)


# ── Programa principal ────────────────────────────────────────

def main():
    print("=" * 60)
    print("MISSION CONTROL AI")
    print("=" * 60)
    print(f"[bold yellow]Missão : [/bold yellow]{NOME_MISSAO}")
    print(f"[bold yellow]Equipe : {NOME_EQUIPE}[/bold yellow]")
    print(f"[bold yellow]Quantidade de ciclos analisados:[/bold yellow] {len(dados_missao)}")
    print("=" * 60)

    riscos          = []
    todos_resultados = []

    for numero, ciclo in enumerate(dados_missao, start=1):
        resultados    = analisar_ciclo(ciclo)
        pontuacao     = calcular_risco_ciclo(resultados)
        classificacao = classificar_ciclo(pontuacao)
        recomendacao  = gerar_recomendacao(resultados, classificacao)

        riscos.append(pontuacao)
        todos_resultados.append(resultados)

        print(f"\n[bold yellow] ------------ CICLO {numero} ----------- [/bold yellow]\n")

        print("=" *65)
        print("[bold orange]GERANDO CICLOS......[/bold orange]")
        print("=" *65)
        time.sleep(5)



        for r in resultados:
            label, valor, status, _, descricao = r
            print(f"  {label:<14}: {valor:>6}  |  {status:<8}  |  {descricao}")
        print()
        print(f"  [bold yellow]Pontuação de risco do ciclo :[/bold yellow] [bold white]{pontuacao}[/bold white]")
        print(f"  [bold yellow]Classificação do ciclo      :[/bold yellow] [bold white]{classificacao}[/bold white]")
        print(f"  [bold yellow]Recomendação                :[/bold yellow] [bold white]{recomendacao}[/bold white]\n\n")
        print("=" *65)

    print()
    gerar_relatorio_final(riscos, todos_resultados)


if __name__ == "__main__":
    main()
