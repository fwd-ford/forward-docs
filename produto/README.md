# Produto: o app da Maria

Documentação viva do ForwardService a partir do rebuild de setembro de 2026. Os documentos de `project/` contam a pesquisa e a Sprint 1; os daqui dizem o que o produto é agora e como está sendo construído.

## Ordem de leitura

| Documento | Para quê | Muda quando |
| --- | --- | --- |
| [BASE-GLOBAL](./BASE-GLOBAL.md) | o que o produto é: glossário, domínio, o cérebro (etiqueta, termômetro, ação), regras do app com código, mapa de telas, integrações | uma regra muda |
| [ROTEIRO-DEMO](./ROTEIRO-DEMO.md) | a história do João e da Maria como teste de aceite, com os números que cada passo precisa bater | o roteiro muda |
| [ESTADO-E-PLANO](./ESTADO-E-PLANO.md) | o que já existe, as levas L0 a L10, cortes, dívidas e lições | a cada leva |
| [EQUIPE-E-TAREFAS](./EQUIPE-E-TAREFAS.md) | quem faz o quê, a divisão de esforço e os épicos no GitHub | a cada redistribuição |
| [levas/](./levas/) | ficha de cada leva: entregas, gates, mutações, prints, desvios | ao fechar a leva |

Decisões de arquitetura ficam em [decisions/](../decisions/). Para rodar tudo na sua máquina: [guides/RODAR-LOCAL.md](../guides/RODAR-LOCAL.md).

## A ideia em três linhas

Todo cliente Ford carrega uma **etiqueta** (que tipo de cliente é), um **termômetro** de 0 a 100 (quão perto está de sumir) e uma **ação sugerida** (o que fazer agora). Um cérebro de regras recalcula as três de madrugada, o n8n executa as ações automáticas por um WhatsApp simulado e a consultora usa o app para falar com quem importa e registrar o resultado uma vez. Quando o cliente volta, ele vira Fiel, e o cérebro aprende.
