# Q&A de Contexto — Respostas Analisadas

![status](https://img.shields.io/badge/status-analisado-brightgreen?style=flat-square)
![respostas](https://img.shields.io/badge/respostas-80%2F80-brightgreen?style=flat-square)
![pendentes](https://img.shields.io/badge/pontos_pendentes-ver_backlog-yellow?style=flat-square)

> Respostas do Jota organizadas com análise e implicações para o projeto.  
> Data: 09/04/2026

---

# Bloco 1 — Você e o Grupo

---

### Q1. Nome
**R:** João, mas chama de Jota.

---

### Q2. O que "vibecoder" significa pra você?
**R:** "Sei mais como instruir o Claude e saber sobre arquitetura de projeto. Eu não só itero, eu planejo, penso e repenso."

**Análise:** Isso ficou claro durante toda a conversa. Jota não é um "me gera código" — é um product thinker que usa IA como acelerador. Isso muda a abordagem: posso discutir tradeoffs de arquitetura com ele em vez de só entregar código. O foco deve ser em decisões de alto nível com Jota, e código como output dessas decisões.

**Como vou usar:** Vou tratar Jota como tech lead, não como dev junior. Decisões de arquitetura são discutidas, não impostas. Código vem acompanhado de "por que", não só "o que".

---

### Q3. Stack e experiência técnica
**R:** Frontend profissional. Stack no trabalho: **Svelte + Go**. Já mexeu com Python, Java, C, TypeScript, React, Next, React Native. Banco: PostgreSQL. Não viu MongoDB. FastAPI nunca mexeu. Node familiarizado. Cloud: Azure, AWS, Vercel, Netlify. ML: fazendo projeto atualmente.

**Análise:** Perfil muito mais forte do que a média de vibecoder. Frontend profissional com Svelte é raro — significa que entende reatividade, componentes, state management de verdade. Go no backend indica que não tem medo de tipagem forte e performance.

**Implicações para a stack:**

| Decisão | Recomendação | Justificativa |
|---|---|---|
| Backend principal | **Go** ou **TypeScript (Node)** | São as que ele domina. Go é mais performante mas TS tem ecossistema mais rico para MVP rápido |
| Frontend web (dashboards) | **Svelte/SvelteKit** | É o que ele domina no trabalho. Não faz sentido forçar React no web se Svelte é sua arma |
| Mobile | **React Native/Expo** | Obrigatório pela disciplina. Já usou 4x com vibecoding |
| ML/IA | **Python** | Padrão da indústria, sem alternativa real |
| Banco | **PostgreSQL via Supabase** | Já tem muita experiência com Supabase |
| Auth | **Supabase Auth** | Já conhece, e cobre JWT por baixo (atende Cybersecurity) |

---

### Q4. Deploy
**R:** "Já coloquei front e back e banco no ar. Sei que tem peculiaridades tipo seed."

**Análise:** Sabe deployar. Não vai travar na hora de colocar no ar. Bom.

---

### Q5-6. IDE e ferramentas IA
**R:** VSCode + Claude Code (plano MAX).

**Análise:** Ambiente ideal. Claude Code MAX tem contexto longo (1M), o que permite sessões longas de desenvolvimento sem perder thread.

---

### Q7. Horas por semana
**R:** "Depende do ânimo, mas até 20h/semana."

**Análise:** 20h é otimista. Vou planejar para **10-12h reais** e tratar 20h como upside. Em 45 dias até a Sprint 1 (10-12h × 6 semanas = ~60-72h de dev), isso é suficiente para um MVP se o escopo for cirúrgico.

---

### Q8. Máquina
**R:** Aguenta o tranco.

---

### Q9-10. Grupo
**R:** 4 integrantes.

| # | Nome | RM |
|---|---|---|
| 1 | Lucca Borges | 554608 |
| 2 | Ruan Melo | 557599 |
| 3 | Rodrigo Jimenez | 558148 |
| 4 | **João Victor Franco (Jota)** | 556790 |

---

### Q11-14. Dinâmica do grupo
**R:** "Quero fazer sozinho o começo e depois coloco eles. Sou o responsável, monitoro PRs depois."

**Análise:** Modelo claro: Jota é o arquiteto e dev principal. Grupo entra depois para tarefas delegadas. Isso é viável se:
1. A arquitetura for modular o suficiente para delegar partes isoladas
2. Jota documentar padrões e conventions antes de delegar
3. As tarefas delegadas forem bem definidas (nada ambíguo)

**Como vou usar:** Vou projetar a arquitetura pensando em "Jota constrói o core, grupo contribui em módulos periféricos". A organização Git (branches, PRs) fica importante.

---

### Q12. Design
**R:** "Não temos tempo pra Figma, mas sou designer e frontend, confia."

**Análise:** Designer + frontend é combo raro e valioso. Vai direto do código pro visual. Sem Figma intermediário. Isso acelera muito.

---

### Q15-16. Alinhamento do grupo
**R:** "Ninguém liga muito, tô tomando a frente." / Pitch ainda não definiu quem apresenta.

**Análise:** Jota é o líder de fato. Grupo passivo. Isso é bom para velocidade de decisão, mas arriscado para apresentações (todos precisam participar no vídeo de 3 min).

---

# Bloco 2 — Contexto FIAP

---

### Q17. Sistema de notas
**R:** Média simples de todas as matérias → aplicada em todas.

**Análise:** Confirmado. Uma matéria fraca puxa tudo pra baixo. Mas Jota não liga para nota — prioridade é o produto.

---

### Q18. Disciplinas — DESCOBERTA IMPORTANTE

**R:** São **8 disciplinas**, não 5:

| # | Disciplina | Professor |
|---|---|---|
| 1 | Arquitetura Orientada a Serviços e Web Services | Salatiel Marinho |
| 2 | CS Software Development | Reinaldo Ramos |
| 3 | Cybersecurity | Vitor Miguel Lasse Silva |
| 4 | Inteligência Artificial e Machine Learning | Carlos Fontoura |
| 5 | Mobile Development e IoT | Hercules Lima Ramos |
| 6 | Operating Systems | José Ricardo Silva de Oliveira |
| 7 | Physical Computing IoT e IOB | Lucas Demetrius Augusto |
| 8 | Testing Compliance e Quality Assurance | Elias Bernardo |

**Análise crítica:** O PDF do Challenge mencionava 5 disciplinas com entregas. Temos 3 a mais que não foram mapeadas:
- **CS Software Development** — o que esse professor espera? Código? Metodologia? Precisa descobrir.
- **Operating Systems** — relevância pro projeto? Containers? Linux? Precisa descobrir.
- **Physical Computing IoT e IOB** — IoT pode ser relevante (sensores de veículo, OBD). Precisa descobrir.

O PDF disse que "algumas disciplinas terão maior relevância" e "as demais terão média baseada nas notas dessas entregas". Provavelmente essas 3 extras usam a média das outras.

**Ação necessária:** Jota precisa confirmar quais disciplinas têm entrega própria e quais herdam nota.

---

### Q19-20. Apresentação e banca
**R:** Apresentação para grupo seleto de professores + pessoa de produto/comercial e engenheiro da Ford. Banca final em outubro.

**Análise:** A Ford VÊ o projeto. Isso eleva a qualidade necessária da apresentação. Não é só nota acadêmica — é impressão para profissionais reais. A banca de outubro é a entrega final do ano.

---

### Q21. Feedback de professores
**R:** Cyber passou orientações sobre leis de proteção (arquivo pendente). Mobile pediu pelo menos um front em React Native.

**Análise:** Cybersecurity quer implementação real de segurança. Mobile quer React Native. Ambos alinhados com o plano.

---

### Q22-23. Produto real
**R:** "Sim, grande parte das pessoas normalmente já fazem isso." / Só Mobile cobra React Native.

**Análise:** A FIAP espera que bons alunos vão além das entregas. Construir um produto real não é exceção — é o padrão dos melhores grupos.

---

### Q24-27. Estado das entregas
**R:** Bases de IA/ML: ainda não recebeu. QA: sem orientações ainda. Cyber: implementação real, professor acompanha. **Tudo zerado.**

**Análise:** Zerado é bom nesse momento — nada pra refazer. Mas precisa das bases de ML logo para começar a segmentação.

---

### Q28-30. Contexto geral FIAP
**R:** Campus Paulista. Híbrido. Já fizeram Challenge antes — sempre sobra algo meio aleatório. Opinião: "projetos que entregam algo físico passam mais, mesmo sem sentido."

**Análise crucial:** **"Projetos que entregam algo físico passam mais."** Isso é insight valioso. O ForwardService precisa de algo tangível e demonstrável — não pode ser só slides e conceito. O app mobile + dashboard + integração WhatsApp são o "algo físico" do projeto.

---

### Q31-34. Repo e organização
**R:** Ainda não tem repo. Quer criar org no GitHub. Scrum Master não faz check-ins. Turma meio a meio entre Desafio 1 e 2. Ford vê algumas apresentações mas não avalia entregas de matéria.

**Análise:** Criar org no GitHub é boa ideia — profissionaliza. Sem check-ins do Scrum Master = autonomia total.

---

# Bloco 3 — Produto e Visão

---

### Q35-36. Ambição
**R:** "Tudo. Quero finalizar tudo até o fim do ano." / "Produto que funciona. Quanto mais dificuldades, mais se aprende."

**Análise:** Ambição máxima, aprendizado como driver. Não está fazendo por nota — está fazendo para crescer como engenheiro. Isso muda o tom: posso propor coisas mais desafiadoras sem medo de "é muito difícil". Ele quer dificuldade.

---

### Q37. Continuidade
**R:** "Não, só quero aprender o máximo possível. Nem ligo se não passar."

**Análise:** Sem pressão de startup ou monetização. Liberdade para experimentar. Mas se o produto ficar bom, a oportunidade existe.

---

### Q38. Se a Ford se interessar
**R:** "Depende, se minha ideia passar mesmo, aí o papo muda."

---

### Q39. Feature mais interessante
**R:** "O zap é zika. Conheço Twilio como provedor."

**Análise:** Integração WhatsApp anima ele. Faz sentido — é a parte mais tangível e demonstrável. Boa âncora para o MVP.

---

### Q40-44. Produto vs. Acadêmico
**R:** Prioridade é o produto. Sprint 1 faz o necessário. Segundo semestre vale 60% da nota anual. Não liga pra nota.

**Análise:** O plano é claro: produto primeiro, entregas acadêmicas como subproduto. Sprint 1 (24/05) é um esboço da ideia, não o produto pronto. O peso real está no 2º semestre (60%) e na banca de outubro.

---

# Bloco 4 — Stack e Implementação

---

### Q45-48. Infra atual
**R:** R$100 Azure (faculdade). Contas em Supabase, Vercel, Netlify, Railway. Vai usar Zenvia ou Twilio para WhatsApp. Não tem chaves de LLM — precisa de recomendação.

**Análise de custos:**

| Serviço | Custo estimado/mês | Uso |
|---|---|---|
| Supabase (free tier) | R$ 0 | Banco + Auth + Realtime |
| Vercel (free tier) | R$ 0 | Frontend web |
| Railway ou Azure | R$ 0-30 | Backend Go/TS |
| Zenvia ou Twilio | R$ 30-50 | WhatsApp API (volume baixo) |
| API de LLM | R$ 20-40 | Claude API ou OpenAI |
| **Total** | **R$ 50-120/mês** | Dentro do budget de R$ 60 + créditos Azure |

**Sobre LLM:** Recomendo **Claude API (Anthropic)** — Jota já usa Claude Code MAX, então familiaridade. Alternativa: OpenAI API (mais barata para alto volume). Pode começar com créditos grátis de ambas.

---

### Q49-57. Preferências técnicas
**R:** Supabase = muita experiência. Prisma 1x. Backend: TS ou Go (principal) + Python (ML). Expo já usou 4x. Dashboards do zero. JWT pedido pelo prof de Cyber, mas Supabase Auth pode atender.

**Stack consolidada (recomendação final):**

| Camada | Tecnologia | Justificativa |
|---|---|---|
| **Mobile** | React Native + Expo | Obrigatório. Jota já usou 4x |
| **Web (dashboards)** | SvelteKit | Domínio profissional do Jota. Mais rápido que React pra ele |
| **Backend API** | Go ou TypeScript (Node) | Go pra performance, TS pra velocidade de dev. Decidir no DOC 03 |
| **ML/IA** | Python (scikit-learn, XGBoost) | Padrão, sem alternativa |
| **Banco** | PostgreSQL via **Supabase** | Já tem muitos projetos, familiaridade máxima |
| **Auth** | **Supabase Auth** (JWT por baixo) | Atende Cybersecurity + Jota já conhece |
| **Realtime** | Supabase Realtime | Grátis, já integrado |
| **WhatsApp** | Zenvia ou Twilio | BSP para mensagens automatizadas |
| **Deploy web** | Vercel | Free tier, familiaridade |
| **Deploy backend** | Railway ou Azure | Budget disponível |
| **Documentação API** | Swagger/OpenAPI | Exigência de Arq/Web Services |

**Sobre Supabase Auth vs. JWT manual:** Supabase Auth usa JWT por baixo. O token de sessão é um JWT assinado. Isso atende o professor de Cyber se Jota explicar que o JWT está embutido no Supabase Auth com assinatura RS256, expiração configurável e RBAC via Row Level Security. Não precisa implementar JWT do zero — isso seria reinventar a roda.

---

### Q58-62. Maturidade de desenvolvimento
**R:** Swagger já gerou. Maior projeto: frontend profissional com Docker, seed, backend, Postman/curl. Lint pesado para padronizar. Já integrou 12+ provedores externos no trabalho.

**Análise:** Esse não é um aluno comum. É um dev profissional que estuda engenharia de software. O nível técnico é real — já trabalha com Docker, múltiplos provedores, padrões de lint. Posso propor arquitetura de nível profissional sem medo.

---

# Bloco 5 — Cronograma

---

### Q63-65. Tempo e recursos
**R:** Sprint 1 é só esboço da ideia, não produto pronto. Todos os dias consegue trabalhar. R$60/mês + R$100 Azure.

**Análise:** Se Sprint 1 é só esboço, o cronograma fica muito mais relaxado para ela. O trabalho pesado é o produto no 2º semestre. Mas ter algo demonstrável na Sprint 1 vai impressionar mais.

---

### Q66. Acesso a dados reais
**R:** "Não, mas meu trabalho é na Vila Olímpia no Cubo do Itaú que fica do lado de uma Ford."

**Análise:** Literalmente ao lado de uma concessionária Ford. Se precisar de dados qualitativos (fotos, experiência de agendamento, preços), pode ir lá pessoalmente. Oportunidade de pesquisa de campo que nenhum outro grupo vai ter.

---

### Q67-68. Figma e Archi
**R:** "Sem Figma, perda de tempo." / Archi nunca usou.

**Análise:** Sem Figma ok — Jota é designer, vai direto pro código. Archi precisa aprender para a entrega de QA (arquivo .archimate obrigatório). É uma ferramenta simples, curva de aprendizado de 2-3h.

---

# Bloco 6 — Meta e Trabalho

---

### Q69-75. Como trabalhar comigo
**R:**
- Decisões: "Os dois, mas de preferência mente aberta"
- Código: "Explica por cima, se precisar eu cobro"
- Arquivos: "Pode se organizar nessa pasta"
- Idioma: **Tudo em inglês, comentários bilíngues, i18n integrada**
- Log de decisões: "Pode ser, bom para evitar conflitos"
- Se algo for inviável: "Me fala o custo de tempo e se tem alternativa melhor por implementação, não por tempo"
- **Nunca usar subagentes para código**

**Análise das regras de trabalho:**

| Regra | Implicação |
|---|---|
| Inglês no código | Variáveis, funções, componentes, rotas — tudo em EN |
| Comentários bilíngues | `// Calculates LSV for each VIN / Calcula LSV para cada VIN` |
| i18n integrada | Plataforma multi-idioma desde o início (pt-BR + en) |
| Sem subagentes para código | Todo código que eu escrever será nesta conversa direta, sem delegar |
| Qualidade > velocidade | Se a melhor solução demora mais, que demore |

---

### Q76. Nome do projeto
**R:** "Aceito sugestões, mas eu tinha pensado tipo FORD (nossa solução/plataforma)."

**Análise:** Nome tipo "Ford [Produto]" faz sentido para um Challenge — mostra que é para a Ford. ForwardService funciona, mas pode ser simplificado. Opções: **Ford Forward**, **Ford Pulse**, **Ford Retain**, ou manter **ForwardService** como nome técnico e usar "Ford Forward" como nome de apresentação.

---

### Q78-80. Monetização e Ford
**R:** Não pensou em monetização. Se a Ford se interessar, quer deixar o mais alinhado possível para implementação real. "Como engenheiro quero resolver problemas das pessoas."

**Análise:** Mentalidade de engenheiro, não de empreendedor. Isso é bom — o foco fica na qualidade da solução. Monetização pode ser adicionada depois se fizer sentido.

---

# Síntese — Perfil Consolidado do Jota

```markmap
# Jota — Perfil
## Dev profissional
- Frontend Svelte + Go no trabalho
- Docker, 12+ integrações externas
- Cubo do Itaú, Vila Olímpia
## Vibecoder estratégico
- Planeja antes de codar
- Claude Code MAX como ferramenta principal
- Pensa em arquitetura, não só em código
## Designer
- Faz UI direto no código
- Sem Figma, sem perda de tempo
## Líder do grupo
- 4 integrantes, Jota na frente
- Delega depois de construir o core
## Mindset
- Aprendizado > nota
- Produto > acadêmico
- Qualidade > velocidade
- Quer dificuldade, não facilidade
```

---

# Implicações para o Projeto

## O que muda com essas respostas

### 1. Stack redefinida
Svelte no web em vez de React. Go ou TS no backend em vez de Python/FastAPI. Supabase como BaaS central. Isso é mais alinhado com o perfil do Jota e vai gerar mais velocidade de desenvolvimento.

### 2. Arquitetura para 1 dev (inicialmente)
Nada de microserviços. Monolito modular com Supabase como hub. Jota constrói o core, grupo entra depois em tarefas específicas. A modularidade permite isso.

### 3. Sprint 1 = esboço demonstrável
Não precisa estar pronto. Precisa impressionar. Um demo com dados sintéticos que mostra o conceito funcionando é suficiente e melhor que slides.

### 4. 8 disciplinas, não 5
Precisamos mapear o que as 3 extras (CS Software Dev, Operating Systems, Physical Computing) exigem. Provavelmente herdam nota, mas melhor confirmar.

### 5. i18n desde o dia 1
Código em inglês, plataforma bilíngue. Isso adiciona uma camada de complexidade mas é profissional e impressiona.

### 6. Ford vê o projeto
Não é só acadêmico. Tem pessoa de produto e engenheiro da Ford na apresentação. O nível de polish precisa ser alto.

### 7. Sem subagentes para código
Todo código gerado diretamente nesta conversa. Sem delegação a agentes paralelos. Entendido.

### 8. Vila Olímpia = pesquisa de campo
Jota trabalha literalmente ao lado de uma concessionária Ford. Pode fazer pesquisa de campo real (agendamento, preços, experiência).

---

# Como vou usar essas informações

| Informação | Como aplico |
|---|---|
| Svelte + Go + Supabase | Stack do DOC 03 e DOC 04 |
| 10-12h/semana reais | Cronograma calibrado, escopo cirúrgico |
| Designer que coda | Sem fase de design separada, UI direto no código |
| Prioridade = produto | Sprint 1 é checkpoint, não deadline final |
| Grupo passivo | Arquitetura modular para delegação posterior |
| Ford na apresentação | Demo tangível > slides conceituais |
| R$60/mês + Azure | Stack com free tiers + budget mínimo |
| i18n + inglês | Setup do projeto desde o início |
| Sem subagentes para código | Tudo nesta conversa |
| Qualidade > velocidade | Escolho a melhor solução, não a mais rápida |

---

> *Este documento alimenta diretamente o DOC 03 (Solution Design) e o DOC 04 (Arquitetura).*
