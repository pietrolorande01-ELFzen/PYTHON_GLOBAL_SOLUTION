# PYTHON_GLOBAL_SOLUTION

---

# INTEGRANTES DO PROJETO 

*Pietro Lorande | RM569125
*Gustavo Bonamico Piccoli | RM 569984
*Maria Eduarda Medeiros Lemos | RM 574094

---

#  Mission Control AI — MOSCOW-4

> Sistema de monitoramento e análise de telemetria para missões espaciais simuladas.

---

##  Descrição

O **Mission Control AI** é um programa Python que simula o monitoramento em tempo real de uma missão espacial. Ele processa dados de telemetria ciclo a ciclo, classifica o estado de cada sensor, calcula o risco operacional e gera um relatório final consolidado com tendências, médias e recomendações automáticas.

Desenvolvido pela **Equipe Lumos** para a missão **MOSCOW-4**.

---

##  Funcionalidades

- **Análise por sensor** com classificação em três níveis: `NORMAL`, `ATENÇÃO` e `CRÍTICO`
- **Cálculo de risco por ciclo** com pontuação acumulada
- **Classificação automática da missão**: Estável, Em Atenção ou Crítica
- **Recomendações operacionais** geradas dinamicamente com base nos alertas
- **Relatório final** com:
  - Médias por sensor ao longo da missão
  - Ciclo mais crítico
  - Tendência geral (melhora, piora ou estabilidade)
  - Área mais afetada da missão
  - Conclusão e classificação final

---

##  Sensores Monitorados

| Sensor | Unidade | Normal | Atenção | Crítico |
|---|---|---|---|---|
| Temperatura interna | °C | 18–30 | <18 ou 30–35 | >35 |
| Comunicação com a base | % | ≥60 | 30–59 | <30 |
| Sistema de energia (bateria) | % | ≥50 | 20–49 | <20 |
| Suporte de oxigênio | % | ≥90 | 80–89 | <80 |
| Estabilidade operacional | % | ≥70 | 40–69 | <40 |

---

## 📊 Ciclos da Missão MOSCOW-4

A missão simula **8 ciclos operacionais**, do lançamento até a estabilização emergencial:

| Ciclo | Descrição |
|---|---|
| 1 | Lançamento estável |
| 2 | Operação nominal |
| 3 | Primeiro distúrbio térmico |
| 4 | Queda de comunicação e energia |
| 5 | Crise operacional crítica |
| 6 | Recuperação inicial |
| 7 | Sistemas parcialmente restaurados |
| 8 | Estabilização emergencial |

---

##  Estrutura do Código

```
mission_control.py
│
├── Constantes e dados
│   ├── NOME_MISSAO, NOME_EQUIPE
│   ├── dados_missao         # Matriz 8×5 com os valores de cada ciclo
│   └── areas_monitoradas    # Nomes dos sensores
│
├── Funções de análise por sensor
│   ├── analisar_temperatura()
│   ├── analisar_comunicacao()
│   ├── analisar_bateria()
│   ├── analisar_oxigenio()
│   └── analisar_estabilidade()
│
├── Funções de avaliação de ciclo
│   ├── analisar_ciclo()        # Executa todas as análises de um ciclo
│   ├── calcular_risco_ciclo()  # Soma os pontos de risco
│   ├── classificar_ciclo()     # Classifica com base na pontuação
│   └── gerar_recomendacao()    # Gera recomendação automática
│
├── Funções de análise global
│   ├── analisar_tendencia()           # Compara primeiro e último ciclo
│   ├── identificar_area_mais_afetada() # Área com maior pontuação acumulada
│   └── calcular_medias()              # Média de cada sensor na missão
│
├── Exibição
│   └── gerar_relatorio_final()        # Relatório consolidado da missão
│
└── main()                             # Loop principal de ciclos
```

---

##  Pré-requisitos

- Python 3.8+
- Biblioteca [`rich`](https://github.com/Textualize/rich) para formatação colorida no terminal

### Instalação da dependência

```bash
pip install rich
```

---

##  Como executar

```bash
python mission_control.py
```

O programa irá processar cada ciclo sequencialmente, exibindo os dados de telemetria, pontuação de risco, classificação e recomendação. Ao final, é exibido o relatório consolidado da missão.

> **Nota:** há pausas de 5 segundos entre ciclos e antes do relatório final, simulando o tempo de processamento em tempo real.

---

##  Sistema de Pontuação de Risco

Cada sensor contribui com **0, 1 ou 2 pontos** por ciclo:

- `0` → NORMAL
- `1` → ATENÇÃO
- `2` → CRÍTICO

A soma dos pontos dos 5 sensores classifica o ciclo:

| Pontuação | Classificação |
|---|---|
| 0–2 |  MISSÃO ESTÁVEL |
| 3–5 |  MISSÃO EM ATENÇÃO |
| 6–10 |  MISSÃO CRÍTICA |

---

##  Exemplo real de saída

```
============================================================
MISSION CONTROL AI
============================================================
Missão : MOSCOW - 4
Equipe : Equipe Lumos
Quantidade de ciclos analisados: 8
============================================================

 ------------ CICLO 1 -----------

  Temperatura   :  22 °C  |  NORMAL    |  Temperatura estável
  Comunicação   :    95%  |  NORMAL    |  Comunicação estável
  Bateria       :    91%  |  NORMAL    |  Energia estável
  Oxigênio      :    97%  |  NORMAL    |  Oxigênio adequado
  Estabilidade  :    93%  |  NORMAL    |  Estabilidade operacional adequada

  Pontuação de risco do ciclo : 0
  Classificação do ciclo      : MISSÃO ESTÁVEL
  Recomendação                : Manter operação normal e continuar monitoramento.
```
