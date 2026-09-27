# QA Sprint 3: plano do projeto no Azure DevOps

Entrega de **Testing, Compliance and Quality Assurance** (Prof. Elias Bernardo) na Sprint 3 do Challenge FIAP x Ford 2026: o plano detalhado do ForwardService no **Azure Boards** (processo Scrum), com backlog alinhado ao TOGAF/ArchiMate, critérios BDD, Definition of Done, MoSCoW, Planning Poker, dependências, release plan balanceado e o detalhamento da Sprint 3.

Comece pelo [**PLANO_AZURE_DEVOPS.md**](PLANO_AZURE_DEVOPS.md): ele explica o plano e traz o passo a passo para publicar no Azure DevOps e dar acesso ao professor.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| [`PLANO_AZURE_DEVOPS.md`](PLANO_AZURE_DEVOPS.md) | Documento do plano: TOGAF/ArchiMate, BDD, DoD, priorização, dependências, release plan, Sprint 3 e como publicar |
| [`backlog.json`](backlog.json) | Fonte única do plano: 6 sprints, 8 épicos, 21 features, 60 PBIs e 34 tarefas da Sprint 3 |
| [`azure_devops_import.py`](azure_devops_import.py) | Publica o plano no Azure DevOps pela REST API 7.1 (só biblioteca padrão, idempotente, com dry-run) |
| [`gen_csv.py`](gen_csv.py) | Gera o `backlog.csv` a partir do `backlog.json` |
| [`backlog.csv`](backlog.csv) | Plano B: Boards > Queries > Import work items (hierarquia Title 1 a Title 4; sem predecessoras) |
| [`tests/test_import_mock.py`](tests/test_import_mock.py) | 37 testes contra um Azure DevOps falso (http.server + unittest) |
| [`dry_run_output.txt`](dry_run_output.txt) | Saída do dry-run offline: tudo o que o script criaria |
| [`wiki/`](wiki/) | As 7 páginas da wiki geradas (mesmo conteúdo publicado no Azure DevOps) |

## Comandos

Na pasta `academic/qa/sprint3`:

```powershell
# testes (sobem um Azure DevOps falso em 127.0.0.1)
python -m unittest discover -s tests -v

# conferência sem alterar nada (sem PAT roda offline)
python azure_devops_import.py --org https://dev.azure.com/<organizacao> --project ForwardService --dry-run

# publicação (pede o PAT de forma oculta ou lê AZDO_PAT)
python azure_devops_import.py --org https://dev.azure.com/<organizacao> --project ForwardService --professor profelias.bernardo@fiap.com.br

# plano B por CSV
python gen_csv.py
```

O PAT nunca é impresso nem salvo. Use um PAT com validade de 1 dia e revogue depois da publicação.

## Equipe

João Victor Franco (Jota, RM 556790), Lucca Saraiva Borges (RM 554608), Ruan Melo Vieira (RM 557599) e Rodrigo César Jimenez (RM 558148). Turma 3ESPZ, Engenharia de Software FIAP.
