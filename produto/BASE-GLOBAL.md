# ForwardService: base global do app da Maria

> Documento mestre do produto. Diz **o que** o app é e **quais regras** ele segue.
> Onde estamos e em que ordem se constrói fica no [ESTADO-E-PLANO](./ESTADO-E-PLANO.md).
> Versão 1.0, 13/09/2026. Substitui o domínio "fila de leads por veículo" do plano de rebuild de 12/09; arquitetura, stack e modelo de acesso daquele plano continuam valendo.

Toda regra tem um código (`ETQ-4`, `REC-12`, `CNV-2`). O código aparece no comentário da migration, na descrição do teste e no `@DisplayName` do Java. Mudou a regra, muda o texto aqui e se procura o código no resto. Número nunca é reaproveitado; regra revogada fica riscada com a data e o motivo. Mudar um limiar cria nova versão de parâmetro com o mesmo código.

## Sumário

1. [O produto em uma página](#1-o-produto-em-uma-página)
2. [Glossário canônico](#2-glossário-canônico)
3. [Modelo de domínio](#3-modelo-de-domínio)
4. [O cérebro: etiqueta, termômetro e ação](#4-o-cérebro-etiqueta-termômetro-e-ação)
5. [Regras do app](#5-regras-do-app)
6. [Mapa de telas e caminho crítico](#6-mapa-de-telas-e-caminho-crítico)
7. [Integrações](#7-integrações)
8. [Real, simulado e mapeado](#8-real-simulado-e-mapeado)
9. [Fora de escopo](#9-fora-de-escopo)
10. [Decisões abertas](#10-decisões-abertas)
11. [Riscos](#11-riscos)

---

## 1. O produto em uma página

**A ideia.** Todo cliente Ford carrega três coisas grudadas nele o tempo todo:

| | O que é | Exemplo |
| --- | --- | --- |
| **Etiqueta** | que tipo de cliente ele é | Esquecido |
| **Termômetro** | quão perto está de sumir, de 0 a 100 | risco 78 |
| **Ação sugerida** | o que fazer com ele agora | ligar e fechar a revisão |

Um cérebro de três camadas recalcula as três de madrugada. O n8n executa as ações automáticas (WhatsApp). A consultora da concessionária, a **Maria**, usa o app para saber com quem falar, ver o que o automático já conversou, ligar, agendar e registrar o resultado uma vez só. O ciclo fecha quando o cliente volta e vira Fiel, e esse dado ensina o cérebro.

**O que o app é.** O celular de trabalho da consultora de pós-venda. Ela abre e o app diz com quem falar agora, por quê e o que já foi dito para esse cliente.

**A frase que define tudo:** *ele não te dá uma lista de clientes, ele te diz com quem falar agora.*

**O buraco que preenche.**

| Hoje | Por que falha |
| --- | --- |
| Sistema da oficina (DMS) | guarda cadastro e ordem de serviço, não prioriza ninguém |
| Planilha e ligação a frio | queima tempo com quem não vai voltar |
| WhatsApp pessoal da atendente | não deixa rastro, ignora consentimento e duplica o que o automático já fez |

**Para quem.** A consultora (papel `dealer_agent`) de uma concessionária piloto, no celular, no dia a dia. Tablet, gerente, cliente e cockpit web da Ford ficam para depois ([seção 9](#9-fora-de-escopo)).

**A restrição que define o resto.** O dado oficial da Ford não tem nome nem telefone de cliente: as identidades são sintéticas e marcadas como tal, e o WhatsApp é simulado. Por isso a honestidade é regra: o selo "canal simulado" aparece sempre, e nada finge ser real.

**A pergunta que decide o projeto.** *A Maria consegue, sem planilha, sair do "começou a responder há 1h" até o "compareceu" num roteiro que roda duas vezes seguidas a partir do reset?* Ver [ROTEIRO-DEMO](./ROTEIRO-DEMO.md).

---

## 2. Glossário canônico

Nome trocado no meio do caminho custa refactor e bug de interpretação. Na interface, a palavra "lead" não aparece: quem vende é o cérebro, quem retém é a consultora.

| Termo | Definição |
| --- | --- |
| Cliente | A pessoa, dona de um ou mais veículos. Sintética na v1 |
| Veículo | O carro; é a unidade do cérebro. Identificado por `vehicle_key` (pseudônimo). VIN e placa não aparecem no app |
| Etiqueta | Perfil histórico do veículo: Novo, Econômico, Fiel, Esquecido, Abandono. Diz quem ele é, não o destino dele |
| Termômetro | 0 a 100, soma de componentes com motivo. Tem faixa (Baixo, Médio, Alto, Crítico), frescor e tendência |
| Severidade (S) | Quanto a revisão passou do prazo Ford: `max(km_desde / intervalo_km, meses_desde / 12)` |
| Ação sugerida | Recomendação do cérebro para o veículo, uma ativa por vez, com executor: automático, Maria ou ninguém |
| Tarefa | Ação que cabe a um humano, na lista da Maria: começar, adiar, descartar |
| Automático | O executor sem humano (n8n + canal). É o nome que aparece na interface |
| Conversa | Fio por cliente e canal, com dono (automático ou Maria), janela de 24 h e mensagens |
| Janela | 24 h desde a última mensagem do cliente. Fora dela, só modelo aprovado |
| Modelo (template) | Mensagem pré-aprovada: **utilidade** (lembrete, recall, confirmação) ou **marketing** (cupom, desconto) |
| Toque | Qualquer contato iniciado pela concessionária, mensagem ou ligação |
| Tentativa | Uma ligação (ou contato presencial) registrada, com resultado |
| Resultado | Código fechado do contato: não atendeu, agendou, número errado, entre outros |
| Agendamento | Horário marcado na oficina: marcado, confirmado, remarcado, cancelado, compareceu, não compareceu |
| Comparecimento | Confirmação de que o serviço aconteceu. Vira evento de serviço e fecha o ciclo |
| Consentimento | Ledger por canal e finalidade (serviço, recall, marketing): concedido ou revogado, com origem e versão do texto |
| Grupo de controle | 10% dos clientes que nunca recebem ação proativa, para medir o que funciona |
| Rodada | Execução noturna do cérebro para uma data (`p_today`) |

---

## 3. Modelo de domínio

```text
Concessionária ── Consultora (membership)
Cliente ─┬─ Pontos de contato (telefone mascarado) ── Consentimentos (ledger)
         └─ Veículo ─┬─ Eventos de serviço (histórico) ── Plano de manutenção do modelo
                     ├─ Recall elegível
                     ├─ Fatos derivados (S, vencimento, hábito, rede)
                     ├─ Etiquetas (histórico) · Termômetro (leituras) · Recomendações
                     ├─ Tarefas ── Tentativas ── Resultado
                     ├─ Agendamentos (ledger) ── Cupom
                     └─ Conversa ── Mensagens ── Status · Cliques · Sinais de engajamento
```

Quatro decisões escondidas aí:

1. **A regra mora no banco.** Etiqueta, termômetro, recomendação, janela, consentimento e guardas são funções SQL testadas com pgTAP. O app mostra o que o banco decidiu; o Java executa comandos chamando funções `private.cmd_*`, e REST e SOAP chamam a mesma função.
2. **Ledgers append-only.** Consentimento, etiqueta, leituras do termômetro, mensagens, status, agendamentos e tentativas são eventos. O estado atual é derivado, nunca um contador sobrescrito.
3. **Data local explícita.** O banco roda em UTC. Toda função de regra recebe `p_today` ou `p_now`; nenhuma usa `now()` ou `current_date` fora de `private.clock_now()`.
4. **Toda escrita passa por uma função com guarda de escopo.** O papel `forward_api` do Java não escreve direto em tabela; cada `cmd_*` é `SECURITY DEFINER`, fixa `search_path` e confere a concessionária do chamador.

### 3.1 Tabelas por domínio

"L" marca ledger append-only. Identificadores em inglês, como exige o forward-infra.

| Domínio | Tabelas |
| --- | --- |
| Veículo e catálogos | `vehicle_models`, `maintenance_plans`, `maintenance_plan_steps`, `service_menu_items`, `vehicles`, `vehicle_status_events` L, `service_events` L, `recall_campaigns`, `recall_campaign_vehicles`, `dealer_channels`, `holidays` |
| Pessoas e consentimento | `customers`, `contact_points`, `consent_texts` L, `consent_events` L, `lgpd_requests` L, `profiles` |
| Cérebro | `private.brain_rule_versions` L, `private.brain_runs` L, `vehicle_facts`, `label_assignments` L, `private.thermometer_engines`, `thermometer_readings` L, `holdout_assignments` L, `action_catalog`, `recommendations`, `recommendation_outcomes` |
| Trabalho humano | `tasks`, `task_events` L, `contact_attempts` L, `automation_pauses` L, `notifications` L, `notification_reads` L |
| Conversas | `conversations`, `conversation_owner_events` L, `conversation_reads`, `messages` L, `message_status_events` L, `message_templates`, `bot_intents`, `short_links` L, `link_clicks` L, `engagement_events` L |
| Ofertas e agenda | `offers`, `coupons` L, `coupon_events` L, `appointments`, `appointment_events` L |
| Integração e segurança | `private.integration_clients`, `private.idempotency_keys`, `private.inbound_webhook_receipts`, `private.outbox_dispatches`, `security_events` L, `audit_log` L |

Das tabelas da Sprint 1, saem `leads`, `lead_outcomes`, `communications` e `churn_scores`; `service_orders` se divide em `service_events` e `appointments`; `customers` perde CPF, telefone e opt-ins (que viram `contact_points` e `consent_events`). O modelo de acesso (`private.memberships`, helpers, `my_context`, `forward_api` sem BYPASSRLS) fica.

### 3.2 O que o app lê

Views `security_invoker`, com escopo da concessionária inteira. O app só tem `SELECT`.

| View | Tela | O essencial |
| --- | --- | --- |
| `app_today` | Hoje | trio (etiqueta, termômetro, ação), motivo, último engajamento, conversa esperando, agendamento de hoje, ordem |
| `app_customers` + `search_customers(q)` | Clientes | busca por nome, final do telefone, chave e modelo (termo no corpo do POST, nunca na URL) |
| `app_customer_file` | Ficha | cabeçalho, veículo e ciclo de vida, cérebro com componentes, ação e tarefa, consentimento, estado da automação, agendamento, recall, cupom |
| `app_timeline` | Linha do tempo | todo evento com ator e horário |
| `app_conversations`, `app_messages` | Conversas | dono, SLA, janela, status de cada mensagem, cliques |
| `app_agenda` | Agenda | horário, status, serviços, orçamento, cupom |
| `app_service_menu` | Agendar | itens e preços da próxima revisão, com e sem cupom |
| `app_automation_schedule` | O automático | o que vai sair hoje, para quem, por qual regra |
| `app_my_performance` | Meu desempenho | agendados que compareceram, taxas, tempo até a primeira ação |
| `app_notifications` | Central | eventos para a consultora |
| `my_context` | Login | papel, concessionária, nome |

---

## 4. O cérebro: etiqueta, termômetro e ação

Três camadas, cada uma simples, rodando juntas de madrugada. Na v1 as três são regras explicáveis. O ML entra depois trocando só o termômetro (TRM-L), sem mudar app nem tabelas.

### 4.1 Fatos por veículo

Calculados em `vehicle_facts` com data de referência `p_today`.

| Fato | Definição |
| --- | --- |
| `n` | número de eventos de serviço |
| `dias_desde` | dias desde a última revisão |
| `gap_avg`, `gap_last` | intervalo médio entre revisões; último intervalo |
| `share` | fração das visitas na concessionária principal |
| `kpm` | km por mês: do histórico, senão da venda, senão a mediana do modelo; limitado a 100..8000 |
| S | severidade (glossário) |
| `due_on` | última revisão + o menor entre prazo por tempo e prazo por km |
| tolerância | 30 dias, ou 1.000 km convertidos em dias (regra Ford) |
| `vencida` | `p_today > due_limit_on` |
| `at_risk_open` | `n ≥ 2` e `dias_desde > 1,5 × gap_avg` e `dias_desde > 90` |
| `k` | número da próxima revisão |
| faixas de S | < 0,8 · 0,8 a 1,0 · 1,0 a 1,3 · 1,3 a 1,7 · 1,7 a 2,5 · > 2,5 |

### 4.2 ETQ: etiqueta

A primeira regra que casar vale. A etiqueta só é gravada quando muda.

| Código | Etiqueta | Condição (parâmetros v1) |
| --- | --- | --- |
| **ETQ-0** | nenhuma | veículo inativo, ou cliente anonimizado ou com pedido de exclusão |
| **ETQ-1** | Novo | vendido há menos de 365 dias, ou `n = 0` e vendido há menos de 540 dias |
| **ETQ-2** | Abandono | `n = 1` e mais de 540 dias; `n = 0` e vendido há 540 dias ou mais; ou, com o parâmetro ligado, `n ≥ 2`, S ≥ 2,5 e mais de 540 dias |
| **ETQ-3** | Econômico | `n = 1` (demais casos) |
| **ETQ-4** | Esquecido | `n ≥ 2` e (vencida, ou `at_risk_open`, ou `share < 0,6` com S ≥ 0,8) |
| **ETQ-5** | Fiel | `n ≥ 2` (demais casos) |

"Quase indo embora" não é etiqueta: é termômetro alto. As etiquetas são as quatro personas do K-means do forward-ml mais "Novo", agora por regra. Medido nos 175.554 VINs (referência 04/05/2026), com abandono multievento ligado: Abandono 40,5%, Econômico 11,5%, Esquecido 17,5%, Fiel 24,3%, Novo 6,2%. O K-means dava 11,5 / 17,2 / 25,2 / 46,0. **Não chamar a etiqueta de "rótulo do ML".**

### 4.3 TRM: termômetro

`valor = clamp(0, 100, BASE + ENGAJ)`, com `BASE = A + B + C + D + E + F + G + H`.

| Código | Componente | Faixa | Regra |
| --- | --- | --- | --- |
| **TRM-A** | Atraso | 0 a 45 | interpolação em S: (0; 0), (0,5; 4), (0,8; 10), (1,0; 24), (1,3; 32), (1,7; 38), (2,5; 45) |
| **TRM-B** | Hábito | 0 a 15 | com `n ≥ 2` e mais de 90 dias: `r = dias_desde / gap_avg` em (1; 0), (1,5; 8), (2; 12); +3 se `gap_last > 1,5 × média` |
| **TRM-C** | Rede | 0 a 12 | `round(15 × (1 − share))`, +3 se a última visita foi fora da principal |
| **TRM-D** | Curva da Morte | 0 a 8 | pela perda na revisão `k`: 6, 6, 7, 8, 7, 7 (31% → 22% → 15% → 9,5% → 6,5% no dado oficial) |
| **TRM-E** | Garantia | 0 a 8 | 8 se acabou entre 365 dias atrás e daqui a 90; 5 se acabou antes |
| **TRM-F** | Produto | 0 a 10 | descontinuado: 6; idade ≥ 10 anos: +4; 8 a 9 anos: +2 |
| **TRM-G** | Recall | 0 a 5 | 5 se o recall pendente tem mais de 180 dias; 2 se menos |
| **TRM-H** | Relação | 0 a 10 | 10 sem interação de mão dupla em 180 dias; +3 se faltou a agendamento em 90 dias |
| **TRM-I** | Engajamento | −30 a 0 | resposta em 48 h: −5. Clique em 48 h: −2 cada, até −4. Pedido de agendamento em 7 dias: −8. Agendamento futuro ativo: −20. Compareceu em 30 dias: −5 |

- **TRM-J** Faixas: Baixo 0 a 39, Médio 40 a 59, Alto 60 a 79, Crítico 80 a 100. Leitura noturna com mais de 30 h fica `stale` e a automação para (guarda G12).
- **TRM-K** Durante o dia, `trm_on_event` congela A a H da noite, recalcula só o engajamento com o horário do evento e grava nova leitura (idempotente por evento). É o que faz o 78 virar 71 às 09h47.
- **TRM-L** Contrato do ML: leitura com `engine = model`, `valor = round(100 × p calibrada)`, primeiro em modo sombra, comparada pela APR. O engajamento continua por regra.

**Números-ouro do João (teste de aceite):**

| Momento | A | B | C | D | E | F | G | H | I | Total | Etiqueta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Quarta 02h | 26 | 11 | 9 | 7 | 5 | 10 | 0 | 10 | 0 | **78** | Esquecido (vencida ontem) |
| Quarta 09h47, respondeu | | | | | | | | | −5 | **73** | |
| Quarta 09h50, clicou | | | | | | | | | −7 | **71** | |
| Quarta 11h06, agendou | | | | | | | | | −27 | **51** | |
| Sábado 02h, depois da revisão | 0 | 0 | 5 | 7 | 5 | 10 | 0 | 0 | −5 | **22** | Fiel |

### 4.4 REC: recomendador

**Catálogo de ações.**

| Ação | Executor | Canal e categoria | Prioridade base | Validade | Cooldown |
| --- | --- | --- | --- | --- | --- |
| `wa_reminder_utility` | automático | WhatsApp, utilidade | 40 | D+2 | 21 dias |
| `wa_offer_marketing` | automático | WhatsApp, marketing com cupom e botão "Parar promoções" | 50 | D+2 | 30 dias |
| `wa_recall_utility` | automático | WhatsApp, utilidade | 70 | D+3 | 14 dias |
| `wa_confirm_appointment` | automático | WhatsApp, utilidade | 60 | até o horário | 1 vez |
| `call_customer` | Maria | ligação | 60 | 5 dias úteis | 14 dias |
| `call_recovery` | Maria | ligação | 65 | 5 dias úteis | 30 dias |
| `call_close_booking` | Maria | ligação | 90 | 48 h | nenhum |
| `call_recall` | Maria | ligação | 75 | 5 dias úteis | 14 dias |
| `reply_conversation` | Maria | texto livre na janela | 95 | SLA 15 min | nenhum |
| `rescue_no_show` | Maria | ligação ou WhatsApp | 85 | 72 h | 1 vez |
| `confirm_appointment_call` | Maria | ligação | 55 | horário −2 h | 1 vez |
| `sales_opportunity` | Maria (informativa) | nenhum | 10 | 30 dias | 180 dias |
| `hold` | ninguém | nenhum | 0 | próxima noite | |

**Regras reativas** (disparadas por evento, fora do grupo de controle):

| Código | Gatilho | Ação |
| --- | --- | --- |
| **REC-1** | recall pendente (nunca vai para o grupo de controle) | `wa_recall_utility`; sem WhatsApp, `call_recall` |
| **REC-2** | resposta, botão, clique ou pedido de agendamento em 48 h, sem agendamento | `call_close_booking`, notifica a Maria e encerra a automação |
| **REC-3** | conversa marcada como precisando de humano | `reply_conversation` |
| **REC-4** | agendou | `wa_confirm_appointment` 24 h antes; sem consentimento, `confirm_appointment_call` |
| **REC-5** | não compareceu | `rescue_no_show` |

**Regras proativas** (de madrugada, sujeitas ao grupo de controle):

| Código | Condição | Ação |
| --- | --- | --- |
| **REC-10** | Novo, S entre 0,8 e 1,3 | lembrete de utilidade (nunca marketing) |
| **REC-11** | S entre 0,8 e 1,0 | lembrete |
| **REC-12** | S entre 1,0 e 1,3, Esquecido, faixa Alta ou maior, marketing permitido, oferta vigente | oferta com cupom (a manhã do João) |
| **REC-13** | S entre 1,0 e 1,3, sem REC-12 | lembrete; sem WhatsApp e faixa Média ou maior, ligação |
| **REC-14** | S entre 1,3 e 1,7 | `call_customer` |
| **REC-15** | S entre 1,7 e 2,5, faixa Alta ou maior | `call_recovery`; depois de 2 "não atendeu", oferta ou `hold` |
| **REC-16** | S > 2,5 ou Abandono | `hold` ("não vale gastar") |
| **REC-17** | Fiel, faixa Baixa, veículo antigo ou descontinuado | `sales_opportunity` |

**Guardas.** Recusa grava a recomendação como `suppressed` com o motivo.

| Guarda | Regra |
| --- | --- |
| **REC-G1** | veículo ativo |
| **REC-G2** | grupo de controle suprime as proativas |
| **REC-G3** | `can_contact(canal, finalidade)` (ver CNS) |
| **REC-G4** | contato válido |
| **REC-G5** | automação só por modelo; texto livre só dentro da janela |
| **REC-G6** | frequência: 1 toque iniciado pela empresa em 7 dias, 2 de marketing em 30, 4 no total em 30 |
| **REC-G7** | cooldowns; "sem interesse" fecha marketing por 90 dias; comparecimento fecha as proativas por 30 dias |
| **REC-G8** | uma recomendação ativa por veículo; a de maior prioridade supera |
| **REC-G9** | agendamento ativo suprime tudo, salvo a confirmação |
| **REC-G10** | horário: seg a sex 8h a 20h, sáb 8h a 14h, sem domingo e feriado; automação a partir das 9h |
| **REC-G11** | até 25 tarefas novas por consultora por dia |
| **REC-G12** | termômetro atualizado |
| **REC-G13** | automação pausada pela concessionária para o cliente (recall continua) |

- Prioridade: `base + round(0,3 × termômetro) + min(10, preço da próxima revisão / 200)`.
- Grupo de controle: 10% por hash estável do `customer_id`, gravado no primeiro uso e nunca reembaralhado.
- Automação iniciada gera notificação para a concessionária ("o automático começou a cuidar de João").

### 4.5 APR: o que funciona

| Código | Regra |
| --- | --- |
| **APR-1** | Atribuição pelo último toque. Janelas a partir do envio: resposta e clique 72 h, agendamento 14 dias, comparecimento e receita 30 dias, opt-out 7 dias. O grupo de controle usa as mesmas janelas a partir da supressão |
| **APR-2** | Célula: versão da regra × ação × etiqueta × faixa de S × faixa de 10 pontos do termômetro, em 90 dias móveis, com mínimo de 30 tratados e 30 controles |
| **APR-3** | Wilson por taxa; intervalo do uplift por Newcombe. "Funciona" se o limite inferior do uplift de agendamento for > 0; "prejudica" se o superior for < 0 ou o opt-out passar de 2%; senão, inconclusivo |
| **APR-4** | Na v1, só relatório ("WhatsApp com cupom funciona para Esquecidos 70 a 80: X de Y voltaram"). Mudar regra é nova versão gravada por humano, auditada |

### 4.6 CNS: consentimento

| Código | Regra |
| --- | --- |
| **CNS-1** | Ledger por canal e finalidade; vale o último evento |
| **CNS-2** | WhatsApp serviço e recall exigem opt-in no canal; marketing exige opt-in de marketing com serviço não revogado |
| **CNS-3** | Ligação de serviço e recall por interesse legítimo, salvo revogação; ligação de marketing exige consentimento |
| **CNS-4** | "Não quer contato" revoga ligação e marketing em todos os canais, exceto recall |
| **CNS-5** | Revogação cancela na hora todo envio pendente do cliente, canal e finalidade, e suprime as recomendações |
| **CNS-6** | Consentimento de marketing só vem do titular (botão no canal); a consultora não registra marketing |
| **CNS-7** | O bloqueio acontece em três pontos: na recomendação, no enfileiramento (trigger) e de novo no envio |

### 4.7 Rodada noturna

`private.run_nightly_safe(p_today, p_force)`, em ordem:

1. advisory lock;
2. idempotência por `p_today`;
3. `p_now` = 02h de São Paulo;
4. expirar vencidos;
5. `build_vehicle_facts`;
6. `etq_assign`;
7. `trm_nightly`;
8. `rec_nightly` (tarefas, notificações, envios com `not_before` 09h);
9. contagens e auditoria.

Jobs no pg_cron (o banco roda em UTC): `fwd-nightly-brain` 02h00, `fwd-apr` 02h30, `fwd-expire` a cada 5 min, `fwd-retention` 03h00, `fwd-lgpd-reaper` 03h30, todos no horário de São Paulo. Em modo demo os jobs não fazem nada e os passos são disparados por comando (REL-4).

### 4.8 REL: relógio

| Código | Regra |
| --- | --- |
| **REL-1** | Toda função de regra recebe `p_today` ou `p_now` explícito; testes usam valor fixo |
| **REL-2** | O padrão vem de `private.clock_now()`: relógio real mais deslocamento, que só a ferramenta de demo altera, e só em modo demo |
| **REL-3** | O app calcula tempo relativo sobre o "agora" do servidor |
| **REL-4** | Em modo demo, pg_cron e gatilhos agendados do n8n ficam calados |
| **REL-5** | Segurança (JWT, HMAC, rate limit) usa o relógio real |
| **REL-6** | `authenticated` nunca executa função que aceite `p_today` nem mexe no relógio |

---

## 5. Regras do app

O que a tela garante. O cálculo mora no banco; aqui está como ele aparece e o que a consultora pode fazer.

### 5.1 Hoje e ficha

| Código | Regra | Por quê |
| --- | --- | --- |
| **HOJ-1** | Ordem: conversa esperando você, "começou a responder", pendentes de registro, agendamentos de hoje, depois tarefas por prioridade | o que esfria primeiro vem primeiro |
| **HOJ-2** | A linha mostra o trio (etiqueta, termômetro com tendência, ação) e uma frase de motivo | a ideia inteira numa linha |
| **HOJ-3** | Ao abrir, a tarefa fica com a consultora por 30 min sem atividade; a colega vê quem está com ela | duas pessoas não ligam para o mesmo cliente |
| **HOJ-4** | Tentativa sem resultado fica fixada no topo como "pendente de registro" | a fila não vira cemitério |
| **HOJ-5** | Alternância "Minhas" e "Concessionária" (leitura das colegas) | clareza sem bagunçar a posse |
| **HOJ-6** | Cliente do grupo de controle nunca aparece como tarefa proativa | medição honesta |
| **FIC-1** | Cabeçalho: nome, etiqueta neutra (sem cor de alarme), termômetro, faixa, tendência e "calculado hoje às 02h" | etiqueta é quem ele é, não destino |
| **FIC-2** | "Por que este termômetro": três motivos em português, componentes e "o que o sistema não sabe" | explicável, sem falsa precisão |
| **FIC-3** | Card da ação sugerida com Fazer, Adiar e Descartar; descartar exige motivo | a resposta à sugestão vira dado |
| **FIC-4** | "O automático está cuidando": o que já saiu, o próximo toque automático e o botão pausar | a consultora não duplica o automático |
| **FIC-5** | Veículo e ciclo de vida: próxima revisão com preço, garantia, recall, número da revisão, km estimado com a fonte | preço antes da ligação evita "custo surpresa" |
| **FIC-6** | Linha do tempo única com ator e horário | controle de tudo o que passou |

### 5.2 Contato e agenda

| Código | Regra | Por quê |
| --- | --- | --- |
| **CTT-1** | Ligar grava a tentativa e revela o telefone (auditado) antes de abrir o discador; com identidade sintética a ligação é simulada | nada se perde, nenhum número real |
| **CTT-2** | Resultado em 1 ou 2 toques, lista fechada de 12; cada um aplica a cadência (não atendeu = nova tentativa; número errado invalida o telefone; sem interesse pausa 90 dias; não quer contato vira opt-out) | dado canônico e rápido |
| **CTT-3** | "Agendou" abre a folha de agendamento e só fecha com agendamento gravado | "agendado" sem horário não existe |
| **CTT-4** | Desfazer por 6 s e corrigir no mesmo dia, sempre como novo evento | erro de toque sem apagar histórico |
| **CTT-5** | Contato de balcão registrável sem ligação (canal presencial) | o cérebro precisa saber |
| **AGD-1** | Agendar mostra o cardápio da próxima revisão, com preço com e sem cupom | transparência de valor |
| **AGD-2** | Agenda do dia e da semana; Compareceu ou Não compareceu com valor informado; qualquer consultora da loja registra e a dona é avisada | fecha o ciclo sem DMS |
| **AGD-3** | Não compareceu gera tarefa de resgate | taxa de comparecimento é o KPI |

### 5.3 Conversa

| Código | Regra | Por quê |
| --- | --- | --- |
| **CNV-1** | Bolhas por autor (cliente, automático, consultora, sistema), com status enviado, entregue, lido ou falhou, e o motivo | ver tudo o que o n8n fez |
| **CNV-2** | Estado da janela sempre visível ("fecha em 3h12"); fechada, o compositor vira seletor de modelos com a categoria | espelha a regra do WhatsApp |
| **CNV-3** | "Assumir conversa" cala o automático; volta sozinho após 4 h sem atividade ou por "Devolver ao automático" | passagem para humano é obrigatória |
| **CNV-4** | "Esperando você" com SLA de 15 min | resposta rápida converte |
| **CNV-5** | Cliques em link e botões aparecem na conversa como eventos | engajamento visível |
| **CNV-6** | Nada de texto gerado por IA; o automático é menu determinístico (`bot_intents`) | política do WhatsApp e auditoria |

### 5.4 Notificações, privacidade, desempenho, estados

| Código | Regra | Por quê |
| --- | --- | --- |
| **NTF-1** | Central in-app sempre; lembrete local; push remoto simulado no simulador | sem conta Apple paga |
| **NTF-2** | Tela bloqueada nunca mostra nome completo nem conteúdo de mensagem | privacidade |
| **NTF-3** | Notificações só no horário de trabalho da consultora (padrão 8h a 18h) | respeito |
| **PRV-1** | Telefone mascarado; revelação auditada, no máximo 30 por hora | exfiltração de lista é a ameaça modelada |
| **PRV-2** | Sem exportar, copiar lista ou compartilhar | LGPD |
| **PRV-3** | VIN e placa nunca aparecem; mostra `vehicle_key` curta e placa mascarada | pseudonimização |
| **DES-1** | Meu desempenho mede agendados que compareceram e receita, não ligações feitas | KPI certo |
| **DES-2** | Sem ranking entre consultoras | não incentivar volume |
| **EST-1** | Toda tela tem carregando, vazio, erro, erro com dado, sem rede, sem permissão, não encontrado e comando falhou | erro invisível vira lista vazia |
| **EST-2** | Sem rede: leitura do cache com "atualizado às HH:MM"; comandos desabilitados, exceto Ligar | UI otimista não pode mentir |
| **EST-3** | Faixa "os termômetros de hoje ainda não foram calculados" se a rodada falhou | falha noturna não pode parecer fila vazia |
| **DEM-1** | Selo "canal simulado" em todo build, dirigido por flag no banco | honestidade |
| **DEM-2** | Ferramentas de demo (relógio, rodada, injeção) só para admin e só em modo demo | nenhuma brecha em produção |

---

## 6. Mapa de telas e caminho crítico

Abas: **Hoje · Clientes · Conversas · Agenda · Eu**. Detalhes são rotas com id, sem barra de abas e com rodapé de ações em vidro. Folhas também são rotas, o que deixa o tablet em dois painéis pronto para depois. Um número dominante por tela.

| # | Tela | Número dominante | O que mostra e faz | Por que existe |
| --- | --- | --- | --- | --- |
| 01 | Entrar | nenhum | e-mail e senha | acesso |
| 02 | Recuperar senha | nenhum | link por e-mail | sem ele o reset morre |
| 03 | Sem acesso | nenhum | sem vínculo ou vínculo ilegível; tentar de novo; sair | o papel vem do banco |
| 10 | **Hoje** | **clientes para falar agora** | ordem HOJ-1, trio por linha, "começou a responder há 1h", pendentes, agendamentos de hoje | a tela do app |
| 11 | Central de notificações | não lidas | respondeu, automático começou, agendamento amanhã, falha de mensagem, colega pegou | nada escapa |
| 12 | O automático hoje | mensagens programadas | o que vai sair, para quem, por qual regra; pausar por cliente | confiança sem duplicar |
| 20 | **Clientes** | total no filtro | busca e filtros por etiqueta, faixa, recall, vencida, conversa | chegar em qualquer cliente |
| 30 | **Ficha do cliente** | **o termômetro** | FIC-1 a FIC-6; rodapé Ligar, Conversa, Registrar | onde a decisão acontece |
| 31 | Linha do tempo completa | eventos | paginada, filtro por tipo | controle total |
| 32 | Veículo e ciclo de vida | próxima revisão | plano, histórico, garantia, recall, km; vendeu o carro; oportunidade de venda | Curva da Morte e ponte serviço-venda |
| 33 | Por que este termômetro | o valor | componentes, tendência, o que não sabe, código da regra | explicável |
| 34 | Consentimentos | nenhum | por canal e finalidade, com origem e data; "não quer contato" | LGPD visível |
| 35 | Adiar ou descartar (folha) | nenhum | data ou motivo | resposta à sugestão |
| 42 | **Ligar** | nenhum | roteiro curto, motivo, preço; revelar e discar (ou simular) | contato auditado |
| 43 | **Registrar resultado** (folha) | nenhum | 12 resultados, retorno com data, nota | fecha a tentativa |
| 44 | **Agendar** (folha) | **preço com cupom** | dia e horário, serviços, orçamento, cupom, recall junto | "agendado" de verdade |
| 50 | **Conversas** | esperando você | dono, SLA, janela, prévia | não deixar cliente no vácuo |
| 51 | **Conversa** | **tempo de janela** | bolhas, status, cliques, assumir e devolver, compositor ou modelos | ver o que o n8n conversou |
| 52 | Escolher modelo (folha) | nenhum | modelos permitidos com categoria; indisponíveis com motivo | fora da janela |
| 60 | **Agenda** | agendamentos de hoje | dia e semana, confirmação | comparecimento |
| 61 | Agendamento | horário | serviços, cupom, histórico, confirmar, remarcar, cancelar | ciclo do agendamento |
| 62 | Registrar comparecimento (folha) | valor faturado | compareceu ou não, km, valor | fecha o ciclo |
| 70 | Eu | nenhum | perfil, aparência, idioma, horário de trabalho, sair | ajustes |
| 71 | Meu desempenho | agendados que compareceram | semana e mês, taxas, tempo até a primeira ação, "o que funciona" | KPI certo |
| 73 | Como o cérebro decide | nenhum | ETQ, TRM e REC em linguagem simples | confiança e onboarding |
| 80 | Diagnóstico (dev) | nenhum | `my_context` e `/me`, rodada, relógio | depuração |
| 81 | Painel de demo (dev e admin) | relógio | avançar relógio, rodar cérebro, abrir o simulador | ensaio em 3 minutos |

**Caminho crítico: 10 Hoje → 30 Ficha → 51 Conversa → 42 Ligar → 43 Resultado → 44 Agendar.** Seis telas. Se esse trecho estiver bom, o app está bom; se estiver ruim, nenhuma outra tela salva.

**Direção visual.** A do app da Sprint 1, refeita: tema escuro por padrão, Playfair Display (títulos editoriais, rótulos em itálico, números grandes) e Manrope (interface), superfícies de vidro, sobrelinha em caixa alta com título serifado, prioridade como selo, status como ponto, um botão primário por tela, alvos de 44 pt, tokens portados 1:1 com teste de paridade e contraste.

---

## 7. Integrações

### 7.1 Comandos da consultora

forward-api-java, REST com Bearer do Supabase. Todo POST exige `Idempotency-Key`; erro em `problem+json` com `code` estável; o app mostra só a tradução do `code`.

| Comando | Função no banco |
| --- | --- |
| `POST /api/v1/tasks/{id}/start`, `/snooze`, `/dismiss` | `cmd_task_*` |
| `POST /api/v1/contact-attempts` (ligação ou presencial) e `/{id}/outcome`, `/{id}/correction` | `cmd_contact_attempt_*` (revelação auditada) |
| `POST /api/v1/conversations/{id}/takeover`, `/release`, `/messages` | `cmd_conversation_*`, `cmd_send_free_form` |
| `POST /api/v1/customers/{id}/templates`, `/automation/pause` | `cmd_send_template`, `cmd_automation_pause` |
| `POST /api/v1/appointments`, `/{id}/reschedule`, `/cancel`, `/confirm`; `PATCH /{id}/attendance` | `cmd_appointment_*` |
| `POST /api/v1/consents` (só "não quer contato") | `cmd_record_consent` |
| `POST /api/v1/notifications/read` | `cmd_notifications_read` |
| `POST /api/v1/admin/brain-runs`, `/admin/demo/clock` (admin e modo demo) | `run_nightly_safe`, `demo_set_clock` |

### 7.2 Integração de máquina

| Código | Regra |
| --- | --- |
| **INT-1** | HMAC no protocolo do `HmacValidator` (`ts:METHOD:path?query:sha256(body)`, janela de 300 s) mais `X-Client-Id`, em `/api/v1/integrations/**` |
| **INT-2** | Cada integração é um principal em `private.integration_clients` com escopos (`n8n-channel-gateway`, `dms-simulator`, `system-dispatcher`, `ml-job`). Sem membership, nenhuma policy passa; só executa `ingest_*` e `claim_*`, que conferem escopo |
| **INT-3** | Entrada: `whatsapp/inbound` e `whatsapp/status` (formato `value` da Cloud API, deduplicação por id da mensagem), `links/clicks`, `service-events` (DMS) |
| **INT-4** | Saída: outbox no banco com guarda de consentimento; o `OutboxDispatcher` do Java faz claim com `SKIP LOCKED`, reaplica as guardas, monta o payload (telefone só aqui) e chama o webhook assinado do n8n |
| **INT-5** | Link curto `GET /l/{code}` público, com rate limit e sem gravar IP; o clique vira sinal de engajamento |
| **INT-6** | SOAP: `GetVehicle` (passa a aceitar `vehicle_key`) e `RecordServiceEvent`, que chama a mesma função do REST e fecha o agendamento como compareceu |

### 7.3 Canal simulado

| Código | Regra |
| --- | --- |
| **CAN-1** | wa-sim (Node) no formato da WhatsApp Cloud API: envio, status `sent`, `delivered`, `read`, interativos (botões e lista) e erros 131047, 131049, 131026, 131050 |
| **CAN-2** | n8n executa: `fwd-channel-out` (webhook do Java → wa-sim) e `fwd-channel-in` (webhook do wa-sim → verifica assinatura → Java assinado). Execuções bem-sucedidas não são salvas (guardariam telefone e texto) |
| **CAN-3** | UI "celular do cliente" com personas: João responde e clica; uma pede atendente; uma manda SAIR; uma fica muda; uma é número errado |
| **CAN-4** | Contrato versionado em JSON Schema com fixtures no formato da Meta, validado por Java, wa-sim e n8n. Ir para o real é trocar a URL base para `graph.facebook.com` e verificar `X-Hub-Signature-256` |

---

## 8. Real, simulado e mapeado

**Real** funciona de ponta a ponta localmente. **Simulado** tem o mesmo contrato com provedor falso. **Mapeado** está desenhado, sem tela provisória nem "em breve" no app.

| Capacidade | Status v1 |
| --- | --- |
| Login, papéis, RLS, auditoria, cifra do telefone | Real |
| Clientes e veículos | Simulado: 800 VINs da amostra do dataset oficial (concessionárias 5094 e 6137), eventos sintetizados coerentes com os agregados, identidades sintéticas |
| Plano de manutenção e preços | Real (fonte pública), faixa indicativa |
| Recall | Campanhas públicas; elegibilidade simulada |
| Etiqueta, termômetro, recomendador, APR | Real (regras) |
| ML no termômetro | Mapeado (contrato TRM-L) |
| Ligar | Comando real; discagem simulada para identidade sintética |
| Agendamento, agenda, comparecimento | Real; capacidade da oficina simulada |
| DMS | Simulado (`dms-sim` por REST com HMAC e SOAP) |
| WhatsApp | Simulado (wa-sim); janela, modelos, posse e consentimento são regras reais |
| n8n | Real (runtime local) |
| Notificação in-app e lembrete local | Real |
| Push remoto | Simulado (`simctl push`) |
| Offline de leitura | Real |
| Realtime, SMS, e-mail | Mapeado |
| Tablet, gerente no app, modo cliente, cockpit web | Mapeado |
| Hospedagem pública de Java e n8n; Supabase cloud | Mapeado |

---

## 9. Fora de escopo

**Fora do celular da Maria na v1:**

| Fora | Por quê |
| --- | --- |
| Disparo em massa | quem decide é o cérebro |
| Criar oferta ou desconto | autoridade de preço não é da consultora |
| Texto por IA | política do WhatsApp e auditoria |
| Exportar dados | LGPD |
| Editar nome e telefone do cliente | o dado não é da consultora |
| VoIP ou gravação de ligação | custo e LGPD |
| Mídia no WhatsApp | simulação só texto e botões |
| Fila offline genérica de comandos | conflito de posse |
| Ranking entre consultoras | incentiva volume |
| Globo e relógio da Home antiga | competem com o número dominante |

**Superfícies futuras, e como o desenho de hoje deixa espaço:**

| Superfície | Espaço deixado |
| --- | --- |
| Tablet em dois painéis | detalhes e folhas são rotas com id |
| Gerente da concessionária no app | papel `dealer_manager` já existe no RLS; métricas são views |
| Modo cliente (João) | `customers.user_id`; agendamento, conversa e consentimento são as mesmas entidades |
| Cockpit web Ford (Carlos) | eventos estruturados com carimbo de tempo alimentam views agregadas |
| WhatsApp real | contrato espelhado (CAN-4) |
| Termômetro por ML | contrato TRM-L |

---

## 10. Decisões abertas

Cada uma tem um padrão assumido pelo plano; mudar é decisão do grupo.

| # | Decisão | Padrão |
| --- | --- | --- |
| 1 | Abandono multievento ligado (40,5%) ou só evento único | ligado, com a comparação ao K-means documentada |
| 2 | Vencida com tolerância de 30 dias | sim |
| 3 | Consultora lê a concessionária inteira | sim, trabalho priorizado por dono |
| 4 | Ligação por interesse legítimo; marketing no WhatsApp só com opt-in pelo canal | sim |
| 5 | Grupo de controle de 10%, recall fora dele | sim |
| 6 | Limites de frequência e faixas 40, 60, 80 | mantém e mede |
| 7 | Garantia de 36 meses por modelo | marcada como assumida |
| 8 | Posse de 30 min, SLA de 15 min, dono humano por 4 h, desfazer em 6 s | sim |
| 9 | 5 abas com rótulo | sim |
| 10 | Push remoto | simulado; real exige conta Apple paga |
| 11 | Selo "canal simulado" também em build de produção | sim |
| 12 | Nome da outra concessionária na ficha | "outra concessionária Ford (cidade)" |
| 13 | Concessionária piloto | código 5094 com nome fictício |
| 14 | Textos e valores de cupom e dos modelos de mensagem | rascunho do produto, aprovação do Jota |

---

## 11. Riscos

| Risco | Mitigação |
| --- | --- |
| Escopo (cerca de 40 tabelas e 40 funções) contra o calendário | levas com cortes que sempre deixam uma demo rodando |
| Função `SECURITY DEFINER` sem guarda de escopo vira bypass | lint e matriz de comandos no pgTAP |
| `now()` escondido quebra a viagem no tempo | lint e regras REL |
| Banca ler "simulado" como falso | selo DEM-1, tabela da seção 8, demonstrar a troca de adaptador |
| Etiqueta por regra confundida com ML | nome "regras v1" e ponte explícita com o forward-ml |
| Duas consultoras no mesmo cliente | posse HOJ-3 |
| O automático e a consultora tocando o mesmo cliente | FIC-4, REC-2 encerra a automação, CNV-3 |
| Métrica que premia ligar muito | DES-1 e DES-2 |
| Discar para número sintético que pertence a alguém | CTT-1: ligação simulada |
| Rodada noturna falha em silêncio | EST-3 e `brain_runs` |
