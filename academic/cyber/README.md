# Cybersecurity — Entrega Sprint 1

![disciplina](https://img.shields.io/badge/disciplina-Cybersecurity-darkred?style=flat-square)
![prof](https://img.shields.io/badge/prof-Vitor-blue?style=flat-square)
![data](https://img.shields.io/badge/entrega-2026--05--24-brightgreen?style=flat-square)

> Documentação de segurança do ForwardService para a disciplina Cybersecurity do Desafio 02 Ford-FIAP 2026.

## Sumário

| Doc | Conteúdo | Para que serve |
|---|---|---|
| [01_THREAT_MODEL.md](./01_THREAT_MODEL.md) | STRIDE aplicado em cada componente (edge, AuthFilter, services, dados); ativos protegidos; superfície de ataque com diagrama Mermaid; riscos residuais aceitos | Provar que a arquitetura foi pensada com ameaça modelada |
| [02_OWASP_TOP10.md](./02_OWASP_TOP10.md) | OWASP Top 10 2021 mapeado linha-a-linha ao código (`A01`...`A10`); pontuação por critério da rubrica | Provar conformidade categórica e justificar decisão de substituir OWASP Dependency-Check por Trivy + Dependabot |
| [03_SECURITY_PLAN.md](./03_SECURITY_PLAN.md) | Postura atual + roadmap priorizado (R1...R12) + compliance LGPD + inventário de controles versionados + procedimento operacional | Documentar o "como" continuar evoluindo a postura após Sprint 1 |

## Pontuação estimada (100 pts)

| Critério (Prof. Vitor) | Estimativa |
|---|---|
| 1. Validação entrada (20) | **20/20** |
| 2. AuthN/AuthZ (20) | **20/20** |
| 3. Proteção API (20) | **20/20** (incluindo HMAC opcional 5 pts) |
| 4. Dados/Privacidade (25) | **22/25** |
| 5. Logs/Auditoria (15) | **13/15** |
| **TOTAL** | **95/100** |

## Highlights da implementação

- **AuthN flexível:** JWT HS256 + JWKS, escolhido pelo header `alg` do token; também aceita `X-API-Key` para server-to-server.
- **HMAC opcional implementado:** `HMAC_SHA256(secret, "<ts>:<METHOD>:<path>:<sha256(body)>")` com replay protection e comparação constant-time. Cobre os 5 pts opcionais da rubrica.
- **RLS Postgres:** defense-in-depth — mesmo se o service falhar, o banco bloqueia.
- **LGPD:** função `anonymize_customer()` + reaper diário com cooling-off de 30 dias.
- **Audit log append-only:** `REVOKE UPDATE, DELETE FROM PUBLIC` no DDL.
- **Sem OWASP Dependency-Check:** substituído por Trivy filesystem (gate CRITICAL/HIGH) + Dependabot. Histórico documentado em [02_OWASP_TOP10.md §A06](./02_OWASP_TOP10.md#a062021--vulnerable-and-outdated-components).
