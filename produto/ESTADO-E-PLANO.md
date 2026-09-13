# ForwardService: estado e plano

> **Onde estamos e em que ordem se constrói.** O que o produto é e as regras ficam na [BASE-GLOBAL](./BASE-GLOBAL.md).
> Este documento muda a cada leva. Última atualização: **13/09/2026**, leva L0 em andamento.

**Se você acabou de chegar:**
1. Leia a seção 1 da [BASE-GLOBAL](./BASE-GLOBAL.md) (uma página).
2. Siga o [guia para rodar local](../guides/RODAR-LOCAL.md).
3. Pegue uma issue sua no quadro (divisão em [EQUIPE-E-TAREFAS](./EQUIPE-E-TAREFAS.md)).

O roteiro que prova o produto está no [ROTEIRO-DEMO](./ROTEIRO-DEMO.md).

## 1. O que existe e funciona

Tudo abaixo é local, nas branches de cada repo, e **ainda não foi publicado na `main`** (publicação por leva, com PR).

| Repo | Branch | O que tem | Prova |
| --- | --- | --- | --- |
| forward-infra | `feat/access-model` | Supabase CLI local; grants fechados (`authenticated` só lê); `private.memberships` com helpers e view `my_context`; papel `forward_api` sem BYPASSRLS; RLS v2 por concessionária; usuários de teste; `stack.sh` e `init-secrets.sh` | 78 testes pgTAP; CI com reset, testes e drift de tipos |
| forward-api-java | `feat/claims-bound-db-session` | JWT do Supabase verificado (exp, aud, iss, sub); toda consulta roda sob as claims do chamador (`ClaimsBoundDbSession`); `/api/v1/me`; SOAP `GetVehicle`; erros com `code` estável em REST e SOAP; revisão adversarial aplicada | 90 testes; Spotless, Checkstyle e SpotBugs verdes; 5 mutações mortas; conferido ao vivo |
| forward-mobile | `rebuild/foundation` | Expo SDK 57 refeito do zero com o design da Sprint 1; tokens com teste de paridade e contraste; primitivas; login, sessão cifrada, guards por status, tela sem acesso; cliente HTTP do Java e tela de diagnóstico | 93 testes; verificado no simulador iOS contra a stack local |

Ainda **não existe**:
- nada do domínio da Maria (fila, ficha com etiqueta e termômetro, conversa, agenda);
- o cérebro;
- o n8n novo e o simulador de WhatsApp.

Os 2 workflows antigos do n8n (`n8n-workflows/`) usam a `X-API-Key`, que foi removida, e serão arquivados na L6.

## 2. Decisões que sustentam o resto

| Decisão | Registro |
| --- | --- |
| O app lê o Supabase sob RLS; todo comando passa pelo Java | [ADR-001](../decisions/ADR-001-leitura-rls-comando-java.md) |
| Cérebro v1 em regras SQL; ML depois só no termômetro | [ADR-002](../decisions/ADR-002-cerebro-v1-regras-no-banco.md) |
| WhatsApp só simulado, com o contrato da Cloud API | [ADR-003](../decisions/ADR-003-whatsapp-simulado.md) |
| Primeiro só a Maria no celular | [ADR-004](../decisions/ADR-004-escopo-maria-celular.md) |
| Relógio do sistema e viagem no tempo para a demo | [ADR-005](../decisions/ADR-005-relogio-e-viagem-no-tempo.md) |
| n8n, simuladores e scripts de demo moram no forward-infra | [ADR-006](../decisions/ADR-006-onde-vivem-n8n-e-simuladores.md) |
| Supabase local agora, sem Fly, hospedagem adiada | [ADR-007](../decisions/ADR-007-supabase-local-sem-fly.md) |
| Processo: pronto é rodar no simulador; publicação por leva | [ADR-008](../decisions/ADR-008-processo-de-entrega.md) |
| BASE-GLOBAL com regras codificadas substitui a fila de leads | [ADR-009](../decisions/ADR-009-base-global-e-codigos-de-regra.md) |

## 3. Levas

Cada leva é uma fatia vertical: começa no banco, passa pelo Java e termina numa tela verificada no simulador. **Toda leva fecha com o mesmo checklist:**
1. gates verdes;
2. mutações registradas;
3. prints das telas novas (carregado, vazio, erro);
4. revisão adversarial;
5. BASE-GLOBAL e este documento atualizados;
6. PR aberta.

| Leva | Entrega | Pronto quando | Tamanho | Status |
| --- | --- | --- | --- | --- |
| **L0** Fundação e método | revisão do Java aplicada; cliente HTTP e diagnóstico; `stack.sh` e `init-secrets.sh`; BASE-GLOBAL, ADRs e este documento; issues distribuídas | diagnóstico mostra o mesmo `dealer_id` pelo Supabase e pelo Java; com o Java parado, a leitura continua | M | **em andamento** |
| **L1** Núcleo, seed, João | relógio; veículo, catálogos, pessoas e consentimento; aposentar tabelas antigas; `app_customers`, `search_customers`, `app_customer_file`; seed determinístico (800 VINs e o João); abas Clientes e Ficha v1 | a Maria busca "João" e vê o Ka 2014 com a revisão às vésperas do limite; outra concessionária não acha nada | G | a fazer |
| **L2** Cérebro e Hoje | parâmetros versionados; `brain_runs`; fatos; ETQ, TRM, REC com guardas; grupo de controle; rodada noturna; `app_today`; Hoje, tela 33, card de ação | rodada de quarta 02h: ficha do João com Esquecido 78, motivos e "WhatsApp com cupom (automático)" | G | a fazer |
| **L3** Contato | tarefas, tentativas, telefone cifrado, auditoria imutável; comandos no Java; telas 35, 42, 43; posse e pendentes | a Maria liga para o João, registra "não atendeu" e vê na linha do tempo | G | a fazer |
| **L4** Agenda e DMS simulado | agendamentos, cupom, cardápio; HMAC e principal de integração; SOAP `RecordServiceEvent`; `dms-sim`; telas 44, 60, 61, 62 | agenda para sexta; o `dms-sim` confirma por SOAP; a rodada seguinte muda a etiqueta | G | a fazer |
| **L5** Conversas sem n8n | conversas, mensagens, status, modelos, menu, links, sinais de engajamento; TRM-I e K; REC-2 e 3; outbox; telas 50, 51, 52 | injeção das 09h47; às 11h a Maria vê "começou a responder há 1h", assume e responde | G | a fazer |
| **L6** Canal simulado | n8n fixado; `fwd-channel-out` e `fwd-channel-in`; wa-sim com UI e personas; contrato em JSON Schema; dispatcher ligado | a mensagem do automático chega pelo n8n no wa-sim, e a resposta aparece sozinha no app | G | a fazer |
| **L7** Automação | disparo das proativas; confirmação e resgate; horários, tetos, pausa; opt-out propagado; falhas do canal; anonimização v2; telas 12 e 34 | o cupom do João sai sem script; a persona que manda SAIR fica sem automação | M | a fazer |
| **L8** Ciclo fechado | atribuição; APR com Wilson e Newcombe; histórico de campanhas; Meu desempenho; telas 71 e 73 | sábado 02h: João Fiel 22; o cartão "o que funciona" aparece com números | M | a fazer |
| **L9** Notificações, offline, acessibilidade | central, lembrete local, push simulado; cache sem telefone nem conversa; acessibilidade; Hoje em menos de 2 s; Android | a resposta do João vira push; em modo avião, Hoje abre do cache com aviso | G | a fazer |
| **L10** Demo e evidências | `demo:reset` e `demo:script` com asserções; vídeo; evidências por disciplina; docs finais | o roteiro passa duas vezes seguidas a partir do reset | M | a fazer |

**Esforço estimado:** cerca de 300 h no total. A divisão por pessoa está em [EQUIPE-E-TAREFAS](./EQUIPE-E-TAREFAS.md). O ritmo real é medido depois da L1 e esta tabela é recalibrada.

**Cortes que sempre deixam uma demo rodando:**

| Corte | Levas | O que a demo mostra |
| --- | --- | --- |
| 1. Loop manual | L0 a L4 | cérebro, Hoje, ficha, ligar, agendar, comparecimento por SOAP, etiqueta mudando depois do serviço |
| 2. Conversa com o automático | L5 e L6 | o WhatsApp simulado de ponta a ponta pelo n8n |
| 3. Ciclo fechado | L7 e L8 | automação e aprendizado |
| 4. Acabamento | L9 e L10 | notificações, offline, vídeo final |

## 4. Dívidas conhecidas

Na ordem em que vão doer.

| Dívida | Origem | Quando resolver |
| --- | --- | --- |
| Nada publicado: três branches só locais (há `git bundle` de backup) | L0 | fim da L0, com PR por repo |
| `AuthFilter` roda antes do rate limit e do `X-Request-Id`: 401 sai sem id de requisição e token inválido não é limitado | revisão do Java, achado baixo não aplicado | L3 (exige desligar o registro duplo dos filtros) |
| `/ready` consulta o banco sem timeout curto: com o banco inalcançável, cada probe espera cerca de 11 s | revisão do Java, achado baixo | L3 |
| Composes antigos do forward-infra (`docker/`) ainda citam `postgres` e `INTERNAL_API_KEY` | revisão do Java | L1 (remover) |
| `forward-docs/api/openapi.yaml` espelha o contrato da Sprint 1 | contrato mudou na branch do Java | quando a branch do Java entrar na `main` |
| 6 pares de contraste abaixo do alvo no tema claro | tokens portados 1:1 | L9 |
| Supabase cloud desativado (NXDOMAIN) | pausa do projeto | quando o Jota reativar |

## 5. Lições que custaram caro

| Lição | O que fazer |
| --- | --- |
| No iOS, fonte embutida é achada pelo nome PostScript, não pelo nome do arquivo; o erro não aparece, cai calado na fonte do sistema | teste lê o nome de dentro do `.ttf` |
| O native stack pinta o fundo com o tema do React Navigation (claro) mesmo com conteúdo transparente | tema de navegação montado com a paleta do app |
| Consultar o Supabase dentro do `onAuthStateChange` trava o supabase-js | adiar para o próximo tick |
| Build iOS e Docker juntos num Mac de 16 GB fizeram o macOS matar a VM do Docker | `stack.sh pre-build-ios` antes de build nativo |
| Leitura prévia sob RLS pode ser mais estreita que a policy de escrita (a visita a outra concessionária virava 404) | deixar a FK e a policy decidirem |
| Teste que compara a classe com a própria constante não prova nada | teste usa o literal |
| Chrome headless esquecido por scripts consumiu um núcleo por 35 dias | matar processos de verificação no fim |

## 6. Como rodar

Passo a passo em [guides/RODAR-LOCAL.md](../guides/RODAR-LOCAL.md). O resumo, com os três repos clonados lado a lado:

```bash
cd forward-infra
npm install
npm run secrets:init
npm run stack:up
cd ../forward-mobile && npm install && npx expo run:ios
```

## 7. Histórico de levas

| Data | Leva | O que aconteceu |
| --- | --- | --- |
| 12/09/2026 | rebuild | decisão de refazer o app, Supabase como plataforma, Java mantido pela disciplina de SOA |
| 13/09/2026 | L0 | ideia final do produto; plano do app da Maria aprovado; revisão do Java aplicada; cliente HTTP; stack local em um comando; esta documentação; issues distribuídas |
