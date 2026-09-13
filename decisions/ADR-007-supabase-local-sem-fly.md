# ADR-007: Supabase local agora, sem Fly, hospedagem adiada

- **Status:** aceita
- **Data:** 12/09/2026
- **Decisores:** Jota

## Contexto

Em 12/09/2026:
- o projeto Supabase da Sprint 1 respondia NXDOMAIN (pausado);
- o Java no Fly.io rodava uma imagem que não era a `main`, com o banco fora.

O desenvolvimento migrou de uma máquina Windows para um Mac.

## Decisão

- **Fly.io abandonado:** nenhum deploy, redeploy ou custo ali.
- **Desenvolvimento na stack local:** Supabase CLI (Postgres 17, Auth, PostgREST), Java em Docker, app no simulador.
- **Supabase cloud:** volta quando o Jota reativar o projeto, aplicando as migrations com dump prévio.
- **Hospedagem pública do Java e do n8n:** fica para depois (decisão D4 do plano de rebuild).

## Consequências

- Toda verificação acontece na stack local (`stack.sh up`), reproduzível por qualquer pessoa do grupo.
- A demo roda num notebook. O limite de memória do Docker e a parada do Java antes de build iOS estão documentados.
- Enquanto não houver cloud, colegas precisam da stack local para ver o app.
