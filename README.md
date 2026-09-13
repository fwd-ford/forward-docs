# forward-docs

![org](https://img.shields.io/badge/org-fwd--ford-blue?style=flat-square)
![type](https://img.shields.io/badge/type-documentation-lightgrey?style=flat-square)

Product specification, decisions, research, academic deliverables and API specs for **ForwardService**, Ford Challenge FIAP 2026.

## Start here

The product was rebuilt in September 2026. The current specification lives in [`produto/`](./produto/):

| Document | What it answers |
| --- | --- |
| [produto/BASE-GLOBAL.md](./produto/BASE-GLOBAL.md) | What the app is: glossary, domain, the brain (label, thermometer, suggested action), coded rules, screen map |
| [produto/ROTEIRO-DEMO.md](./produto/ROTEIRO-DEMO.md) | The Maria and João story as an acceptance test |
| [produto/ESTADO-E-PLANO.md](./produto/ESTADO-E-PLANO.md) | What exists today, the delivery batches (L0 to L10), debts and lessons |
| [produto/EQUIPE-E-TAREFAS.md](./produto/EQUIPE-E-TAREFAS.md) | Who does what, effort split and the GitHub epics |
| [guides/RODAR-LOCAL.md](./guides/RODAR-LOCAL.md) | Run database, API and app on your machine |
| [decisions/](./decisions/) | Architecture Decision Records |

## Structure

```text
produto/          # Current product specification, plan, team and batch records (pt-BR)
decisions/        # Architecture Decision Records (ADRs)
guides/           # How-to guides (running locally, API keys)
project/          # Research and Sprint 1 design (base, research results, solution design)
academic/         # Academic deliverables per discipline
  pitch/          # Presentation slides
  canvas/         # Business Canvas
  togaf/          # Archi .archimate file
  video/          # Pitch video link/script
  cyber/          # Cybersecurity documentation
api/              # OpenAPI specs
n8n-workflows/    # Sprint 1 workflows (superseded, see ADR-006)
```

## Related repos

| Repo | Stack | Purpose |
|---|---|---|
| [forward-mobile](https://github.com/fwd-ford/forward-mobile) | React Native, Expo SDK 57 | App for the dealership consultant |
| [forward-api-java](https://github.com/fwd-ford/forward-api-java) | Java 17, Spring Boot 3.5 | Service layer: REST and SOAP commands under the caller's RLS claims, integrations |
| [forward-infra](https://github.com/fwd-ford/forward-infra) | Supabase, PostgreSQL, Docker | Schema, Row Level Security, the brain rules, local stack, n8n and simulators |
| [forward-ml](https://github.com/fwd-ford/forward-ml) | Python | Dataset features, segmentation, ML thermometer track |
| [forward-web](https://github.com/fwd-ford/forward-web) | SvelteKit | Ford web cockpit (future) |
