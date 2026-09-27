# Critérios de priorização (MoSCoW) e estimativa (Planning Poker)

## MoSCoW (obrigatoriedade, necessidade e opcionalidade)

| MoSCoW | Priority no Azure | Critério |
| --- | --- | --- |
| Must | 1 | Obrigatório: exigido pela rubrica de uma disciplina do Challenge, pela LGPD ou pré-requisito de outro Must. Sem ele a release não é aceita. |
| Should | 2 | Necessário: alto valor para o usuário ou para a qualidade, mas existe contorno temporário. Entra na release se a capacidade permitir. |
| Could | 3 | Opcional: desejável, com baixo impacto se ficar de fora; primeiro candidato a corte. |
| Won't | 4 | Fora deste horizonte: registrado para transparência, sem sprint planejada; reavaliado a cada release. |

Distribuição dos PBIs:

| MoSCoW | PBIs | Pontos |
| --- | --- | --- |
| Must | 38 | 197 |
| Should | 15 | 87 |
| Could | 4 | 26 |
| Won't | 3 | 47 |

## Planning Poker

Escala: 1, 2, 3, 5, 8, 13, 21 (Fibonacci modificada).

- Cada integrante vota em segredo e as cartas são reveladas juntas.
- Se os votos divergem mais de dois valores da escala, os extremos explicam e há nova rodada (no máximo três).
- A história de referência (5 pontos) é o PBI-011, registro de evento de serviço com erros RFC 7807: conhecida por todo o time e com esforço estável.
- Itens acima de 13 pontos não entram em sprint: são quebrados (o 21 aparece apenas no backlog futuro).
- Tarefas são estimadas em horas (Remaining Work) com uma nota de complexidade em pontos Fibonacci.

História de referência: **PBI-011 Registro de evento de serviço com erros RFC 7807 e contrato OpenAPI** (5 pontos).

## Valor de negócio

Business Value de 1 a 100, definido pelo PO a partir do Quadro de Valor; desempata itens com a mesma prioridade.

| MoSCoW | Faixa de Business Value |
| --- | --- |
| Must | 60 a 90 |
| Should | 60 a 85 |
| Could | 55 a 70 |
| Won't | 30 a 40 |
