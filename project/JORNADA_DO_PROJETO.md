# Jornada do Projeto — ForwardService

![status](https://img.shields.io/badge/status-em_construção-yellow?style=flat-square)
![início](https://img.shields.io/badge/início-09%2F04%2F2026-blue?style=flat-square)

> Como a ForwardService foi concebida, pesquisada, validada e projetada — do PDF da Ford até a primeira linha de código.  
> Este documento registra as decisões, os pivôs e o raciocínio por trás de cada etapa.

---

## Contexto

Este projeto nasceu dentro do **Challenge FIAP 2026**, uma atividade anual onde uma empresa parceira expõe suas dores reais e desafia estudantes de Engenharia de Software a desenvolverem soluções. A empresa deste ano: **Ford Motor Company**.

O Challenge tem duas dimensões que coexistem:
- **Entregas por disciplina** — cada matéria exige um entregável específico com rubrica própria
- **Produto livre** — uma solução construída sem restrições de formato, com foco em resolver o problema de verdade

A premissa desde o início: **inovar é valioso, mas resolver o problema de forma concreta é prioridade**. Não queríamos um PowerPoint bonito. Queríamos algo que funcione.

---

## Capítulo 1 — Entendendo a Ford

### O ponto de partida

Tudo começou com o PDF oficial do Challenge: *"Ford FIAP 2026: Kick-off do Projeto"*. A primeira decisão foi **não sair construindo nada** antes de entender profundamente o que a Ford estava pedindo.

O PDF apresentava dois desafios:

| Desafio | Tema |
|---|---|
| **Desafio 01** | Inteligência Competitiva Automotiva — ferramenta para comparar specs de veículos concorrentes (validação: Ranger Raptor vs. Hilux, Amarok, etc.) |
| **Desafio 02** | VIN Share na América do Sul — reter clientes no pós-venda, aumentar a porcentagem de veículos Ford que usam a rede oficial para manutenção |

A primeira ação foi fazer uma **leitura exaustiva do PDF**, mapeando cada exigência, cada rubrica, cada critério de avaliação. O resultado foi o documento `challenge_ford_2026_analise.md` — um consolidado de tudo que o PDF continha, organizado por desafio, por disciplina e por critério de avaliação.

### A escolha do desafio

A decisão entre Desafio 01 e 02 não foi imediata. Houve debate.

O Desafio 01 (inteligência competitiva) era mais simples de demonstrar — entrada de dados, saída padronizada, validação clara com a Ranger Raptor. Mas tinha um problema: **a disciplina de IA/ML estava 100% alinhada ao Desafio 02** (segmentação e classificação de clientes para retenção). Se escolhêssemos o Desafio 01, o trabalho de IA/ML ficaria desconectado do restante.

O Desafio 02 (VIN Share / retenção pós-venda) tinha maior complexidade mas **todas as disciplinas convergiam naturalmente**: a API serviria dados de clientes e serviços, o app mobile seria a interface do concessionário, a segurança protegeria dados sensíveis de clientes, e o ML faria a segmentação e predição. Era um ecossistema coerente.

**Decisão: Desafio 02.** A convergência entre disciplinas era o fator decisivo. Menos retrabalho, mais coerência, produto mais forte.

---

## Capítulo 2 — Pesquisa antes de solução

### A recusa de começar pela tecnologia

A tentação natural era pular direto para "vamos fazer um dashboard com ML". Mas a decisão consciente foi **pesquisar primeiro**. Não dá para resolver um problema que não se entende profundamente.

Antes de propor qualquer solução, fizemos uma pesquisa de mercado abrangente cobrindo:
- O que é VIN Share e como é medido na indústria
- A situação específica da Ford Brasil (fechamento das fábricas em 2021, frota de 12,4M de veículos, 80% descontinuados, 109→145 concessionárias)
- Por que clientes abandonam a rede oficial (preço percebido, fim da garantia, inconveniência)
- Tendências globais em retenção pós-venda (veículos conectados, CRM preditivo, programas de fidelidade)
- Técnicas de segmentação e predição de churn no setor automotivo

Essa pesquisa inicial revelou o primeiro grande insight: **a Ford Brasil tem um problema que nenhuma outra montadora no mundo tem na mesma escala** — 80% da sua frota é de modelos que ela não fabrica mais (Ka, Fiesta, EcoSport), atendida por uma rede drasticamente menor que a dos concorrentes.

### A formalização do processo

Percebendo que o projeto tinha potencial para ser algo real (não apenas acadêmico), a decisão foi **formalizar um processo de trabalho**. Não por burocracia, mas para evitar que ideias boas se perdessem e para garantir que cada decisão fosse rastreável.

O processo definido:

```
Fase 1: Fundação (DOC 00)     → O que estamos resolvendo e por quê
Fase 2: Pesquisa (DOC 01+02)  → O que precisamos saber e o que descobrimos
Fase 3: Solution Design (DOC 03) → O que vamos construir e como
Fase 4: Arquitetura (DOC 04)  → Contratos técnicos e infraestrutura
Fase 5: Implementação (DOC 05) → Quem faz o quê e quando
Fase 6: Entrega               → Código, app, apresentação
```

A regra fundamental: **nenhuma fase posterior pode contradizer uma anterior sem revisão explícita**. Isso evita que decisões de implementação contaminem a visão estratégica.

---

## Capítulo 3 — A Base Fundacional

### Construindo a tese

A Base Fundacional (DOC 00) foi o primeiro documento formal. Não era sobre tecnologia — era sobre **o problema e a lógica de como resolvê-lo**.

A tese central emergiu da pesquisa:

> *ForwardService não é uma ferramenta. É uma estratégia de retenção pós-venda habilitada por tecnologia, desenhada especificamente para o contexto único da Ford Brasil pós-fechamento das fábricas.*

A palavra "estratégia" era intencional. A Ford não precisa de mais um dashboard. Precisa de uma forma de pensar sobre retenção que reconheça sua realidade única.

### Os 4 pilares

A solução foi estruturada em 4 pilares, cada um respondendo uma pergunta de negócio:

| Pilar | Pergunta |
|---|---|
| **Intelligence Hub** | Quem estou perdendo, por quê, onde e quando? |
| **Action Engine** | O que fazer com cada cliente, automaticamente? |
| **Experience Layer** | Como garantir que o cliente queira voltar? |
| **Performance Console** | Funcionou? Quanto retornou? O que otimizar? |

Essa estrutura não foi escolhida por ser bonita. Foi escolhida porque **cada pilar se sustenta sozinho**, mas juntos formam um ciclo: dados → inteligência → ação → experiência → medição → dados melhores (Flywheel).

### As 9 lógicas de negócio

O verdadeiro diferencial da proposta não está nos pilares — está nas **lógicas de negócio embutidas**. São 9 conceitos que tornam a ForwardService impossível de replicar com um CRM genérico:

1. **Economia do VIN (LSV)** — cada cliente tem valor em reais calculável
2. **Curva da Morte** — existe um momento exato onde a retenção desaba, e é diferente para cada perfil
3. **Rede Invertida** — 145 dealers não cobrem o Brasil; o serviço precisa ir até o cliente
4. **Recall como Porta de Entrada** — 3,4M de recalls pendentes são oportunidades de reconexão
5. **Índice de Saúde da Concessionária** — um score único (0-100) que resume a performance de cada dealer
6. **Segmentação da Frota Descontinuada** — 80% da frota não pode ser tratada como massa uniforme
7. **Closed-Loop ROI** — cada ação rastreada até o resultado financeiro
8. **Flywheel de Dados** — a plataforma fica mais inteligente com o uso
9. **Ponte Serviço-Venda** — retenção no pós-venda gera vendas futuras

Cada lógica nasceu de uma pergunta: "o que a Ford precisa que nenhuma solução de prateleira oferece?"

### A análise crítica

Após a primeira versão da Base Fundacional, a decisão foi **questioná-la antes de validá-la**. A pergunta: "se eu fosse a Ford, isso me convenceria?"

A análise revelou problemas:
- Alguns módulos eram genéricos demais (Customer Vista 360 é o que todo CRM faz)
- O programa de fidelidade (FordRewards) propunha pontos, mas nenhuma montadora no Brasil usa pontos
- A proposta não endereçava diretamente o elefante na sala: 80% da frota é de modelos descontinuados

Essas críticas levaram à reestruturação de 9 módulos para 4 pilares e à decisão de que **as lógicas de negócio, não a tecnologia, seriam o diferencial**.

---

## Capítulo 4 — A Fase de Pesquisa

### O mapa de pesquisa

Antes de pesquisar, mapeamos **exatamente o que precisávamos descobrir**. O DOC 01 (Mapa de Pesquisa) listou 30 perguntas organizadas por pilar e lógica de negócio, cada uma com:
- A hipótese a validar
- Onde buscar
- O critério de sucesso (quando a pergunta está respondida)
- A prioridade (crítica, importante ou enriquecimento)

Isso evitou pesquisa sem foco. Cada busca tinha objetivo claro.

### 30 pesquisas, 0 invalidadas

As 30 pesquisas foram executadas em paralelo, organizadas em 6 blocos temáticos:

| Bloco | Foco | Pesquisas |
|---|---|---|
| 1 | Métricas fundamentais e KPIs | VIN Share, KPIs da indústria, Curva da Morte, correlação serviço-recompra |
| 2 | Dados e ML | Técnicas de segmentação, features de churn, estimativa de km, fontes de VIO |
| 3 | Operações de dealer | DMS, recalls, manutenção Ford, cobertura geográfica, margens |
| 4 | Comunicação e estratégias | Canais no Brasil, WhatsApp API, estratégias com ROI, custo de aquisição |
| 5 | Experiência e fidelidade | Jornada Ford atual, programas de fidelidade, Service as Product, apps automotivos |
| 6 | Lógicas de negócio | Ciclo de vida, oficinas parceiras, recalls no Brasil, benchmarking, flywheel |

**Resultado:** 27 hipóteses validadas, 2 parcialmente validadas, 0 invalidadas. A base estava sólida.

### Os dados que mudaram tudo

Algumas descobertas foram esperadas. Outras mudaram a direção do projeto:

**"A Ford é a única grande montadora sem programa de fidelidade no Brasil."**
Renault, Hyundai, Toyota, VW, Fiat, BMW, Mercedes — todas têm planos de manutenção pré-pagos. A Ford não tem nenhum. Essa descoberta matou o conceito original de "FordRewards" (programa de pontos) e deu origem ao **Ford Care** — plano pré-pago com preço fixo, alinhado com o que o mercado inteiro já faz.

**"Retenção cai de 78% para 20% ao fim da garantia — e a crise está acelerando."**
Dados do Cox Automotive (2025) mostraram que a retenção caiu de 72% para 54% em apenas 2 anos, mesmo para veículos novos. Isso não é um problema antigo se estabilizando — é uma crise em aceleração. A urgência da proposta ficou muito mais clara.

**"A Stellantis comprou a DPaschoal por R$ 2,6 bilhões."**
Uma montadora literalmente comprou uma rede de oficinas independentes (900 centros) para resolver exatamente o mesmo problema de cobertura pós-venda que a Ford tem. Isso transformou a LN3 (Rede Invertida) de "ideia interessante" para "componente central com precedente de mercado".

**"Preço da concessionária é MENOR que da oficina independente."**
Cox Automotive revelou que dealers cobram $261 em média vs. $275 das independentes. O problema não é preço — é percepção. Isso validou o componente "Transparência de Valor" no Experience Layer.

### As 3 adaptações pós-pesquisa

A pesquisa não só validou — corrigiu. Três mudanças foram aplicadas à Base Fundacional:

| Adaptação | Antes | Depois | Evidência |
|---|---|---|---|
| FordRewards → **Ford Care** | Programa de pontos | Planos pré-pagos com preço fixo | Nenhuma montadora no BR usa pontos. Pré-pago: retenção 3x |
| + **Fluxo Simplificado** | App só para modelos conectados | Adiciona experiência digital para modelos sem telemetria | 80% da frota sem conectividade. 2,5M+ excluídos digitalmente |
| LN3 elevada a **central** | Rede Invertida como recomendação | Componente central com mapeamento de desertos | Stellantis+DPaschoal prova viabilidade (R$ 2,6bi) |

---

## Capítulo 5 — Do conceito ao produto

### O questionário de contexto

Antes de desenhar o produto, havia uma lacuna: **o projeto estava bem pensado como conceito de negócio, mas não como produto de software**. Faltava entender:
- Quem vai construir (perfil técnico, tempo disponível)
- Com que ferramentas (stack, infra, budget)
- Em quanto tempo (cronograma realista)
- Com que prioridade (nota acadêmica vs. produto real)

Um questionário de 80 perguntas foi elaborado cobrindo: perfil do desenvolvedor, grupo, contexto FIAP, visão do produto, stack técnica, cronograma e forma de trabalho.

As respostas revelaram o perfil real do projeto:
- **Desenvolvedor principal:** profissional de frontend (Svelte + Go), trabalhando no Cubo do Itaú
- **Abordagem:** vibecoder estratégico — planeja e discute arquitetura antes de codar, usa IA como acelerador
- **Prioridade:** produto que funciona > nota acadêmica
- **Time:** 4 integrantes, mas o core técnico é construído pelo líder; grupo contribui depois via PRs
- **Budget:** R$ 60/mês + R$ 100 em créditos Azure

### A análise dos repos profissionais

Um passo não convencional: analisar os repositórios da empresa onde o desenvolvedor trabalha (g-bra) para entender padrões reais de organização, CI/CD e qualidade de código. Isso revelou:
- Naming convention: `{produto}-{tipo}` (onp-web, onp-api, onp-infra)
- Go API com layers claras: Handler → Service → Repository
- Design system próprio em Svelte com ~48 componentes
- CLAUDE.md em cada repo com regras explícitas
- CI rigoroso: lint + test + security scan + Docker + GitOps

A ForwardService foi projetada para seguir esses mesmos padrões — familiar para o desenvolvedor, não alienígena.

### O Solution Design

O DOC 03 traduziu todo o trabalho anterior em decisões concretas de produto.

**A decisão de arquitetura mais importante:** Supabase-first. Em vez de construir um backend monolítico, o Supabase faz 80% do trabalho (CRUD, auth, realtime). O Go API existe só para integrações externas (WhatsApp, webhooks). O Python existe só para ML. Menos código = menos bugs = mais velocidade para um desenvolvedor solo.

**A stack:** SvelteKit (web) + Expo (mobile) + Go (API) + Python (ML) + Supabase (banco + auth + realtime). Cada tecnologia escolhida com base no que o desenvolvedor domina profissionalmente, não no que está na moda.

**O MVP:** corte cirúrgico. Vista 360, Radar de Churn, Service Share Map, Pulse Leads, WhatsApp básico, Dashboard de ROI. Tudo que demonstra valor. Nada cosmético. Features como Recall Gateway completo, Strategy Simulator e gamificação entre dealers ficam para v2.

**A separação produto vs. acadêmico:** o produto é a prioridade. As entregas acadêmicas são subprodutos do produto — o notebook de ML sai do forward-ml, a documentação de API sai do forward-api, o pitch sai do forward-docs. Produto primeiro, disciplinas depois.

---

## Capítulo 6 — A infraestrutura

### GitHub Organization

A decisão por multi-repo (em vez de monorepo) veio do padrão profissional: cada serviço em repo separado facilita CI/CD independente, permissões granulares e delegação de tarefas.

A org **fwd-ford** foi criada com 6 repositórios:

| Repo | Stack | Responsabilidade |
|---|---|---|
| `forward-web` | SvelteKit | Dashboard web |
| `forward-mobile` | React Native / Expo | App mobile |
| `forward-api` | Go | Integrações externas |
| `forward-ml` | Python | ML service |
| `forward-infra` | SQL / Docker | Supabase config |
| `forward-docs` | Markdown | Documentação |

Cada repo foi inicializado com:
- **README.md** — descrição, stack, estrutura, repos relacionados
- **CLAUDE.md** — regras de linguagem, patterns obrigatórios, arquitetura de layers
- **.env.example** — template de variáveis de ambiente
- **Makefile** (onde aplicável) — targets padronizados
- Estrutura de pastas seguindo o padrão da g-bra

### As regras de trabalho

Definidas explicitamente para evitar ambiguidade:
- Código em inglês. Comentários bilíngues. i18n desde o início.
- Qualidade sobre velocidade — se a melhor solução demora mais, que demore.
- Design direto no código, sem fase de Figma separada.
- Branch strategy: trunk-based com feature branches, PRs para main.
- Delegação para o grupo via issues com descrição precisa.

---

## Capítulo 7 — O que vem a seguir

Com a base completa (DOC 00-03), a pesquisa validada (30/30), a stack definida e os repos criados, o projeto está na transição de **planejamento para execução**.

Os próximos marcos:

| Marco | O que entrega |
|---|---|
| **Schema + Seed** | Banco de dados no Supabase com dados sintéticos realistas |
| **Notebook ML** | Segmentação + Classificação com dados do professor |
| **Dashboard v1** | Service Share Map + Vista 360 + Pulse Leads no SvelteKit |
| **App mobile v1** | Telas básicas de leads e Vista 360 no Expo |
| **Sprint 1 (24/05)** | Esboço demonstrável + entregas acadêmicas |
| **MVP completo** | Produto funcional com WhatsApp, scores, dashboards |
| **Banca final (outubro)** | Apresentação para professores e representantes da Ford |

---

## Lições até aqui

**1. Pesquisar antes de construir não é perder tempo — é economizar tempo.**
As 30 pesquisas evitaram pelo menos 3 decisões erradas (pontos em vez de pré-pago, ignorar frota descontinuada, tratar Rede Invertida como secundária).

**2. Questionar a própria proposta é mais valioso que defendê-la.**
A análise crítica da primeira versão revelou módulos genéricos, gaps de contexto e um programa de fidelidade que ninguém no mercado usa. Sem essa autocrítica, a proposta seria medíocre.

**3. O diferencial está na lógica de negócio, não na tecnologia.**
XGBoost, SvelteKit, Supabase — qualquer grupo pode usar. Mas a Economia do VIN, a Curva da Morte e a Segmentação da Frota Descontinuada são lógicas que só existem porque alguém entendeu profundamente o problema da Ford Brasil. Isso não se copia.

**4. Adaptar o processo ao contexto real, não ao contexto ideal.**
O processo de trabalho foi desenhado para um vibecoder solo com 10-12h/semana e R$ 60/mês de budget. Não para um time de 10 engenheiros com infra própria. Supabase-first não é a arquitetura "ideal" — é a arquitetura que permite entregar um MVP real com os recursos disponíveis.

**5. Produto primeiro, disciplinas depois.**
As entregas acadêmicas são importantes, mas são subprodutos do produto. Quando o produto é bom, as entregas de disciplina saem naturalmente. Quando o produto é fraco, nenhuma formatação de slide salva.

---

> *Este documento será atualizado conforme o projeto avança. Cada capítulo novo registra não apenas o que foi feito, mas por que foi feito dessa forma.*
