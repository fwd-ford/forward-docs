# 02e — Dataset Oficial Ford + Fontes Externas

![version](https://img.shields.io/badge/versão-1.0-blue?style=flat-square)
![data](https://img.shields.io/badge/coleta-2026--05--11-brightgreen?style=flat-square)
![internas](https://img.shields.io/badge/análises_internas-5%2F5-brightgreen?style=flat-square)
![externas](https://img.shields.io/badge/fontes_externas-5%2F5-brightgreen?style=flat-square)

> **DOC 02e** — Inventário do dataset oficial Ford (`vin_share_Desafio_02.xlsx`, recebido 11/05/2026) + pesquisa em 5 fontes externas públicas. Sucessor da sequência 02 → 02c → 02d. Substitui as 30+ pesquisas do bloco A do DOC 02c que foram feitas em cima do **dataset de treino** (`ford_clientes_*.csv`) — agora temos o dado real.
>
> **Bibliografia completa das fontes externas:** [02e_REFERENCIAS.md](./02e_REFERENCIAS.md) (90+ URLs organizadas por tema)

---

## TL;DR — 10 linhas

1. **Dataset oficial:** 602.788 eventos × 25 colunas, **175.554 VIN_Hash únicos**, **100% Brasil**, 435 dealers, 21 modelos, anos 2017-2026.
2. **Schema completamente diferente** do dataset de treino: oficial é **log de eventos de serviço por VIN**, não tabela de cliente com features socioeconômicas e labels prontos.
3. **3 colunas são constantes** (`Country=BRA`, `ServiceType=Maintenance`, `StatusUSA=(60) Concluded`) — schema global da Ford herdado, mas BR-only no dado.
4. **Curva da Morte aparece direto no dado:** `MaintenanceNumber` distribui 1ª revisão **31%** → 2ª **22%** → 3ª **15%** → 4ª **9%** → cai progressivamente. **A retenção desaba a cada revisão.**
5. **72,7% dos VINs são "monogâmicos"** com um único dealer; 27,3% transitam — feature de lealdade ao dealer é forte.
6. **VIN_Hash é SHA1 robusto** — 5 milhões de tentativas de reversão com prefixos Ford BR não geraram nenhum match. Provavelmente com salt. Tratar como pseudonimizado por segurança (CY01).
7. **VIN Share absoluto calculado: ~3,5% a 5%** (175k VINs vistos / 3,5-5M frota Ford BR estimada). Validação direta da tese do projeto.
8. **Pesquisas externas (5 fontes) cobriram:** FENABRAVE (VIO), Ford dealers (geo), FIPE (valores), Senacon (12 recalls Ford), Manual de manutenção (intervalo padrão **10k km / 12 meses**).
9. **Features comportamentais derivadas: 175k VINs × ~20 features** prontas pra ML (CSV em `tmp_research/official/data/vin_features.csv`).
10. **O que muda no DOC 00:** Pilar 1 (Intelligence Hub) precisa **re-modelagem** — saímos de classificação supervisionada para **survival analysis + clustering comportamental**. Pilares 2/3/4 e infra/cyber/governança **sobrevivem** com ajustes pontuais.

---

## Sumário

1. [O dataset oficial — fatos](#parte-1--o-dataset-oficial--fatos)
2. [Surpresas críticas no schema](#parte-2--surpresas-críticas-no-schema)
3. [Features comportamentais derivadas](#parte-3--features-comportamentais-derivadas)
4. [Codebook inferido](#parte-4--codebook-inferido)
5. [Teste de reversão SHA1](#parte-5--teste-de-reversão-sha1)
6. [Fontes externas — resumos](#parte-6--fontes-externas--resumos)
7. [VIN Share absoluto](#parte-7--vin-share-absoluto)
8. [Reconciliação com DOC 02c](#parte-8--reconciliação-com-doc-02c)
9. [Decisões propostas](#parte-9--decisões-propostas)
10. [Próximos passos](#parte-10--próximos-passos)
11. [Anexo — Arquivos gerados](#anexo--arquivos-gerados)

---

## Parte 1 — O dataset oficial: fatos

| Métrica | Valor |
|---|---|
| Arquivo | `Ford_oficial/vin_share_Desafio_02.xlsx` |
| Recebido em | 11/05/2026 (via coordenação FIAP) |
| Total de linhas (eventos) | **602.788** |
| Colunas | **25** |
| VIN_Hash únicos | **175.554** |
| Eventos médios por VIN | **3,43** |
| Country | **BRA** (100%) |
| ModelYear | 2017-2026 |
| Dealers únicos (`DealerCode`) | **435** |
| Modelos únicos | **21** (4 são códigos internos não-decodificados: KFA, KHC, BDA, 7BC) |
| ServiceDate | mistura de formatos `dd/mm/yyyy` e `m/d/yyyy` por linha |

### Distribuição por modelo (top)

| Modelo | % eventos |
|---|---:|
| RANGER | 56,7% |
| KA | 22,2% |
| ECOSPORT | 7,5% |
| TERRITORY | 4,4% |
| BRONCO SPORT | 2,8% |
| MAVERICK, F-150, MUSTANG, FIESTA, FOCUS, EDGE, TRANSIT, FUSION/MONDEO, MUSTANG MACH-E, F-SERIES, CARGO | <2% cada |

> **Observação importante:** RANGER + KA somam **78,9%** dos eventos. O dataset é dominado por dois polos: a frota nova (Ranger) e a frota descontinuada (Ka). É um espelho fiel do problema do DOC 00 — 80% da frota Ford é descontinuada.

### Distribuição por ModelYear (top)

| Ano | % eventos |
|---|---:|
| 2021 | 22,2% |
| 2023 | 20,1% |
| 2020 | 19,7% |
| 2024 | 16,2% |
| 2022 | 11,6% |
| 2019, 2018, 2017 | <10% combinados |

---

## Parte 2 — Surpresas críticas no schema

### Surpresa 1: Colunas constantes

Três colunas inteiras têm **1 único valor** em todas as 602k linhas — **inúteis como feature**:
- `Country = 'BRA'` (100%)
- `ServiceType = 'Maintenance'` (100%)
- `StatusUSA = '(60) Concluded'` (100%)

Isso significa: o dataset é só de **manutenções concluídas no Brasil**. Sistema da Ford tem schema global ("USA" no nome da coluna), mas o recorte que recebemos é cirurgicamente filtrado.

### Surpresa 2: Curva da Morte aparece direto no dado

`MaintenanceNumber` (número sequencial da revisão programada) tem distribuição:

| Revisão # | % eventos | Interpretação |
|---:|---:|---|
| 1ª | 31,3% | Cliente trouxe na 1ª revisão programada |
| 2ª | 22,3% | Voltou pra 2ª — retenção 71% (22/31) |
| 3ª | 15,0% | Retenção 67% (15/22) |
| 4ª | 9,5% | Retenção 63% (9/15) |
| 5ª | 6,5% | Retenção 68% (6/9) |
| 6ª+ | 15,4% | cauda longa |

> **Cada degrau perde ~30-40% dos clientes anteriores.** É o gráfico da Curva da Morte do DOC 00 (Cox Automotive 82% → 22%) **traduzido para dado interno Ford**. Não é mais hipótese — é fato medido.

### Surpresa 3: Dois targets diferentes pra "VIN ativo"

A distribuição de **eventos por VIN** mostra uma cauda muito longa:

| Eventos | VINs | % |
|---:|---:|---:|
| 1 | 50.499 | 28,8% |
| 2 | 39.564 | 22,5% |
| 3 | 31.177 | 17,8% |
| 4 | 16.076 | 9,2% |
| 5 | 11.418 | 6,5% |
| 6-10 | 20.344 | 11,6% |
| 11-15 | 4.350 | 2,5% |
| 16+ | 2.126 | 1,2% |

**28,8% dos VINs apareceram só 1 vez** — provavelmente churned ou recém-comprados. Cria ambiguidade fundamental na definição de churn:
- *"VIN com 1 evento de 2020"* = churned (sumiu há 4 anos)
- *"VIN com 1 evento de 2026"* = recente (ainda vai voltar)

A definição de churn no pipeline ML **deve ser por recência absoluta** (`days_since_last_service > N`), não por contagem de eventos.

### Surpresa 4: 72,7% dos VINs visitam um único dealer

| Dealers distintos | VINs | % |
|---:|---:|---:|
| 1 | 127.654 | 72,7% |
| 2 | 38.015 | 21,7% |
| 3 | 7.796 | 4,4% |
| 4+ | 2.089 | 1,2% |

**A lealdade ao dealer é o padrão, não a exceção.** Quem muda de dealer (~27%) é um sinal forte — pode indicar mudança geográfica, insatisfação, ou cliente que tá "passeando" antes de churnar. Feature comportamental rica.

### Surpresa 5: Data quality issues

- **`KM` máximo = 955.388.451** (955 milhões de km — fisicamente impossível). Outliers de digitação que precisam clipping (sugiro cap em 500k km).
- **`MainSource` tem duplicata por trailing space**: `'Agenda + Official Maintenance'` (71,5%) e `'Agenda + Official Maintenance '` (22,5%) — **precisa `.strip()` na ingestão**.
- **Datas com formato misto** na mesma linha — `ServiceDate=10/07/2023` (dd/mm) mas `InvoiceDate=4/17/2023` (m/d). Parser tem que ser por-coluna.

### Surpresa 6: O que NÃO tem

| O que esperávamos do dataset de treino | Está no oficial? |
|---|:---:|
| `cliente_id` | ❌ |
| `idade`, `renda_mensal`, `score_credito` | ❌ |
| `distancia_concessionaria_km`, CEP | ❌ |
| `perfil_latente` (label) | ❌ |
| `churn_rede_24m` (label) | ❌ |
| `share_revisoes_rede_24m` (label) | ❌ |
| `satisfacao_marca_24m` (label) | ❌ |
| trim/versão do veículo | ❌ |
| codebook de `ServiceCode`/`ServiceRepairTypeCode` | ❌ |

**Não tem nenhum label de ML pronto.** Targets precisam ser **construídos por engenharia de label**.

---

## Parte 3 — Features comportamentais derivadas

Mesmo sem socioeconômico, o dataset é **rico longitudinalmente**. Foram derivadas **20+ features por VIN** sem fonte externa:

| Família | Features |
|---|---|
| **Recência** | `days_since_last_service`, `gap_last_days`, `gap_last_vs_avg` (proxy) |
| **Frequência** | `events_count`, `tenure_days`, `gap_avg_days`, `gap_min/max_days` |
| **Lealdade** | `dealers_distinct`, `primary_dealer`, `primary_dealer_share` |
| **Uso** | `km_max`, `km_min` |
| **Mix** | `service_types_distinct`, `service_codes_distinct` |
| **Ciclo de vida** | `first_service_date`, `last_service_date`, `invoice_date`, `sales_date`, `warranty_start` |
| **Modelo** | `model_name`, `model_year` |

**CSV completo:** `tmp_research/official/data/vin_features.csv` (175.554 linhas).

### Distribuições-chave

- **Tenure** (dias entre compra e último serviço): median **669 dias (~22 meses)**, p75 **34 meses**.
- **Gap médio entre serviços:** median **221 dias (~7 meses)** — coerente com cronograma Ford de 10k km / 12 meses, com flexibilidade.
- **KM máximo:** median **29.508 km**, p75 **48.323 km**. Frota relativamente nova/pouco rodada (filtrando o outlier).

### Implicação pra ML

O target de "cliente em risco" pode ser construído com regra direta:

```text
churned = days_since_last_service > 365 AND last_service_date < (max_data_date - 365 days)
at_risk = days_since_last_service > (gap_avg_days * 1.5) AND days_since_last_service > 90
healthy = days_since_last_service <= gap_avg_days
```

Features de churn de maior peso esperado (sem ainda treinar):
1. `days_since_last_service` (recência absoluta)
2. `gap_last_days / gap_avg_days` (acelerando ou retardando)
3. `events_count` (engajamento histórico)
4. `dealers_distinct` (estabilidade)
5. `service_codes_distinct` (riqueza comportamental)

---

## Parte 4 — Codebook inferido

Como a Ford não forneceu o codebook oficial, foi feita inferência por co-ocorrência de campos. Resultados parciais:

### `ServiceCode` (139 valores únicos)

Top 6 códigos somam **~60%** dos eventos. Provável correspondência com revisões padrão:

| Código | % eventos | Hipótese |
|---|---:|---|
| 569 | 19,8% | 1ª revisão padrão? |
| 571 | 14,3% | 2ª revisão? |
| 573 | 9,8% | 3ª revisão? |
| 574 | 6,2% | 4ª? |
| 1226 | 5,4% | Reparo comum (família 1xxx)? |
| 575 | 4,1% | 5ª? |

**Confirmar com codebook oficial via Ford** ou inferir cruzando com `MaintenanceNumber`.

### `ServiceRepairTypeCode` (6 valores, 77% missing)

| Código | % (do não-missing) | Hipótese |
|---|---:|---|
| C | 90,4% | **C**ustomer-pay (paga cliente) |
| W | 7,0% | **W**arranty (garantia) |
| I | 2,6% | **I**nternal (interno) |
| A, U | <0,2% | ? |

### `ServiceDeptCode` (4 valores, 77% missing)

| Código | Hipótese |
|---|---|
| S | Service department |
| Q | Quick lane / Quick service |
| U | Used vehicles / Body shop? |
| B | Body shop? |

> **77% de missing** em ambos os campos sugere que esses códigos só são preenchidos em fluxos específicos (reparos com garantia ou em departamentos específicos).

### `MainSource` (4 valores)

| Valor | % |
|---|---:|
| `Agenda + Official Maintenance` | 71,5% + 22,5% (duplicata com espaço) = **94,0%** |
| `Official Maintenance` | 5,4% |
| `Official Maintenance + GUDB` | 0,5% |

**94% das visitas vêm via agendamento.** O canal "agenda" é dominante — implica que o pipeline de retenção pode otimizar contato pré-agendamento.

---

## Parte 5 — Teste de reversão SHA1

**Método:** 5.000.000 tentativas com prefixos Ford BR conhecidos (9BF, 8AF, 9BB) + 6 chars VDS + 8 chars VIS placeholder, comparando contra 50 hashes amostrados.

**Resultado:** **0 matches**.

**Conclusão:**
- O VIN_Hash **não é** SHA1 simples sobre o VIN cru. Provavelmente tem salt ou é HMAC.
- Reversão por rainbow table no espaço completo (~17 chars × 32 caracteres válidos = ~10²⁵ combinações) é **computacionalmente inviável**.
- **Decisão CY01:** tratar como **pseudonimizado** (não anonimizado) por precaução LGPD. Mas o risco real de reidentificação é baixíssimo.

---

## Parte 6 — Fontes externas — resumos

> **Detalhes completos** em `tmp_research/official/02_external_sources/*.md`. Resumo de cada uma abaixo.

### 6.1 FENABRAVE / Sindipeças — VIO Ford BR

**Achados-chave:**
- **VIO Ford BR estimado: 3,5 a 5 milhões** de veículos (gap: Anuário Sindipeças oficial por marca é pago)
- ~80% da frota = Ka + Fiesta + EcoSport (descontinuados)
- Idade média frota BR 2024: **10 anos e 11 meses** (frota Ford ainda mais velha)
- Vendas Ford BR: 226k (2018) → 20k (2022, colapso) → 48k (2024) → 49k (2025)
- Concessionárias: 283 (2021) → 80 (2023) → 140 (2025, padrão Signature 2.0)

**Limitações:** detalhamento por marca/modelo do Anuário Sindipeças exige compra (~R$200-400). Estimativa derivada de produção × idade × sucateamento.

### 6.2 Diretório de concessionárias Ford

**Achados-chave:**
- **80 dealers únicos coletados** via ABRADIF (cobertura ~67% da rede de ~120 estimada)
- **25/27 UFs cobertas** (faltam AM, SE) — CSV com nome, cidade, UF, endereço, CEP, lat/long
- Concentração SP+PR+SC+RS+MG = **61%** dos dealers
- `fordconcessionaria.com.br` está **fora do ar** (NXDOMAIN); `ford.com.br` retorna 403 (anti-bot)

**Limitação crítica:** **DealerCode (do dataset) → nome do dealer NÃO foi mapeado.** Esses códigos numéricos (4146, 2033, etc.) são internos da Ford (DMS proprietário). O catálogo público usa nomes, não códigos.

**Workaround:** cruzar dataset com 80 dealers por agrupamento regional/UF inferido (mas não direto por dealer).

### 6.3 Tabela FIPE — valores por modelo/ano

**Achados-chave:**
- **71/95 combinações modelo×ano cobertas** (75%) via API Parallelum, ref maio/2026
- **Spread confirma a tese de LSV diferenciado por modelo:**
  - Ka 2017 R$ 38.005 (menor)
  - Mustang Dark Horse 2025 R$ 609.262 (maior)
  - **Fator 16× entre os extremos**
- Ranger Limited V6 2026 (R$ 318k) = **8,4×** Ka base — prioridade de lead justificada com número
- Variação por trim: ±25% médio; Ranger Raptor 2025 chega a +99%

**CSV pronto:** `tmp_research/official/data/fipe_values.csv` (95 linhas, colunas `model, year, fipe_mean_brl, min, max, n_versions, reference_month, source`).

### 6.4 Senacon — Recalls Ford BR

**Achados-chave:**
- **12 campanhas Ford BR mapeadas** (2015-2026), 9 abertas/recentes (2024-2026)
- Modelos mais afetados: Bronco Sport, Maverick, Mustang, Ranger (recentes); Territory, EcoSport, Edge, Fusion, Troller (histórico)
- **Ford liderou recalls globais em 2025**: 104 convocações (Stellantis em 2º com 21)
- **Estoque de recalls pendentes Brasil:** ~3,4 milhões (set/2024)
- **Adesão média setor BR: ~40%**; 27% das campanhas têm adesão <10%

**Alavanca regulatória forte:** novo CTB 2024-2025 **bloqueia licenciamento** de veículo com recall pendente >1 ano — incentivo direto pro Recall Gateway (LN4).

**Limitação:** códigos oficiais Senacon não públicos (portal exige login). Recomendar pedido LAI ao Ministério da Justiça.

### 6.5 Manual de manutenção Ford

**Achados-chave:**
- **8/8 modelos prioritários cobertos** (Ka, Fiesta, EcoSport, Focus, Ranger, Maverick, Territory, Transit)
- **Intervalo padrão Ford BR linha 2015+: `10.000 km ou 12 meses`**, o que vier primeiro (confirmado oficial)
- Exceções: Ranger 3.0 V6 e Maverick FHEV 2023+ = 16k km (Revisão Inteligente); Transit = 20k km
- Tolerância oficial Ford: **±1.000 km ou ±30 dias** (sem perder garantia)
- Preços por revisão: Ka R$ 400-1.200; Ranger R$ 1.129-1.679; total 60k km Ranger = **R$ 7.384-8.074**

**Regra "atrasado pra revisão"** pronta com hierarquia de severidade 0.8 → 2.5+:

```
severidade = max(km_desde_ultima / intervalo_km, meses_desde_ultima / intervalo_meses)
- 0.8-1.0: pré-aviso
- 1.0-1.3: lembrete + cupom
- 1.3-1.7: outreach proativo (concessionária liga)
- 1.7-2.5: recuperação ativa (Ford Protect)
- > 2.5:   cliente perdido — não desperdiçar verba
```

**CSV pronto:** `tmp_research/official/data/maintenance_schedules.csv` (65 linhas, 11 variantes de modelo).

---

## Parte 7 — VIN Share absoluto

A métrica central do projeto finalmente tem número:

```
Numerador (VINs vistos na rede oficial): 175.554
Denominador (VIO Ford BR estimado):     3,5M a 5M

VIN Share = 3,5% a 5,0%
```

**Implicações:**
- **95-96,5% da frota Ford BR não passa pela rede oficial** — confirma e quantifica o problem statement do DOC 00.
- Como o dataset cobre 2017-2026 (10 anos), o VIN Share refere-se a **frequência de retorno cumulativa**, não fluxo anual.
- Para o pitch, pode ser apresentado como:
  > *"Apenas 175 mil dos cerca de 4 milhões de Fords em circulação no Brasil passaram pela rede oficial nos últimos 10 anos — um VIN Share de ~4%. O resto vai pra oficinas independentes. O Ford Forward existe pra mudar essa equação."*

**Caveat:** o número está **inflado** comparado ao "VIN Share anual" porque agrega 10 anos. Versão anual seria menor (~1-2%). Recomenda-se reportar ambos.

---

## Parte 8 — Reconciliação com DOC 02c

Das 20 pesquisas críticas do DOC 02c, foram revalidadas com o dataset oficial:

| Pesquisa | Status pós-oficial | Decisão |
|---|---|---|
| **DS01** — Estrutura completa | ❌ Obsoleta (500k×37 era treino) | Substituída por este DOC |
| **DS02** — Anti-leakage / 13 colunas pós-compra | ❌ Inaplicável (não há labels prontos) | Engenharia de label substitui anti-leakage |
| **DS03** — Outliers | ⚠️ Parcial (KM tem outlier 955M, mas é diferente do treino) | Re-executar limpeza |
| **DS04** — K-means k=4 ARI 0.78 | ❌ Inválida (não há `perfil_latente` ground truth) | K-means cego sobre features comportamentais |
| **DS05** — Número ótimo de clusters | ❌ Inválida | Re-executar com features novas |
| **DS06** — Curva da Morte por perfil (11x) | ✅ **Confirmada de forma direta** via `MaintenanceNumber` | Manter narrativa do pitch, atualizar números |
| **DS07-10** — Demais data quality | ⚠️ Parcial | Re-executar para schema novo |
| **CY01** — Pseudonimização | ✅ **Simplificada** — Ford já anonimizou via SHA1 robusto | Tratamento conservador como pseudonimizado mantido |
| **CY02-12** — Demais Cyber | ✅ **Sobrevivem** (independem de schema) | Sem mudança |
| **IF01-11** — Infra/custo Azure | ✅ **Sobrevivem** | Sem mudança |

**Síntese:** **Bloco A (Dataset, DS01-10) precisa de revisão profunda** — virá DOC 02f específico. **Blocos C (Infra) e D (Cyber) ficam intactos**.

### Impacto nos pilares do DOC 00

| Componente | Impacto | Ação |
|---|---|---|
| **Pilar 1 — Customer Vista 360 (socioeconômico)** | 🔴 Não viável só com oficial — falta cliente | Adaptar: usar CSV de treino como **simulação honesta** ou modelar só comportamental |
| **Pilar 1 — Radar de Churn (XGBoost supervisionado)** | 🔴 Sem target — repensar | Migrar para **survival analysis (Kaplan-Meier)** ou classificação com **target engenheirado** (recência > N) |
| **Pilar 1 — Service Share Map** | 🟢 Reforçado — temos DealerCode + 80 dealers geo | Implementar com FENABRAVE + ABRADIF |
| **Pilar 1 — LSV (LN1)** | 🟡 Adapta — temos FIPE + cronograma de revisão | Fórmula: `LSV = FIPE × P(recompra) + soma(custo_revisão × P(retorno))` |
| **Pilar 1 — Curva da Morte (LN2)** | 🟢 **Confirmada empiricamente** com dado real | Usar `MaintenanceNumber` diretamente como base |
| **Pilar 1 — Fleet Segmentation (LN6)** | 🟢 OK | RANGER (56%) vs KA+ECOSPORT (29%) já segmenta espontaneamente |
| **Pilar 2 — Pulse Leads** | 🟢 OK | Lead = VIN com `gap_atual > 1.5 × gap_avg` |
| **Pilar 2 — CommEngine / WhatsApp** | 🟢 OK (independe) | Sem mudança |
| **Pilar 2 — Recall Gateway (LN4)** | 🟡 Parcial — temos 12 campanhas, falta universo BR | Piloto com 4-5 campanhas com chassi público |
| **Pilar 3 — Ford Care, Fluxo Simplificado** | 🟢 OK (independe) | Sem mudança |
| **Pilar 4 — IHC, Closed-Loop ROI, Dealer Benchmark** | 🟢 **Reforçados** — 435 DealerCode reais | Implementar com agrupamento regional |
| **LN3 — Rede Invertida (desertos)** | 🟢 Implementável — temos 80 dealers geocodificados | Mapa de calor de VINs × distância ao dealer |

---

## Parte 9 — Decisões propostas

### D1 — Modelagem ML migra de classificação supervisionada para survival/comportamental

**Antes (DOC 02c, baseado em treino):** XGBoost com `churn_rede_24m` como target, SHAP pra interpretabilidade, AUC 0.82-0.90 esperado.

**Agora (com oficial):** Target precisa ser engenheirado. Proposta:
- **Modelo A (recência):** classificação binária com target `churned = days_since_last_service > 365` — XGBoost continua valendo
- **Modelo B (survival):** Kaplan-Meier por modelo/ano pra estimar curva de retorno — preditor de "tempo até próximo serviço"
- **Modelo C (segmentação):** K-means sobre features comportamentais (20 features), sem ground truth — usar Silhouette + análise de personas pós-hoc

### D2 — Adotar normalização obrigatória na ingestão

- `MainSource`: `.strip()` (duplicata por trailing space)
- `KM`: clip a 500.000 (outliers físicos)
- Datas: parser por-coluna (`ServiceDate` e `ServiceOpenDate`/`ServiceClosedDate` em formato BR; `InvoiceDate`/`SalesDate`/`DeliveryDate`/`RegistrationDate`/`WarrantyStartDate` em formato US)
- `ServiceType`, `Country`, `StatusUSA`: dropar (constantes)
- `ScheduleID`, `MaintenanceID`: chaves técnicas — manter mas não usar como feature

### D3 — VIN_Hash tratado como pseudonimizado (mesmo com salt provável)

LGPD pede esse tratamento conservador. O SHA1 forte limita risco real, mas a decisão arquitetural mantém:
- Sem reverse engineering
- Sem cruzamento com fontes externas que poderiam expor identidade
- Repositório com dataset deve ser **privado**, mesmo com hash

### D4 — Fontes externas adotadas

| Fonte | Uso no Sprint 1 |
|---|---|
| FENABRAVE/Sindipeças | VIN Share absoluto no pitch (3,5-5%) |
| FIPE | Componente do LSV (`fipe_values.csv` join no pipeline) |
| Manual de manutenção | Flag "atrasado pra revisão" como regra de negócio |
| ABRADIF (80 dealers) | Service Share Map preliminar (cobertura UF) |
| Senacon | Recall Gateway com piloto de 4-5 campanhas (Troller, Territory 2021, Mustang BCM, Bronco/Maverick EGR) |

### D5 — Dataset de treino vira "simulação socioeconômica"

O CSV `ford_clientes_*.csv` (500k) **não é descartado**. Vira **dataset de simulação** das variáveis ausentes no oficial (idade, renda, score). Uso:
- Modelo paralelo de **propensão socioeconômica** (treinado no CSV)
- Documentar honestamente no pitch como "componente preparado para ingerir dados oficiais quando disponibilizados"
- Justifica arquitetura preparada pra ingestão de CRM/parceiros no futuro

---

## Parte 10 — Próximos passos

Sequência sugerida (em ordem de prioridade, para o Sprint 1):

1. **Atualizar DOC 03 (Solution Design)** com as decisões D1-D5 — especialmente mudança do Radar de Churn (XGBoost supervisionado → survival/comportamental)
2. **Criar DOC 02f** específico sobre engenharia de label (definir formalmente "churn", "ativo", "em risco")
3. **Implementar pipeline de ingestão no `forward-ml`** com normalizações da D2 — output: dataset limpo pra modelagem
4. **Notebook baseline** com K-means cego em features comportamentais — comparar com personas hipotéticas do DOC 00 (fiel/econômico/esquecido/abandono)
5. **Atualizar ADR-001 (Pseudonimização)** com o teste SHA1 e a decisão D3
6. **Atualizar Pitch** com o número-chefe: **VIN Share ~3,5-5% no Brasil** (validado com dado real)
7. **Sprint 2-3 (pós-24/05):** mapear DealerCode → cidade via heurística (qual UF tem mais eventos por código), e geocoding complementar dos ~40 dealers faltantes

---

## Anexo — Arquivos gerados

### Análises internas (do dataset oficial)
- `tmp_research/official/01_internal_analysis/inventory.md` — schema completo, distribuições, qualidade
- `tmp_research/official/01_internal_analysis/geography.md` — Country 100% BRA
- `tmp_research/official/01_internal_analysis/codebook_inferred.md` — cross-tabs Service*
- `tmp_research/official/01_internal_analysis/behavioral_features.md` — features comportamentais derivadas
- `tmp_research/official/01_internal_analysis/sha1_reversal_test.md` — teste de reversão SHA1

### Pesquisas externas
- `tmp_research/official/02_external_sources/fenabrave_vio.md` — VIO Ford BR
- `tmp_research/official/02_external_sources/ford_dealers.md` — diretório de 80 dealers
- `tmp_research/official/02_external_sources/fipe_values.md` — valores FIPE por modelo/ano
- `tmp_research/official/02_external_sources/senacon_recalls.md` — 12 campanhas de recall
- `tmp_research/official/02_external_sources/manuals_maintenance.md` — cronograma oficial de manutenção

### Dados estruturados (CSV)
- `tmp_research/official/data/profile.json` — perfil quantitativo do dataset
- `tmp_research/official/data/vin_features.csv` — 175k VINs × 20+ features (input pro ML)
- `tmp_research/official/data/ford_dealers.csv` — 80 dealers geocodificados
- `tmp_research/official/data/fipe_values.csv` — 95 combinações modelo×ano
- `tmp_research/official/data/ford_recalls.csv` — 12 campanhas
- `tmp_research/official/data/maintenance_schedules.csv` — 65 linhas de cronograma

### Scripts (em `Ford_oficial/`)
- `_inspect.py` — inspeção estrutural inicial
- `_profile_full.py` — profile completo
- `_internal_analysis.py` — análise interna em 5 blocos

---

> **Status:** Dataset oficial inventariado e cruzado com 5 fontes externas. Decisões propostas prontas pra validação do grupo. Próximo passo é atualizar DOC 03 (Solution Design) refletindo as mudanças, especialmente no Pilar 1.
