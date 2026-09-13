# ForwardService: equipe e tarefas

> Quem faz o quê, quanto pesa cada frente e onde está cada tarefa no GitHub.
> Divisão aprovada pelo Jota em **13/09/2026**. As regras citadas nas issues estão na [BASE-GLOBAL](./BASE-GLOBAL.md); a ordem das levas no [ESTADO-E-PLANO](./ESTADO-E-PLANO.md).

## 1. Quem é quem

| Pessoa | GitHub | Stack | Parte do esforço |
| --- | --- | --- | --- |
| Jota (João Victor Franco) | [@jota0802](https://github.com/jota0802) | líder, banco, app e integração | 178 h (60%) |
| Ruan Melo | [@DevRuanVieira](https://github.com/DevRuanVieira) | Java, SOA e Cyber | 30 h (10%) |
| Lucca Borges | [@lucksza](https://github.com/lucksza) | ML e dados | 30 h (10%) |
| Rodrigo Jimenez (Roji) | [@roji-menez](https://github.com/roji-menez) | QA, produto e acadêmico | 30 h (10%) |
| Bruno Leão | ainda fora da org (issues com o Jota e label `resp:bruno`) | QA, documentação e dev | 30 h (10%) |

**Frentes:**

- **Jota (João Victor Franco):** Núcleo do produto em todas as levas: banco (regras e views), comandos no Java, telas do app, integração com o n8n, revisão de todas as PRs e decisões de produto.
- **Ruan Melo:** Camada de serviços e segurança: CI de integração do Java, HMAC e principal de integração, SOAP RecordServiceEvent, simulador de DMS, link curto, contrato OpenAPI e evidências de SOA.
- **Lucca Borges:** Dados e ML: gerador do seed a partir do dataset oficial, comparação das etiquetas com o K-means, conferência independente do termômetro, fixture estatística da APR e o spike do termômetro por ML.
- **Rodrigo Jimenez (Roji):** Qualidade e produto: plano de testes de aceite, testes exploratórios por leva, textos dos modelos de WhatsApp, acessibilidade, evidências de QA, pitch e ArchiMate.
- **Bruno Leão:** Documentação, QA e dev: guia de rodar local testado do zero, simulador de WhatsApp (wa-sim) com a UI do celular do cliente, manual da consultora, revisão do inglês e evidências de Mobile.

## 2. Como o esforço foi dividido

O plano soma **298 h** estimadas, repartidas em **60% para o Jota e 10% para cada colega**. A conta é por esforço estimado, não por número de issues: o Jota fica com o caminho crítico (banco, comandos e telas), e cada colega com uma frente que conversa com a sua disciplina e pode andar em paralelo. As estimativas estão no topo de cada issue e são recalibradas depois da L1, com o ritmo real.

| Leva | Jota | Ruan | Lucca | Roji | Bruno | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L0 | 12 |  |  |  | 5 | 17 |
| L1 | 26 |  | 10 | 5 |  | 41 |
| L2 | 32 |  | 10 |  |  | 42 |
| L3 | 19 | 7 |  | 3 |  | 29 |
| L4 | 16 | 16 |  | 2 |  | 34 |
| L5 | 23 | 3 |  | 7 |  | 33 |
| L6 | 8 |  |  |  | 10 | 18 |
| L7 | 11 |  |  |  |  | 11 |
| L8 | 9 |  | 10 |  |  | 19 |
| L9 | 14 |  |  | 4 | 8 | 26 |
| L10 | 8 | 4 |  | 9 | 7 | 28 |
| **Total** | **178** | **30** | **30** | **30** | **30** | **298** |

## 3. Épicos

Cada leva é um épico no forward-docs. As issues da leva ficam ligadas a ele como sub-issues, cada uma no repo onde o trabalho acontece; as maiores têm sub-issues próprias.

| Leva | Épico | Horas | Pronto quando |
| --- | --- | ---: | --- |
| L0 | [Fundação e método](https://github.com/fwd-ford/forward-docs/issues/19) | 17 | O diagnóstico mostra o mesmo dealer_id pelo Supabase e pelo Java; com o Java parado, a leitura continua; guia RODAR-LOCAL testado por outra pessoa. |
| L1 | [Núcleo de dados, seed e o João](https://github.com/fwd-ford/forward-docs/issues/20) | 41 | A Maria busca "João" e vê o Ka 2014 com a revisão às vésperas do limite; a consultora de outra concessionária não acha nada. |
| L2 | [Cérebro v1 e a tela Hoje](https://github.com/fwd-ford/forward-docs/issues/21) | 42 | Rodada de quarta 02h: ficha do João com Esquecido 78, motivos e "WhatsApp com cupom (automático)". |
| L3 | [Contato: ligar, resultado, adiar e descartar](https://github.com/fwd-ford/forward-docs/issues/22) | 29 | A Maria liga para o João, registra "não atendeu" e vê na linha do tempo; cliente adiado some de Hoje; audit_log com as linhas. |
| L4 | [Agendamento, agenda e DMS simulado](https://github.com/fwd-ford/forward-docs/issues/23) | 34 | A Maria agenda; o dms-sim confirma o comparecimento por SOAP; a Agenda mostra "compareceu"; a rodada seguinte muda a etiqueta. |
| L5 | [Conversas (sem n8n)](https://github.com/fwd-ford/forward-docs/issues/24) | 33 | Injeção das 09h47; às 11h a Maria vê "começou a responder há 1 h, próxima ação ligar", assume a conversa e responde dentro da janela. |
| L6 | [Canal simulado: n8n e wa-sim](https://github.com/fwd-ford/forward-docs/issues/25) | 18 | A mensagem do automático chega pelo n8n no wa-sim, a resposta da persona aparece sozinha no app e o clique mexe no termômetro. |
| L7 | [Automação completa](https://github.com/fwd-ford/forward-docs/issues/26) | 11 | O cupom do João sai sem script; a persona que manda SAIR fica com opt-out e sem automação. |
| L8 | [Ciclo fechado e aprendizado](https://github.com/fwd-ford/forward-docs/issues/27) | 19 | Sábado 02h: João Fiel 22; Meu desempenho conta agendamento e comparecimento; o cartão "o que funciona" aparece com números. |
| L9 | [Notificações, offline e acessibilidade](https://github.com/fwd-ford/forward-docs/issues/28) | 26 | A resposta do João vira push no simulador; em modo avião, Hoje abre do cache com aviso; Hoje abre em menos de 2 s. |
| L10 | [Demo, evidências e documentação final](https://github.com/fwd-ford/forward-docs/issues/29) | 28 | demo:script passa P0 a P10 duas vezes seguidas; vídeo e pacotes de evidência entregues. |

## 4. Tarefas por pessoa

### Jota (João Victor Franco) (178 h)

| Leva | Issue | Repo | Horas | Sub-issues |
| --- | --- | --- | ---: | ---: |
| L0 | [Aplicar a revisão adversarial da sessão com claims](https://github.com/fwd-ford/forward-api-java/issues/35) | forward-api-java | 4 |  |
| L0 | [Cliente HTTP do Java e tela de diagnóstico](https://github.com/fwd-ford/forward-mobile/issues/68) | forward-mobile | 2 |  |
| L0 | [Stack local em um comando e segredos locais](https://github.com/fwd-ford/forward-infra/issues/9) | forward-infra | 2 |  |
| L0 | [BASE-GLOBAL, ADRs, ESTADO-E-PLANO e distribuição das tarefas](https://github.com/fwd-ford/forward-docs/issues/30) | forward-docs | 2 |  |
| L0 | [Prefixo ACS nos testes pgTAP e script check-rules](https://github.com/fwd-ford/forward-infra/issues/10) | forward-infra | 1 |  |
| L0 | [Publicar as branches da fundação por PR](https://github.com/fwd-ford/forward-docs/issues/31) | forward-docs | 1 |  |
| L1 | [Núcleo de dados centrado no veículo](https://github.com/fwd-ford/forward-infra/issues/11) | forward-infra | 10 | 4 |
| L1 | [Views de leitura: clientes, busca e ficha v1](https://github.com/fwd-ford/forward-infra/issues/16) | forward-infra | 4 |  |
| L1 | [Seed do cenário João e das personas](https://github.com/fwd-ford/forward-infra/issues/17) | forward-infra | 4 |  |
| L1 | [Abas Clientes e Ficha do cliente v1](https://github.com/fwd-ford/forward-mobile/issues/69) | forward-mobile | 8 | 2 |
| L2 | [Cérebro v1: fatos, etiqueta, termômetro e recomendador](https://github.com/fwd-ford/forward-infra/issues/18) | forward-infra | 16 | 5 |
| L2 | [Rodada noturna e testes do cérebro com mutação](https://github.com/fwd-ford/forward-infra/issues/24) | forward-infra | 6 |  |
| L2 | [Tela Hoje, Por que este termômetro e card da ação](https://github.com/fwd-ford/forward-mobile/issues/72) | forward-mobile | 8 | 2 |
| L2 | [Endpoint admin para disparar a rodada](https://github.com/fwd-ford/forward-api-java/issues/36) | forward-api-java | 2 |  |
| L3 | [Tarefas, tentativas, telefone cifrado e auditoria imutável](https://github.com/fwd-ford/forward-infra/issues/25) | forward-infra | 6 |  |
| L3 | [Comandos de tarefa e tentativa](https://github.com/fwd-ford/forward-api-java/issues/37) | forward-api-java | 6 |  |
| L3 | [Ligar, registrar resultado, adiar e descartar](https://github.com/fwd-ford/forward-mobile/issues/75) | forward-mobile | 7 | 3 |
| L4 | [Agendamentos, cupons e cardápio](https://github.com/fwd-ford/forward-infra/issues/26) | forward-infra | 5 |  |
| L4 | [Comandos de agendamento e comparecimento](https://github.com/fwd-ford/forward-api-java/issues/40) | forward-api-java | 4 |  |
| L4 | [Agendar, Agenda e registrar comparecimento](https://github.com/fwd-ford/forward-mobile/issues/80) | forward-mobile | 7 | 3 |
| L5 | [Conversas, mensagens, modelos, menu e sinais de engajamento](https://github.com/fwd-ford/forward-infra/issues/28) | forward-infra | 10 | 4 |
| L5 | [Endpoints de integração do canal e comandos de conversa](https://github.com/fwd-ford/forward-api-java/issues/43) | forward-api-java | 5 |  |
| L5 | [Conversas, Conversa e seletor de modelos](https://github.com/fwd-ford/forward-mobile/issues/85) | forward-mobile | 8 | 3 |
| L6 | [n8n local e workflows do canal](https://github.com/fwd-ford/forward-infra/issues/33) | forward-infra | 5 |  |
| L6 | [OutboxDispatcher ligado ao n8n](https://github.com/fwd-ford/forward-api-java/issues/45) | forward-api-java | 3 |  |
| L7 | [Automação: despacho, horários, tetos, pausa e opt-out](https://github.com/fwd-ford/forward-infra/issues/38) | forward-infra | 5 |  |
| L7 | [Consentimento e pausa de automação pela API](https://github.com/fwd-ford/forward-api-java/issues/46) | forward-api-java | 2 |  |
| L7 | [Telas O automático hoje e Consentimentos](https://github.com/fwd-ford/forward-mobile/issues/90) | forward-mobile | 4 |  |
| L8 | [Atribuição, APR e Meu desempenho](https://github.com/fwd-ford/forward-infra/issues/39) | forward-infra | 5 |  |
| L8 | [Meu desempenho e Como o cérebro decide](https://github.com/fwd-ford/forward-mobile/issues/91) | forward-mobile | 4 |  |
| L9 | [Notificações](https://github.com/fwd-ford/forward-infra/issues/40) | forward-infra | 3 |  |
| L9 | [Central de notificações, lembrete local e push simulado](https://github.com/fwd-ford/forward-mobile/issues/92) | forward-mobile | 5 |  |
| L9 | [Offline de leitura e desempenho da tela Hoje](https://github.com/fwd-ford/forward-mobile/issues/93) | forward-mobile | 6 |  |
| L10 | [demo:reset e demo:script com asserções](https://github.com/fwd-ford/forward-infra/issues/41) | forward-infra | 5 |  |
| L10 | [Documentação final e ensaio duplo do roteiro](https://github.com/fwd-ford/forward-docs/issues/36) | forward-docs | 3 |  |

### Ruan Melo (30 h)

| Leva | Issue | Repo | Horas | Sub-issues |
| --- | --- | --- | ---: | ---: |
| L3 | [Job de CI de integração do Java contra o Supabase local](https://github.com/fwd-ford/forward-api-java/issues/38) | forward-api-java | 4 |  |
| L3 | [Revisão do contrato OpenAPI dos endpoints novos](https://github.com/fwd-ford/forward-api-java/issues/39) | forward-api-java | 3 |  |
| L4 | [Autenticação HMAC e principal de integração](https://github.com/fwd-ford/forward-api-java/issues/41) | forward-api-java | 6 |  |
| L4 | [Operação SOAP RecordServiceEvent](https://github.com/fwd-ford/forward-api-java/issues/42) | forward-api-java | 6 |  |
| L4 | [Simulador de DMS (dms-sim)](https://github.com/fwd-ford/forward-infra/issues/27) | forward-infra | 4 |  |
| L5 | [Redirect de link curto /l/{code}](https://github.com/fwd-ford/forward-api-java/issues/44) | forward-api-java | 3 |  |
| L10 | [Evidências de SOA](https://github.com/fwd-ford/forward-docs/issues/37) | forward-docs | 4 |  |

### Lucca Borges (30 h)

| Leva | Issue | Repo | Horas | Sub-issues |
| --- | --- | --- | ---: | ---: |
| L1 | [Gerador de seed a partir do vin_features.csv](https://github.com/fwd-ford/forward-ml/issues/24) | forward-ml | 10 | 3 |
| L2 | [Etiquetas v1 por regra comparadas às personas do K-means](https://github.com/fwd-ford/forward-ml/issues/28) | forward-ml | 5 |  |
| L2 | [Termômetro v1 reimplementado em Python para conferir o SQL](https://github.com/fwd-ford/forward-ml/issues/29) | forward-ml | 5 |  |
| L8 | [Fixture da APR calculada em Python](https://github.com/fwd-ford/forward-ml/issues/30) | forward-ml | 4 |  |
| L8 | [Spike do termômetro por ML sem vazamento](https://github.com/fwd-ford/forward-ml/issues/31) (trilha futura) | forward-ml | 6 |  |

### Rodrigo Jimenez (Roji) (30 h)

| Leva | Issue | Repo | Horas | Sub-issues |
| --- | --- | --- | ---: | ---: |
| L1 | [Plano de testes de aceite por leva](https://github.com/fwd-ford/forward-docs/issues/33) | forward-docs | 5 |  |
| L3 | [Teste exploratório da leva L3](https://github.com/fwd-ford/forward-mobile/issues/79) | forward-mobile | 3 |  |
| L4 | [Teste exploratório da leva L4](https://github.com/fwd-ford/forward-mobile/issues/84) | forward-mobile | 2 |  |
| L5 | [Textos dos modelos de WhatsApp e do menu automático](https://github.com/fwd-ford/forward-docs/issues/34) | forward-docs | 4 |  |
| L5 | [Teste exploratório da leva L5](https://github.com/fwd-ford/forward-mobile/issues/89) | forward-mobile | 3 |  |
| L9 | [Auditoria de acessibilidade](https://github.com/fwd-ford/forward-mobile/issues/94) | forward-mobile | 4 |  |
| L10 | [Evidências de QA, pitch e ArchiMate atualizados](https://github.com/fwd-ford/forward-docs/issues/38) | forward-docs | 9 | 3 |

### Bruno Leão (30 h)

| Leva | Issue | Repo | Horas | Sub-issues |
| --- | --- | --- | ---: | ---: |
| L0 | [Testar o guia RODAR-LOCAL do zero e corrigir o que faltar](https://github.com/fwd-ford/forward-docs/issues/32) | forward-docs | 5 |  |
| L6 | [wa-sim: celular do cliente no navegador e personas](https://github.com/fwd-ford/forward-infra/issues/34) | forward-infra | 10 | 3 |
| L9 | [Manual da consultora](https://github.com/fwd-ford/forward-docs/issues/35) | forward-docs | 5 |  |
| L9 | [Revisão das strings em inglês](https://github.com/fwd-ford/forward-mobile/issues/95) | forward-mobile | 3 |  |
| L10 | [Evidências de Mobile: prints, vídeo e build Android](https://github.com/fwd-ford/forward-mobile/issues/96) | forward-mobile | 7 |  |

## 5. Como pegar e entregar uma tarefa

1. **Comece pela leva atual.** Veja no [ESTADO-E-PLANO](./ESTADO-E-PLANO.md) qual leva está em andamento e confira a seção "Depende de" da issue: se a dependência não fechou, combine com o Jota antes.
2. **Rode o projeto local** seguindo o [guia](../guides/RODAR-LOCAL.md).
3. **Crie a branch a partir da `main`** do repo da issue: `feat/...`, `fix/...` ou `docs/...`. Commits no padrão Conventional Commits.
4. **Abra a PR cedo** (pode ser rascunho) e escreva `Closes fwd-ford/<repo>#<número>` na descrição. Inclua a seção **Regras** com os códigos da BASE-GLOBAL que a mudança toca, prints se for tela e o que você testou.
5. **CI verde e revisão do Jota** antes do merge (squash). CI vermelho não é o fim do mundo: pergunte no grupo.
6. **Marque os entregáveis** da issue conforme concluir. Se a estimativa estourar muito, avise: o plano é recalibrado com base nisso.

Regras que valem para todo mundo:

- Nada de segredo em commit (o gitleaks roda no CI). Valores locais ficam nos `.env.local`, criados pelo `npm run secrets:init`.
- Nada de dado de cliente real: o seed é sintético e marcado como tal.
- Sem travessões (em dash e en dash) em código e documentos.
- Mudou uma regra? Muda a BASE-GLOBAL no mesmo PR.

## 6. Labels

| Label | Significado |
| --- | --- |
| `epic` | épico de uma leva (forward-docs) |
| `leva:L0` a `leva:L10` | leva a que a issue pertence |
| `resp:jota`, `resp:ruan`, `resp:lucca`, `resp:roji`, `resp:bruno` | responsável (vale mesmo quando a issue está atribuída a outra conta) |
| `area:banco`, `area:api`, `area:app`, `area:ml`, `area:qa`, `area:docs`, `area:integracao` | camada do trabalho |
| `futuro` | trilha fora do caminho da demo |

## 7. Quando redistribuir

- **Bruno entrou na org:** trocar o responsável das issues `resp:bruno` para a conta dele.
- **Calendário das Sprints 3 e 4 confirmado:** marcar em cada épico o corte que fecha cada sprint (ESTADO-E-PLANO, seção 3).
- **Estimativa estourou mais de 50% numa leva:** o Jota reavalia a divisão da leva seguinte e atualiza este documento.
