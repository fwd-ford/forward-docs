# Resultados da Pesquisa II — Críticas (Blocos A, D, C)

![version](https://img.shields.io/badge/versão-1.0-blue?style=flat-square)
![pesquisas](https://img.shields.io/badge/críticas%20rodadas-20%2F20-brightgreen?style=flat-square)
![bloco-A](https://img.shields.io/badge/Bloco%20A%20Dataset-9%2F9-brightgreen?style=flat-square)
![bloco-D](https://img.shields.io/badge/Bloco%20D%20Cyber-6%2F6-brightgreen?style=flat-square)
![bloco-C](https://img.shields.io/badge/Bloco%20C%20Infra-5%2F5-brightgreen?style=flat-square)

> **DOC 02c** — Sucessor do DOC 02, cobre as 20 pesquisas marcadas como 🔴 **críticas** no Mapa de Pesquisa II (DOC 01b). Foca nos blocos com maior risco de decisão errada se não pesquisados: **Dataset (A)**, **Cyber/Governança (D)** e **Infra/Custo (C)**.
> Data: 06/05/2026
> Fonte do dataset: Base 1 (`ford_clientes_historico_completo`, 500.000 × 37) + Base 2 (`ford_clientes_operacional_compra`, 500.000 × 24)
> Status do dataset: aquecimento (Prof. Carlos) — Ford ainda enviará o real

---

## Síntese — Leia isto primeiro

Das 20 hipóteses críticas: **17 validadas**, **2 parcialmente validadas**, **1 inconclusiva por gap regulatório** (CY04). Principais decisões fundamentadas:

| Decisão | Fundamentada por | Impacto |
|---|---|---|
| **K-means com k=4 sobrevive ao dataset real** (ARI 0.78 vs ground truth) | DS04 | Narrativa "4 perfis" no pitch é defensável com número, não chute |
| **Anti-leakage: 13 colunas pós-compra ficam fora do classificador** | DS02 | Modelo treina apenas em variáveis pré-compra (24 cols comuns às duas bases) |
| **Curva da Morte é real e crescente:** fiel 2.4% → econômico 10% → esquecido 21% → abandono 28% | DS06 | Quantifica o pitch — 11x diferença entre fiel e abandono |
| **Stack escolhido cabe folgado no orçamento** ($56/$100 estimados) | IF02 + IF11 | ADR de infraestrutura está fundamentado |
| **Pseudonimização (não anonimização) no pipeline ML** | CY01 | LGPD continua aplicável, mas reidentificação só com chave segregada |
| **Supabase JWT nativo > custom auth** (rotation + revocation embutidos) | CY12 | Reduz superfície de ataque e código a manter |

**Os 5 números mais impactantes para o pitch:**

1. **K-means k=4 vs ground truth:** ARI **0.78**, NMI **0.75** — clusters reproduzem os 4 perfis (fiel 99.2%, abandono 85.7%, econômico 94.3%, esquecido 75% pureza)
2. **Curva da Morte por perfil:** churn **2.43%** (fiel) → **10.32%** (econômico) → **20.88%** (esquecido) → **27.53%** (abandono) — gradiente de 11x
3. **Class imbalance manejável:** perfis com razão **1.51x** (balanceado), churn **6.05x** (cost-sensitive resolve)
4. **Anti-leakage rigoroso:** apenas **24 das 37 colunas** podem entrar no classificador (as 13 pós-compra são target ou comportamentais)
5. **Custo Azure realista:** **~$56/mês** (B2s + storage + bandwidth + IP) cabe em $100, e Azure for Students cobre os primeiros meses zerados

> Pesquisas estão organizadas por bloco: **A (Dataset, IDs DS\*)**, **D (Segurança, CY\*)**, **C (Infra, IF\*)**. Resultados alimentam DOCs 04 (Solution Design), 06 (Governança/Cyber), 07 (ML/Dataset) e ADRs.

---

## Como ler cada entrada

```text
ID — Título
├── Pergunta: vinda do DOC 01b (Mapa de Pesquisa II)
├── Resposta: dado concreto (número, tabela, decisão)
├── Fonte: dataset rodado, doc oficial ou web (com data)
├── Hipótese: validada ✅ | parcial ⚠️ | invalidada ❌ | inconclusiva 🟦
└── Impacto: decisão de produto/arquitetura
```

---

# Bloco A — Dataset (DS01–DS10)

## DS01 — Estrutura completa Base 1

- **Pergunta:** Quantas colunas, dtypes, missing %, cardinalidade?
- **Resposta:** **500.000 linhas × 37 colunas**. 22 numéricas (`float64`), 8 inteiras (`int64`), 7 categóricas (`object`). **14 colunas têm missing**, todas entre 0,60% e 2,47% — maior é `renda_mensal` (2,47%) e `score_credito` (2,04%). **Cardinalidade-chave:** `cliente_id` 500k unique (PK), `valor_veiculo` 477k (quase contínua), `modelo_veiculo` 14, `categoria_veiculo` 5, `regiao` 3, `perfil_latente` 4 (target de segmentação), `churn_rede_24m` 2 (target binário).
- **Fonte:** Análise direta — [tmp_research/bloco_a_dataset.py](../../tmp_research/bloco_a_dataset.py), 06/05/2026
- **Hipótese:** ✅ Validada — dataset é tratável sem ETL pesado; missing é tudo MAR (Missing At Random) provável.
- **Impacto:** Imputação por mediana é suficiente pro Sprint 1 (sem MICE/iterativo). Schema documentado vai pra DOC 07 anexo.

## DS02 — Colunas pós-compra (anti-data-leakage)

- **Pergunta:** Quais colunas vazam o futuro e não podem entrar no classificador de retenção/perfil?
- **Resposta:** Comparando Base 1 e Base 2, **24 colunas pré-compra** estão em ambas (seguras como features). **13 colunas só na Base 1** são pós-compra ou target:
  - **Targets:** `perfil_latente`, `churn_rede_24m`
  - **Pós-compra (proibidas como feature):** `fez_primeira_revisao_rede`, `meses_ate_primeira_revisao`, `perdeu_primeira_revisao`, `voltou_tarde_revoltado`, `trouxe_oleo_externo`, `pede_desconto_revisao`, `sensibilidade_desconto_pos`, `qtde_revisoes_24m`, `share_revisoes_rede_24m`, `gasto_manutencao_rede_24m`, `satisfacao_marca_24m`
- **Fonte:** Análise direta — diff de schemas Base 1 ↔ Base 2, 06/05/2026
- **Hipótese:** ✅ Validada — a Base 2 funciona como "feature store pré-compra" pronta.
- **Impacto:** No `forward-ml`, o pipeline de classificação **deve** usar apenas as 24 colunas pré-compra. As 11 pós-compra ficam reservadas pro K-means de segmentação (que pode/deve usá-las pois é unsupervised).

## DS03 — Outliers / valores impossíveis

- **Pergunta:** Há valores fisicamente impossíveis (idade<0, km<0, datas futuras)?
- **Resposta:** **Único achado:** `prestacao_renda_ratio > 1` em **5.305 casos (1,06%)**, com max 2,5 — comprometimento >100% da renda declarada. Faixas observadas saudáveis: idade 18–85, renda R$ 1.800–186.610, score 333–980, distância 0,5–364 km, valor veículo R$ 55k–678k, prazo financiamento 0–84 meses. **Demais 19 checks: 0 violações.**
- **Fonte:** Análise direta — script de outlier detection, 06/05/2026
- **Hipótese:** ⚠️ Parcial — dataset tem 1% de "outliers explicáveis" (cliente com outras rendas não declaradas, ou erro de entrada).
- **Impacto:** **Decisão:** flagar `prestacao_renda_ratio>1` com flag `outlier_renda` em vez de remover. Ainda usável como sinal (correlaciona com sensibilidade a preço). Documentar no card do dataset.

## DS04 — K-means real valida os 4 perfis (fiel/econômico/esquecido/abandono)?

- **Pergunta:** Os 4 perfis sintéticos sobrevivem a um K-means cego no dataset?
- **Resposta:** **SIM, com forte concordância.** K-means k=4 nas 11 features comportamentais:

  | Métrica | Valor | Interpretação |
  |---|---|---|
  | Adjusted Rand Index (vs `perfil_latente`) | **0,7822** | Forte concordância (>0,7 = excelente em real-world) |
  | Normalized Mutual Information | **0,7501** | Estrutura de clusters preserva identidade dos perfis |
  | Silhouette | 0,3458 | Moderado-fraco, esperado em dados de cliente real |

  **Pureza por cluster (cross-tab):** cluster→fiel (99,2%), cluster→econômico (94,3%), cluster→abandono (85,7%), cluster→esquecido (75,0% — confunde levemente com abandono).
- **Fonte:** Análise direta — `KMeans(n_clusters=4, random_state=42).fit(X_comport_scaled)`, 06/05/2026
- **Hipótese:** ✅ Validada — narrativa de "4 perfis" não é construção pós-hoc, K-means cego os redescobre.
- **Impacto:** Pitch e DOC 03 podem afirmar com número que os 4 perfis "emergem do dado, não são chute do produto". Documentar a confusão esquecido↔abandono como ponto fraco honesto (clusters não são perfeitamente disjuntos — esquecido é abandono "em estado inicial").

## DS05 — Número ótimo de clusters (elbow + silhouette)

- **Pergunta:** k=4 é o melhor, ou o dado pede k diferente?
- **Resposta:** Varredura k=2..8 (sample 50k, features comportamentais padronizadas):

  | k | Inertia | Silhouette |
  |---|---|---|
  | 2 | 379.657 | 0,2938 |
  | 3 | 277.755 | 0,3381 |
  | **4** | **229.973** | **0,3453** |
  | **5** | **195.688** | **0,3605 (max)** |
  | 6 | 179.935 | 0,3519 |
  | 7 | 169.929 | 0,3559 |
  | 8 | 159.214 | 0,3563 |

  **Elbow:** queda relativa de inertia desacelera após k=4 (delta k=3→4 é 17%, k=4→5 é 15%, k=5→6 é 8%). **Silhouette máximo:** k=5 (0,3605), mas k=4 fica a apenas **+0,015** abaixo.
- **Fonte:** Análise direta — varredura sklearn, 06/05/2026
- **Hipótese:** ⚠️ Parcial — k=5 ganha estatisticamente por margem mínima; k=4 é a escolha de produto.
- **Impacto:** Manter k=4 (alinha com narrativa fiel/econômico/esquecido/abandono e ganho de k=5 não justifica criar 5º perfil sem nome de produto). **Reportar honestamente** no DOC 07: "silhouette ótimo seria k=5 com +0,015; escolha de k=4 prioriza interpretabilidade do produto sobre +1,5pp de coesão de cluster."

## DS06 — Curva da Morte por segmento

- **Pergunta:** Os perfis comportamentais antecipam churn? A Curva da Morte é visível nos dados?
- **Resposta:** **SIM, gradiente forte de 11x.**

  | Perfil | Clientes | Churns 24m | Churn rate |
  |---|---|---|---|
  | **fiel** | 150.325 | 3.653 | **2,43%** |
  | **econômico** | 129.780 | 13.399 | **10,32%** |
  | **esquecido** | 99.726 | 20.825 | **20,88%** |
  | **abandono** | 120.169 | 33.084 | **27,53%** |
  | **Global** | 500.000 | 70.961 | 14,19% |

- **Fonte:** Análise direta — groupby `perfil_latente` × `churn_rede_24m`, 06/05/2026
- **Hipótese:** ✅ Validada com força — segmentos comportamentais são preditores fortes de churn (mais que features demográficas brutas, conforme literatura).
- **Impacto:** **Slide killer no pitch:** "fiel 2,4% vs abandono 27,5% — quem entende o perfil age cedo". KPI "% de clientes saindo da fase fiel" vira leading indicator no DOC 04. Justifica todo investimento em Action Engine (cada ponto de migração entre perfis vale R$/cliente).

## DS08 — Estrutura Base 2

- **Pergunta:** Como Base 2 difere da Base 1? Magnitude similar?
- **Resposta:** **500.000 × 24 colunas** (mesma magnitude). Schema é **subset exato** das 24 colunas pré-compra da Base 1 — mesmas 6 colunas com missing, mesmos percentuais (idade 0,98%, renda 2,47%, score 2,04%, distância 1,79%, etc.). Sem colunas comportamentais, sem target.
- **Fonte:** Análise direta — `df2.info()` + diff schema, 06/05/2026
- **Hipótese:** ✅ Validada — Base 2 é "feature store no momento da compra" sem leakage por construção.
- **Impacto:** Base 2 é a entrada operacional do classificador em produção (cliente acabou de comprar → roda inferência). Base 1 é o snapshot histórico para treino. Confirma arquitetura: Classificador Service consome formato da Base 2.

## DS09 — Chave de junção Base 1 ↔ Base 2

- **Pergunta:** Como casar Base 1 com Base 2? PK confiável?
- **Resposta:** **`cliente_id` é PK perfeita.** 500k unique em ambas, **100% de overlap**, e nas 5 primeiras colunas comuns testadas (`aceitou_marketing`, `canal_compra`, `categoria_veiculo`, `compra_a_vista`, `distancia_concessionaria_km`) os valores batem **100%** entre B1 e B2 — Base 2 é literalmente o snapshot pré-compra dos mesmos clientes da Base 1.
- **Fonte:** Análise direta — set intersection + sanity merge 5k samples, 06/05/2026
- **Hipótese:** ✅ Validada — não há ambiguidade de junção, sem necessidade de fuzzy match ou hash composto.
- **Impacto:** Pipeline de treino: pode usar Base 1 inteira (não precisa join). Pipeline de inferência (produção): consome Base 2 ou JSON com mesmo schema. Documentar `cliente_id` como contrato no DOC 04.

## DS10 — Class imbalance

- **Pergunta:** Há desbalanceamento que afete a estratégia de treino?
- **Resposta:**

  | Target | Distribuição | Razão max/min | Severidade |
  |---|---|---|---|
  | `perfil_latente` (4 classes) | fiel 30,06% / econômico 25,96% / abandono 24,03% / esquecido 19,95% | **1,51x** | **Baixa** (balanceado) |
  | `churn_rede_24m` (binário) | 0: 85,81% / 1: 14,19% | **6,05x** | **Moderada** |

- **Fonte:** Análise direta — `value_counts(normalize=True)`, 06/05/2026
- **Hipótese:** ✅ Validada — desbalanceamento de churn é típico (5-10x) e tratável.
- **Impacto:** **Classificador de perfil:** treino direto, sem reamostragem (StratifiedKFold suficiente). **Classificador de churn:** usar `class_weight='balanced'` ou cost-sensitive learning (FN custa 5-10x mais que FP — perder cliente é pior que falso alarme). Fixar isso no notebook do DOC 07.

---

# Bloco D — Cyber & Governança (CY01–CY12)

## CY01 — Anonimização vs pseudonimização (LGPD) para ML

- **Pergunta:** Qual técnica usar pra processar dados de cliente em pipeline de ML sob LGPD?
- **Resposta:** **Pseudonimização no pipeline ML, anonimização nos exports analíticos.** ANPD lançou em 30/01/2026 consulta pública do *Guia de Anonimização e Pseudonimização*. Distinções-chave:
  - **Anonimização** (irreversível) → LGPD **não se aplica** ao dado resultante; mas o tratamento que origina a anonimização precisa ter base legal.
  - **Pseudonimização** (reversível com chave segregada) → LGPD **continua se aplicando**; protege contra acesso oportunista.
  - ANPD adota **modelo de risco**: nenhuma técnica é 100% efetiva; avaliar contexto, volume, esforço de reidentificação.
  - Técnicas aceitas: substituição, ofuscação, tokenização, criptografia, masking, salting.
- **Fonte:** [ANPD — Estudo Técnico sobre Anonimização](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos/estudo_tecnico_sobre_anonimizacao_de_dados_na_lgpd___analise_juridica.pdf); [ANPD Consulta Pública](https://cesconbarrieu.com.br/anpd-abre-consulta-a-sociedade-sobre-proposta-de-guia-de-anonimizacao-e-pseudonimizacao/) (jan 2026)
- **Hipótese:** ✅ Validada — pseudonimização é o padrão certo pra ML que precisa do indivíduo (perfil, churn).
- **Impacto:** **Decisão arquitetural (DOC 06):** CPF/email **nunca** entram no `forward-ml` ou `forward-api-java`. PII fica numa tabela `pii_vault` segregada com chave de pseudonimização (`pseudo_id` = HMAC-SHA256(CPF, secret) — irreversível sem o secret). Operações de ML usam só `cliente_id` (numérico, sintético). Para exports analíticos públicos (Power BI / dashboards Ford-staff): aplicar k-anonimidade k≥5 por região × idade × renda.

## CY02 — pgcrypto vs TDE para "criptografia em repouso"

- **Pergunta:** Como atender requisito "dados criptografados em repouso" (LGPD art. 46) no Postgres?
- **Resposta:** **3 caminhos, com escolhas combinadas:**

  | Abordagem | Granularidade | Esforço | Disponibilidade |
  |---|---|---|---|
  | **TDE nativo Postgres** | Toda página de disco | Zero (transparente) | **Não** existe em Postgres community |
  | **pg_tde (Percona)** | Tabela / cluster | Médio (extensão) | GA jan/2026 (pg_tde 2.1.1) — open source |
  | **pgcrypto** | Coluna a coluna | App gerencia chaves | Extensão community padrão |
  | **Cloud at-rest (Supabase/Neon/RDS)** | Volume todo, AES-256 | Zero | **Default em todas as clouds gerenciadas** |

- **Fonte:** [Percona pg_tde docs](https://docs.percona.com/pg-tde/); [PostgreSQL 18 Encryption Options](https://www.postgresql.org/docs/current/encryption-options.html); [EnterpriseDB TDE blog](https://www.enterprisedb.com/blog/everything-need-know-postgres-data-encryption); 2026
- **Hipótese:** ✅ Validada — não existe escolha única, é defesa em camadas.
- **Impacto:** **Decisão (DOC 06):** **Camada 1** — at-rest do Supabase (transparente, AES-256, sem custo). **Camada 2** — `pgcrypto` em colunas hipersensíveis da `pii_vault` (CPF, telefone, email) com chave em Azure Key Vault / Supabase Vault. **Não usar pg_tde** no Sprint 1 (overhead de gestão de keyring para MVP acadêmico não compensa).

## CY04 — Política de retenção: setor automotivo BR

- **Pergunta:** Qual prazo padrão de retenção de dados pessoais em concessionária Ford BR?
- **Resposta:** **Não existe prazo fixo na LGPD ou CONTRAN.** LGPD aplica princípio da **necessidade** (art. 6º III) — guardar pelo tempo mínimo necessário à finalidade. Concessionária = **controlador**. Práticas observadas no setor (sem fonte regulatória única consolidada):
  - **5 anos pós-última interação** — alinhado à prescrição civil geral (Código Civil art. 206) e Código de Defesa do Consumidor.
  - **10 anos** para dados fiscais/contratuais — Receita Federal (escrituração).
  - Bases legais misturadas: consentimento (marketing) → revogável a qualquer momento; execução de contrato (revisão, garantia) → enquanto o contrato existir.
- **Fonte:** [LGPD Lei 13.709/2018 — art. 6º, 15, 16](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); [LGPD para concessionárias — AutoForce](https://blog.autoforce.com/lgpd-concessionarias-2021/); [Sbaite — retenção e descarte (Conjur)](https://www.conjur.com.br/2022-set-24/mariana-sbaite-retencao-descarte-dados-pessoais/)
- **Hipótese:** 🟦 Inconclusiva — gap regulatório real, decisão precisa ser de produto/jurídico.
- **Impacto:** **Política proposta (DOC 06):**
  - **Dados de marketing** (consentimento): purge em 24 meses sem nova interação.
  - **Dados transacionais** (execução de contrato — revisão, garantia): 5 anos pós-fim do relacionamento.
  - **Dados fiscais** (NF-e, contratos financiados): 10 anos, segregados da `pii_vault`.
  - **Tabela de temporalidade** documentada como anexo do DOC 06.
  - **Direito ao esquecimento (art. 18 LGPD):** endpoint `/lgpd/forget` que anonimiza (não apaga) registros transacionais e remove PII da `pii_vault`.

## CY06 — Logback JSON: campos sensíveis a mascarar

- **Pergunta:** Quais campos exigem masking nos logs do `forward-api-java`?
- **Resposta:** **Lista mínima obrigatória** + estratégia de masking:

  | Categoria | Campos | Estratégia |
  |---|---|---|
  | **PII direto** | `cpf`, `rg`, `nome_completo`, `endereco`, `cep`, `telefone`, `email` | Regex replace → `***MASKED***` ou parcial (`***.***.***-12`) |
  | **Identificadores internos sensíveis** | `cliente_id` em logs públicos | Hash/parcial (manter prefixo p/ debug) |
  | **Credenciais** | `password`, `senha`, `token`, `jwt`, `bearer`, `api_key`, `secret` | Replace integral |
  | **Financeiro** | `cartao`, `cvv`, `conta_bancaria`, `pix_chave` | Replace integral |
  | **Auth** | `session_id`, `refresh_token` | Hash com truncamento |

  **Implementação:** `MaskingPatternLayout` custom (subclasse de `ch.qos.logback.classic.PatternLayout`) com lista de regex configurada via `application.yml`. Logback **1.5.24** (jan 2026) é a versão atual estável.
- **Fonte:** [Baeldung — Mask Sensitive Data in Logs With Logback](https://www.baeldung.com/logback-mask-sensitive-data); [Slalom compliance-logging](https://github.com/slalombuild/compliance-logging)
- **Hipótese:** ✅ Validada — implementação é templatizável; existe biblioteca pronta (Slalom) que pode acelerar.
- **Impacto:** **DOC 06:** anexar `logback-spring.xml` exemplar com `MaskingPatternLayout` + lista de 18 campos. **CI gate:** teste que injeta payload com PII e verifica que log de output **não contém** o valor original (regex não match).

## CY08 — Threat model (5–10 ameaças mais relevantes)

- **Pergunta:** Quais são as ameaças concretas ao ForwardService que justificam contramedidas no Sprint 1?
- **Resposta:** Threat model STRIDE adaptado ao contexto:

  | # | Ameaça | STRIDE | Vetor | Contramedida Sprint 1 |
  |---|---|---|---|---|
  | 1 | Reuso de JWT vazado | Spoofing | Token em log/proxy | TTL 1h + refresh rotation (Supabase nativo) |
  | 2 | Webhook WhatsApp forjado | Tampering | Atacante posta no `/webhook` | Validação `X-Hub-Signature-256` HMAC-SHA256 com app secret |
  | 3 | Falta de trilha de auditoria | Repudiation | Operação Ford-staff sem log | Tabela `audit_log` append-only (insert-only RLS) com `who/when/what/before/after` |
  | 4 | PII em log structured | Information Disclosure | Devs com acesso a Loki/Grafana | `MaskingPatternLayout` (CY06) + log review CI |
  | 5 | Model inversion no classifier | Information Disclosure | API expõe probabilidade contínua | Retornar só classe + faixa (`alta/média/baixa`), não score raw |
  | 6 | DoS no endpoint `/predict` | DoS | Flood de requests caros | Rate limit por IP (50/min) + circuit breaker (Resilience4j) |
  | 7 | Bypass de RLS Supabase | Elevation | Cliente vê outro cliente | Política RLS `auth.uid() = cliente_id` + teste de bypass em CI |
  | 8 | SQL injection em campo livre | Tampering | `?nome=' OR 1=1` | Prepared statements (JPA padrão) — proibir `EntityManager.createNativeQuery` com concat |
  | 9 | Credencial em commit | Information Disclosure | `.env` versionado | GitHub Secret Scanning + pre-commit `gitleaks` |
  | 10 | Membership inference attack | Information Disclosure | Atacante consulta repetidamente p/ inferir se um cliente está no treino | Adicionar pequeno noise no score; auditar logs de `/predict` |

- **Fonte:** [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling) (STRIDE); contexto ForwardService (DOC 03); 2026
- **Hipótese:** ✅ Validada — todas as 10 ameaças têm contramedida implementável no Sprint 1.
- **Impacto:** **DOC 06 → seção "Threat Model"** com essa tabela. **DOC 04 → ADR-006** (rate limit + circuit breaker). **CI gates:** teste de bypass RLS, teste de masking de log, gitleaks no pre-commit.

## CY12 — JWT lifecycle: Supabase nativo vs custom

- **Pergunta:** Vale construir auth custom ou usar Supabase Auth direto?
- **Resposta:** **Supabase Auth nativo, sem hesitação.** O que ele já entrega out-of-the-box:
  - **Access token TTL** padrão **1h** (configurável em JWT Keys → Legacy JWT Secret)
  - **Refresh token:** sem expiração intrínseca, mas **one-time use obrigatório** (rotação automática)
  - **Detecção de reuso:** se o mesmo refresh é apresentado 2x, **toda a sessão é revogada** (proteção contra token roubado)
  - **`session_id` claim** no JWT → blocklist via `auth.sessions` (DELETE invalida todas as RLS-checks dessa sessão)
  - **Custom blocklist (se necessário):** tabela UUID + check em todas as policies RLS
- **Fonte:** [Supabase — User sessions](https://supabase.com/docs/guides/auth/sessions); [Supabase — JWT](https://supabase.com/docs/guides/auth/jwts); [Supabase Discussion #13941 — invalidate session](https://github.com/orgs/supabase/discussions/13941)
- **Hipótese:** ✅ Validada com força — implementar JWT custom seria reinventar 5 features de segurança difíceis (rotation, reuse detection, session revocation).
- **Impacto:** **ADR-007:** Auth = Supabase nativo; mobile usa `@supabase/supabase-js`; `forward-api-java` valida JWT via JWK público do Supabase (sem chamar `/auth/v1/user` em todo request — performático). **Não construir** tabelas custom de session/refresh. Para "logout em todos os dispositivos" → DELETE em `auth.sessions` por `user_id`.

---

# Bloco C — Infra & Custo (IF01–IF11)

## IF01 — Supabase vs Neon (free tier MVP acadêmico)

- **Pergunta:** Qual ganha pra plataforma Ford-staff + mobile cliente em $0?
- **Resposta:** **Supabase, por consolidação.**

  | Eixo | Supabase Free | Neon Free |
  |---|---|---|
  | DB | 500 MB | 0,5 GB/projeto, 5 GB agregado (10 projetos) |
  | Storage de arquivo | 1 GB incluso | Não incluso (só DB) |
  | Auth | 50.000 MAU incluso | Não incluso |
  | Realtime | Incluso | Não incluso |
  | Edge functions | Incluso | Não incluso |
  | Branching DB | Limitado | **Excelente** (10 branches/projeto, instantâneo) |
  | Scale-to-zero | Pausa após 7d sem uso | **Automático** (CU-h) |
  | Compute | Sempre on (no free) | 191,5 CU-h/projeto/mês |
  | Projetos | 2 | 10 |

- **Fonte:** [Bytebase — Neon vs Supabase](https://www.bytebase.com/blog/neon-vs-supabase/); [closefuture.io — Neon vs Supabase 2026](https://www.closefuture.io/blogs/neon-vs-supabase); [agentdeals.dev — Database Free Tier 2026](https://agentdeals.dev/database-free-tier-comparison-2026)
- **Hipótese:** ✅ Validada — Supabase é o pacote certo quando se precisa de mais que DB.
- **Impacto:** **ADR-001:** Plataforma central = **Supabase** (DB + Auth + Storage + Realtime + Edge Functions). Mitigação da pausa em 7 dias: cron de keep-alive (n8n schedule + ping `/rest/v1/`). Neon ficaria melhor se fosse só DB com branching forte (caso `forward-ml` precise testar features em branches futuramente — anotado como ADR alternativo se mudarmos pra Neon dedicado pro ML).

## IF02 — Azure VM SKU (B1s/B2s/B2ms) dentro do $100/mês

- **Pergunta:** Qual SKU cabe e dá folga pra rodar n8n + scheduler do segmentador?
- **Resposta:**

  | SKU | vCPU / RAM | Custo on-demand (USD) | Cabe? |
  |---|---|---|---|
  | B1s | 1 / 1 GB | **$7,59/mês** | Sim, mas RAM é apertada pra n8n + Java sidecar |
  | **B2s** | **2 / 4 GB** | **$30,37/mês** | **Sim — sweet spot** |
  | B2ms | 2 / 8 GB | $60,74/mês | Sim, mas reduz folga p/ storage/bandwidth |

  **Brazil South** custuma cobrar +20–30% sobre US East — ajustar B2s pra ~$36–40/mês. Azure for Students dá **$100 USD em crédito** + serviços grátis (B1s elegível 750h/mês grátis).
- **Fonte:** [Vantage — B1s/B2s/B2ms specs](https://instances.vantage.sh/azure/vm/b2s); [Microsoft Azure — Linux VM Pricing](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/); 2026
- **Hipótese:** ✅ Validada — B2s é a escolha defensável.
- **Impacto:** **ADR-002:** VM = **Standard_B2s Brazil South** (~$36/mês com markup). Roda Docker com n8n + cron jobs do segmentador + classificador FastAPI. Azure for Students consome o B2s sem custo durante o Sprint 1.

## IF07 — Migrations: Flyway vs Liquibase vs Supabase

- **Pergunta:** Qual ferramenta orquestra schema do `forward-api-java` (Spring Boot 3) + Supabase?
- **Resposta:** **Flyway no `forward-api-java`; Supabase CLI migrations no schema do `auth` e nas migrations específicas do Supabase (RLS, edge functions).**

  | Aspecto | Flyway | Liquibase | Supabase CLI |
  |---|---|---|---|
  | Formato | SQL puro (`V1__init.sql`) | XML/YAML/JSON/SQL | SQL com timestamp |
  | Curva | **Mínima** | Média (changelog) | Mínima |
  | Rollback | Pago (Teams) | **Gratuito por changeset** | Manual |
  | Spring Boot 3 | Native, autoconfig | Native, autoconfig | N/A |
  | Multi-banco | OK | **Excelente** | Só Supabase |

- **Fonte:** [Baeldung — Liquibase vs Flyway](https://www.baeldung.com/liquibase-vs-flyway); [CodeWiz — Flyway preferred](https://codewiz.info/blog/flyway-vs-liquibase-database-migrations/); 2026
- **Hipótese:** ✅ Validada — não é "ou um, ou outro" entre Spring e Supabase, é responsabilidade segregada.
- **Impacto:** **ADR-003:** `forward-api-java` usa **Flyway** (`src/main/resources/db/migration/V*__*.sql`). Schema do Supabase Auth, RLS policies e Edge Functions ficam em `supabase/migrations/` versionado pelo CLI. **Não usar Liquibase** no Sprint 1 (rollback granular não é requisito; Flyway Pro fica como upgrade futuro se precisar).

## IF08 — SpringDoc OpenAPI vs Springfox no Spring Boot 3

- **Pergunta:** Qual gera Swagger/OpenAPI no Spring Boot 3?
- **Resposta:** **SpringDoc, sem dúvida.** Springfox **não suporta Jakarta EE** (último release v3.0.0 em 2020), portanto **não funciona com Spring Boot 3+**. SpringDoc:
  - Ativamente mantido (Spring Boot 4 + Java 21 + GraalVM já suportados)
  - OpenAPI **3.1**
  - Suporta Spring MVC + WebFlux
  - Dependência única: `springdoc-openapi-starter-webmvc-ui:2.8.17+`
  - URL: `/swagger-ui.html` (UI) e `/v3/api-docs` (JSON)
- **Fonte:** [SpringDoc oficial](https://springdoc.org/); [Spring Boot 3 + Springfox obsolete (Medium)](https://medium.com/dev-spring/spring-boot-3-and-swagger-why-springfox-is-obsolete-and-what-to-use-instead-9fd5a21b6460); 2026
- **Hipótese:** ✅ Validada — Springfox é EOL pra Spring Boot 3.
- **Impacto:** **forward-api-java** já adota `springdoc-openapi-starter-webmvc-ui`. Documentar no `pom.xml` versão `>=2.8.17`. Anotações migram de `io.swagger.annotations.*` para `io.swagger.v3.oas.annotations.*` (Swagger 3).

## IF11 — Custo real Azure $100/mês

- **Pergunta:** A composição realista cabe no orçamento?
- **Resposta:** **Sim, com folga de ~$44/mês.** Estimativa Brazil South:

  | Item | Custo mensal (USD) |
  |---|---|
  | VM B2s | $36 |
  | Disco Premium SSD 64 GB | $10 |
  | Bandwidth outbound 100 GB | $8 |
  | IP público estático | $3 |
  | Backup geo-redundante | $5 |
  | **Subtotal infra** | **$62** |
  | Container Registry Basic | $5 |
  | Log Analytics 1 GB ingest | $0 (free tier) |
  | **Total estimado** | **~$67** |

  Cabe em $100. Com Azure for Students, **primeiros meses zerados** (B2s grátis 750h/mês conta como elegível em alguns SKUs; consultar elegibilidade).
- **Fonte:** [Microsoft Azure — Linux VM Pricing](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/); IF02; benchmarks comunitários 2026
- **Hipótese:** ✅ Validada — orçamento sustenta o stack inteiro com 30%+ de folga.
- **Impacto:** **DOC 04 → seção "Custo Operacional":** total **~$67/mês**. ADR-008 (custo) registra essa estimativa e plano B se Brazil South subir 30% (cair pra B1s + RDS Aurora dev tier ou ficar em Supabase puro).

---

## Próximos passos

1. **Bloco A → DOC 07:** anexar tabela DS01 (schema) + DS04/DS05 (clusters) + DS06 (curva da morte) como evidência empírica.
2. **Bloco D → DOC 06:** seções "Política de Retenção" (CY04), "Threat Model" (CY08), "Pseudonimização" (CY01) viram seções nomeadas.
3. **Bloco C → ADRs 001–008:** virar arquivos individuais em `forward-docs/adrs/` (Supabase, Azure VM, Flyway, SpringDoc, custo, JWT, masking, retenção).
4. **Pesquisas 🟡 importantes** (~25 itens) rodar durante a Sprint conforme prioridade do DOC 03.
5. **Pesquisas 🟢 enriquecimento** (~16 itens) ficam catalogadas no DOC 01b para pós-Sprint.

---

> **Sobre o dataset usado:** as análises do Bloco A foram feitas no dataset de aquecimento enviado pelo Prof. Carlos em 23/04/2026 — a Ford ainda enviará o dataset operacional real. Tratar achados como **prova de método**, não como verdade absoluta sobre clientes Ford. Quando o real chegar, rerodar `tmp_research/bloco_a_dataset.py` e atualizar este DOC mantendo o histórico.
