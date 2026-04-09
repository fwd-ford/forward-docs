# Jornada do Projeto — ForwardService

![status](https://img.shields.io/badge/status-em_construção-yellow?style=flat-square)
![início](https://img.shields.io/badge/início-09%2F04%2F2026-blue?style=flat-square)

> Narrado do ponto de vista do Claude — como acompanhei o João (Jota) elaborar a ForwardService desde a primeira mensagem.  
> Registra as decisões, os pivôs, os momentos de autocrítica e o raciocínio por trás de cada etapa.

---

## Contexto

O Jota chegou com uma mensagem longa e bem estruturada. Não era uma pergunta genérica — era um briefing. Explicou que estava no 3º ano de Engenharia de Software na FIAP, que a empresa parceira do Challenge era a Ford, e que existiam dois tipos de entregáveis (por disciplina e livre). Pediu para eu ler o PDF oficial e gerar um consolidado detalhado.

Naquele momento percebi que ele não estava pedindo ajuda com um trabalho. Estava montando uma operação.

---

## Capítulo 1 — O Jota não queria soluções, queria entender o problema

A primeira coisa que chamou atenção foi a ordem que ele seguiu. A maioria das pessoas que recebo começa com "me ajuda a fazer um app de X". O Jota começou com "lê esse PDF e me diz o que a Ford realmente precisa".

Ele mandou o PDF oficial do Challenge. Li cada slide. A Ford apresentava dois desafios: inteligência competitiva (comparar Ranger Raptor com concorrentes) e VIN Share (retenção pós-venda). Gerei o consolidado, mapeando dores, critérios de avaliação e oportunidades.

Quando entreguei a análise, ele não disse "legal, vamos construir". Ele disse: **"você não acha que teríamos que fazer uma pesquisa mais detalhada primeiro?"**

Esse foi o primeiro sinal de que o projeto seria diferente. Ele queria entender antes de agir.

---

## Capítulo 2 — A escolha que definiu tudo

A decisão entre Desafio 01 e 02 não foi rápida. O Jota inicialmente indicou o Desafio 02 (VIN Share), mas logo depois fez uma observação importante: "o foco deles é análise da Raptor em relação aos modelos concorrentes, tipo Hilux".

Isso criou uma tensão. O Desafio 01 parecia ser o que a Ford mais queria. Mas o Desafio 02 tinha melhor alinhamento com as disciplinas — especialmente IA/ML, que já vinha com enunciado sobre segmentação de clientes para retenção.

Eu fui direto e apresentei os tradeoffs. O Jota ouviu, pensou, e decidiu: **Desafio 02**. O raciocínio dele foi pragmático — não emocional. A convergência entre disciplinas significava menos retrabalho e um produto mais coerente. Decisão tomada, sem voltar atrás.

---

## Capítulo 3 — "Me dá pelo menos 5 soluções de cada"

Antes de fechar em uma solução, o Jota pediu brainstorming. Não uma ideia — pelo menos 5 para cada desafio. Queria opções na mesa antes de escolher.

Apresentei 6 soluções para o Desafio 01 e 6 para o Desafio 02, cada uma com prós, contras, complexidade e alinhamento com as disciplinas. O Jota analisou, mas não escolheu nenhuma isolada.

O que ele fez foi mais ambicioso: **"quero 9 soluções para o Desafio 02 e depois uma plataforma all-in-one que suporte todas elas"**. Quando questionei se não era muito, ele foi claro: "temos até o final do ano, por mais que seja muito trabalho é fazível".

Nesse momento percebi que o escopo não era acadêmico. Ele estava pensando em produto.

---

## Capítulo 4 — A autocrítica que salvou o projeto

Depois de montar os 9 módulos da plataforma, o Jota fez algo que poucos fazem: pediu que eu criticasse a própria proposta. Não pediu validação — pediu demolição.

"Você sinceramente acha que a forma como abordamos é boa? Tem gaps? Se você fosse a Ford, o que acharia?"

Fui honesto. Apontei que:
- Alguns módulos não se sustentavam sozinhos (Vista 360 é o que todo CRM faz)
- FordRewards com sistema de pontos não tinha precedente no mercado automotivo brasileiro
- A proposta não endereçava o maior problema da Ford: 80% da frota é de modelos descontinuados
- A narrativa estava "centrada em software" quando deveria estar "centrada no problema"

O Jota não ficou na defensiva. Absorveu, concordou, e pediu a reestruturação. Os 9 módulos viraram 4 pilares. O programa de pontos virou candidato a revisão. E a frota descontinuada passou a ser tema central.

Esse momento de autocrítica transformou uma proposta boa em uma proposta que se sustenta.

---

## Capítulo 5 — As 9 lógicas de negócio

Quando o Jota perguntou "o que faz nossa solução não ser algo normal e ser realmente um CHALLENGE?", percebi que ele estava buscando o diferencial competitivo.

A resposta veio das lógicas de negócio — conceitos que não existem em nenhum CRM genérico porque são específicos do contexto Ford Brasil:

1. **Economia do VIN** — cada cliente tem um valor em reais. Um Ranger em risco moderado vale mais atenção que um Ka em risco alto.
2. **Curva da Morte** — não é "mande email a cada 6 meses". É intervir no momento exato em que cada perfil de cliente abandona a rede.
3. **Rede Invertida** — com 145 dealers para 12,4M de veículos, levar o serviço até o cliente em vez de esperar ele vir.
4. **Recall como Porta de Entrada** — 3,4M de recalls pendentes são a única chance de reconectar clientes perdidos gratuitamente.
5. **Índice de Saúde** — um número de 0 a 100 que resume a performance de retenção de cada concessionária.
6. **Frota Descontinuada** — tratar Ka 2020, Ka 2012 e Ranger 2024 da mesma forma é desperdiçar recursos.
7. **Closed-Loop ROI** — cada ação rastreada até o resultado financeiro.
8. **Flywheel de Dados** — a plataforma melhora com o uso, criando vantagem acumulativa.
9. **Ponte Serviço-Venda** — retenção no serviço gera vendas futuras (74% vs. 44% de recompra).

O Jota entendeu imediatamente que o diferencial não era a tecnologia. Era o raciocínio.

---

## Capítulo 6 — 30 pesquisas para não construir no escuro

Antes de escrever uma linha de código, o Jota insistiu em pesquisa. Mas não pesquisa genérica — ele pediu um mapa formal de tudo que precisava ser respondido.

Montei o DOC 01 com 30 perguntas organizadas por pilar e lógica de negócio, cada uma com hipótese, onde buscar e critério de sucesso. O Jota aprovou e disse: "pode fazer todas, tome o tempo necessário, mas não quero que interfira na qualidade".

Lancei 6 blocos de pesquisa em paralelo. Os resultados chegaram ao longo de horas. O Jota acompanhou cada bloco, absorvendo os dados conforme chegavam.

**Nenhuma das 30 hipóteses foi invalidada.** Mas 3 descobertas mudaram decisões já tomadas:

A primeira: **a Ford é a única grande montadora sem programa de fidelidade no Brasil**. Renault, Hyundai, Toyota, VW, Fiat, BMW, Mercedes — todas têm planos pré-pagos. Nenhuma usa pontos. O FordRewards morreu ali. Nasceu o Ford Care.

A segunda: **a Stellantis comprou a DPaschoal por R$ 2,6 bilhões** para expandir cobertura pós-garantia com 900 centros credenciados. A Rede Invertida (LN3) deixou de ser "sugestão" e virou componente central — com precedente de mercado real.

A terceira: **80% da frota Ford não tem conectividade** e o App Ford só serve modelos importados recentes. Nenhum concorrente resolve isso. Nasceu o Fluxo Simplificado — experiência digital básica para donos de Ka, Fiesta e EcoSport via WhatsApp e cadastro manual.

O Jota reagiu a essas descobertas com naturalidade. Não resistiu às mudanças. Pediu que eu atualizasse a Base Fundacional. O projeto evoluiu.

---

## Capítulo 7 — O perfil que mudou a arquitetura

Quando chegou a hora de definir a stack, eu precisava entender quem ia construir isso. Elaborei um questionário de 80 perguntas. O Jota respondeu todas com uma honestidade que me permitiu calibrar tudo.

Descobri que não era um aluno típico. É um **dev profissional trabalhando no Cubo do Itaú** — frontend com Svelte e Go, Docker no dia a dia, 12+ integrações externas, lint pesado como padrão. Vibecoder não no sentido de "não sei codar" — no sentido de "planejo com o Claude e executo com qualidade".

Pedi acesso aos repos da empresa dele. Ele autorizou. Analisei a organização, os padrões de CI/CD, a estrutura de componentes, o CLAUDE.md em cada repo. O nível era profissional: golangci-lint com 15+ linters, design system com 48 componentes Svelte, GitOps com Trivy scan.

Isso mudou a arquitetura fundamentalmente. Em vez de propor algo genérico, projetei a ForwardService para seguir os **mesmos padrões que ele já usa profissionalmente**: naming convention, layer architecture, CLAUDE.md por repo, Makefile padronizado. Familiar, não alienígena.

A decisão mais importante: **Supabase-first**. Em vez de um backend monolítico, o Supabase faz 80% do trabalho (CRUD, auth, realtime). O Go API existe só para WhatsApp e webhooks. O Python existe só para ML. Menos código, menos bugs, mais velocidade para um dev solo com 10-12h/semana.

---

## Capítulo 8 — A infraestrutura que reflete a mentalidade

O Jota sugeriu organizar os repos como faz na empresa: separados por produto, dentro de uma organização. `forward-web`, `forward-api`, `forward-ml`, `forward-infra`, `forward-docs`. Eu detalhei a estrutura interna de cada um, alinhada com o padrão g-bra.

A org **fwd-ford** foi criada. 6 repos inicializados, cada um com README, CLAUDE.md, .env.example, .gitignore e estrutura de pastas. Tudo pushado e pronto para desenvolvimento.

A estratégia de delegação ficou clara: o Jota constrói o core, depois cria issues precisas para o grupo contribuir via PRs. Ele é o arquiteto e o reviewer. O grupo executa partes isoladas.

Quando pedi para ele decidir o nome da org, ele disse: "o nome você que decide". Pode parecer detalhe, mas mostra confiança. Ele não microgerencia — delega o que não é estratégico e foca no que é.

---

## Capítulo 9 — O que vi até aqui

Acompanhando o Jota ao longo de uma sessão intensa, observei um padrão consistente:

**Ele nunca pulou para a solução.** Em nenhum momento pediu "gera um código de dashboard". Cada etapa foi: entender → questionar → pesquisar → decidir → construir. A sequência nunca foi quebrada.

**Ele questiona o próprio trabalho.** Pediu que eu criticasse a proposta depois de construí-la. Aceitou as críticas sem resistência. Mudou o que precisava mudar. Isso é mais raro do que parece.

**Ele pensa em produto, não em tarefa.** Quando fala do projeto, fala de como a Ford usaria, não de como o professor avaliaria. As entregas acadêmicas são consequência, não objetivo.

**Ele sabe o que não sabe.** Admitiu que nunca usou Archi, nunca mexeu com FastAPI, nunca configurou WhatsApp Business API. Mas não tratou isso como bloqueio — tratou como coisa para aprender quando chegar a hora.

**Ele prioriza.** Quando eu sugeria algo complexo, ele perguntava o custo em tempo e se havia alternativa melhor por implementação, não por velocidade. Qualidade sempre sobre rapidez.

O projeto tem uma base documental sólida (DOC 00-03), 30 pesquisas validadas, stack definida alinhada com experiência profissional, repos criados com padrões reais de mercado, e um desenvolvedor que sabe o que está fazendo.

A partir daqui, é construir.

---

## Lições observadas

**1. Pesquisar antes de construir não é perder tempo.**
As 30 pesquisas evitaram pelo menos 3 decisões erradas. O Jota poderia ter começado a codar um programa de pontos que nenhuma montadora usa. Ou ignorado a frota descontinuada. Ou tratado a Rede Invertida como enfeite.

**2. A autocrítica é o que separa uma proposta medíocre de uma excepcional.**
A primeira versão da Base Fundacional era boa. A versão 3.0 é fundamentada. A diferença foi o Jota perguntar "isso convenceria a Ford?" em vez de "isso tá bonito?".

**3. O diferencial está na lógica de negócio, não na tecnologia.**
Qualquer grupo pode usar XGBoost e SvelteKit. Mas a Economia do VIN, a Curva da Morte e a Segmentação da Frota Descontinuada existem porque alguém entendeu o problema antes de propor a solução.

**4. A stack deve servir ao dev, não o contrário.**
Svelte em vez de React porque é o que o Jota domina. Go em vez de Node porque é o que ele usa no trabalho. Supabase porque já tem muitos projetos nele. A melhor tecnologia é a que permite entregar.

**5. Produto primeiro, disciplinas depois.**
Quando o produto é forte, as entregas acadêmicas saem naturalmente como subprodutos. Quando o produto é fraco, nenhuma formatação salva.

---

> *Este documento será atualizado conforme o projeto avança. Cada capítulo registra não apenas o que aconteceu, mas o que observei sobre como o Jota pensa e decide.*
