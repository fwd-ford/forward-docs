# Decisões de arquitetura (ADRs)

Cada decisão que custa caro reverter tem um registro: contexto, decisão, consequências e alternativas. ADR aceita não se edita para mudar de ideia; escreve-se uma nova que a substitui.

| ADR | Decisão | Data |
| --- | --- | --- |
| [001](./ADR-001-leitura-rls-comando-java.md) | O app lê o Supabase sob RLS; todo comando passa pelo Java | 12/09/2026 |
| [002](./ADR-002-cerebro-v1-regras-no-banco.md) | Cérebro v1 em regras no banco; ML depois só no termômetro | 13/09/2026 |
| [003](./ADR-003-whatsapp-simulado.md) | WhatsApp só simulado, com o contrato da Cloud API | 13/09/2026 |
| [004](./ADR-004-escopo-maria-celular.md) | Primeiro só a Maria, no celular | 13/09/2026 |
| [005](./ADR-005-relogio-e-viagem-no-tempo.md) | Relógio do sistema e viagem no tempo | 13/09/2026 |
| [006](./ADR-006-onde-vivem-n8n-e-simuladores.md) | n8n, simuladores e scripts de demo no forward-infra | 13/09/2026 |
| [007](./ADR-007-supabase-local-sem-fly.md) | Supabase local agora, sem Fly, hospedagem adiada | 12/09/2026 |
| [008](./ADR-008-processo-de-entrega.md) | Processo de entrega | 13/09/2026 |
| [009](./ADR-009-base-global-e-codigos-de-regra.md) | BASE-GLOBAL com regras codificadas | 13/09/2026 |

Modelo para uma nova ADR:

```markdown
# ADR-NNN: título curto

- **Status:** proposta | aceita | substituída por ADR-NNN
- **Data:** dd/mm/aaaa
- **Decisores:** quem

## Contexto
## Decisão
## Consequências
## Alternativas consideradas
```
