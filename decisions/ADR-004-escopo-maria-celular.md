# ADR-004: primeiro só a Maria, no celular

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota

## Contexto

A ideia completa tem quatro superfícies:
- a consultora no app (Maria);
- o cliente no mesmo app, em modo cliente (João);
- o gerente da concessionária;
- o cockpit web da Ford (Carlos).

Construir tudo ao mesmo tempo dilui o caminho crítico.

## Decisão

O plano detalha só o app da consultora (papel `dealer_agent`) no celular. Ficam **mapeados**, sem tela detalhada:
- tablet em dois painéis;
- gerente da concessionária no app;
- modo cliente;
- cockpit web.

## Consequências

O desenho de hoje deixa espaço para cada superfície futura:

| Superfície futura | Espaço deixado |
| --- | --- |
| Tablet | telas de detalhe e folhas são rotas com id |
| Gerente | o papel `dealer_manager` já existe no RLS; métricas são views |
| Modo cliente | `customers.user_id`; agendamento, conversa e consentimento são as mesmas entidades |
| Cockpit | eventos estruturados com carimbo de tempo alimentam views agregadas |

- Nada mapeado vira tela "em breve" no app.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Maria no tablet desde já | aumenta layout e teste antes de o caminho crítico existir |
| Incluir gerente e modo cliente | dobra o escopo; ficam como frentes futuras |
