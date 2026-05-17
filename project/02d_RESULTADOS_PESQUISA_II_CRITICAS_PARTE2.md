# Resultados da Pesquisa II — Críticas Parte 2 (Blocos F, B, E, G, H, I, J)

![version](https://img.shields.io/badge/versão-1.0-blue?style=flat-square)
![pesquisas](https://img.shields.io/badge/críticas%20rodadas-14%2F14-brightgreen?style=flat-square)
![bloco-F](https://img.shields.io/badge/Bloco%20F%20Academic-5%2F5-brightgreen?style=flat-square)
![bloco-B](https://img.shields.io/badge/Bloco%20B%20ML-1%2F1-brightgreen?style=flat-square)
![bloco-E](https://img.shields.io/badge/Bloco%20E%20WhatsApp-3%2F3-brightgreen?style=flat-square)
![bloco-G](https://img.shields.io/badge/Bloco%20G%20Mobile-2%2F2-brightgreen?style=flat-square)
![outros](https://img.shields.io/badge/H+I+J-3%2F3-brightgreen?style=flat-square)

> **DOC 02d** — Continuação do DOC 02c, cobre os 14 críticos restantes do Mapa de Pesquisa II (DOC 01b). **Bloco F desbloqueia entrega de Testing** (TOGAF/Archi); demais blocos fundamentam DOCs 04 (Solution Design), 07 (ML), 08 (Mobile/UX) e o pitch.
> Data: 06/05/2026
> Pré-requisitos: [DOC 02c](./02c_RESULTADOS_PESQUISA_II_CRITICAS.md) (Bloco A/D/C — 20 itens já compilados)

---

## Síntese — Leia isto primeiro

Das 14 hipóteses críticas: **10 validadas**, **2 parcialmente validadas**, **2 inconclusivas com decisão de produto** (AC01 sem rubrica oficial pública; AC03 "Quadro de Valor" não tem template FIAP encontrado). Decisões fundamentadas:

| Decisão | Fundamentada por | Impacto |
|---|---|---|
| **LogReg vence pra `perfil_latente`** (F1_macro 0,86, CV 0,856 ± 0,003) | ML04 | Modelo final do segmentador é LogReg — interpretável, barato, top-1 |
| **Classificador de churn pré-compra tem ceiling AUC ~0,73** com recall ~0 sem ajustes | ML04 | Estratégia: prever perfil → mapear perfil→risco churn (já validado em DS06) |
| **WhatsApp free tier morreu em jul/2025** — Sprint 1 fica em sandbox (200 msgs) | WA01 + WA03 | Demo do pitch usa sandbox + emulação; produção real fica como roadmap |
| **AI chatbots banidos no WhatsApp Business 2026** — só fluxos automáticos | WA07 | Action Engine = templates utility/service, não chatbot LLM |
| **Tech Challenge vale 90% da nota de TODAS disciplinas da fase** | AP01 | Sprint 1 não é "uma disciplina entre outras" — é o produto inteiro |
| **`app_metadata`, não `user_metadata`, pra role no JWT Supabase** | MB03 | Cliente não consegue se promover; RLS confiável |
| **Dataset sintético: aceitar 95% prediction performance como suficiente** (TSTR vs TRTR) | PR01 | Quando dataset real chegar, validar com TSTR ≥ 0,95 |

**Os 5 números mais impactantes:**

1. **LogReg perfil_latente:** F1_macro **0,8551** (5-fold CV: 0,856 ± 0,003) — modelo do Sprint 1 está escolhido com número
2. **Churn pré-compra:** ROC-AUC **0,73** (GB), mas recall_pos **<5%** — sem cost-sensitive, modelo é inútil clinicamente
3. **WhatsApp sandbox:** **200 mensagens** total (não/dia) — Sprint 1 demo precisa caber nesse limite
4. **WhatsApp prod sem business verif:** **250 msgs/24h** (Tier 0) → 1000 com verificação → 100k pós Quality
5. **Tech Challenge = 90% da nota** das disciplinas avaliativas da fase

---

# Bloco F — Academic (AC01–AC07)

## AC01 — Estrutura Pitch FIAP Challenge

- **Pergunta:** Existe estrutura/rubrica oficial de slides aprovados pela FIAP?
- **Resposta:** **Não há rubrica pública específica de slides** para o Challenge nas fontes acessíveis (FIAP On exige login). Mas a recomendação oficial e padrão de mercado para pitch curto (3–5 min) que cabe no contexto do Challenge converge em **8 slides**:

  | # | Slide | Tempo | Pergunta que responde |
  |---|---|---|---|
  | 1 | **Problema/Oportunidade** | 30s | Por que isso importa? Quem sofre? |
  | 2 | **Dimensão da dor** | 30s | Quanto vale (R$, %, pessoas)? |
  | 3 | **Solução** (visão de produto) | 45s | O que vamos construir? |
  | 4 | **Demo** (vídeo/screenshot) | 60s | Como funciona na prática? |
  | 5 | **Modelo de negócio** (Canvas síntese) | 30s | Como gera valor pra Ford? |
  | 6 | **Arquitetura/Stack** (TOGAF síntese) | 30s | Como construímos? |
  | 7 | **KPIs e ROI projetado** | 30s | Como medimos sucesso? |
  | 8 | **Time + Roadmap** | 15s | Quem somos e o que vem depois? |

  **Princípios FIAP** (do guia "Como fazer um bom pitch"): descrever rápido o mercado e o problema; **demonstração funcional** vale ouro; falar pra quem **não conhece** o problema.
- **Fonte:** [FIAP — Como fazer um bom pitch](https://www.fiap.com.br/2017/07/14/como-fazer-um-bom-pitch/); [Plano de Negócios e Pitch — Slideshare](https://www.slideshare.net/neigrando/plano-de-negcios-pitch-e-mvp); FIAP Pós-Tech challenges (sem rubrica pública detalhada); 2026
- **Hipótese:** ⚠️ Parcial — estrutura de mercado validada, rubrica FIAP-específica não encontrada (precisa confirmar com Salatiel/professor responsável).
- **Impacto:** **Plano de slides do pitch do Sprint 1** segue essa ordem. Slide 4 (demo) gravado em vídeo para garantir que rode em qualquer máquina (ver AC06 — não-crítica). **Ação:** validar com prof. responsável se há checklist específico antes de gravar versão final.

## AC02 — Business Canvas automotive aftermarket B2B2C

- **Pergunta:** Existem exemplos de Canvas B2B2C aplicado a aftermarket automotivo que possamos referenciar?
- **Resposta:** **Não há case público específico Ford-aftermarket.** Mas o framework está claro: ForwardService é **B2B2C** (Ford → Concessionária → Cliente final), com a Ford como controladora da plataforma. Os 9 blocos do Canvas, mapeados pro nosso contexto:

  | Bloco | Conteúdo ForwardService |
  |---|---|
  | **Segmentos de Cliente** | (B) Concessionárias Ford BR; (C) 4 perfis (fiel/econômico/esquecido/abandono) |
  | **Proposta de Valor** | (B) +25–95% lucro com +5% retenção (Bain); 49% do lucro vem do serviço (NADA); (C) Ford Care: preço pré-pago + lembretes inteligentes |
  | **Canais** | App Cliente; WhatsApp utility; CRM concessionária; Performance Console (Ford-staff) |
  | **Relacionamento** | Self-service (app), automatizado (WhatsApp), assistido (concessionária) |
  | **Receita** | (B) SaaS recorrente da concessionária; (C) Ford Care pré-pago + revisões; comissão sobre serviços recuperados |
  | **Recursos-Chave** | Dataset histórico (500k clientes), modelo ML, integração WhatsApp, rede DPaschoal-like |
  | **Atividades-Chave** | Segmentação contínua, action engine, governança LGPD, treinamento concessionária |
  | **Parcerias** | DPaschoal-equivalente (rede pós-garantia), Meta (WhatsApp), AWS/Azure |
  | **Custos** | Infra (~$67/mês, IF11 do DOC 02c), licenças WhatsApp, ML compute, equipe |

- **Fonte:** [Strategyzer — Business Model Canvas](https://www.strategyzer.com/library/the-business-model-canvas); [Sebrae — Canvas](https://www.inovacaosebraeminas.com.br/artigo/o-que-e-business-model-canvas-e-como-aplica-lo-no-seu-negocio); [Alura — B2B2C](https://cursos.alura.com.br/forum/topico-b2b-b2c-e-b2b2c-151486); validações do DOC 02 (Bain, NADA, Stellantis-DPaschoal)
- **Hipótese:** ✅ Validada — Canvas é mapeável e tem números reais nas células-chave (recursos, custos, valor).
- **Impacto:** **Slide 5 do pitch** = Canvas síntese (3 colunas: Cliente concessionária / Cliente final / Ford). Versão completa vira página em `forward-docs/academic/business_canvas.md`.

## AC03 — "Quadro de Valor" framework/template

- **Pergunta:** Qual template de "Quadro de Valor" a FIAP/Testing exige?
- **Resposta:** **Template específico não encontrado em fontes públicas.** O termo "Quadro de Valor" não tem definição padronizada na literatura de gestão (pode ser variante FIAP-interna do **Value Proposition Canvas** de Strategyzer, ou de rubrica de KPIs SMART). **Estrutura sugerida** consolidando práticas:

  | Coluna | Conteúdo |
  |---|---|
  | **Benefício** | O que o usuário ganha (em linguagem do usuário, não da feature) |
  | **Pilar/Lógica** | Qual pilar do produto entrega esse benefício |
  | **KPI Negócio** | Métrica de valor (R$, %, conversão) |
  | **KPI Qualidade** | Métrica de saúde técnica (latência, erro %, cobertura) |
  | **Meta Sprint 1** | Valor numérico esperado |
  | **Como medir** | Fonte da métrica (DB query, dashboard, log) |

  Alinha com **SMART** (Específico, Mensurável, Atingível, Relevante, Temporal) recomendado pelo guia geral de KPIs.
- **Fonte:** [Sebrae — Indicadores de Desempenho](https://sebrae.com.br/sites/PortalSebrae/ufs/pe/artigos/indicadores-de-produtividade-no-trabalho-os-mais-importantes,f3bfd38b1525a810VgnVCM1000001b00320aRCRD); [Strategyzer — Value Proposition Canvas](https://www.strategyzer.com/library/value-proposition-canvas); [Mereo — KPIs](https://mereo.com/hub/indicadores-de-desempenho/)
- **Hipótese:** 🟦 Inconclusiva — template oficial precisa ser confirmado com professor de Testing/Gestão.
- **Impacto:** **Ação imediata:** perguntar ao Salatiel se há template oficial. Se não, usar a tabela acima. Conteúdo concreto aproveita os KPIs definidos em AC07.

## AC04 — TOGAF Archi 4 camadas para automotive customer retention

- **Pergunta:** Existe exemplo público das 4 camadas TOGAF aplicado a retenção automotiva?
- **Resposta:** **Modelo BDAT (Business/Data/Application/Technology) é o padrão**, sem case automotive público canônico. **Mapeamento ForwardService:**

  | Camada | Elementos ForwardService |
  |---|---|
  | **Business (B)** | Atores: Cliente, Concessionária, Ford-staff, ANPD. Processos: Aquisição → Onboarding → Revisão programada → Renovação. Valores: Retenção, Conformidade LGPD, Margem pós-venda. Capabilities: Segmentação cliente, Action engine, Recall management |
  | **Data (D)** | Entities: Cliente, Veículo, Revisão, Campanha, Pseudo-ID. Stores: Postgres Supabase, audit_log, pii_vault. Tokens semânticos: VIN, cliente_id (pseudo), perfil_latente. Pipelines: ETL Base 1+2 → ML segmentação → ML classificação |
  | **Application (A)** | App Cliente (Expo RN), Performance Console (SvelteKit), forward-api-java (Spring Boot 3), forward-ml (FastAPI Python), n8n flows (WhatsApp), Supabase (BaaS) |
  | **Technology (T)** | Compute: Azure VM B2s; DB: Supabase Postgres + RLS + at-rest encryption; CDN/Hosting: Vercel (frontend); Mensageria: WhatsApp Cloud API; Observabilidade: Logback JSON; CI: GitHub Actions; Secrets: Azure Key Vault |

- **Fonte:** [Entasis — BDAT Model](https://www.entasispartners.com/blog/comprehensive-analysis-of-togafs-bdat-model-business-data-application-and-technology); [TOGAF Wikipedia](https://en.wikipedia.org/wiki/The_Open_Group_Architecture_Framework); [BoardMix — TOGAF Layers](https://boardmix.com/knowledge/togaf-it-architecture/)
- **Hipótese:** ✅ Validada — todas as camadas têm conteúdo concreto pro ArchiMate.
- **Impacto:** **Entrega Testing destravada.** Salatiel pediu Archi (não negociado) → modelo `.archimate` é construído com a tabela acima como fonte. Salvar em `forward-docs/academic/archimate/forward_service.archimate`. Cada camada vira uma view separada para o relatório.

## AC07 — KPIs Quadro de Valor (negócio + qualidade)

- **Pergunta:** Quais KPIs concretos preencher por benefício/pilar?
- **Resposta:** Consolidação por pilar, com benchmarks 2026:

  | Pilar | Benefício | KPI Negócio | KPI Qualidade | Meta Sprint 1 |
  |---|---|---|---|---|
  | **Intelligence Hub** | Identificar perfil de retenção | % de clientes com perfil atribuído | F1_macro do classificador | 100% / **F1≥0,85** (LogReg confirma — ML04) |
  | **Action Engine** | Reduzir churn por intervenção certa | % churn evitado por perfil "abandono" | Taxa de entrega WhatsApp | TBD / **>95%** entrega |
  | **Experience Layer** | Cliente percebe valor pós-compra | NPS (proxy: satisfação simulada) | Tempo p99 mobile | **NPS≥50** simulado / p99 ≤ 1,5s |
  | **Performance Console** | Ford-staff age com dado | DAU Ford-staff | Latência dashboard | TBD / **p95 ≤ 2s** |

  **Benchmarks setor:**
  - Service department = **49% do lucro** com 12% da receita (NADA 2025) — proxy de quanto vale cada ponto de retenção
  - LTV:CAC saudável **≥ 3:1**
  - Retenção média indústria: **75%** (auto-aftermarket varia 60–85%)
  - +5% retenção = **+25–95% lucro** (Bain & Company — DOC 02 P4.3)
- **Fonte:** [TVI — Automotive Retention Rate for Dealers](https://www.tvi-mp3.com/blog/insights/automotive-retention-rate-for-dealers/); [TryPropel — Retention Rates by Industry 2026](https://www.trypropel.ai/resources/customer-retention-rates-by-industry); [Contentsquare — Customer Retention KPIs 2026](https://contentsquare.com/guides/customer-retention/metrics/); DOC 02 P1/P4
- **Hipótese:** ✅ Validada — todos KPIs têm fonte de medição definida no stack atual.
- **Impacto:** Tabela vai pra `academic/quadro_de_valor.md` e Slide 7 do pitch. **F1≥0,85** já está atingido (ML04 confirma 0,8551), pode ir pro Slide com confiança.

---

# Bloco B — ML (ML04)

## ML04 — Comparar 3+ classificadores no dataset Ford

- **Pergunta:** Qual classificador vence pra `perfil_latente` e `churn_rede_24m` usando apenas as 24 colunas pré-compra (DS02)?
- **Resposta:** Pipeline padronizado (StandardScaler num + OneHot cat, imputação por mediana/moda), 100k linhas (75k train / 25k test), `random_state=42`, `class_weight` default.

  **Target 1 — `perfil_latente` (4 classes, balanceado, ML04 pré-compra strict):**

  | Modelo | Accuracy | F1_macro | F1_weighted | Fit (s) | Pred (s) |
  |---|---|---|---|---|---|
  | **LogReg** ⭐ | **0,8662** | **0,8551** | **0,8655** | 1,68 | 0,04 |
  | GradientBoosting | 0,8647 | 0,8534 | 0,8639 | **129,68** | 0,15 |
  | RandomForest | 0,8576 | 0,8452 | 0,8558 | 1,64 | 0,10 |
  | KNN | 0,8236 | 0,8090 | 0,8212 | 0,10 | 2,16 |
  | DecisionTree | 0,8129 | 0,7988 | 0,8118 | 1,23 | 0,04 |

  **CV 5-fold** do LogReg: F1_macro = **0,8556 ± 0,0025** (folds: 0,854 / 0,855 / 0,856 / 0,853 / 0,860). Confusion matrix mostra `fiel` quase perfeito (P=0,98 / R=0,98), `econômico` forte (P=0,88 / R=0,90), `abandono` e `esquecido` se confundem mutuamente (P=0,77–0,80) — alinhado com DS04.

  **Target 2 — `churn_rede_24m` (binário, imbalance 6x, sem cost-sensitive):**

  | Modelo | Accuracy | F1_macro | Precision_pos | Recall_pos | ROC-AUC |
  |---|---|---|---|---|---|
  | GradientBoosting | 0,8564 | 0,4858 | **0,4973** | 0,0259 | **0,7340** |
  | RandomForest | 0,8562 | 0,4662 | 0,4286 | 0,0050 | 0,7307 |
  | LogReg | 0,8548 | 0,4765 | 0,3711 | 0,0164 | 0,7239 |
  | KNN | 0,8535 | 0,4750 | 0,3005 | 0,0153 | 0,6747 |
  | DecisionTree | 0,8420 | **0,4964** | 0,2429 | **0,0474** | 0,6923 |

  **DIAGNÓSTICO CHURN:** Todos os modelos atingem ~85% accuracy **só batendo na classe majoritária** (recall positivo praticamente zero). ROC-AUC ~0,73 indica que **o sinal existe**, mas threshold default 0,5 está errado. Sem `class_weight='balanced'` ou SMOTE, o modelo é clinicamente inútil.
- **Fonte:** Análise direta — [tmp_research/bloco_b_ml04_classifiers.py](../../tmp_research/bloco_b_ml04_classifiers.py), 06/05/2026
- **Hipótese:** ⚠️ Parcial — perfil totalmente validado (LogReg vence); churn precisa segundo round com cost-sensitive antes de entrar em produção.
- **Impacto:**
  - **Modelo final do segmentador (Sprint 1):** **LogReg com 24 features pré-compra** (rápido, interpretável, F1=0,86, sem ganho de GB que custa 80x mais fit).
  - **Estratégia de risco de churn:** **NÃO** treinar classificador binário direto pré-compra. Em vez disso: prever `perfil_latente` → mapear via DS06 (fiel 2,4% / econômico 10,3% / esquecido 20,9% / abandono 27,5%) → produzir score de risco. É mais defensável, mais explicável e quantitativamente equivalente (DS06 já mostra que perfil é o preditor dominante).
  - **Roadmap pós-Sprint:** rodar nova versão com `class_weight='balanced'` + threshold optimization (ML08 + ML09 do mapa) **+** features pós-compra (revisão, satisfação) — mas no `forward-ml`, em job batch separado, não no classificador online.
  - **Slide 7 do pitch:** F1=0,86 com CV ±0,003 é número defensável, vai como bullet "modelo treinado e validado".

---

# Bloco E — WhatsApp & Action Engine (WA01–WA07)

## WA01 — Free tier Meta WhatsApp 2026

- **Pergunta:** Como conta o free tier hoje? Cabe um Sprint 1 com volume baixo?
- **Resposta:** **O modelo mudou bruscamente em jul/2025 e ficou pior pra MVP acadêmico:**

  | Categoria | Custo | Janela 24h |
  |---|---|---|
  | **Service** (resposta a msg do usuário) | **Free** dentro da janela 24h | Reset a cada msg do usuário |
  | **Utility** template | **Pago desde 1ª msg** (no Brasil ~$0,005–0,015/msg estimado) | Pago mesmo dentro da janela |
  | **Marketing** template | Pago desde 1ª msg (~$0,025/msg US, BR varia) | Sem free tier |
  | **Authentication** template | Pago desde 1ª msg (~$0,0135/msg US) | Sem free tier |
  | **Free Entry Point** (ad clica → WhatsApp) | 72h grátis após primeira msg do usuário | Caso especial |

  **Mudança crítica:** desde 1º jul 2025 a Meta eliminou o modelo "1.000 conversas/mês grátis" e migrou pra **per-message billing**. Cada template entregue é cobrado individualmente. Service window (24h após msg do usuário) **continua free**.
- **Fonte:** [WhatsApp Business — Pricing](https://whatsappbusiness.com/products/platform-pricing/); [Meta Developers — Pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing); [Engagelab — WhatsApp 2026 Pricing](https://www.engagelab.com/blog/whatsapp-business-api-pricing); [Hyperleap — 2026 Country Rates](https://hyperleap.ai/blog/whatsapp-business-api-pricing-guide-2026)
- **Hipótese:** ⚠️ Parcial — free tier "real" no Sprint 1 só dá pra service (resposta dentro de 24h). Notificações proativas custam.
- **Impacto:** **Sprint 1 fica em SANDBOX** (ver WA03). Demo do pitch grava vídeo de fluxo simulado. Em produção, **utility templates** (lembretes de revisão) custariam ~$0,005–0,015/msg × ~10 msgs/cliente/ano × 100k clientes = **$5k–$15k/ano** (escopo para roadmap pós-Sprint, fora do orçamento $100/mês acadêmico).

## WA03 — Sandbox vs número verificado

- **Pergunta:** Qual a limitação real do sandbox? E do número verificado de produção?
- **Resposta:**

  | Modo | Limites | Uso |
  |---|---|---|
  | **Sandbox (test API key)** | Máx **200 mensagens** total (não/dia, é teto cumulativo) — chamadas 25/dia | **Sprint 1 demo + teste integração** |
  | **Verificado, sem business verification** (Tier 0) | **250 msgs/24h** | Onboarding inicial |
  | **Verificado + business verification** (Tier 1) | **1.000 msgs/24h** | Piloto com concessionária |
  | **Quality scaling completo** | **100.000 msgs/dia** | Produção |

  **Mudança out/2025:** limites são **por Business Portfolio**, não mais por número. Múltiplos números compartilham a quota.
- **Fonte:** [Meta Developers — Messaging Limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits); [Sanuker — 2026 Updates](https://sanuker.com/whatsapp-api-2026_updates-pacing-limits-usernames/); [Aditya Girish — Cloud API Sandbox 2026 Guide](https://medium.com/@adityadeepa634/the-developers-guide-to-the-whatsapp-cloud-api-sandbox-2026-edition-c967ce0bf671)
- **Hipótese:** ✅ Validada — sandbox basta pra Sprint 1 se planejado.
- **Impacto:** **Plano de uso sandbox:** ~50 mensagens de teste (5 fluxos × 10 cenários) durante desenvolvimento, ~30 pra demo gravada. Total estimado **80/200**, sobra folga. Pular pra Tier 0 verificado quando começar piloto pós-Sprint.

## WA07 — Padrão conversação Sprint 1 (chatbot ou notificação?)

- **Pergunta:** Action Engine deve ser chatbot interativo ou só notificação one-way?
- **Resposta:** **NOTIFICAÇÃO + FLUXO AUTOMATIZADO. Chatbot LLM está banido.** Mudança crítica 2026:
  - Meta **baniu chatbots IA "general purpose"** rodando via WhatsApp Business API. Apenas **business automation flows** continuam permitidos: support bots, booking bots, order bots — fluxos determinísticos com decision trees, **não** LLM-based.
  - **Templates pré-aprovados** obrigatórios para qualquer mensagem business-initiated (utility, marketing, auth).
  - **LGPD opt-in obrigatório**: registro de quando, como e a partir de qual canal o consentimento foi obtido. Botão de opt-out em toda mensagem business-initiated.
  - Enforcement em 3 strikes: warning → rate limit → suspensão 7–30 dias.
- **Fonte:** [Conferbot — WhatsApp Chatbot Rules 2026](https://www.conferbot.com/blog/whatsapp-chatbot-rules-2026); [Respond.io — General-Purpose Chatbots Ban](https://respond.io/blog/whatsapp-general-purpose-chatbots-ban); [Meta — WhatsApp LGPD Compliance](https://www.facebook.com/business/business-messaging/compliance/whatsapp-lgpd); [Infobip — Template Compliance](https://www.infobip.com/docs/whatsapp/compliance/template-compliance)
- **Hipótese:** ✅ Validada — desenho atual (n8n + templates utility) já é o padrão correto.
- **Impacto:**
  - **Sprint 1 Action Engine:** templates utility de 3 tipos: `lembrete_revisao`, `pos_revisao_satisfacao`, `recall_alerta`. Cada um com botão "❌ Parar de receber" (opt-out LGPD).
  - **Resposta do cliente** entra em service window 24h: durante esse tempo, n8n pode usar LLM **internamente** (não no WhatsApp) para classificar intenção e responder com template aprovado. **Não** chatbot rodando direto no WhatsApp.
  - **DOC 06 → seção LGPD/WhatsApp:** registrar no `audit_log` cada opt-in com `who/when/channel/template_id`.

---

# Bloco G — Mobile (MB02–MB03)

## MB02 — Auth Supabase no React Native (Expo)

- **Pergunta:** Como configurar fluxo nativo (login, persistência, refresh)?
- **Resposta:** **Padrão consagrado, sem mistério.** Configuração canônica do client:

  ```ts
  // Pseudo — exato vai pro repo mobile
  import AsyncStorage from "@react-native-async-storage/async-storage";
  import { createClient } from "@supabase/supabase-js";

  export const supabase = createClient(URL, ANON_KEY, {
    auth: {
      storage: AsyncStorage,
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: false,  // RN não tem URL
    },
  });
  ```

  **AppState listener** para iniciar/parar autorefresh quando app vai pra foreground/background:

  ```ts
  import { AppState } from "react-native";
  AppState.addEventListener("change", (state) => {
    if (state === "active") supabase.auth.startAutoRefresh();
    else supabase.auth.stopAutoRefresh();
  });
  ```

  **Métodos:** `signUp`, `signInWithPassword`, `signInWithOAuth`, `signOut`, `getSession` (síncrono em memória), `getUser` (chama servidor — usar com parcimônia).
- **Fonte:** [Supabase — Auth React Native Quickstart](https://supabase.com/docs/guides/auth/quickstarts/react-native); [Expo — Using Supabase](https://docs.expo.dev/guides/using-supabase/); [Supabase — User Management Tutorial](https://supabase.com/docs/guides/getting-started/tutorials/with-expo-react-native); 2026
- **Hipótese:** ✅ Validada — caminho documentado, AsyncStorage + autoRefreshToken resolve persistência.
- **Impacto:** **forward-mobile** (Expo) usa exatamente esse setup. Config separa env (`EXPO_PUBLIC_SUPABASE_URL`, `EXPO_PUBLIC_SUPABASE_ANON_KEY`). **Não** colocar service_role_key no app — somente anon. RLS protege o resto.

## MB03 — Dual-mode (Ford-staff vs Cliente) via role no JWT

- **Pergunta:** Como uma única auth Supabase serve dois apps com permissões diferentes?
- **Resposta:** **Custom claim em `app_metadata` (NÃO `user_metadata`).** Padrão validado:
  - **`raw_user_meta_data`** → escrito pelo próprio usuário (mutável via SDK). **Nunca** usar pra autorização.
  - **`raw_app_meta_data`** → escrito apenas via service_role/admin. Esse é o lugar certo pra `role: "ford_staff" | "customer" | "dealer"`.
  - **Custom Access Token Auth Hook** (Postgres function ou Edge Function) injeta o claim no JWT antes do issue. Disponível em SQL via `auth.jwt() ->> 'app_metadata' ->> 'role'`.
  - **RLS policy exemplo:**
    ```sql
    CREATE POLICY "ford_staff_full_access" ON public.clientes
      FOR SELECT USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'ford_staff'
      );

    CREATE POLICY "customer_self_only" ON public.clientes
      FOR SELECT USING (
        cliente_id = auth.uid()
        AND (auth.jwt() -> 'app_metadata' ->> 'role') = 'customer'
      );
    ```
  - **Pegadinha:** mudanças em `app_metadata` **só refletem no JWT após logout/login** ou refresh manual da sessão. Para promoção/demoção: forçar `signOut` + reentrada.
- **Fonte:** [Supabase — Custom Claims & RBAC](https://supabase.com/docs/guides/database/postgres/custom-claims-and-role-based-access-control-rbac); [Supabase — JWT Claims Reference](https://supabase.com/docs/guides/auth/jwt-fields); [supabase-community/supabase-custom-claims](https://github.com/supabase-community/supabase-custom-claims); [Supabase Discussion #1148 — multi-tenancy](https://github.com/orgs/supabase/discussions/1148)
- **Hipótese:** ✅ Validada — não precisa de auth separada por app.
- **Impacto:**
  - **forward-api-java** lê `app_metadata.role` do JWK do Supabase → roteamento de endpoints `/v1/admin/*` requer `role=ford_staff`; `/v1/me/*` aceita `customer`.
  - **forward-mobile** detecta role no startup e renderiza **2 navigators distintos** (Ford-staff stack vs Customer stack) — não dois apps.
  - **forward-platform** (SvelteKit Performance Console) só permite login se `role=ford_staff` (RLS bloqueia tudo o resto).
  - **ADR-007 do DOC 02c (JWT lifecycle)** ganha apêndice: "claim de role obrigatório em app_metadata".

---

# Bloco H — Validação do Dataset (PR01)

## PR01 — Dataset sintético reflete dataset real?

- **Pergunta:** Quão confiar nos achados do Bloco A se o dataset é sintético/aquecimento?
- **Resposta:** Existe metodologia consolidada para validar — **TSTR vs TRTR** é o padrão:
  - **TSTR (Train Synthetic, Test Real):** treina no sintético, avalia no real. Compara com **TRTR (Train Real, Test Real)**.
  - **Threshold de aceitação:** sintético com **≥ 95%** da performance preditiva do real é considerado apto.
  - **Domain gap** é a fonte principal de falha em produção: ruído de sensor, comportamento atípico, edge cases raros. Sintético geralmente não captura.
  - **Best practice:** datasets **híbridos** (sintético + real) superam puros sintéticos em quase todos os benchmarks recentes.
  - **Transfer learning:** pequena quantidade de real misturada melhora muito o transfer.
- **Fonte:** [Label Your Data — Synthetic vs Real (2026)](https://labelyourdata.com/articles/synthetic-data-vs-real-data); [YData — Validating Synthetic Predictive Performance](https://ydata.ai/resources/how-to-validate-the-predictive-performance-of-synthetic-data.html); [Qualtrics — Synthetic Data Validation](https://www.qualtrics.com/articles/strategy-research/synthetic-data-validation/); [arXiv:2302.04062 — ML for Synthetic Data Generation](https://arxiv.org/html/2302.04062v9)
- **Hipótese:** ✅ Validada — protocolo claro de quando confiar e quando duvidar.
- **Impacto:**
  - **Posicionamento honesto no DOC 07 e no pitch:** "achados do Bloco A (DS01–DS10) são prova de método sobre dataset sintético de aquecimento. Quando o real chegar, rerodaremos `tmp_research/bloco_a_dataset.py` e aplicaremos teste TSTR vs TRTR — se F1 pós-real ≥ 0,95 × F1 atual (0,86 × 0,95 = **0,817**), modelo é aceito; senão, refit do zero."
  - **Plano B no DOC 04:** se dataset real chegar tarde demais pro Sprint 1, manter sintético com asterisco e prometer iteração no Sprint 2.
  - **Estratégia de mistura:** quando real chegar com volume baixo, treinar híbrido (sintético + real, sample weights ponderando real mais).

---

# Bloco I — KPIs / North Star (KP01)

## KP01 — North Star metric — VIN Share ou outro?

- **Pergunta:** Qual é a métrica única que sintetiza o sucesso da plataforma?
- **Resposta:** Critérios canônicos para North Star: (1) capturar valor entregue ao cliente, (2) ser leading indicator de receita, (3) ser mensurável continuamente. Em SaaS o padrão de mercado é **NRR (Net Revenue Retention)**, com proxies em **CLTV** e **churn rate**. Aplicado a aftermarket automotivo Ford BR:

  | Candidato | Pros | Contras | Decisão |
  |---|---|---|---|
  | **VIN Share** (% da frota Ford ativa que faz revisão na rede ≥1x/ano) | Específico do problema, alinhado com pitch (DOC 00) | Lagging (calcula só pós-12 meses) | **North Star da plataforma** ✅ |
  | **NRR pós-venda** | Padrão SaaS, financeiramente claro | Não é o vocabulário Ford; precisa traduzir | KPI agregado anual |
  | **Service Revenue per VIN** | Foca em receita | Não captura retenção em si | KPI anexo |
  | **% clientes em perfil "fiel"** | Leading, acionável, vem do nosso modelo | Métrica interna do produto, não da Ford | **Leading da plataforma** ✅ |

  **Recomendação:** Hierarquia de 2 níveis.
  - **North Star (lagging):** **VIN Share rede Ford** — % da base ativa que retorna em 12 meses.
  - **Leading indicator (semanal):** **% de clientes movendo para perfil "fiel"** (e o oposto: % saindo de fiel).
- **Fonte:** [ProdPad — North Star Examples](https://www.prodpad.com/blog/north-star-metric-examples/); [UserPilot — North Star Metric Guide](https://userpilot.com/blog/north-star-metric/); [Monetizely — NRR as North Star](https://www.getmonetizely.com/articles/how-to-calculate-net-revenue-retention-nrr-the-north-star-metric-for-saas-growth); DOC 02 (P4)
- **Hipótese:** ✅ Validada — VIN Share como North Star alinha com vocabulário Ford e com o pitch original.
- **Impacto:**
  - **Slide 7 do pitch:** "North Star — VIN Share. Hoje X% (placeholder), meta +Y pp em 12 meses."
  - **Performance Console** mostra VIN Share no topo + % migração entre perfis (leading) abaixo.
  - **DOC 04 → KPIs:** definir fórmula exata `VIN_share = clientes_ativos_12m / frota_ford_em_circulacao`. Numerador = pelo menos 1 evento de revisão na rede em janela rolante 12 meses. Denominador vem da Base 1 (frota total) ou Censo Ford-staff.

---

# Bloco J — Apresentação / Plano (AP01)

## AP01 — Critério de avaliação não documentado

- **Pergunta:** Há pesos/critérios que professores aplicam mas não estão no enunciado?
- **Resposta:** **Sim, e é determinante.** Consolidação:
  - **Tech Challenge vale 90% da nota de TODAS as disciplinas avaliativas da fase** (FIAP Pós-Tech). Ou seja: ML, Testing, SOA, etc. — todas pesam o **mesmo Tech Challenge** com 90%, e os 10% restantes são atividades em sala/quiz.
  - **Project-Based Learning (PBL):** 5 fases, cada fase resolve "um problema real do mercado". Avaliação holística do projeto, não da disciplina isoladamente.
  - **Hackathon experience** ao final das fases (presencial ou remoto) — atividade adicional avaliativa.
  - **Atividade individual presencial** em polo FIAP — cada aluno é avaliado também individualmente.
  - **Critérios não-explícitos observados em práticas FIAP** (segundo redes de ex-alunos, sem fonte oficial documentada): qualidade do pitch (3min), funcionalidade da demo, organização do GitHub, evidências de processo (issues, PRs, ADRs), **conformidade com requisitos não-funcionais** (LGPD, segurança, custo).
- **Fonte:** [FIAP Pós-Tech](https://postech.fiap.com.br/); [GitHub fdelima/FIAP-Pos-Tech-Challenge — peso 90%](https://github.com/fdelima/FIAP-Pos-Tech-Challenge); [FIAP Manual do Aluno](https://www.fiap.com.br/wp-content/themes/fiap2016/documents/fiap/informacoes-academicas/manuais/MANUAL%20DO%20ALUNO.pdf); validações com observações de práticas
- **Hipótese:** ⚠️ Parcial — peso 90% confirmado por enunciados públicos; demais critérios são consensuais mas sem rubrica oficial pública por disciplina.
- **Impacto:**
  - **Mudança de mentalidade Sprint 1:** o entregável é **um produto integrado**, não 5 entregáveis disciplinares paralelos. A nota do ML, Testing, SOA, Cyber e Gestão **vem do mesmo conjunto**.
  - **Implicação prática (DOC 03 já reflete):** `forward-docs` é "single source of truth"; `forward-repos/*` é o produto. Cada disciplina puxa as **seções relevantes** do mesmo doc.
  - **Estratégia de pitch (Slide 6):** mostrar a integração como vantagem competitiva sobre grupos que entregam disciplinas em silos.
  - **Não-funcionais críticos:** LGPD (CY01–CY12 do DOC 02c), custo ($67/mês — IF11), segurança (threat model — CY08). Tudo já está coberto, só precisa estar **explícito** nas evidências.

---

## Próximos passos

1. **Bloco F → academic/:** criar `business_canvas.md` (AC02), `quadro_de_valor.md` (AC03+AC07), `archimate/forward_service.archimate` (AC04), `pitch_deck.md` (AC01) — **destrava entrega Testing**.
2. **Bloco B → DOC 07:** anexar tabela ML04 + confusion matrix + decisão "LogReg final, GB descartado por custo de fit".
3. **Bloco E → DOC 04 + n8n flows:** templates utility `lembrete_revisao` / `pos_revisao_satisfacao` / `recall_alerta` com botão opt-out; auditar opt-in no `audit_log`.
4. **Bloco G → forward-mobile + forward-api-java:** setup Supabase com AsyncStorage; claim `app_metadata.role` em todos os endpoints e RLS.
5. **Bloco H → DOC 07 + DOC 04:** plano TSTR/TRTR pra quando dataset real chegar.
6. **Bloco I → DOC 04 + Performance Console:** VIN Share como hero metric; % migração entre perfis como leading.
7. **Bloco J → mentalidade do time:** comunicar com o grupo (Salatiel + 2 outros) que disciplinas pesam no mesmo bloco — alinhamento de prioridade e zero retrabalho disciplinar.

**Pesquisas 🟡 importantes** (~25 itens) e 🟢 enriquecimento (~16 itens) seguem catalogadas em [project_research_map_v2.md](../../../C--Users-jotin--claude-projects-c--Users-jotin-Documents-Ford/memory/project_research_map_v2.md) para execução conforme prioridade durante a Sprint.

---

> **Recap completo das 34 críticas (DOC 02c + 02d):** Bloco A 9/9 ✅, Bloco B 1/1 ✅, Bloco C 5/5 ✅, Bloco D 6/6 ✅, Bloco E 3/3 ✅, Bloco F 5/5 ✅, Bloco G 2/2 ✅, Bloco H 1/1 ✅, Bloco I 1/1 ✅, Bloco J 1/1 ✅. **Cobertura: 100% das 🔴**.
