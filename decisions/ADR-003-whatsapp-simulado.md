# ADR-003: WhatsApp só simulado, com o contrato da Cloud API

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota

## Contexto

A ideia do produto tem o n8n conversando com o cliente pelo WhatsApp. O número de produção exige verificação do Meta Business com CNPJ, templates aprovados e custo por mensagem. O sandbox tem limite baixo. O projeto é acadêmico e não tem concessionária real.

## Decisão

- O canal WhatsApp é **simulado**. Um simulador (wa-sim) faz o papel da Meta e do celular do cliente, no formato da WhatsApp Cloud API: envio, status `sent`, `delivered` e `read`, interativos e códigos de erro.
- O **n8n é real** e executa o transporte: webhook assinado do Java para o wa-sim, e webhook do wa-sim para o Java.
- As regras do canal são **reais** e moram no banco:
  - janela de 24 h;
  - categorias utilidade e marketing;
  - limites de frequência;
  - opt-out;
  - dono da conversa (automático ou humano).
- A decisão do menu automático também mora no banco (`bot_intents`), e o n8n só transporta.
- O contrato é versionado em JSON Schema com fixtures no formato da Meta.

## Consequências

- A demo roda sem internet e sem conta Meta, de forma reproduzível.
- Ir para o real é trocar a URL base para `graph.facebook.com` e verificar `X-Hub-Signature-256`.
- O app mostra o selo "canal simulado" em todo build, para ninguém confundir com o real.
- A ideia original dizia que o cliente "nem sabe que falou com um sistema". A política atual do WhatsApp exige caminho claro para humano, por isso a interface chama o executor de "Automático" e há passagem para a consultora.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Número de teste da Meta com os celulares do grupo | dependência externa e limite de destinatários; descartado pelo Jota |
| Número de produção verificado | exige CNPJ, aprovação e custo; só faz sentido com concessionária real |
