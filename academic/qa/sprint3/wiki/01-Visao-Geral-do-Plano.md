# Visão geral do plano ForwardService

ForwardService: plataforma de retenção pós-venda para a rede Ford (Desafio 02, VIN Share). Score de churn por VIN, leads priorizados para o atendente e ações proativas medidas de ponta a ponta. Challenge FIAP x Ford 2026, turma 3ESPZ, Engenharia de Software.

Processo: **Scrum**. Fonte única do plano: `forward-docs/academic/qa/sprint3/backlog.json`, publicado por `azure_devops_import.py` (REST API 7.1).

## Time

| Integrante | RM | Papel |
| --- | --- | --- |
| João Victor Franco | 556790 | Líder técnico e Scrum Master; Mobile |
| Lucca Saraiva Borges | 554608 | ML e dados |
| Ruan Melo Vieira | 557599 | Backend e SOA |
| Rodrigo César Jimenez | 558148 | Product Owner; QA e produto |

## Números do backlog

| Nível | Quantidade |
| --- | --- |
| Épicos | 8 |
| Features | 21 |
| PBIs | 60 |
| Tarefas da Sprint 3 | 34 |

## Sprints

| Sprint | Início | Fim | Status | Pontos | Objetivo |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 | 02/03/2026 | 19/04/2026 | Concluída | 49 | Descoberta e fundação: pesquisa validada, visão de produto, arquitetura-alvo e base técnica (repositórios, CI, banco e scaffolds). |
| Sprint 2 | 20/04/2026 | 24/05/2026 | Concluída | 52 | MVP demonstrável: API REST/SOAP, app do atendente, pipeline de ML e artefatos de negócio e arquitetura TOGAF/ArchiMate. |
| Sprint 3 | 03/08/2026 | 27/09/2026 | Em andamento | 56 | Segurança e qualidade de ponta a ponta: JWT e RBAC próprios, contrato REST nível 2, testes com evidência, app em release APK, DevSecOps e plano no Azure DevOps. |
| Sprint 4 | 28/09/2026 | 11/10/2026 | Planejada | 49 | Entrega final do Challenge: vídeo pitch técnico, ambiente de demonstração estável e hardening final. |
| Sprint 5 | 12/10/2026 | 08/11/2026 | Planejada | 52 | Piloto com ação: Action Engine no WhatsApp, Performance Console e monitoramento em produção. |
| Sprint 6 | 09/11/2026 | 06/12/2026 | Planejada | 52 | Ciclo fechado: agendamento, Recall Gateway, ROI, recomendador por ML e LGPD completa. |

## Como navegar

- **Boards > Backlogs**: PBIs na ordem de implementação; troque o nível para Features ou Epics no seletor.
- Itens concluídos (Sprints 1 e 2) ficam ocultos no backlog; ligue **View options > Completed child items** ou use as consultas abaixo.
- **Boards > Sprints**: backlog e taskboard da Sprint 3 com as tarefas, horas restantes e responsáveis.
- **Boards > Queries > Shared Queries > ForwardService - Plano**: consultas prontas.

## Páginas desta wiki

- Definition of Done
- Critérios de Priorização (MoSCoW) e Estimativa (Planning Poker)
- Release Plan e Roadmap
- Sprint 3 — Detalhamento
- Rastreabilidade TOGAF e ArchiMate
- BDD — Guia de Critérios de Aceite
