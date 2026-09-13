# ADR-001: o app lê o Supabase sob RLS e todo comando passa pelo Java

- **Status:** aceita
- **Data:** 12/09/2026
- **Decisores:** Jota (líder), com o plano de rebuild

## Contexto

O Supabase volta a ser a plataforma (Postgres, Auth, Storage). O forward-api-java precisa continuar, porque a disciplina de SOA exige serviços REST e SOAP em Java. É preciso decidir o que o app mobile faz direto no Supabase e o que passa pelo Java, sem duplicar regra.

## Decisão

- O app **lê** direto do Supabase por views `security_invoker`, sob Row Level Security. O papel `authenticated` só tem `SELECT`.
- Todo **comando** com regra de negócio, integração ou segredo passa pelo forward-api-java.
- O Java conecta como o papel `forward_api` (sem BYPASSRLS) e grava as claims do usuário por transação (`set_config('request.jwt.claims', ..., true)`). Assim, o Java enxerga exatamente o que o usuário enxergaria.
- Papel e concessionária vêm de `private.memberships` (view `my_context`), nunca das claims do JWT.

## Consequências

- **Leitura:** continua funcionando com o Java fora do ar.
- **Autorização de linha:** mora num lugar só (SQL), testada com pgTAP como o app e como o `forward_api`.
- **Toda escrita:** vira função `private.cmd_*` com guarda de escopo, chamada pelo Java (REST ou SOAP).
- **Risco:** subir o Java com um usuário com BYPASSRLS desligaria a autorização. A configuração documentada usa `forward_api`, e há reforço previsto de checagem no boot.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Tudo pelo Java (BFF) | toda leitura dependeria do Java; mais latência e mais código sem ganho de segurança |
| Java só para integrações | a disciplina de SOA pede a camada de serviços do domínio |
