# ADR-006: n8n, simuladores e scripts de demo moram no forward-infra

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota

## Contexto

O produto precisa, além do banco, de peças executáveis locais:
- n8n com os workflows;
- simulador de WhatsApp com a UI do celular do cliente;
- simulador de DMS (REST e SOAP);
- scripts de reset e roteiro da demo.

Os workflows antigos estão em `forward-docs/n8n-workflows/`, um repo de documentação sem nada executável.

## Decisão

| Peça | Local |
| --- | --- |
| Compose do n8n (versão fixada por digest), workflows em JSON normalizado, wa-sim, personas | `forward-infra/automation/` |
| `dms-sim` | `forward-infra/tools/` |
| `demo:reset` e `demo:script` | `forward-infra/scripts/demo/` |

- Os dois workflows antigos do forward-docs são arquivados na L6, com um README apontando o novo lugar.

## Consequências

- Um repo só sobe a stack inteira (`stack.sh`).
- Workflows passam a ter lint: sem segredo literal, sem `pinData`, sem host fixo.
- O CI do forward-infra ganha os testes do wa-sim e o smoke de import do n8n.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| forward-docs | não tem nada executável nem CI de código |
| Repo novo | mais CI e onboarding, sem ganho |
