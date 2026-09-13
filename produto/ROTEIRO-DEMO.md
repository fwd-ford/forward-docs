# ForwardService: roteiro da demo (um dia da Maria)

> A história do produto contada como **teste de aceite**. Cada passo tem o que acontece, onde se vê e o que precisa ser verdade no banco.
> Regras citadas pelo código estão na [BASE-GLOBAL](./BASE-GLOBAL.md).

## A história

João Silva comprou um Ka 2014 na concessionária. Anos depois, sumiu: não fez a última revisão, não responde campanha, não atende ligação. Para a Ford, virou um número numa planilha; para a concessionária, prejuízo.

**Quarta, 02h.** A plataforma não dorme. O cérebro acorda, lê o banco e reetiqueta os clientes. João, que ontem era Fiel, vira **Esquecido**, e o termômetro sobe para **78**, porque a próxima revisão dele venceu ontem.

**09h12.** O recomendador olha para o João: Esquecido, risco 78, sem app, última conversa há 8 meses. Decide mandar WhatsApp com cupom de 20% na revisão e avisar a concessionária de que há uma ação aberta.

**09h13.** O n8n, braço executor do sistema, dispara a mensagem.

**09h47.** João responde "quanto fica pra rodar tudo?". O automático manda o cardápio da revisão e um link curto. Cada clique volta para o banco, e o termômetro já mexe: **78 → 73 → 71**. Ele está engajando.

**11h.** Maria, consultora da concessionária, abre o app. No topo: *João Silva, Esquecido, risco 71, começou a responder no WhatsApp há 1 h. Próxima ação: ligar e fechar o agendamento da revisão.* Ela liga, marca para sexta às 9h e registra "agendou" uma vez só.

**Sexta.** João faz a revisão.

**Sábado, 02h.** O cérebro acorda de novo. João muda de Esquecido para **Fiel**, e o termômetro cai para **22**. O ciclo fechou, e o dado dessa conversão alimenta o próprio cérebro: ele aprende que WhatsApp com cupom funciona para Esquecidos de risco 70 a 80.

> A ideia original dizia "sexta, 02h" depois do serviço de sexta, o que é impossível. O roteiro usa o sábado.

## O João nos dados

| Fato | Valor |
| --- | --- |
| Veículo | Ka 2014 SE 1.0, descontinuado, garantia encerrada em 2017, cerca de 700 km por mês |
| Histórico | 5 revisões em 4 anos, intervalos de 180, 220, 256 e 400 dias (média 264) |
| Concessionárias | 3 visitas na principal, 2 em outra; a última foi fora (share 0,6) |
| Contato | WhatsApp de serviço e de marketing concedidos pelo próprio canal |
| Última conversa de mão dupla | 240 dias antes (cerca de 8 meses) |
| Na quarta | 396 dias sem revisão, S 1,084, revisão vencida no dia anterior (fim da tolerância) |

## Passo a passo com asserções

`npm run demo:script -- --until Pn` executa os passos até `Pn` e confere o banco. As ações da Maria são feitas no simulador iOS, com print de cada tela.

| Passo | Relógio | Quem | O que acontece | Tem que ser verdade | Onde se vê |
| --- | --- | --- | --- | --- | --- |
| P0 | terça 23h | demo | `demo:reset` | estado inicial com o mesmo hash do ensaio anterior; João Fiel | login da Maria |
| P1 | quarta 02h | rodada noturna | ETQ, TRM, REC | João **Esquecido** (ETQ-4, vencida); termômetro **78** (A 26, B 11, C 9, D 7, E 5, F 10, G 0, H 10); rodada registrada | ficha 30 e tela 33 |
| P2 | quarta 02h | recomendador | REC-12 | ação `wa_offer_marketing`, executor automático, consentimento ok, cupom emitido, envio com `not_before` 09h; notificação para a concessionária | tela 12 "O automático hoje" |
| P3 | quarta 09h13 | Java, n8n e wa-sim | despacho | mensagem de modelo de marketing entregue; recomendação `dispatched` | conversa 51 com a bolha do automático |
| P4 | quarta 09h47 e 09h50 | persona João no wa-sim | responde, recebe o cardápio, clica | janela aberta até quinta 09h47; termômetro **73** e depois **71** (TRM-I); tarefa `call_close_booking` da Maria (REC-2); automação encerrada; notificação "respondeu" | Hoje 10 com "começou a responder há 1 h" |
| P5 | quarta 11h | Maria | abre Hoje, a ficha e a conversa | nenhuma escrita | prints de 10, 30 (71 com −7) e 51 |
| P6 | quarta 11h02 a 11h06 | Maria | liga, registra "atendeu, agendou" para sexta 9h com o cupom | tentativa e revelação do telefone auditadas; agendamento `booked`; cupom reservado; termômetro **51**; confirmação agendada para quinta (REC-4) | 42, 43, 44 e agenda 60 |
| P7 | quinta 09h | automático | confirmação de utilidade | mensagem entregue | conversa 51 |
| P8 | sexta 09h | `dms-sim` por SOAP | `RecordServiceEvent` | evento de serviço; agendamento `showed`; cupom resgatado | agenda 61 "compareceu" |
| P9 | sábado 02h | rodada e APR | ETQ, TRM, APR | João **Fiel** (ETQ-5); termômetro **22**; nenhuma proativa por 30 dias (REC-G7); atribuição preenchida | ficha 30 e Meu desempenho 71 |
| P10 | qualquer | outra concessionária e auditoria | isolamento | `agent.b` não vê nada do João; `audit_log` com P1, P6 e P8; nenhum telefone em log | Hoje vazia do `agent.b` |

## Como ensaiar

1. `npm run stack:up` no forward-infra. Na L6 em diante, sobe junto o perfil com n8n e wa-sim.
2. `npm run demo:reset`: banco recriado, seed determinístico, modo demo ligado, relógio na terça 23h.
3. Abrir o app no simulador e entrar como a Maria.
4. Avançar passo a passo com `npm run demo:script -- --until P1`, depois `P4`, e assim por diante. Na quarta 09h47, a resposta do João sai do wa-sim (a persona responde sozinha) ou é injetada pelo script.
5. Tirar os prints indicados em cada passo.
6. Rodar tudo duas vezes seguidas a partir do reset. Só assim o roteiro está pronto.

Antes da L10, cada leva roda o roteiro até onde já existe (versão reduzida). Qualquer data de entrega encontra uma demo que funciona.
