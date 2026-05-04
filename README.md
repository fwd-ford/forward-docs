# forward-docs

![org](https://img.shields.io/badge/org-fwd--ford-blue?style=flat-square)
![type](https://img.shields.io/badge/type-documentation-lightgrey?style=flat-square)

Project documentation, research, academic deliverables and API specs for **ForwardService** — Ford Challenge FIAP 2026.

## Structure

```
project/          # Project docs (base, research, solution design, architecture)
academic/         # Academic deliverables per discipline
  pitch/          # Presentation slides
  canvas/         # Business Canvas
  togaf/          # Archi .archimate file
  video/          # Pitch video link/script
  cyber/          # Cybersecurity documentation
api/              # Swagger/OpenAPI specs, Postman collections
decisions/        # Architecture Decision Records (ADRs)
```

## Related Repos

| Repo | Stack | Purpose |
|---|---|---|
| [forward-web](https://github.com/fwd-ford/forward-web) | SvelteKit | Dashboard web |
| [forward-mobile](https://github.com/fwd-ford/forward-mobile) | React Native / Expo | Mobile app |
| [forward-api-java](https://github.com/fwd-ford/forward-api-java) | Java 17 / Spring Boot 3 | **Official backend** — REST + SOAP, JWT auth, integrations |
| [forward-ml](https://github.com/fwd-ford/forward-ml) | Python | ML service |
| [forward-infra](https://github.com/fwd-ford/forward-infra) | SQL / Docker | Infrastructure |
