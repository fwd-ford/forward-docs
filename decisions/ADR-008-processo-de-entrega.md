# ADR-008: processo de entrega

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota

## Contexto

Na Sprint 1, telas com dados de demonstração esconderam backend quebrado, e lint quebrado entrou na `main`. No rebuild, o código é escrito com apoio de IA e cada mudança precisa de prova, não de "compila".

## Decisão

- **Pronto é rodar:** uma tela só está pronta quando roda no simulador (iOS; Android quando houver aparelho) contra a stack local, com print dos estados carregado, vazio e erro.
- **Gates por camada:**
  - pgTAP rodando como o papel do app e como `forward_api`;
  - JUnit com Spotless, Checkstyle e SpotBugs;
  - Jest e RNTL com typecheck e lint.
- **Mutação:** testes-chave passam por mutação. A regra é quebrada de propósito e o teste precisa ficar vermelho.
- **Revisão adversarial:** revisores independentes procuram defeitos com prova antes de fechar a leva. Achado sem reprodução não conta.
- **Publicação por leva:** cada leva vira PR por repo. Ninguém dá push direto na `main` (o ruleset exige PR).
- **Agentes de IA:** só pesquisam, revisam e verificam. O código do projeto é escrito na conversa principal ou pelas pessoas do grupo.
- **Sem dados de demonstração nas telas:** o seed é explícito, determinístico e marcado como sintético.
- **Sem travessões** (em dash e en dash) em código e documentos, e com lint de i18n.

## Consequências

- Cada leva custa mais do que "fazer a tela", mas o que entra na `main` funciona.
- As fichas de leva registram gates, mutações e prints.
