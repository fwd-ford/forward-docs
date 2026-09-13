# Leva L0: fundação e método

- **Status:** em andamento (13/09/2026)
- **Objetivo:** três repos revisados e com backup, app falando com o Java, stack local em um comando e o método pronto antes da primeira regra de produto.

## Entregas

| Repo | Commit (branch local) | Entrega |
| --- | --- | --- |
| forward-infra | `ee7797d`, `cfafa1a` (`feat/access-model`) | modelo de acesso com RLS v2 e 78 pgTAP; `scripts/dev/stack.sh` e `init-secrets.sh` |
| forward-api-java | `2b7adf4`, `e4cab52` (`feat/claims-bound-db-session`) | sessão ligada às claims; revisão adversarial aplicada |
| forward-mobile | `5a234ed`, `9c4e3e9` (`rebuild/foundation`) | sessão e login verificados no simulador; cliente HTTP do Java e tela de diagnóstico |
| forward-docs | esta branch (`docs/produto-app-maria`) | BASE-GLOBAL, ROTEIRO-DEMO, ESTADO-E-PLANO, EQUIPE-E-TAREFAS, ADRs 001 a 009, guia RODAR-LOCAL |
| GitHub | org fwd-ford | épicos L0 a L10 com issues e sub-issues distribuídas |

## Gates

| Camada | Resultado |
| --- | --- |
| forward-infra | `db reset` e 78 testes pgTAP verdes; `init-secrets` idempotente (segunda execução não muda nada); `stack.sh up` com a stack já de pé sai com código 0 |
| forward-api-java | Spotless, Checkstyle 0, SpotBugs 0, 90 testes |
| forward-mobile | typecheck, lint, formatação, travessões e 93 testes |

## Revisão adversarial do Java

17 agentes: 3 revisores (segurança, correção, testes) e um cético por achado. Foram 9 achados confirmados e aplicados:

1. `POST` no caminho do WSDL pulava a autenticação.
2. A leitura prévia do veículo sob RLS barrava a visita a outra concessionária.
3. A falta de GRANT aparecia como 403.
4. Faults SOAP sem código e com vazamento da mensagem da exceção.
5. Contrato OpenAPI desatualizado.
6. Teste da sessão tautológico (comparava com a própria constante).
7. Testes de serviço não provavam a sessão.
8. Fábrica de validadores JWT sem teste.
9. Remoção da `X-API-Key` sem prova.

Refutado: autorização aberta com usuário BYPASSRLS. Exige configuração contra a documentação e não é regressão.

Ficaram como dívida (achados baixos): ordem dos filtros antes da autenticação e timeout do `/ready`.

## Mutações

| Mutação | Morta por |
| --- | --- |
| `POST` no WSDL volta a ser público | `AuthFilterTest.post_to_the_wsdl_path_is_not_public` |
| `set_config(..., false)` | `ClaimsBoundDbSessionTest` |
| consulta fora da sessão | `CustomerServiceTest` |
| fault SOAP com a mensagem da exceção | `SoapErrorResolverTest` |
| falta de GRANT tratada como 403 | `SqlErrorsTest` |
| `AuthProvider` sem contador de geração, chamada síncrona no callback, sem limpar timers, confiando no papel, relendo no refresh | `AuthProvider.test.tsx` |

## Verificação ao vivo

| Onde | O que se viu |
| --- | --- |
| Simulador iOS | login de `agent.a` mostra papel e concessionária; conta sem vínculo cai em "Acesso não liberado"; sair revoga a sessão no servidor; a sessão sobrevive a reload |
| Diagnóstico | `my_context` e `/api/v1/me` mostram o mesmo `dealer_id`; com o container da API parado, o lado do Supabase continua e o lado do Java mostra o erro traduzido com `request_id` |
| API | `POST` no WSDL sem token: 401. Visita a veículo de outra concessionária: 201. VIN inexistente: 404. Consultora citando outra concessionária: 403. Fault SOAP com `code` no detalhe |

## Desvios do plano

- O plano previa a integração local das três branches numa `main` local. Ficou `git bundle` de backup em cada repo, porque a publicação vai por PR.
- O prefixo ACS nas descrições dos 78 testes pgTAP e o `check-rules.mjs` ficaram para o início da L1.

## Pendências para fechar a L0

- [ ] PRs das branches de forward-infra, forward-api-java e forward-mobile (com OK do Jota)
- [ ] Prefixo ACS nos testes pgTAP e `check-rules.mjs`
- [ ] Guia RODAR-LOCAL testado do zero por outra pessoa do grupo
