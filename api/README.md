# API specs

Esta pasta espelha contratos OpenAPI publicados pelos serviços da plataforma
ForwardService. Source-of-truth fica no repositório do serviço; o que está
aqui é uma cópia versionada para a banca e equipes downstream consumirem
sem precisar clonar cada backend.

## Conteúdo

| Arquivo | Source-of-truth | Endpoint runtime |
| ------- | --------------- | ---------------- |
| [`openapi.yaml`](openapi.yaml) | [`fwd-ford/forward-api-java/openapi.yaml`](https://github.com/fwd-ford/forward-api-java/blob/main/openapi.yaml) | `GET /v3/api-docs.yaml` (springdoc) |

## Como atualizar (refresh manual)

A geração é manual por enquanto. Quando algum endpoint mudar em
`forward-api-java`, regenere e replique aqui:

```bash
# 1. Dentro de forward-api-java, com a app rodando local:
./mvnw spring-boot:run
curl http://localhost:8080/v3/api-docs.yaml -o openapi.yaml

# 2. Copie pro mirror neste repo:
cp openapi.yaml ../forward-docs/api/openapi.yaml

# 3. Commit nos dois repos (ou abra duas PRs):
git -C ../forward-api-java add openapi.yaml && git -C ../forward-api-java commit -m "docs(openapi): regenerate"
git add openapi.yaml && git commit -m "docs(api): mirror openapi.yaml refresh"
```

## Visualização

| Onde | URL |
| ---- | --- |
| Swagger UI (local) | `http://localhost:8080/swagger-ui/index.html` |
| Swagger UI (produção Fly.io) | `https://forward-api-java.fly.dev/swagger-ui/index.html` |
| Editor online | Cole o conteúdo de `openapi.yaml` em [editor.swagger.io](https://editor.swagger.io) |

## Tech-debt acordado

- **Sem auto-sync ainda**: refresh é manual, então pode haver drift de poucas
  horas entre forward-api-java/main e este mirror. Sprint 2 deve adicionar
  um workflow `mirror-openapi.yml` (cron diário ou `repository_dispatch` do
  forward-api-java em push de `openapi.yaml`) e remover esta nota.
