# Definition of Done

A DoD vale para todo o time e é verificada na Sprint Review pelo Product Owner. Cada PBI repete a DoD na descrição (seção Critérios de Pronto) e soma critérios específicos. No board de Backlog items, a coluna Approved mostra a Definition of Ready e a coluna Committed mostra a DoD.

## Definition of Ready (entrada na sprint)

1. História no formato Como &lt;persona&gt;, quero &lt;ação&gt;, para &lt;benefício&gt;, usando uma persona do mapa de personas (Base Fundacional e ArchiMate).
2. Critérios de aceite em Gherkin (pt-BR) com o caminho feliz e pelo menos um cenário de erro ou de borda.
3. Estimado em Planning Poker na escala Fibonacci (1, 2, 3, 5, 8, 13); itens maiores que 13 são quebrados antes da sprint.
4. Dependências (predecessoras) identificadas e concluídas ou planejadas para antes do item.
5. Rastreabilidade registrada: feature pai, elemento ArchiMate e requisito de qualidade (REQ-xx) nas tags.
6. Prioridade MoSCoW definida pelo Product Owner e valor de negócio atribuído.

## DoD de PBI

1. Todos os cenários Gherkin do critério de aceite verificados e evidenciados (teste automatizado, relatório ou roteiro com prints).
2. Código ou artefato revisado em pull request aprovado por outro integrante (CODEOWNERS) e integrado à branch main.
3. Pipeline de CI verde: build, testes, lint e verificações de segurança (SAST, SCA e secret scan).
4. Testes automatizados para o caminho feliz e para os cenários de erro sempre que o item envolve código.
5. Nenhuma vulnerabilidade High/Critical aberta sem aceite formal, nenhum segredo commitado e dados pessoais tratados conforme a LGPD (REQ-05).
6. Requisitos de qualidade aplicáveis (REQ-01 a REQ-07) atendidos e medidos.
7. Documentação atualizada (README, OpenAPI, wiki ou model card) e rastreabilidade ArchiMate mantida nas tags.
8. Demonstrado ao Product Owner na Sprint Review e estado atualizado para Done no Azure Boards.

## DoD de Feature

1. Todos os PBIs filhos em Done ou movidos explicitamente pelo Product Owner.
2. Fluxo ponta a ponta da feature demonstrado em ambiente integrado.
3. Critérios de aceite da feature verificados na Sprint Review.
4. Documentação e diagramas afetados atualizados (README, wiki, views ArchiMate).

## DoD de Épico

1. Features necessárias em Done; as remanescentes repriorizadas pelo Product Owner.
2. Métricas de sucesso do épico medidas e registradas na wiki.
3. Views ArchiMate atualizadas quando a arquitetura mudou.
4. Resultado apresentado aos stakeholders (banca FIAP x Ford) e lições registradas na retrospectiva.

## DoD de Tarefa

1. Trabalho commitado em branch vinculada ao PBI e revisado por outro integrante.
2. Remaining Work zerado e estado Done no taskboard.
3. Evidência registrada no PBI quando a tarefa é de teste ou de documentação.

## Evolução da DoD

| Sprints | DoD vigente |
| --- | --- |
| Sprints 1 e 2 | DoD inicial: PR revisado, CI mínimo (lint e build), critérios de aceite demonstrados ao PO e documentação no README. |
| Sprint 3 em diante | DoD atual: soma testes automatizados com relatório, pipeline DevSecOps (SAST, SCA, secret scan e Trivy), requisitos de qualidade REQ-01 a REQ-07 medidos e rastreabilidade ArchiMate nas tags. |
