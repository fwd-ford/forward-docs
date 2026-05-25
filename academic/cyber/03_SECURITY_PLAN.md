# Plano de Segurança — ForwardService

![status](https://img.shields.io/badge/status-Sprint_1-brightgreen?style=flat-square)
![data](https://img.shields.io/badge/atualizado-2026--05--24-blue?style=flat-square)
![escopo](https://img.shields.io/badge/escopo-Sprint_1_a_3-orange?style=flat-square)

> **Para quem é:** Prof. Vitor (Cybersecurity), avaliadores do Sprint 1, mantenedores futuros.
>
> **Objetivo:** documentar a estratégia de segurança do ForwardService, os controles que já estão implementados, e o roadmap dos próximos passos com priorização, dono e janela de execução.
>
> **Documentos relacionados:**
> - [01_THREAT_MODEL.md](./01_THREAT_MODEL.md) — análise STRIDE por componente
> - [02_OWASP_TOP10.md](./02_OWASP_TOP10.md) — mapeamento OWASP Top 10 2021 ao código

---

## 1. Princípios de segurança do produto

1. **Privacy by default.** PII só circula entre camadas que precisam dela. ML não recebe PII direta, só features derivadas do VIN_Hash já pseudonimizado pela Ford.
2. **Defense in depth.** Cada controle assume que o anterior pode falhar: AuthFilter + RBAC service + RLS Postgres + audit log.
3. **Fail secure.** Estados ambíguos viram 401 ou 403 com mensagem genérica; nunca 200 com payload parcial.
4. **Least privilege.** Roles distintas com permissões mínimas. `audit_log` é append-only por DDL, não por convenção.
5. **Auditability.** Toda ação destrutiva ou sensível deixa trilha. Correlation ID atravessa do edge até o banco.
6. **Reproducible posture.** Toda decisão de segurança vira código, configuração ou migration versionada — não documento solto.

---

## 2. Postura atual (resumo por categoria)

### 2.1 Validação de entrada (rubrica 20 pts)
- Regex RFC 4122 para UUID, ISO 3779 para VIN.
- Enum whitelist explícita.
- Bounds em parâmetros numéricos.
- Body limit 1MB (Tomcat) com env override.
- Bean Validation + handler RFC 7807 sem stack trace.

**Status:** ✅ pronto. Detalhes em [02_OWASP_TOP10.md A03](./02_OWASP_TOP10.md#a032021--injection).

### 2.2 AuthN e AuthZ (rubrica 20 pts)
- JWT Supabase via HS256 ou JWKS, escolhido pelo header `alg`.
- `X-API-Key` para chamadas server-to-server (N8N).
- `AuthPrincipal` por request, sem ThreadLocal global.
- RBAC inline em service + RLS Postgres em paralelo.

**Status:** ✅ pronto. Detalhes em [02_OWASP_TOP10.md A01, A07](./02_OWASP_TOP10.md#a012021--broken-access-control).

### 2.3 Proteção API (rubrica 20 pts)
- `force_https = true` no edge Fly.io.
- HSTS, CSP lockdown, X-Frame-Options DENY, Permissions-Policy restritivo.
- CORS allowlist explícita, nunca `*`.
- Rate limit Bucket4j 60 req/min por IP+sub.
- HMAC-SHA256 com timestamp + 5 min skew + constant-time compare (5 pts opcionais).

**Status:** ✅ pronto. Detalhes em [02_OWASP_TOP10.md A02, A05, A08](./02_OWASP_TOP10.md#a022021--cryptographic-failures).

### 2.4 Dados e privacidade (rubrica 25 pts)
- VIN pré-pseudonimizado pela Ford com SHA1 (5M reversões = 0 hits).
- AES-256 em repouso no Supabase storage layer.
- Função `anonymize_customer(uuid)` preserva FK setando PII para NULL.
- Reaper diário `anonymize_expired_customers()` com cooling-off de 30 dias.
- Direito ao esquecimento via `lgpd_deletion_requested_at`.

**Status:** ✅ pronto. Risco residual: field-level encryption aplicacional (R2).

### 2.5 Logs e auditoria (rubrica 15 pts)
- JSON estruturado via Logstash encoder em produção.
- `X-Request-Id` em MDC + response header.
- Tabela `audit_log` append-only com REVOKE de UPDATE/DELETE.
- Cada anonimização registrada com `reason` e `at`.

**Status:** ✅ pronto. Risco residual: cobertura de audit_log para CRUD comum (R4) e PII masking em log (R3).

---

## 3. Roadmap

Itens marcados como **risco residual aceito** no [01_THREAT_MODEL.md §6](./01_THREAT_MODEL.md#6-riscos-residuais-aceitos-para-sprint-1). Aqui consolidamos prioridade, esforço e janela.

| ID | Item | Prioridade | Esforço | Janela | Critério de pronto |
| --- | --- | --- | --- | --- | --- |
| R1 | Migrar RBAC inline para `@PreAuthorize` declarativo | P2 | 1 dia | Sprint 2 | Todos os endpoints anotados; testes de RBAC verdes |
| R2 | Field-level encryption (Hibernate `@Converter` ou Jasypt) para CPF/e-mail/telefone | P1 | 2 dias | Sprint 2 | DB dump não revela PII em claro |
| R3 | `MaskingPatternLayout` no Logback para mascarar CPF/e-mail/telefone em logs | P1 | 0.5 dia | Sprint 2 | Grep no Loki/Fly logs por CPF de fixture retorna 0 hits |
| R4 | Expansão de `audit_log` para CRUD sensível (ler customer, criar service event, atualizar lead status) | P2 | 1 dia | Sprint 2 | 5 ações principais com cobertura via `@AuditAction` aspect |
| R5 | Migrar Bucket4j de in-memory para Redis | P3 | 1 dia | Quando escalar > 1 instância | Rate limit consistente entre instâncias |
| R6 | `X-API-Key` constant-time via `MessageDigest.isEqual` | P3 | 1 hora | Sprint 2 | Comparação não vaza em microbench timing |
| R7 | Avaliar WAF (Cloudflare Free) na borda | P3 | 0.5 dia | Pré-lançamento público | Regras OWASP Core Rule Set ativas |
| R8 | SSRF protections caso N8N receba webhooks customizáveis | P3 | 1 dia | Quando viabilizar feature | Allowlist + reject de IPs privados |
| R9 | Habilitar HMAC obrigatório em endpoints sensíveis (criação de service event via N8N) | P2 | 0.5 dia | Sprint 2 | Endpoints retornam 401 sem assinatura válida |
| R10 | Mergear PR [`.github#3`](https://github.com/fwd-ford/.github/pull/3) para remover job OWASP DC do workflow compartilhado | P3 | 5 min | Sprint 2 | Workflow sem job dependency-check |
| R11 | Adicionar `lgpd_consent_at` no fluxo de signup do mobile (já modelado no banco) | P1 | 0.5 dia | Sprint 2 | Cliente novo registra consentimento; reaper de 12m passa a ter dado |
| R12 | Threat model review trimestral | P2 | 2 horas | Recorrente | Documento atualizado por trimestre |

**Prioridade:**
- **P1** = bloqueia conformidade plena com LGPD ou OWASP Top 10
- **P2** = melhoria de postura ou auditoria, sem risco imediato
- **P3** = otimização ou cenário futuro

---

## 4. Compliance LGPD

| Artigo / requisito | Implementação |
| --- | --- |
| Art. 5 — base legal e consentimento | Coluna `lgpd_consent_at` em `customers`; mobile precisa coletar (R11) |
| Art. 16 — eliminação após término | Reaper `anonymize_expired_customers()` diário ([013](https://github.com/fwd-ford/forward-infra/blob/main/supabase/migrations/013_lgpd_retention_policy.sql)) |
| Art. 18 — direitos do titular (deletion request) | `lgpd_deletion_requested_at` + cooling-off 30d + `anonymize_customer()` |
| Art. 37 — registro de operações | `audit_log` append-only com `actor_id`, `action`, `resource_*`, `created_at` |
| Art. 46 — segurança (medidas técnicas) | TLS, HSTS, AES-256 em repouso, JWT assinado, rate limit, RLS |
| Art. 48 — comunicação de incidente | Procedimento P0 em [01_THREAT_MODEL.md §7](./01_THREAT_MODEL.md#7-procedimento-de-resposta-a-incidente-resumo): notificação ANPD em 72h |

**Encarregado de dados (DPO):** não atribuído — Sprint 1 é piloto sem dados reais de cliente final. Quando o piloto evoluir para produção com dados reais, formalizar DPO antes do go-live.

---

## 5. Inventário de controles versionados

Todos os controles abaixo são código ou configuração versionada — nada é "manual operacional".

| Controle | Tipo | Arquivo |
| --- | --- | --- |
| Force HTTPS | Config | [fly.toml:18](https://github.com/fwd-ford/forward-api-java/blob/main/fly.toml) |
| Security headers | Filter | [SecurityHeadersFilter.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/web/SecurityHeadersFilter.java) |
| CORS allowlist | Config + Bean | [CorsConfig.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/web/CorsConfig.java) + [fly.toml:11](https://github.com/fwd-ford/forward-api-java/blob/main/fly.toml) |
| Spring Security chain | Bean | [SecurityConfig.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/security/SecurityConfig.java) |
| JWT validators (HS256, JWKS, Alg-aware) | Class | [security/](https://github.com/fwd-ford/forward-api-java/tree/main/src/main/java/com/fwdford/forwardapi/security) |
| Auth filter | Filter | [AuthFilter.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/security/AuthFilter.java) |
| Rate limit | Filter | [RateLimitFilter.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/security/RateLimitFilter.java) |
| HMAC validator | Class | [HmacValidator.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/security/HmacValidator.java) |
| Input validation | Class | [Validations.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/web/Validations.java) |
| Request ID | Filter | [RequestIdFilter.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/web/RequestIdFilter.java) |
| Global exception handler | Advice | [GlobalExceptionHandler.java](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/java/com/fwdford/forwardapi/error/GlobalExceptionHandler.java) |
| RLS Postgres | Migration | [010_rls_policies.sql](https://github.com/fwd-ford/forward-infra/blob/main/supabase/migrations/010_rls_policies.sql) |
| Audit log | Migration | [009_create_audit_log.sql](https://github.com/fwd-ford/forward-infra/blob/main/supabase/migrations/009_create_audit_log.sql) |
| LGPD retention | Migration | [013_lgpd_retention_policy.sql](https://github.com/fwd-ford/forward-infra/blob/main/supabase/migrations/013_lgpd_retention_policy.sql) |
| JSON logs | Config | [logback-spring.xml](https://github.com/fwd-ford/forward-api-java/blob/main/src/main/resources/logback-spring.xml) |
| CI security scan | Workflow | [java-security.yml](https://github.com/fwd-ford/.github/blob/main/.github/workflows/java-security.yml) |
| Secret scan | Workflow | [secrets-scan.yml](https://github.com/fwd-ford/.github/blob/main/.github/workflows/secrets-scan.yml) |
| Dependabot | Config | configurado por repo |

---

## 6. Métricas de segurança (objetivos)

Métricas que devem ser medidas continuamente em produção. Para Sprint 1 são alvos; instrumentação completa entra no Sprint 2.

| Métrica | Alvo Sprint 1 | Alvo Sprint 2 |
| --- | --- | --- |
| % requests com `X-Request-Id` correlacionável end-to-end | 100% | 100% (já garantido por filtro) |
| Tempo entre CVE CRITICAL publicado e PR aberto | < 7 dias | < 24h (Dependabot + Trivy) |
| Tempo médio para anonimizar request LGPD | manual | < 30 dias (reaper diário) |
| % endpoints autenticados com rate limit aplicado | 100% | 100% |
| % endpoints `/api/v1/*` cobertos por teste de RBAC | 60% | 100% |
| Vazamentos de stack trace em prod | 0 | 0 |
| Cobertura de `audit_log` em ações sensíveis | anonimização | 5 ações principais (CRUD sensível) |
| MTTR para resposta a incidente P0 (vazamento PII) | < 24h | < 4h |

---

## 7. Procedimento operacional

### 7.1 Adicionar novo endpoint

Checklist obrigatório antes de mergear PR que adiciona endpoint REST ou SOAP:

1. [ ] Path adicionado ao `openapi.yaml`.
2. [ ] DTO de entrada com Bean Validation ou validação via `Validations.*`.
3. [ ] Service valida `AuthPrincipal` antes de retornar dados sensíveis.
4. [ ] Repository usa `NamedParameterJdbcTemplate` parametrizado.
5. [ ] Se ação é destrutiva ou sensível, insere linha em `audit_log`.
6. [ ] Se acessa nova tabela, RLS policy adicionada em migration nova.
7. [ ] Teste unit cobre caso autenticado E não autenticado.
8. [ ] CORS allowlist coberta para a origem que vai chamar (mobile/web).

### 7.2 Rotação de segredo

Procedimento para `SUPABASE_JWT_SECRET`, `INTERNAL_API_KEY`, ou senha de banco:

1. Gerar novo valor (`openssl rand -hex 32` para chaves simétricas).
2. `flyctl secrets set NOME=valor` (Fly.io faz rolling restart).
3. Atualizar callers (N8N workflow para `INTERNAL_API_KEY`).
4. Validar com smoke test em `/api/v1/me`.
5. Após confirmação de propagação, revogar valor antigo no Supabase.
6. Registrar rotação em `audit_log` com `action=rotate_secret, resource_type=env_var`.

### 7.3 Resposta a incidente

Ver [01_THREAT_MODEL.md §7](./01_THREAT_MODEL.md#7-procedimento-de-resposta-a-incidente-resumo).

---

## 8. Pendências para fechamento do Sprint 1

| # | Item | Status | Quem |
| --- | --- | --- | --- |
| 1 | Threat model documentado | ✅ pronto | Cyber |
| 2 | OWASP Top 10 mapeado | ✅ pronto | Cyber |
| 3 | Plano de segurança (este doc) | ✅ pronto | Cyber |
| 4 | Demonstrar HMAC funcional via teste | ✅ ([HmacValidatorTest](https://github.com/fwd-ford/forward-api-java/tree/main/src/test/java)) | já existente |
| 5 | Demonstrar reaper LGPD em execução local | ⚠️ rodar `SELECT anonymize_expired_customers();` em DB com fixture | Quem fizer demo |
| 6 | Vídeo de pitch: incluir slide rápido sobre LGPD + RLS + audit_log | ⚠️ pendente | Quem grava pitch |

---

## 9. Referências

- [01_THREAT_MODEL.md](./01_THREAT_MODEL.md)
- [02_OWASP_TOP10.md](./02_OWASP_TOP10.md)
- LGPD Lei 13.709/2018
- [OWASP ASVS 4.0](https://owasp.org/www-project-application-security-verification-standard/)
- [CIS Controls v8](https://www.cisecurity.org/controls/cis-controls-list)
- [NIST 800-53 r5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf)
- [Spring Security 6 reference](https://docs.spring.io/spring-security/reference/)
- [Bucket4j docs](https://bucket4j.com/)
- [Fly.io secrets](https://fly.io/docs/reference/secrets/)
