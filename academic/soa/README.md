# SOA — Entrega Sprint 1

![disciplina](https://img.shields.io/badge/disciplina-SOA-purple?style=flat-square)
![prof](https://img.shields.io/badge/prof-Salatiel-blue?style=flat-square)
![data](https://img.shields.io/badge/entrega-2026--05--24-brightgreen?style=flat-square)
![combinado](https://img.shields.io/badge/diagramas-Mermaid_(combinado_c%2F_Salatiel)-orange?style=flat-square)

> Pacote da disciplina **SOA (Service-Oriented Architecture)** do Desafio 02 Ford-FIAP 2026.
> Entrega via **Mermaid no markdown** em vez de ferramenta gráfica externa, conforme combinado com o Prof. Salatiel.

---

## 1. O que está sendo entregue

| Item | Onde está | Por quê |
| --- | --- | --- |
| **Arquitetura de serviços (diagramas)** | `forward-docs/project/03_SOLUTION_DESIGN.md` — 5 blocos Mermaid | Visão geral, elenco, fluxos, modelo de dados |
| **REST API (Spring Boot)** | `forward-api-java/src/main/java/com/fwdford/forwardapi/web/` — 8 endpoints | Camada síncrona de aplicação |
| **SOAP API (Spring WS)** | `forward-api-java/src/main/java/com/fwdford/forwardapi/soap/` — 1 operação contract-first | Interoperabilidade legacy / requisito SOA |
| **OpenAPI / Swagger** | `springdoc-openapi 2.7.0` em runtime: `/swagger-ui.html` + `/v3/api-docs` | Contrato auto-documentado |
| **Migrations versionadas** | `forward-infra/supabase/migrations/` — 13 arquivos SQL numerados | Persistência rastreável |
| **Deploy contínuo** | Fly.io (`forward-api-java`) + Supabase (Postgres) | API live, acessível pelo mobile e pelo Swagger |

---

## 2. Catálogo de endpoints REST

Base path: `/api/v1`. Autenticação: `Authorization: Bearer <JWT>` (HS256+JWKS) ou `X-API-Key`.

| Verbo | Path | Controller | Função |
| --- | --- | --- | --- |
| `GET` | `/health` | [HealthController.java:32](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/HealthController.java#L32) | Liveness probe (Fly.io / Kubernetes) |
| `GET` | `/ready` | [HealthController.java:48](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/HealthController.java#L48) | Readiness probe (DB + dependências) |
| `GET` | `/api/v1/me` | [MeController.java:24](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/MeController.java#L24) | Quem é o caller (claims do JWT) |
| `GET` | `/api/v1/customers/{id}` | [CustomerController.java:33](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/CustomerController.java#L33) | Detalhe de cliente (RBAC dealer/analyst/admin) |
| `GET` | `/api/v1/vehicles/{vin}` | [VehicleController.java:32](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/VehicleController.java#L32) | Detalhe de veículo por VIN |
| `GET` | `/api/v1/leads` | [LeadController.java:38](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/LeadController.java#L38) | Lista de leads do atendente (paginada + filtros) |
| `GET` | `/api/v1/scores/{customerId}` | [ScoreController.java:33](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/ScoreController.java#L33) | Churn score atual de um cliente |
| `POST` | `/api/v1/service-events` | [ServiceEventController.java:40](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/ServiceEventController.java#L40) | Registra evento de serviço (contato, agendamento, fechamento) |

Cada controller usa `@Operation` do springdoc, então o Swagger renderiza descrição, parâmetros e exemplos em runtime sem trabalho manual.

---

## 3. Catálogo SOAP

Spring WS contract-first em `urn:forwardservice:vehicles`.

| Item | Valor |
| --- | --- |
| **Endpoint** | `POST /soap/*` (servlet `MessageDispatcherServlet`) |
| **WSDL público** | `GET /soap/vehicles.wsdl` (gerado dinamicamente) |
| **Schema XSD** | [forward-api-java/src/main/resources/xsd/vehicles.xsd](../../../forward-api-java/src/main/resources/xsd/vehicles.xsd) |
| **Operação** | `GetVehicleRequest → GetVehicleResponse` |
| **Bootstrap** | [WebServiceConfig.java](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/soap/WebServiceConfig.java) |
| **Handler** | [VehicleEndpoint.java](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/soap/VehicleEndpoint.java) |

Schema (fonte da verdade):

```xml
<xs:element name="GetVehicleRequest">
  <xs:complexType><xs:sequence>
    <xs:element name="VIN" type="xs:string"/>
  </xs:sequence></xs:complexType>
</xs:element>

<xs:element name="GetVehicleResponse">
  <xs:complexType><xs:sequence>
    <xs:element name="VIN"          type="xs:string"/>
    <xs:element name="Model"        type="xs:string"/>
    <xs:element name="Year"         type="xs:int"/>
    <xs:element name="Discontinued" type="xs:boolean"/>
  </xs:sequence></xs:complexType>
</xs:element>
```

**Por que SOAP além de REST?** O critério SOA exige interoperabilidade entre serviços com contrato forte. REST cobre o cliente moderno (mobile, web). SOAP cobre o cenário "concessionária com ERP legacy que só fala WSDL" — exatamente o público real da Ford.

---

## 4. Diagramas (Mermaid)

Os 5 diagramas Mermaid vivem no [03_SOLUTION_DESIGN.md](../../project/03_SOLUTION_DESIGN.md). Combinado com o Prof. Salatiel: Mermaid renderiza nativo no GitHub, o que substitui Archi sem perder rastreabilidade.

| # | Linha | Tipo | Sobre o quê |
| --- | --- | --- | --- |
| 1 | [75](../../project/03_SOLUTION_DESIGN.md#L75) | `flowchart` | Visão geral — cenário e tese em uma página |
| 2 | [152](../../project/03_SOLUTION_DESIGN.md#L152) | `flowchart` | Elenco e interligação entre as 7 plataformas |
| 3 | [595](../../project/03_SOLUTION_DESIGN.md#L595) | `gantt`/`timeline` | Cronograma original v2.0 (referência histórica) |
| 4 | [658](../../project/03_SOLUTION_DESIGN.md#L658) | `erDiagram` | Modelo de dados completo (tabelas + FKs) |
| 5 | [789](../../project/03_SOLUTION_DESIGN.md#L789) | `flowchart` | Pipeline `vin_features` (derivação do dataset oficial) |

Padrão Mermaid usado: **labels curtas, sem emojis, sem `&` em strings** (quebra o parser).

---

## 5. Persistência e migrations

13 migrations versionadas em [forward-infra/supabase/migrations/](../../../forward-infra/supabase/migrations/):

```
001_create_dealers.sql              008_create_lead_outcomes.sql
002_create_customers.sql            009_create_audit_log.sql
003_create_vehicles.sql             010_rls_policies.sql
004_create_service_orders.sql       011_triggers_updated_at.sql
005_create_churn_scores.sql         012_add_service_event_fields.sql
006_create_leads.sql                013_lgpd_retention_policy.sql
007_create_communications.sql
```

Aplicadas via Supabase MCP em prod (projeto `ysewoopjgdpvnkfhffgy`, região SP). Cada migration é idempotente e revisada por `get_advisors` (security + performance lints).

---

## 6. Princípios SOA evidenciados

| Princípio (Erl, *SOA Principles of Service Design*) | Como está aplicado |
| --- | --- |
| **Standardized Service Contract** | Swagger gerado de annotations + WSDL gerado de XSD. Contrato é a fonte da verdade, não o código. |
| **Service Loose Coupling** | Mobile não conhece nada do ML. Backend serve score já calculado. ML escreve em tabela própria. |
| **Service Abstraction** | SOAP esconde a implementação Java por trás do envelope. REST esconde Postgres por trás dos DTOs. |
| **Service Reusability** | `VehicleService` é consumido pelo `VehicleController` (REST) **e** pelo `VehicleEndpoint` (SOAP). Mesma lógica, dois transportes. |
| **Service Autonomy** | Cada controller falha de forma isolada (RFC 7807 com `requestId`, sem leak entre serviços). |
| **Service Statelessness** | JWT carrega claims (`sub`, `role`, `dealerId`). Servidor não guarda sessão. |
| **Service Discoverability** | `/swagger-ui.html` + `/soap/vehicles.wsdl` ambos públicos, sem auth, prontos para discovery. |
| **Service Composability** | `POST /service-events` aciona n8n (WhatsApp), que pode acionar `GET /scores/{id}` em fluxo orquestrado. |

---

## 7. Como testar (Prof. Salatiel)

### REST via Swagger
```bash
# API em prod (Fly.io)
open https://forward-api-java.fly.dev/swagger-ui.html

# Local
cd forward-repos/forward-api-java && bash mvnw spring-boot:run
open http://localhost:8080/swagger-ui.html
```

### SOAP via WSDL
```bash
curl https://forward-api-java.fly.dev/soap/vehicles.wsdl

# Chamada de exemplo
curl -X POST https://forward-api-java.fly.dev/soap/vehicles \
  -H "Content-Type: text/xml" \
  -H "SOAPAction: " \
  --data '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:v="urn:forwardservice:vehicles">
  <soap:Body>
    <v:GetVehicleRequest><v:VIN>1FTFW1ET5DFC10312</v:VIN></v:GetVehicleRequest>
  </soap:Body>
</soap:Envelope>'
```

### Mobile consumindo a API
App em Expo Go, credencial de teste `teste@gmail.com` / `teste123` (ver [forward-mobile/README.md](../../../forward-mobile/README.md)). Os 8 endpoints REST estão sendo chamados no fluxo Home → Leads → Lead Detail.

---

## 8. Checklist de cobertura

| Item | Estado |
| --- | --- |
| REST com no mínimo 3 endpoints distintos | 8/3 — sobrou |
| SOAP com no mínimo 1 operação contract-first | 1/1 |
| Documentação automática do contrato | Swagger (OpenAPI 3) + WSDL dinâmico |
| Persistência versionada (migrations) | 13 arquivos SQL numerados |
| Diagrama de arquitetura | 5 Mermaid em `03_SOLUTION_DESIGN.md` |
| Deploy live para demonstração | Fly.io (`forward-api-java.fly.dev`) |
| Princípios SOA documentados | 8/8 (Erl) na §6 |
| Segurança no transporte | JWT HS256+JWKS, RBAC, HMAC opcional — ver [academic/cyber/](../cyber/) |

---

## Apêndice — Onde olhar primeiro

| Quero ver... | Vou pra... |
| --- | --- |
| Os diagramas | [project/03_SOLUTION_DESIGN.md §1, §2, §8](../../project/03_SOLUTION_DESIGN.md) |
| Os controllers REST | [forward-api-java/src/main/java/com/fwdford/forwardapi/web/](../../../forward-api-java/src/main/java/com/fwdford/forwardapi/web/) |
| O contrato SOAP | [forward-api-java/src/main/resources/xsd/vehicles.xsd](../../../forward-api-java/src/main/resources/xsd/vehicles.xsd) |
| As migrations | [forward-infra/supabase/migrations/](../../../forward-infra/supabase/migrations/) |
| O backend rodando | `https://forward-api-java.fly.dev/swagger-ui.html` |
| Como o mobile consome | [forward-mobile/lib/api.ts](../../../forward-mobile/lib/api.ts) |
