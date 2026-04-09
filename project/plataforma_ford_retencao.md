# FordConnect Pro - Plataforma All-in-One de Retencao Pos-Venda

> Proposta de solucao integrada para o Challenge Ford x FIAP 2026
> 9 modulos independentes, 1 plataforma unificada

---

## A Tese Central

A Ford perde clientes no pos-venda porque opera de forma **reativa**: espera o cliente aparecer.
A proposta e inverter essa logica para um modelo **proativo e inteligente**: a plataforma sabe quem precisa de servico, quando, por que, e qual a melhor forma de trazer esse cliente de volta.

**Nome da plataforma:** ForwardService (sugestao - combina "Ford" + "Forward" + "Service", transmite proatividade)

> Nomes alternativos para discutir: FordPulse, RetainFord, FordConnect Pro, ServiceIQ

---

## Visao da Plataforma

```
┌─────────────────────────────────────────────────────────────┐
│                    FORWARDSERVICE                            │
│                Plataforma All-in-One                         │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│  CAMADA  │  CAMADA  │  CAMADA  │  CAMADA  │    CAMADA      │
│  DADOS   │  INTEL.  │  ACAO    │  CLIENTE │    GESTAO      │
├──────────┼──────────┼──────────┼──────────┼────────────────┤
│ M1-Vista │ M2-Radar │ M4-Pulse │ M7-MyFord│ M8-Benchmark  │
│   360    │  Churn   │  Leads   │   App    │   Dealer       │
│          │          │          │          │                │
│ M3-Share │ M9-Simul │ M5-Comm  │ M7-Loyal │ M6-Journey    │
│   Map    │  ador    │  Engine  │  ty      │   Optimizer    │
└──────────┴──────────┴──────────┴──────────┴────────────────┘
```

---

## Os 9 Modulos

---

### MODULO 1 - Customer Vista 360

**O que e:** Perfil unificado de cada cliente/veiculo, consolidando TODOS os dados disponiveis numa unica tela.

**Problema que resolve:** Hoje, as informacoes do cliente estao espalhadas em sistemas diferentes (DMS, CRM, historico de servico, garantia, dados do veiculo conectado). O atendente da concessionaria nao tem visao completa. Quando um cliente liga, ninguem sabe o historico dele sem procurar em 3 sistemas.

**O que mostra para cada cliente:**
- Dados do veiculo: modelo, ano, VIN, km estimada, cor, versao
- Historico completo de servicos na rede (datas, tipos, valores, concessionaria)
- Status de garantia (ativa, expirada, estendida, quando expira)
- Recalls pendentes
- Score de risco de churn (vem do Modulo 2)
- Perfil comportamental/segmento (vem do trabalho de IA/ML - ex: "cliente economico")
- Ultima interacao e canal preferido
- Proxima manutencao prevista
- Lifetime Value estimado

**Como vender pra Ford:**
> "Imagine se, quando um cliente liga para a concessionaria, o atendente ja sabe: esse e um cliente de alto valor, esta fora da garantia ha 6 meses, nao faz revisao ha 14 meses, e sensivel a preco, e o modelo dele tem um recall pendente. Em 3 segundos, ele sabe exatamente como conduzir a conversa."

**Valor de negocio:** Atendimento personalizado aumenta conversao de agendamento em ate 35% (benchmark industria). Reduz tempo de atendimento. Elimina a sensacao de "a Ford nao me conhece".

**Entregavel tecnico:** API REST que consolida dados de multiplas fontes + tela de perfil no app mobile + tela web para o atendente.

---

### MODULO 2 - Radar de Churn (Motor Preditivo)

**O que e:** Modelo de Machine Learning que atribui a cada cliente/veiculo um **score de risco de abandono** (0-100) e classifica em perfis comportamentais.

**Problema que resolve:** A concessionaria nao sabe QUEM esta prestes a sair da rede. Age de forma generica (manda a mesma comunicacao pra todo mundo) ou so percebe que perdeu o cliente quando ja e tarde demais.

**Como funciona:**
1. **Segmentacao comportamental** (aprendizado nao-supervisionado - Base 1)
   - Clustering para identificar perfis reais: fiel, abandono, esquecido, economico (ou os que os dados revelarem)
   - Cada perfil tem comportamento e motivacoes distintas
   
2. **Classificacao preditiva** (aprendizado supervisionado - Base 2)
   - Dado um cliente novo (momento da compra), prever a qual perfil ele pertence
   - Features: modelo, versao, forma de pagamento, regiao, concessionaria, faixa etaria
   
3. **Score de risco dinamico**
   - Combina o perfil previsto com comportamento real observado ao longo do tempo
   - Score atualizado mensalmente: quanto maior, mais urgente a acao

**Output para outros modulos:**
- Score de risco (0-100) alimenta o Modulo 4 (Leads) e Modulo 5 (Comunicacao)
- Perfil comportamental alimenta o Modulo 1 (Vista 360) e Modulo 5 (tom da mensagem)
- Analise agregada alimenta o Modulo 3 (Dashboard) e Modulo 9 (Simulador)

**Como vender pra Ford:**
> "Hoje a Ford descobre que perdeu um cliente quando ele simplesmente para de aparecer. Com o Radar de Churn, a concessionaria sabe 3 meses antes que o cliente vai sair - e tem tempo de agir. E mais: desde o dia da compra, ja sabemos o perfil provavel desse cliente e qual estrategia usar com ele."

**Valor de negocio:** Modelos de churn tipicamente geram lift de 2-4x na eficacia de campanhas de retencao. Cada ponto percentual de VIN Share recuperado em uma frota de 12,4M de veiculos representa dezenas de milhares de servicos adicionais.

**Entregavel tecnico:** Jupyter Notebook com analise completa + modelo deployado como API + integracao com demais modulos.

**Alinhamento direto:** Este modulo E a entrega de IA/ML da disciplina. Dois coelhos com uma cajadada.

---

### MODULO 3 - Service Share Map (Dashboard Analitico)

**O que e:** Dashboard interativo que visualiza o VIN Share em todas as granularidades relevantes, permitindo que gestores da Ford e gerentes de concessionarias entendam ONDE e POR QUE estao perdendo clientes.

**Problema que resolve:** O VIN Share hoje e um numero agregado. Ninguem sabe se o problema esta em veiculos velhos, numa regiao especifica, num tipo de servico, ou numa concessionaria com mau atendimento. Sem granularidade, nao ha acao direcionada.

**Visualizacoes principais:**

1. **Curva de Retencao por Idade do Veiculo**
   - Grafico de linha: VIN Share (%) vs idade (0-15 anos)
   - Mostra exatamente onde a queda se acelera (tipicamente no fim da garantia)
   - Filtros: por modelo, regiao, concessionaria

2. **Mapa Geografico de Calor**
   - Mapa do Brasil com VIN Share por estado/cidade/CEP
   - Identifica "desertos" onde nao ha concessionaria perto e o VIN Share despenca
   - Overlay com localizacao das 109 concessionarias

3. **Ranking de Concessionarias**
   - Tabela comparativa: quais dealers retem melhor, quais perdem mais
   - Drill-down para entender o que o top performer faz de diferente

4. **Decomposicao do VIO (Vehicles in Operation)**
   - Treemap: composicao do parque Ford por modelo/ano
   - Mostra que a maioria sao Ka, Fiesta, EcoSport (descontinuados) - e qual o VIN Share de cada fatia

5. **Funil de Perda**
   - Waterfall: de onde vem as perdas (por tipo de servico, faixa etaria, motivo estimado)
   - Responde: "estamos perdendo mais em revisoes programadas ou em reparos?"

6. **Trend Mensal com Meta**
   - Evolucao temporal do VIN Share vs meta definida
   - Correlacao com acoes executadas (campanhas, promocoes)

7. **Cohort Analysis**
   - Acompanhar grupos de clientes ao longo do tempo (ex: "todos que compraram Ranger em 2024")

**Como vender pra Ford:**
> "Voces sabem o VIN Share nacional. Mas sabem qual concessionaria esta perdendo mais clientes de Ranger com 3-5 anos no interior de SP? Com o Service Share Map, voces veem o problema em alta definicao - e cada problema visivel e um problema que pode ser resolvido."

**Valor de negocio:** Visibilidade granular permite acoes cirurgicas em vez de campanhas genericas. Concessionarias bottom-performer podem aprender com as top-performer. Gestores regionais ganham ferramenta de gestao real.

**Entregavel tecnico:** Dashboard web (React ou Power BI embarcado) + APIs de dados + versao resumida no app mobile.

---

### MODULO 4 - Pulse Leads (Geracao Inteligente de Leads de Servico)

**O que e:** Motor que gera leads de servico proativos para cada concessionaria: uma lista priorizada de "quem contatar hoje, por que, e com qual abordagem."

**Problema que resolve:** A concessionaria nao sabe quem precisa de servico agora. Espera o cliente ligar. Quando tenta fazer marketing, manda a mesma mensagem pra todo mundo. A taxa de conversao e baixa porque o timing e a relevancia sao ruins.

**Como gera leads:**

| Tipo de Lead | Gatilho | Prioridade |
|---|---|---|
| **Manutencao programada** | Veiculo proximo de 10K, 20K, 30K km (estimado por padrao de uso) | Alta |
| **Garantia expirando** | Garantia acaba em 30/60/90 dias - oportunidade de vender extensao | Muito alta |
| **Cliente sumiu** | Ultima visita ha mais de X meses (variavel por perfil) | Alta |
| **Recall pendente** | Recall aberto nao atendido - oportunidade de reconexao | Muito alta |
| **Score de churn alto** | Radar de Churn (M2) indica risco elevado | Critica |
| **Sazonalidade** | Checagem antes de viagem (ferias, feriados prolongados) | Media |
| **Historico de problema** | Modelo/ano com incidencia conhecida de defeito em X km | Media |

**Para cada lead, o sistema entrega:**
- Nome do cliente e dados de contato
- Veiculo e dados relevantes (km estimada, ultima visita, garantia)
- Motivo do lead (por que contatar agora)
- Perfil do cliente (do Modulo 2) e tom recomendado
- Script sugerido ou template de mensagem
- Melhor canal (do Modulo 5)
- Prioridade (urgente / alta / media / baixa)

**Como vender pra Ford:**
> "Todo dia de manha, o gerente de servico abre o app e ve: 'Hoje voce tem 23 leads prioritarios. 5 sao clientes com garantia expirando este mes, 8 estao com revisao atrasada, 3 tem recall pendente, e 7 estao com score de churn critico.' Ele nao precisa pensar em quem ligar - o sistema ja fez essa inteligencia."

**Valor de negocio:** Leads proativos convertem 3-5x mais que marketing massivo. A concessionaria para de gastar em campanha generica e foca onde ha maior probabilidade de retorno.

**Entregavel tecnico:** Motor de regras + ML para priorizacao + API de leads + tela no app mobile e web.

---

### MODULO 5 - CommEngine (Orquestrador de Comunicacao)

**O que e:** Sistema que automatiza e personaliza toda a comunicacao com o cliente, definindo QUANDO, POR QUAL CANAL, e COM QUAL MENSAGEM contatar cada pessoa.

**Problema que resolve:** A comunicacao da concessionaria com o cliente e generica, no timing errado, e pelo canal errado. Mandam email pra quem so usa WhatsApp. Mandam promocao de desconto pra quem nao e sensivel a preco. Mandam lembrete 1 semana depois que o cliente ja foi numa oficina independente.

**Logica de personalizacao por perfil (do Modulo 2):**

| Perfil | Canal Preferido | Tom | Tipo de Mensagem |
|---|---|---|---|
| **Cliente Fiel** | App/Email | Premium, exclusivo | "Agradecimento + beneficio VIP + agendamento facilitado" |
| **Cliente Economico** | WhatsApp/SMS | Direto, focado em economia | "Revisao dos 40K com 25% de desconto so esta semana" |
| **Cliente Esquecido** | WhatsApp + Ligacao | Acolhedor, sem pressao | "Faz tempo que nao vemos seu [modelo]. Tudo bem com ele? Temos horario disponivel para um check-up gratuito" |
| **Cliente de Abandono** | Ligacao pessoal | Win-back, oferta forte | "Gostarimos de te ouvir. Preparamos uma condicao especial de retorno" |

**Automacoes pre-configuradas:**
1. Boas-vindas pos-compra (dia 1, 7, 30)
2. Lembrete de 1a revisao (baseado em km estimada)
3. Alerta de garantia expirando (90, 60, 30 dias)
4. Follow-up pos-servico (NPS + agendamento da proxima)
5. Reativacao de cliente inativo (cadencias progressivas)
6. Lembrete de recall pendente
7. Conteudo educativo sobre cuidados com o veiculo (nurturing)
8. Oferta sazonal (pre-ferias, pre-inverno)

**Como vender pra Ford:**
> "Cada cliente Ford recebe a mensagem certa, no momento certo, pelo canal certo. O cliente fiel recebe tratamento VIP. O economico recebe a promocao que vai convence-lo. O esquecido recebe um lembrete gentil. E tudo isso roda automaticamente - a concessionaria so precisa atender quem responder."

**Valor de negocio:** Comunicacao personalizada aumenta taxa de abertura em 2-3x e conversao em 3-5x vs comunicacao generica. Automacao reduz custo operacional da concessionaria.

**Entregavel tecnico:** Motor de regras de comunicacao + templates + API de disparo (integravel com WhatsApp Business, email, push notification) + metricas de performance de cada campanha.

---

### MODULO 6 - Journey Optimizer (Otimizador da Jornada Pos-Venda)

**O que e:** Modulo que mapeia e otimiza toda a jornada do cliente dentro da concessionaria, desde o agendamento ate o pos-servico.

**Problema que resolve:** A experiencia do cliente na concessionaria e friccionada. Agendar e dificil. Nao sabe quanto vai custar. Nao sabe quando fica pronto. Nao recebe feedback depois. Cada ponto de friccao e uma razao para nao voltar.

**Funcionalidades:**

1. **Agendamento inteligente**
   - Agenda online/app com horarios disponiveis em tempo real
   - Sugestao do melhor horario baseado no historico do cliente
   - Estimativa de tempo e custo antes de confirmar
   - Lembrete automatico no dia anterior

2. **Check-in digital**
   - Cliente faz check-in pelo app ao chegar
   - Sem fila, sem formulario em papel
   - Ordem de servico pre-preenchida com base no lead/agendamento

3. **Acompanhamento em tempo real**
   - Status do servico atualizado: recebido, em diagnostico, em execucao, pronto
   - Notificacao push quando o carro fica pronto
   - Se surgir servico adicional: aprovacao pelo app com foto/video do problema

4. **Transparencia de precos**
   - Orcamento detalhado antes de autorizar
   - Comparativo: "Revisao dos 40K na Ford custa R$ 890 com pecas genuinas e garantia de 1 ano"
   - Destaque do valor agregado vs oficina independente

5. **Pesquisa pos-servico (NPS)**
   - NPS automatico 24h depois do servico
   - Se nota baixa: alerta imediato para o gerente intervir
   - Se nota alta: pedir avaliacao no Google + convite para programa de indicacao

6. **Agendamento da proxima visita**
   - Ao final de cada servico, sugerir e pre-agendar a proxima manutencao
   - "Sua proxima revisao e em aproximadamente 6 meses. Quer ja deixar agendado?"

**Como vender pra Ford:**
> "O cliente sai da concessionaria e em 24h recebe um 'como foi?'. Se deu nota 9 ou 10, pedimos avaliacao no Google. Se deu nota baixa, o gerente liga em 1 hora para resolver. Antes de sair, a proxima revisao ja esta pre-agendada. Cada interacao e projetada para garantir que ele volte."

**Valor de negocio:** Concessionarias com processo de agendamento digital tem 20-30% mais visitas de servico. Pre-agendamento da proxima visita aumenta retencao em ate 40%. NPS rapido permite correcao antes de perder o cliente.

**Entregavel tecnico:** APIs de agendamento e status + telas no app mobile (cliente) + painel web (concessionaria) + integracao com DMS.

---

### MODULO 7 - FordRewards (Programa de Fidelidade e Engajamento)

**O que e:** Programa de pontos e beneficios que recompensa o cliente por manter o veiculo na rede Ford.

**Problema que resolve:** Nao ha incentivo tangivel para o cliente voltar a concessionaria apos o fim da garantia. A oficina do bairro e mais barata e mais perto. Falta um motivo concreto para escolher a rede Ford.

**Mecanica do programa:**

| Acao do Cliente | Pontos | Valor Estimado |
|---|---|---|
| Fazer revisao programada na rede | 500 pts | ~R$ 50 em credito |
| Fazer servico adicional (freio, pneu, etc.) | 300 pts | ~R$ 30 |
| Responder pesquisa NPS | 50 pts | ~R$ 5 |
| Indicar amigo que faz servico | 1000 pts | ~R$ 100 |
| Manter veiculo com revisoes em dia (bonus anual) | 2000 pts | ~R$ 200 |
| Agendar pelo app (incentivo digital) | 100 pts | ~R$ 10 |

**Resgate de pontos:**
- Desconto em servicos e pecas
- Acessorios genuinos Ford
- Experiencias (test-drive de modelos novos, eventos Ford)
- Desconto na compra do proximo Ford (fidelidade cross-sell)

**Tiers de cliente:**

| Tier | Criterio | Beneficios |
|---|---|---|
| **Blue** | Cadastro | Acesso ao programa + descontos basicos |
| **Silver** | 2+ servicos no ano | +10% desconto em pecas + prioridade no agendamento |
| **Gold** | 4+ servicos OU 3 anos consecutivos | +20% desconto + carro reserva gratis + check-up gratuito semestral |

**Como vender pra Ford:**
> "O cliente pensa: 'Por que ir na Ford se a oficina do bairro e mais barata?' Com o FordRewards, a resposta e: 'Porque cada revisao me da pontos que viram desconto, porque sou Gold e tenho carro reserva gratis, e porque se eu indicar um amigo, ganho R$100 em credito.' O programa transforma custo percebido em investimento percebido."

**Valor de negocio:** Programas de fidelidade no setor automotivo aumentam retencao em 2-3x (case Hyundai/Kia). Clientes fidelizados tem ticket medio 25% maior. Indicacoes geram leads de altissima conversao.

**Entregavel tecnico:** API de pontos e tiers + telas no app mobile + painel de gestao para concessionaria + regras de acumulo e resgate.

---

### MODULO 8 - Dealer Benchmark (Benchmarking entre Concessionarias)

**O que e:** Ferramenta que compara a performance de cada concessionaria Ford contra as demais, identifica best practices e cria um ciclo de melhoria continua.

**Problema que resolve:** As 109 concessionarias Ford operam de forma isolada. Nenhuma sabe como se compara as outras. Melhores praticas nao se espalham. Concessionarias com baixa performance nao tem referencia de onde melhorar.

**Metricas comparadas:**

| Categoria | Metricas |
|---|---|
| **Retencao** | VIN Share, taxa de retorno, churn rate |
| **Operacional** | Tempo medio de servico, taxa de agendamento digital, NPS |
| **Financeiro** | Ticket medio, receita de servicos por VIN, margem |
| **Leads** | Taxa de conversao de leads, tempo de resposta, contatos realizados |
| **Fidelidade** | % clientes no programa, % Gold/Silver, taxa de indicacao |

**Funcionalidades:**
1. **Ranking geral e por categoria** - "Voce e a 15a de 109 em retencao e a 3a em NPS"
2. **Comparacao com pares** - Comparar com concessionarias de porte e regiao similar
3. **Identificacao de gaps** - "Sua taxa de agendamento digital e 12%. A media das top-10 e 45%. Oportunidade: investir no canal digital."
4. **Compartilhamento de best practices** - Cases anonimizados de o que as top performers fazem de diferente
5. **Metas e gamificacao** - Premios trimestrais para as concessionarias que mais evoluirem

**Como vender pra Ford:**
> "Hoje a Ford nao sabe por que a concessionaria X retem 60% dos clientes e a Y retem 15%. Com o Dealer Benchmark, nao so vamos mostrar a diferenca - vamos mostrar O QUE a X faz de diferente e criar um playbook para a Y replicar. Em 12 meses, o piso da rede sobe."

**Valor de negocio:** Benchmarking eleva a performance media da rede. Se as bottom 20 concessionarias chegarem ao nivel da media, o impacto no VIN Share nacional e massivo. Gamificacao entre dealers cria motivacao intrinseca.

**Entregavel tecnico:** Dashboard web comparativo + API de metricas + ranking + sistema de metas.

---

### MODULO 9 - Strategy Simulator (Simulador de Estrategias de Retencao)

**O que e:** Ferramenta de simulacao "what-if" onde gestores da Ford podem testar o impacto estimado de diferentes estrategias de retencao ANTES de investir dinheiro.

**Problema que resolve:** A Ford investe em campanhas de retencao sem saber o ROI esperado. Decisoes sao baseadas em intuicao: "Vamos dar 20% de desconto pra todo mundo". Nao ha forma de comparar estrategias antes de executar.

**Exemplos de simulacao:**

| Cenario | Parametros | Output |
|---|---|---|
| "E se dermos 15% de desconto na revisao dos 30K para clientes economicos no Sudeste?" | Publico: perfil economico, regiao SE, veiculo 2-4 anos. Acao: 15% desconto. | Estimativa: +2.300 VINs recuperados, custo: R$ 180K, receita gerada: R$ 690K, ROI: 3.8x |
| "E se ligarmos para todos os clientes com recall pendente?" | Publico: recall aberto. Acao: ligacao + oferta de check-up gratuito. | Estimativa: +1.800 VINs reconectados, custo: R$ 45K (telemarketing), receita estimada: R$ 320K |
| "E se abrirmos 5 novas concessionarias no Nordeste?" | Regiao: NE, +5 dealers. | Estimativa: +4.500 VINs capturados na regiao, payback: 24 meses |

**Como funciona:**
1. Gestor define o publico-alvo (filtros de perfil, regiao, modelo, idade)
2. Define a acao (desconto, comunicacao, novo canal, novo dealer)
3. O modelo (baseado em dados historicos e elasticidades estimadas) projeta:
   - Quantos VINs seriam impactados
   - Estimativa de conversao (quantos voltariam)
   - Custo da acao
   - Receita esperada
   - ROI projetado
   - Impacto no VIN Share (pontos percentuais)
4. Gestor pode comparar multiplos cenarios lado a lado

**Como vender pra Ford:**
> "Antes de gastar R$ 1 em campanha, o gestor regional pode simular 5 estrategias diferentes, comparar o ROI de cada uma, e investir so na que tem maior retorno. E como ter um laboratorio de estrategia onde voce testa antes de arriscar. Isso transforma o pos-venda de centro de custo em centro de investimento com retorno previsivel."

**Valor de negocio:** Otimizacao de investimento em retencao. Elimina "achismo" nas decisoes estrategicas. Permite justificar budget com projecoes de ROI. Cria cultura data-driven na gestao do pos-venda.

**Entregavel tecnico:** Motor de simulacao (modelos estatisticos + ML) + interface web para configurar cenarios + visualizacao comparativa + API.

---

## A Plataforma All-in-One: Como Tudo se Conecta

### Fluxo de Dados Entre Modulos

```
DADOS BRUTOS (DMS, CRM, veiculos conectados, garantia)
        │
        ▼
┌─ MODULO 1: Customer Vista 360 ─────────────────────┐
│  Consolida todos os dados por cliente/veiculo       │
│  Alimenta todos os outros modulos                   │
└─────────────┬───────────────────────────────────────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
┌─ MODULO 2 ─┐   ┌─ MODULO 3 ─┐
│ Radar Churn │   │ Share Map  │
│ Score/Perfil│   │ Dashboard  │
└──────┬──────┘   └──────┬─────┘
       │                 │
       ▼                 ▼
┌─ MODULO 4 ──────────────────┐
│ Pulse Leads                  │
│ Gera leads priorizados       │
│ usando score + ciclo de vida │
└──────┬───────────────────────┘
       │
       ▼
┌─ MODULO 5 ──────────────────┐
│ CommEngine                   │
│ Envia a mensagem certa       │
│ pelo canal certo              │
└──────┬───────────────────────┘
       │
       ▼
┌─ MODULO 6 ──────────────────┐    ┌─ MODULO 7 ─────────────────┐
│ Journey Optimizer            │◄──►│ FordRewards                │
│ Agendamento, check-in,      │    │ Pontos, tiers, beneficios  │
│ acompanhamento, NPS          │    │ Resgate, indicacao          │
└──────┬───────────────────────┘    └────────────────────────────┘
       │
       ▼
┌─ MODULO 8 ──────────────────┐    ┌─ MODULO 9 ─────────────────┐
│ Dealer Benchmark             │◄──►│ Strategy Simulator         │
│ Compara concessionarias      │    │ What-if de retencao         │
│ Best practices               │    │ ROI projetado               │
└──────────────────────────────┘    └────────────────────────────┘
```

### Personas e Quem Usa o Que

| Persona | Modulos que usa | Plataforma |
|---|---|---|
| **Cliente final (dono do Ford)** | M6 (agendar, acompanhar), M7 (pontos, resgatar) | App mobile |
| **Atendente da concessionaria** | M1 (ver perfil do cliente), M4 (lista de leads), M6 (check-in, OS) | App mobile + Web |
| **Gerente de servico (dealer)** | M3 (dashboard local), M4 (leads), M8 (benchmark) | Web + App |
| **Gestor regional Ford** | M3 (dashboard regional), M8 (benchmark), M9 (simulador) | Web |
| **Diretoria Ford (estrategico)** | M3 (visao nacional), M9 (simulacao de investimentos) | Web |

### Stack Tecnica Sugerida

| Camada | Tecnologia | Justificativa |
|---|---|---|
| **Mobile** | React Native + Expo | Exigencia da disciplina |
| **Backend/APIs** | Node.js ou Python (FastAPI) | APIs REST, microservicos |
| **IA/ML** | Python (scikit-learn, XGBoost, pandas) | Segmentacao, classificacao, simulacao |
| **Banco de dados** | PostgreSQL | Relacional, migracoes, robusto |
| **Dashboard** | React (web) ou Power BI embarcado | Visualizacoes interativas |
| **Autenticacao** | JWT + OAuth2 com RBAC | Exigencia de Cybersecurity |
| **Comunicacao** | API WhatsApp Business + SendGrid (email) + Firebase (push) | Multi-canal |
| **Infra** | Docker + Cloud (AWS/Azure) | Escalabilidade |
| **Documentacao** | Swagger/OpenAPI | Exigencia de Arq/WebServices |
| **Arquitetura** | Archi (TOGAF) | Exigencia de QA |

---

## Alinhamento com as Disciplinas

| Disciplina | O que Entrega | Modulos Envolvidos |
|---|---|---|
| **Arq. Servicos/WebServices** | APIs REST de todos os modulos, Swagger, arquitetura SOA, banco com migracoes | Todos |
| **Mobile** | App React Native/Expo com telas de Vista 360, Leads, Agendamento, Rewards, Dashboard resumido | M1, M4, M6, M7, M3 |
| **Testing/QA** | Pitch da plataforma, Canvas, Quadro de Valor, Arquitetura TOGAF no Archi, video | Visao geral |
| **Cybersecurity** | JWT/OAuth2, RBAC, validacao, HTTPS, rate limiting, criptografia, LGPD, logs | Todos |
| **IA/ML** | Segmentacao (Base 1), Classificacao (Base 2), Jupyter Notebook, Relatorio PDF | M2 (Radar de Churn) |

---

## Roadmap de Entregas

### Sprint 1 (ate 24/05/2026) - Fundacao
- [ ] M2 - Radar de Churn: segmentacao + classificacao (entrega IA/ML)
- [ ] M1 - Customer Vista 360: API + tela basica
- [ ] M3 - Service Share Map: dashboard com visualizacoes principais
- [ ] APIs REST documentadas com Swagger (entrega Arq/WebServices)
- [ ] App mobile com telas de M1 + M3 resumido (entrega Mobile)
- [ ] Seguranca implementada em todas as APIs (entrega Cyber)
- [ ] Pitch + Canvas + TOGAF + video (entrega QA)

### Sprints 3-4 (2o semestre) - Expansao
- [ ] M4 - Pulse Leads: motor de geracao de leads
- [ ] M5 - CommEngine: orquestrador de comunicacao
- [ ] M6 - Journey Optimizer: agendamento, acompanhamento, NPS
- [ ] M7 - FordRewards: programa de fidelidade
- [ ] M8 - Dealer Benchmark: comparacao entre concessionarias
- [ ] M9 - Strategy Simulator: simulador de cenarios
- [ ] Integracao end-to-end entre todos os modulos
- [ ] App mobile completo com todos os modulos

---

*Este documento e a base estrategica do projeto. Cada modulo sera detalhado em documentos proprios conforme o desenvolvimento avançar.*
