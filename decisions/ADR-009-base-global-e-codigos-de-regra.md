# ADR-009: BASE-GLOBAL com regras codificadas

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota
- **Substitui:** o domínio "fila de leads por veículo" do plano de rebuild de 12/09/2026. A arquitetura, a stack e o modelo de acesso daquele plano continuam valendo.

## Contexto

A ideia final do produto (etiqueta, termômetro, ação, n8n e o ciclo fechado) muda o domínio: não é mais uma fila de leads gerada por uma regra de atraso. O projeto precisa de uma especificação única, que o código, os testes e a apresentação citem sem divergir.

## Decisão

- **Dois documentos centrais:**
  - [BASE-GLOBAL](../produto/BASE-GLOBAL.md): o quê e as regras;
  - [ESTADO-E-PLANO](../produto/ESTADO-E-PLANO.md): onde estamos e a ordem das levas.
- **Código por regra, com prefixo por domínio:** REL, ACS, NUC, ETQ, TRM, REC, APR, CNS, HOJ, FIC, CTT, AGD, CNV, INT, CAN, NTF, PRV, DES, EST, DEM.
- **Onde o código aparece:**

  | Onde | Como |
  | --- | --- |
  | Migration | comentário em inglês acima da cláusula (`-- ETQ-4: forgotten when overdue`) |
  | pgTAP | descrição começa pelo código (`'ETQ-4: ...'`), um arquivo por domínio |
  | Java | `@DisplayName("CTT-2: ...")` |
  | App | só nos testes do que a tela reflete; nenhuma regra implementada no app |
  | PR | seção "Regras" lista os códigos tocados |

- **Ciclo de vida de uma regra:**
  - número nunca é reaproveitado;
  - regra revogada fica riscada, com data e motivo;
  - mudar um limiar cria nova versão de parâmetro com o mesmo código.
- **Verificação:** um script `check-rules` cruza catálogo, código e testes. Ele falha quando uma regra real não tem teste, quando o código cita um código fora do catálogo ou quando um código revogado continua citado.

## Consequências

- Mudar uma regra é mudar um parágrafo e procurar o código no resto.
- Tabelas, colunas e funções ficam em inglês, como exige o forward-infra; os códigos e os textos ficam em português.
- O "lead" some da interface; `leads` vira `recommendations` (o que o cérebro sugere) e `tasks` (o que cabe a um humano).
