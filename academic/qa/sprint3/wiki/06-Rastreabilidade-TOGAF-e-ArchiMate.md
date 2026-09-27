# Rastreabilidade TOGAF e ArchiMate

Os nomes abaixo são exatamente os elementos do modelo `academic/togaf/gen_archimate.py` (ForwardService.archimate). Cada item carrega as tags `ArchiMate:<elemento>` e `REQ-xx` (nas tags, vírgula vira ponto porque o Azure DevOps não aceita vírgula em tag).

## Épicos x camadas e elementos

| Épico | Pilar | Elementos ArchiMate | Requisitos |
| --- | --- | --- | --- |
| EP-01 Fundação de dados e plataforma | Transversal (Technology Layer) | Supabase / PostgreSQL; PostgreSQL 16; Flyway migrations; GitHub Actions CI; Docker Engine; Azure VM (B-series); Azure VNet; SOA — Portão Único | REQ-02, REQ-05 |
| EP-08 Governança de produto, qualidade e entregas | Governança (Motivation e Implementation) | Ford Brasil (Diretoria); Equipe ForwardService; Aumentar VIN Share; ForwardService.archimate; PITCH.pptx; VIDEO_PITCH.mp4; Sprint 1 — Entrega 24/05/2026 | - |
| EP-03 Portão Único SOA: forward-api-java | Transversal (Backend Core) | forward-api-java; REST API (OpenAPI); SOAP / WSDL; Auth/RBAC Service; Lead Prioritization; Serviço de Leads; JVM (Java 17); forward-api-java.jar; SOA — Portão Único | REQ-01, REQ-02, REQ-05 |
| EP-04 Experience Layer: app do atendente e do cliente | Experience Layer | forward-mobile; Atendente; Priorizar Leads; forward-mobile.apk/.ipa; Expo Push API; Cliente Ford | REQ-05, REQ-06, REQ-07 |
| EP-02 Intelligence Hub: scoring e segmentação de churn | Intelligence Hub | forward-ml; Scoring Service; Segmentar Clientes; Serviço de Scoring; client_scores; client_segments; ML Model Monitor; Flywheel de Dados; Reduzir churn pós-venda | REQ-03, REQ-04, REQ-05 |
| EP-05 Segurança, privacidade (LGPD) e compliance | Transversal (Cybersecurity) | Auth/RBAC Service; Audit Trail Service; audit_log; audit_log viewer; HTTPS / TLS 1.2+; GitHub Actions CI | REQ-02, REQ-05 |
| EP-07 Performance Console e observabilidade | Performance Console | forward-web; Analytics Service; Medir ROI; IHC — Saúde do Dealer; Grafana Dashboard; Alert: API p95 &gt; 300ms; Alert: Disponibilidade &lt;99%; ROI mensurável; Aumentar VIN Share | REQ-01, REQ-02 |
| EP-06 Action Engine: n8n e WhatsApp | Action Engine | n8n (Action Engine); n8n (Docker); WhatsApp Business API; WhatsApp Business API (Meta); Notification Service; Serviço de Notificação; Disparar Ação; Recall como Porta; Agendamento Digital; Proatividade sobre reatividade | REQ-05, REQ-07 |

## Requisitos de qualidade (Requirements View)

| Requisito | PBIs que realizam ou evidenciam |
| --- | --- |
| REQ-01: Latência API p95 &lt; 300ms | PBI-009, PBI-010, PBI-011, PBI-016, PBI-020, PBI-021, PBI-022, PBI-029, PBI-039, PBI-047, PBI-048, PBI-049, PBI-054, PBI-057 |
| REQ-02: Disponibilidade ≥ 99% | PBI-001, PBI-016, PBI-017, PBI-022, PBI-025, PBI-029, PBI-033, PBI-042, PBI-048, PBI-049 |
| REQ-03: AUC classificador ≥ 0,82 | PBI-014, PBI-016, PBI-031, PBI-050, PBI-051 |
| REQ-04: Falsos positivos churn &lt; 10% | PBI-013, PBI-014, PBI-016, PBI-031, PBI-051 |
| REQ-05: LGPD — dados pseudonimizados | PBI-005, PBI-008, PBI-013, PBI-015, PBI-016, PBI-018, PBI-019, PBI-024, PBI-027, PBI-028, PBI-029, PBI-030, PBI-034, PBI-035, PBI-036, PBI-037, PBI-045, PBI-050, PBI-055, PBI-056, PBI-057 |
| REQ-06: Onboarding atendente &lt; 15 min | PBI-007, PBI-012, PBI-016, PBI-023, PBI-024, PBI-025, PBI-026, PBI-037, PBI-038, PBI-053, PBI-056 |
| REQ-07: Entrega WhatsApp &lt; 30s | PBI-016, PBI-043, PBI-044, PBI-045, PBI-046, PBI-052, PBI-053 |

## Elemento ArchiMate x PBIs

| Elemento | PBIs |
| --- | --- |
| 3,4M Recalls pendentes | PBI-002, PBI-052 |
| Agendamento Digital | PBI-053 |
| Alert: API p95 &gt; 300ms | PBI-029, PBI-039, PBI-049 |
| Alert: Disponibilidade &lt;99% | PBI-029, PBI-049 |
| Analista ML | PBI-008 |
| Analytics Service | PBI-047, PBI-054 |
| Atendente | PBI-007, PBI-012, PBI-037 |
| Audit Trail Service | PBI-015, PBI-030, PBI-035, PBI-036, PBI-055 |
| audit_log | PBI-015, PBI-036, PBI-055 |
| audit_log viewer | PBI-029, PBI-036, PBI-049 |
| Aumentar VIN Share | PBI-003, PBI-058 |
| Auth/RBAC Service | PBI-018, PBI-019, PBI-024, PBI-030, PBI-034 |
| Azure VM (B-series) | PBI-042 |
| Azure VNet | PBI-042 |
| Ação Recomendada | PBI-050 |
| CANVAS.pdf | PBI-016 |
| Churn pós-garantia | PBI-002 |
| client_scores | PBI-014 |
| client_segments | PBI-013 |
| Cliente Ford | PBI-056 |
| Cron segmentador 02h | PBI-051 |
| Diretor Regional | PBI-048 |
| Disparar Ação | PBI-043, PBI-044 |
| Docker Engine | PBI-005, PBI-027, PBI-028, PBI-033, PBI-042 |
| Equipe ForwardService | PBI-001, PBI-032, PBI-040, PBI-041 |
| Escalar cobertura | PBI-003, PBI-056 |
| Expo Push API | PBI-046 |
| Flyway migrations | PBI-005, PBI-017 |
| Flywheel de Dados | PBI-050, PBI-051 |
| forward-api-java | PBI-004, PBI-006, PBI-009, PBI-010, PBI-011, PBI-017, PBI-018, PBI-019, PBI-020, PBI-021, PBI-022, PBI-023, PBI-028, PBI-039, PBI-045, PBI-047, PBI-053, PBI-057, PBI-060 |
| forward-api-java.jar | PBI-033 |
| forward-ml | PBI-004, PBI-008, PBI-013, PBI-014, PBI-031, PBI-050 |
| forward-mobile | PBI-004, PBI-007, PBI-012, PBI-024, PBI-025, PBI-026, PBI-034, PBI-037, PBI-038, PBI-046, PBI-056 |
| forward-mobile.apk/.ipa | PBI-026 |
| forward-web | PBI-004, PBI-048, PBI-058 |
| forward-web (static) | PBI-048 |
| ForwardService.archimate | PBI-016, PBI-032 |
| Frota descontinuada | PBI-002 |
| GitHub Actions CI | PBI-001, PBI-022, PBI-027, PBI-038, PBI-057 |
| Grafana Dashboard | PBI-029, PBI-049 |
| HTTPS / TLS 1.2+ | PBI-028, PBI-033 |
| IHC — Saúde do Dealer | PBI-047 |
| JVM (Java 17) | PBI-006 |
| Lead Prioritization | PBI-009 |
| Medir ROI | PBI-054, PBI-059 |
| ML Model Monitor | PBI-031, PBI-051 |
| ML models (pickle/joblib) | PBI-014 |
| n8n (Action Engine) | PBI-004, PBI-043, PBI-044, PBI-045, PBI-052 |
| n8n (Docker) | PBI-042 |
| Notification Service | PBI-043 |
| Perfil de Segmento | PBI-013 |
| PITCH.pptx | PBI-016 |
| PostgreSQL 16 | PBI-005 |
| Priorizar Leads | PBI-007, PBI-012 |
| Python 3.11 | PBI-008 |
| QUADRO_DE_VALOR.pdf | PBI-016 |
| Recall como Porta | PBI-052 |
| recommended_actions | PBI-043, PBI-050 |
| Reduzir churn pós-venda | PBI-003 |
| REST API (OpenAPI) | PBI-006, PBI-009, PBI-011, PBI-020, PBI-021 |
| ROI mensurável | PBI-003, PBI-054, PBI-059 |
| Score de Churn | PBI-014 |
| Scoring Service | PBI-009, PBI-014, PBI-031 |
| Segmentar Clientes | PBI-013 |
| Serviço de Agendamento | PBI-011, PBI-053, PBI-060 |
| Serviço de Leads | PBI-009, PBI-012 |
| Serviço de Notificação | PBI-044 |
| SOA — Portão Único | PBI-004, PBI-023 |
| SOAP / WSDL | PBI-010 |
| Supabase / PostgreSQL | PBI-004, PBI-005, PBI-015, PBI-017, PBI-035, PBI-055 |
| Vercel / Netlify | PBI-048 |
| VIDEO_PITCH.mp4 | PBI-040 |
| VIN Share baixo | PBI-002 |
| vin_features.csv | PBI-013 |
| WebSocket Push | PBI-046 |
| WhatsApp Business API | PBI-044, PBI-045 |
| WhatsApp Business API (Meta) | PBI-044 |
