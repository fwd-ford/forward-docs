# Quadro de Valor — ForwardService

![version](https://img.shields.io/badge/versão-1.0-blue?style=flat-square)
![status](https://img.shields.io/badge/status-entrega_QA--3-brightgreen?style=flat-square)

> **QA-3** — Quadro de Valor cruzando stakeholders × expectativas × promessa × métricas.
> Cada linha tem **1 métrica de negócio + 1 métrica de qualidade** (requisito do PDF Ford-FIAP).
> Responsável: Rodrigo Jimenez (Roji) | Disciplina: Testing, Compliance & Quality Assurance — Prof. Elias Bernardo

---

## Quadro Principal

| Stakeholder | Dor / Expectativa | Promessa do ForwardService | Métrica de Negócio | Métrica de Qualidade | Prioridade |
|---|---|---|---|---|:---:|
| **Ford Brasil (Diretoria)** | "Não sei onde estou perdendo clientes nem quanto isso custa" | Dashboard nacional em tempo real: VIN Share por UF, Curva da Morte medida, ROI de cada ação rastreável | VIN Share ≥ 8% em 24 meses (base: ~3,5–5% hoje) | Disponibilidade da plataforma ≥ 99% / Latência API p95 < 300ms | 🔴 Alta |
| **Gestor Regional Ford** | "Não consigo comparar meus dealers nem justificar budget de campanha" | Cockpit regional: IHC 0-100 por dealer, ranking, identificação de dealers abaixo da meta | Número de dealers acima da meta regional (meta: 80%+) | Atualização do IHC 1×/dia sem falha; Silhouette K-means > 0,4 | 🔴 Alta |
| **Dono de Concessionária** | "Minha equipe age no escuro — não sei quem está prestes a sair" | Pulse Leads: lista priorizada diária por risco + LSV, com ação sugerida já embutida | Taxa de conversão lead → revisão agendada ≥ 35% | Latência endpoint `/leads` < 200ms; zero leads duplicados por dia | 🔴 Alta |
| **Gerente de Serviço (dealer)** | "Passo horas tentando decidir quem ligar. Sempre erro" | Ficha do cliente com etiqueta colorida de segmento + ação sugerida automaticamente | Redução de 40% no tempo médio de priorização de contatos | Precisão do segmentador: AUC ≥ 0,82; falsos positivos < 10% | 🔴 Alta |
| **Atendente (dealer)** | "Não sei nada do cliente que me liga — tenho que perguntar tudo de novo" | Vista 360: histórico completo, modelo, última revisão, score, ação sugerida numa tela | NPS do atendimento ≥ 60 (benchmark setor: ~50) | Tempo de carga da Vista 360 < 1 segundo; tempo de onboarding < 15 min | 🟡 Média |
| **Dono de modelo recente** (Ranger, Territory) | "Manutenção na Ford é cara e eu não sei quando fazer" | App mobile Modo Cliente: revisão sugerida por km/meses, Ford Care com preço fixo pré-pago, agendamento em 1 toque | Taxa de adoção Ford Care ≥ 20% dos clientes elegíveis em 12 meses | Tempo de resposta do app < 2s; push notification entregue em < 5s | 🟡 Média |
| **Dono de modelo descontinuado** (Ka, EcoSport, Fiesta) | "A Ford me abandonou — não tenho app, não recebo lembrete, peça sumiu" | Fluxo Simplificado: WhatsApp como canal principal, cadastro de VIN, lembrete por km estimada, agendamento sem app | Reativação de VINs inativos há > 12 meses ≥ 15% no 1º semestre | Entrega da msg WhatsApp < 30s; taxa de abertura ≥ 80% (meta Meta Brasil) | 🔴 Alta |
| **Equipe Técnica ForwardService** | "Precisamos garantir que o sistema escale sem degradar os modelos" | Flywheel de Dados: precisão cresce com uso. Arquitetura SOA com fronteiras claras — cada componente muda sem quebrar os outros | Precisão ML: mês 1 70% → mês 6 80% → ano 2 90% | Cobertura de testes ≥ 70%; deploy sem downtime (rolling update) | 🟡 Média |
| **Analista de Retenção Ford** | "Não consigo simular o impacto de uma campanha antes de aprovar o budget" | Strategy Simulator: "Se investir R$ X em [ação] para [perfil], retorno esperado: R$ Y" com margem ±25% | Redução de 30% no ciclo de aprovação de campanhas de retenção | Tempo de cálculo do simulador < 3s; precisão da estimativa ±25% (padrão de mercado) | 🟢 Baixa |

---

## Legenda

| Símbolo | Prioridade |
|---|---|
| 🔴 Alta | Blocking — sem isso o produto não entrega valor mínimo |
| 🟡 Média | Importante — diferencia o produto da concorrência |
| 🟢 Baixa | Desejável — eleva a proposta mas não é crítico no Sprint 1 |

---

## Métricas de Negócio — Resumo Consolidado

| Métrica | Baseline (hoje) | Meta Sprint 1 | Meta 12 meses |
|---|---|---|---|
| VIN Share Ford BR | ~3,5–5% | Medir com precisão | ≥ 8% |
| Taxa de retorno pós-1ª revisão | 71% (22/31 no dataset) | Identificar perfis em risco | ≥ 80% |
| Conversão WhatsApp → agendamento | nd | 30–45% (benchmark) | ≥ 40% |
| Dealers com IHC > 70 | nd | IHC calculado para todos | ≥ 80% dos dealers |
| Recalls atendidos | ~40% (setor BR) | Piloto 4–5 campanhas | ≥ 60% das campanhas-piloto |
| ROI campanha retenção | nd | 300:1 validado em teste | Rastreado por Closed-Loop ROI |
| NPS cliente | nd | Instrumento montado | ≥ 50 |

---

## Métricas de Qualidade — Resumo Consolidado

| Componente | Métrica | Valor-alvo |
|---|---|---|
| Backend API (forward-api-java) | Latência p95 | < 300ms |
| Backend API | Disponibilidade | ≥ 99% (≤ 7h15 downtime/ano) |
| ML — Classificador (XGBoost) | AUC | 0,82–0,90 |
| ML — Segmentador (K-means) | Silhouette | > 0,4 |
| ML — Falsos positivos | Churn não real | < 10% |
| ML — Flywheel | Precisão ao longo do tempo | 70% → 80% → 90% |
| Mobile app | Tempo de carga | < 2s |
| WhatsApp (n8n) | Entrega da mensagem | < 30s |
| Onboarding atendente | Tempo de treinamento | < 15 minutos |
| Testes automatizados | Cobertura de código | ≥ 70% |
| Dados (LGPD) | Reversibilidade do VIN_Hash | 0 matches em 5M tentativas |
| Deploy | Downtime por release | 0 (rolling update) |

---

## Fontes

- `forward-docs/project/00_BASE_FUNDACIONAL.md` — 4 pilares, 9 lógicas, LSV, Curva da Morte
- `forward-docs/project/03_SOLUTION_DESIGN.md` v2.1 — critérios de qualidade, RBAC, benchmarking
- `forward-docs/project/02e_DATASET_OFICIAL_E_FONTES.md` — VIN Share, Curva da Morte real (dataset Ford)
- Cox Automotive 2025 — retenção pós-garantia, CAV
- NADA 2025 — 49% do lucro dealer vem do pós-venda
- Bain & Company — +5% retenção = +25–95% lucro

---

*Entrega: `forward-docs/academic/valor/QUADRO_DE_VALOR.pdf` + este arquivo MD rastreável*
