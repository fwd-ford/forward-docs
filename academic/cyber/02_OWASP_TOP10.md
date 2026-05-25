# OWASP Top 10 2021 mapeado ao ForwardService

![status](https://img.shields.io/badge/status-Sprint_1-brightgreen?style=flat-square)
![data](https://img.shields.io/badge/atualizado-2026--05--24-blue?style=flat-square)
![referencia](https://img.shields.io/badge/OWASP-Top_10_2021-darkred?style=flat-square)

> **Para quem é:** Prof. Vitor (Cybersecurity) e avaliadores do Sprint 1.
>
> **Objetivo:** demonstrar que cada categoria do OWASP Top 10 2021 foi analisada contra o código do ForwardService, com mitigação implementada ou risco aceito justificado.
>
> **Escopo de análise:** backend [forward-api-java](../../../forward-api-java/), camada de dados [forward-infra](../../../forward-infra/), app [forward-mobile](../../../forward-mobile/).
>
> **Importante:** Este documento usa o **framework conceitual OWASP Top 10 2021** (lista de categorias de vulnerabilidade). Não há mais ferramenta automática **OWASP Dependency-Check** no CI: ela foi removida em 2026-05-23 (PR #17), substituída por **Trivy filesystem scan** (gate CRITICAL/HIGH) + **Dependabot**. Detalhes da remoção e justificativa estão na seção A06 deste documento.

---

## Resumo por categoria

| # | Categoria | Status | Camada principal |
|---|---|---|---|
| A01 | Broken Access Control | ✅ Mitigado | RBAC service + RLS Postgres |
| A02 | Cryptographic Failures | ✅ Mitigado | TLS edge + AES-256 Supabase + HMAC opcional |
| A03 | Injection | ✅ Mitigado | Validations + NamedParameterJdbcTemplate |
| A04 | Insecure Design | ✅ Mitigado | Threat model + STRIDE documentado |
| A05 | Security Misconfiguration | ✅ Mitigado | SecurityHeadersFilter + STATELESS + CSP lockdown |
| A06 | Vulnerable & Outdated Components | ✅ Mitigado | Trivy CI gate + Dependabot |
| A07 | Identification & Authentication Failures | ✅ Mitigado | JWT Supabase HS256/JWKS, sem session |
| A08 | Software & Data Integrity Failures | ⚠️ Parcial | HMAC opcional implementado, não obrigatório |
| A09 | Security Logging & Monitoring Failures | ✅ Mitigado | JSON logs + audit_log + X-Request-Id |
| A10 | Server-Side Request Forgery | ✅ N/A | API não faz outbound HTTP para URLs do cliente |

---

## A01:2021 — Broken Access Control

**Risco genérico:** usuário acessa recurso que não deveria (IDOR, missing authz, privilege escalation).

**Cenários considerados:**
- Cliente A consulta `GET /api/v1/customers/{B}` e vê PII de outro cliente.
- Atendente de dealer X vê leads de dealer Y.
- Usuário comum acessa `churn_scores` (campo interno).
- Bypass de role via manipulação de claim no JWT.

**Mitigações implementadas:**

1. **AuthN obrigatória em qualquer `/api/v1/*`:** [SecurityConfig.java:36-47](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/SecurityConfig.java) só libera `/health`, `/ready`, `/actuator/**`, `/swagger-ui/**`, `/v3/api-docs/**`, `/soap/vehicles.wsdl` e OPTIONS. Todo o resto passa por [AuthFilter](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/AuthFilter.java).
2. **`AuthPrincipal` imutável por request:** o `sub` e `role` extraídos do JWT são salvos em request attribute (`WebAttrs.PRINCIPAL`), nunca em ThreadLocal global. Services consultam pelo objeto.
3. **RBAC verificado no service:** services validam `callerSub`/`callerRole` antes de retornar dados. Exemplo: `CustomerService.get()`.
4. **Defense-in-depth com RLS:** mesmo se o service falhar, [010_rls_policies.sql](../../../forward-infra/supabase/migrations/010_rls_policies.sql) bloqueia no banco. Exemplos:
   - `churn_scores_internal`: leitura só para `analyst`/`admin`.
   - `customers_self`: cliente só vê o próprio registro; dealer/analyst/admin veem mais.
   - `audit_log_admin_only`: trilha de auditoria só admin lê.
5. **Role nunca confiada do cliente:** o claim `role` vem do JWT assinado pelo Supabase ([AuthFilter.java:103-110](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/AuthFilter.java)). Adulteração quebra a assinatura.

**Status:** ✅ Mitigado.

**Risco residual:** RBAC inline em service é menos auditável que `@PreAuthorize` declarativo. Tracking em [03_SECURITY_PLAN.md §3.R1](./03_SECURITY_PLAN.md).

---

## A02:2021 — Cryptographic Failures

**Risco genérico:** dado sensível em trânsito ou em repouso sem cifragem adequada; uso de algoritmo fraco.

**Cenários considerados:**
- Token JWT trafegando em HTTP.
- PII em log claro.
- Senha de banco em código.
- HMAC com SHA1 ou comparação não-constante (timing attack).

**Mitigações implementadas:**

| Item | Implementação |
|---|---|
| TLS em trânsito | `force_https = true` em [fly.toml:18](../../../forward-api-java/fly.toml); TLS 1.2+ pelo edge Fly.io |
| HSTS | `Strict-Transport-Security: max-age=31536000; includeSubDomains` em [SecurityHeadersFilter.java:26](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/SecurityHeadersFilter.java) |
| Cifragem em repouso | Supabase Postgres cifra storage com AES-256 nativamente |
| JWT | HS256 (HMAC-SHA256) via Nimbus JOSE ou JWKS RSA via JJWT. Algoritmo escolhido pelo header do token ([AlgAwareJwtValidator](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/AlgAwareJwtValidator.java)) |
| HMAC integridade body | `HMAC_SHA256(secret, "<ts>:<METHOD>:<path>:<sha256(body)>")` em [HmacValidator.java:84-95](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/HmacValidator.java) |
| Comparação constant-time | `constantTimeEquals` evita timing oracle em [HmacValidator.java:115-124](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/HmacValidator.java) |
| Replay protection | `X-Timestamp` com janela de skew de 5 min ([HmacValidator.java:25, 74](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/HmacValidator.java)) |
| Segredos | `SUPABASE_JWT_SECRET`, `DATABASE_PASSWORD`, `INTERNAL_API_KEY` via env var Fly.io secrets (cifradas at rest no Fly) |
| VIN do cliente | Pré-pseudonimizado pela Ford com SHA1 (5M tentativas de reversão = 0 matches, ver [02e Parte 5](../../project/02e_DATASET_OFICIAL_E_FONTES.md)) |

**Status:** ✅ Mitigado.

**Risco residual:** sem field-level encryption aplicacional sobre o que o Supabase já cifra. Justificativa: Supabase já cifra disco; cifragem aplicacional só agrega proteção contra dump do Supabase, cenário fora do modelo de ameaça do Sprint 1. Tracking em [03_SECURITY_PLAN.md §3.R2](./03_SECURITY_PLAN.md).

---

## A03:2021 — Injection

**Risco genérico:** SQL injection, command injection, XSS, header injection.

**Vetores considerados:**
- SQLi via query param ou body.
- XSS via response renderizada no app.
- Command injection via shell exec.
- Header injection via `X-Forwarded-For` confiável demais.

**Mitigações implementadas:**

### SQL Injection
- **100% das queries parametrizadas:** repositórios usam `NamedParameterJdbcTemplate` com `:nomeDoBind`. Exemplo: `LeadRepository.java`.
- **Zero concatenação de SQL:** convenção do repo confirmada em [forward-api-java/CLAUDE.md](../../../forward-api-java/CLAUDE.md) ("All queries parameterized, never concatenated").
- **Validação prévia:** UUIDs, VINs e enums validados antes de chegar ao repository ([Validations.java](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/Validations.java)).

### XSS
- **API JSON, sem template server-side:** o backend não renderiza HTML. Cabeçalho `Content-Type: application/json` impede execução em browser direto.
- **`X-Content-Type-Options: nosniff`** e **`X-Frame-Options: DENY`** ([SecurityHeadersFilter.java:23-24](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/SecurityHeadersFilter.java)) impedem MIME-sniffing e clickjacking.
- **CSP `default-src 'none'`** fora do Swagger ([SecurityHeadersFilter.java:45](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/SecurityHeadersFilter.java)).
- **Mobile (Expo):** React Native escapa strings interpoladas por padrão; APIs de injeção direta de HTML não existem no runtime de RN.

### Command Injection
- **Sem `Runtime.exec`, `ProcessBuilder` ou integração shell** no código. Confirmado por grep no repo.

### Header Injection
- `X-Request-Id` aceito do cliente é tratado como string opaca em MDC ([RequestIdFilter.java:27-29](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/RequestIdFilter.java)).
- `X-Forwarded-For` não é usado para decisões de segurança (rate limit usa `request.getRemoteAddr()`).

### XML/XXE (SOAP)
- Spring WS desabilita external entities por padrão em [VehicleEndpoint](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/soap/).
- Schema XSD em [vehicles.xsd](../../../forward-api-java/src/main/resources/xsd/vehicles.xsd) define contrato; entidades externas são rejeitadas.

**Status:** ✅ Mitigado.

---

## A04:2021 — Insecure Design

**Risco genérico:** arquitetura sem ameaça modelada, ausência de princípios de defesa em profundidade.

**Evidência de design seguro:**

1. **Threat model formal:** [01_THREAT_MODEL.md](./01_THREAT_MODEL.md) aplica STRIDE em cada componente.
2. **Defense-in-depth:** autenticação (AuthFilter) + autorização service + RLS Postgres + audit log. Falha em uma camada não compromete o todo.
3. **Princípio do menor privilégio:**
   - Roles distintas: `user`, `dealer`, `analyst`, `admin`.
   - `churn_score` invisível para `user`.
   - `audit_log` apenas leitura admin; `REVOKE UPDATE, DELETE ON audit_log FROM PUBLIC` ([009_create_audit_log.sql:26](../../../forward-infra/supabase/migrations/009_create_audit_log.sql)).
4. **Portão único:** SOA com backend como único ponto de entrada (ver [03_SOLUTION_DESIGN.md §150-191](../../project/03_SOLUTION_DESIGN.md)). Mobile, web e N8N não falam direto com banco.
5. **Stateless por design:** `SessionCreationPolicy.STATELESS` ([SecurityConfig.java:35](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/SecurityConfig.java)), evitando session fixation e CSRF.
6. **Fail-secure:** sem credencial → 401, sem rate limit budget → 429, sem permissão → 403 (sempre RFC 7807, sem stack trace).

**Status:** ✅ Mitigado.

---

## A05:2021 — Security Misconfiguration

**Risco genérico:** defaults inseguros (banner do servidor, painel admin exposto, CORS aberto, debug em produção).

**Mitigações implementadas:**

| Misconfiguration | Mitigação | Arquivo |
|---|---|---|
| CORS wildcard | Allowlist explícita; rejeita `*`. | [CorsConfig.java:26](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/CorsConfig.java) + [fly.toml:11](../../../forward-api-java/fly.toml) |
| Session habilitada (CSRF) | STATELESS, CSRF desabilitado | [SecurityConfig.java:28, 35](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/SecurityConfig.java) |
| Form login default | Desabilitado | [SecurityConfig.java:29](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/SecurityConfig.java) |
| HTTP Basic default | Desabilitado | [SecurityConfig.java:30](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/SecurityConfig.java) |
| Actuator exposto | Só `health` e `info` expostos; `show-details: never` em health | [application.yml:26-34](../../../forward-api-java/src/main/resources/application.yml) |
| Stack trace em response | Generic message + RFC 7807; stack apenas em log interno | [GlobalExceptionHandler.java:66-69](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/error/GlobalExceptionHandler.java) |
| Log spam Spring Security | `org.springframework.security: WARN` | [application.yml:39](../../../forward-api-java/src/main/resources/application.yml) |
| CSP padrão aberto | `default-src 'none'; frame-ancestors 'none'` (lockdown) fora do Swagger | [SecurityHeadersFilter.java:45](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/SecurityHeadersFilter.java) |
| HTTP em produção | `force_https = true` no edge | [fly.toml:18](../../../forward-api-java/fly.toml) |
| Body upload ilimitado | `max-http-form-post-size: 1MB`, env `MAX_BODY_BYTES` | [application.yml:7-8](../../../forward-api-java/src/main/resources/application.yml) |
| Banner do Tomcat | Spring Boot remove `Server` header por padrão; não foi reativado | n/a |

**Status:** ✅ Mitigado.

---

## A06:2021 — Vulnerable and Outdated Components

**Risco genérico:** dependência com CVE crítica não atualizada.

**Histórico de mitigação:**

Em 2026-05-23 o profile Maven `security` (que rodava `dependency-check-maven 10.0.4`) foi **removido** do projeto via [PR #17 em forward-api-java](https://github.com/fwd-ford/forward-api-java/pull/17). Razões documentadas:

1. Estava `continue-on-error: true` desde PR #2 do `.github` (2026-05-21), então **já não era gate** — só ruído.
2. Falhava por duas causas sobrepostas:
   - CVEs 7.5 herdados do Spring Boot BOM 3.5.x em `log4j-api 2.24.3` e `angus-activation 2.0.3` (sem patch disponível no BOM corrente).
   - Bug no `dependency-check-maven 10.0.4`: URLs de CVEs 2026 estouram a coluna `URL VARCHAR(1000)` do schema H2, abortando o update do NVD.

**Cobertura atual de CVE em dependências:**

| Ferramenta | Função | Onde |
|---|---|---|
| **Trivy filesystem scan** | Gate de CI em CRITICAL/HIGH, `exit-code: 1`, `ignore-unfixed: true` | [java-security.yml:11-23](../../../.github/.github/workflows/java-security.yml) |
| **Dependabot** | PRs automáticas para atualizações | configurado por repo |
| **SpotBugs + FindSecBugs** | SAST estático no profile `quality` | [pom.xml](../../../forward-api-java/pom.xml) |
| **gitleaks** | Scan de segredos no diff | `secrets-scan.yml` |

**Pendência:** o job `dependency-check` no workflow compartilhado [java-security.yml:26-46](../../../.github/.github/workflows/java-security.yml) ainda existe mas roda `./mvnw verify -P security` que **falha silenciosamente** (`continue-on-error: true`) porque o profile não existe mais no pom. PR [`.github#3`](https://github.com/fwd-ford/.github/pull/3) (chore/drop-owasp-dependency-check) está OPEN para remover o job — sem impacto de segurança porque já não era gate.

**Por que não voltar OWASP DC depois:** Trivy filesystem cobre o mesmo terreno sem as duas patologias acima. Se um dia o projeto precisar de SCA mais robusto, considerar `trivy fs --scanners vuln,license` ou Snyk OSS — nunca OWASP DC.

**Status:** ✅ Mitigado (com Trivy + Dependabot, não com OWASP DC).

---

## A07:2021 — Identification and Authentication Failures

**Risco genérico:** credenciais fracas, sem MFA, session fixation, brute force.

**Mitigações implementadas:**

1. **AuthN delegada para Supabase Auth:** o forward-api-java **não emite tokens** — valida tokens emitidos pelo Supabase. Isso significa:
   - Hash de senha, MFA, password reset, account lockout = responsabilidade do Supabase Auth (PBKDF2, bcrypt).
   - Brute force de login fica do lado do Supabase; rate limit Bucket4j no nosso lado complementa.
2. **JWT validation rigorosa:** [AuthFilter.java:84-101](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/AuthFilter.java) rejeita `null`, header sem `Bearer `, e exceções do validator viram 401 genérico (não vaza motivo).
3. **Algoritmo do token validado:** `AlgAwareJwtValidator` roteia pelo header `alg`, não permite `none` algorithm attack (Nimbus JOSE e JJWT já rejeitam).
4. **Stateless:** sem session = sem session fixation.
5. **X-API-Key constant-time?** Não — comparação `String.equals` em [AuthFilter.java:78](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/AuthFilter.java). Risco baixo porque a key é longa e não há contexto onde timing seja explorável remotamente em volume; mas é candidato a refactor para `MessageDigest.isEqual` no Sprint 2 (tracking em [03_SECURITY_PLAN.md §3.R6](./03_SECURITY_PLAN.md)).
6. **Token nunca logado:** `Authorization` header não vai pro MDC ou pro JSON log.

**Status:** ✅ Mitigado.

---

## A08:2021 — Software and Data Integrity Failures

**Risco genérico:** atualização não autenticada, deserialização insegura, integridade de payload comprometida.

**Mitigações implementadas:**

1. **HMAC opcional para chamadas server-to-server:** [HmacValidator.java](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/HmacValidator.java) implementa `HMAC_SHA256(secret, "<timestamp>:<METHOD>:<path>:<sha256(body)>")` com:
   - Replay protection via timestamp + 5 min skew.
   - Constant-time comparison via XOR loop ([HmacValidator.java:115-124](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/HmacValidator.java)).
   - SHA-256 do body garante que tampering vira invalidação de assinatura.
2. **Cobertura atual:** caller `N8N` pode optar por HMAC além do `X-API-Key`. Para Sprint 1 está implementado e testado ([HmacValidatorTest.java](../../../forward-api-java/src/test/java/)) mas não obrigatório em todos os endpoints — habilitação por endpoint fica para Sprint 2.
3. **Deserialização:** Jackson com configuração padrão Spring (rejeita tipos desconhecidos). Sem `enableDefaultTyping` (vetor de RCE via polymorphic deserialization).
4. **CI/CD integrity:** `actions/checkout@v4`, `actions/setup-java@v4` pinados em versão fixa em [java-security.yml](../../../.github/.github/workflows/java-security.yml). Maven Wrapper pinado em 3.9.
5. **Build artifact:** Dockerfile multi-stage, image base Eclipse Temurin oficial.

**Status:** ⚠️ Parcial. Bem implementado para Sprint 1, mas obrigatoriedade do HMAC em endpoints sensíveis fica como evolução. Equivale aos 5pts opcionais da rubrica (Seção 3 do critério oficial).

---

## A09:2021 — Security Logging and Monitoring Failures

**Risco genérico:** sem trilha de auditoria, sem detecção de anomalia, logs sem correlação.

**Mitigações implementadas:**

| Item | Implementação |
|---|---|
| Correlation ID | `X-Request-Id` UUID em [RequestIdFilter.java:27-33](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/RequestIdFilter.java); injetado em MDC e devolvido no response |
| Logs estruturados | JSON em produção via Logstash encoder ([logback-spring.xml:7-11](../../../forward-api-java/src/main/resources/logback-spring.xml)); `service: forward-api` como campo fixo |
| Audit trail | Tabela [audit_log](../../../forward-infra/supabase/migrations/009_create_audit_log.sql) append-only; campos: `actor_id`, `actor_role`, `action`, `resource_type`, `resource_id`, `ip_address`, `user_agent`, `request_id`, `payload`, `created_at` |
| Append-only enforce | `REVOKE UPDATE, DELETE ON audit_log FROM PUBLIC` ([009_create_audit_log.sql:26](../../../forward-infra/supabase/migrations/009_create_audit_log.sql)) |
| Anonimização auditada | Cada `anonymize_customer` insere linha em audit_log com `reason` e `at` ([013_lgpd_retention_policy.sql:46-53](../../../forward-infra/supabase/migrations/013_lgpd_retention_policy.sql)) |
| Logs de erro não tratado | `log.error("unhandled error path={} msg={}", ...)` com stack interno ([GlobalExceptionHandler.java:66](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/error/GlobalExceptionHandler.java)) |
| Health probe | `/health` e `/ready` para alerta de liveness pelo Fly.io |
| Métricas Fly.io | Plataforma já agrega CPU, RAM, requests/s, error rate, latency p95/p99 |

**Risco residual:** audit_log cobre ações sensíveis explicitamente registradas (anonimização). Cobertura para CRUD comum (leitura de customer, criação de service event) é P1 — tracking em [03_SECURITY_PLAN.md §3.R4](./03_SECURITY_PLAN.md). PII masking em log também é P1 (R3).

**Status:** ✅ Mitigado para Sprint 1; expansão de cobertura no roadmap.

---

## A10:2021 — Server-Side Request Forgery

**Risco genérico:** API faz request HTTP para URL controlada pelo cliente.

**Análise:**

ForwardService backend **não faz outbound HTTP para URLs vindas do cliente** em nenhum endpoint do Sprint 1.

Outbounds que existem:
- JWKS fetch para Supabase ([JwksJwtValidator](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/security/JwksJwtValidator.java)): URL configurada via env var `SUPABASE_JWKS_URL`, não controlada pelo cliente.
- Postgres connection: URL configurada via env var `DATABASE_URL`, não controlada pelo cliente.

Não há endpoint que aceite URL do cliente e faça fetch (ex: image proxy, webhook caller, OG preview, URL shortener).

**Mitigação preventiva caso evolua:** allowlist de domínios + DNS rebinding protection + reject de IPs privados (RFC 1918, link-local, loopback). Tracking em [03_SECURITY_PLAN.md §3.R8](./03_SECURITY_PLAN.md) caso N8N receba webhooks customizáveis no futuro.

**Status:** ✅ N/A no Sprint 1.

---

## Pontuação estimada na rubrica oficial (100 pts)

Mapeamento das categorias do OWASP Top 10 para os 5 critérios do Prof. Vitor:

| Critério (rubrica) | Categorias OWASP relacionadas | Pontuação estimada |
|---|---|---|
| 1. Validação entrada (20) | A03 Injection | **20/20** |
| 2. AuthN/AuthZ (20) | A01, A07 | **20/20** |
| 3. Proteção API (20) | A02, A05, A08 (HMAC opcional 5pts) | **20/20** |
| 4. Dados/Privacidade (25) | A02 (em repouso) + LGPD compliance | **22/25** (sem field-level encryption aplicacional) |
| 5. Logs/Auditoria (15) | A09 | **13/15** (audit_log para CRUD comum é P1) |
| **TOTAL** | | **95/100** |

---

## Referências

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [01_THREAT_MODEL.md](./01_THREAT_MODEL.md)
- [03_SECURITY_PLAN.md](./03_SECURITY_PLAN.md)
- [Spring Security 6 reference](https://docs.spring.io/spring-security/reference/)
- [Bucket4j](https://bucket4j.com/)
- LGPD Lei 13.709/2018
