# ADR-005: relógio do sistema e viagem no tempo

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota

## Contexto

O roteiro da demo acontece entre quarta 02h e sábado 02h. Ele precisa rodar em minutos, várias vezes, com os mesmos números. O banco roda em UTC: `current_date` às 21h de Brasília já é o dia seguinte. Esse bug já custou caro em outro projeto do Jota.

## Decisão

As regras REL-1 a REL-6 da BASE-GLOBAL:

1. Toda função de regra recebe `p_today` ou `p_now` explícito; os testes usam valor fixo.
2. O valor padrão vem de `private.clock_now()`: relógio real mais um deslocamento, que só a ferramenta de demo altera e só com o modo demo ligado.
3. O app calcula tempo relativo ("há 1 h") sobre o "agora" do servidor.
4. Em modo demo, os jobs do pg_cron e os gatilhos agendados do n8n ficam calados; os passos são disparados por comando.
5. Segurança (validade do JWT, janela do HMAC, rate limit) usa sempre o relógio real.
6. O papel `authenticated` nunca executa função que aceite `p_today` nem mexe no relógio.

## Consequências

- Um lint no CI do forward-infra proíbe `now()`, `current_date` e `current_timestamp` fora de `clock_now()`.
- O roteiro vira teste de aceite automatizável (`demo:script`).
- A ferramenta de demo é uma superfície de ataque, por isso fica restrita a admin e modo demo, com pgTAP garantindo.
