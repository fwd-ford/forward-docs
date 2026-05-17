# Codebook inferido (Service* fields)

> Inferencia por co-ocorrencia. Nao substitui o codebook oficial da Ford, mas da pistas fortes.

## ServiceType x ServiceRepairTypeCode

| Outer | Top Inner (com %) | Total |
|---|---|---:|
| `Maintenance` | `` (77.0%); `C` (20.8%); `W` (1.6%); `I` (0.6%); `A` (0.0%); `U` (0.0%) | 602,788 |

## ServiceType x ServiceCode

| Outer | Top Inner (com %) | Total |
|---|---|---:|
| `Maintenance` | `569` (19.8%); `571` (14.3%); `573` (9.8%); `574` (6.2%); `1226` (5.4%); `575` (4.1%) | 602,788 |

## ServiceDeptCode x ServiceType

| Outer | Top Inner (com %) | Total |
|---|---|---:|
| `` | `Maintenance` (100.0%) | 464,412 |
| `S` | `Maintenance` (100.0%) | 66,674 |
| `Q` | `Maintenance` (100.0%) | 44,635 |
| `U` | `Maintenance` (100.0%) | 26,570 |
| `B` | `Maintenance` (100.0%) | 427 |
| ` ` | `Maintenance` (100.0%) | 70 |

## MainSource x ServiceType

| Outer | Top Inner (com %) | Total |
|---|---|---:|
| `Agenda + Official Maintenance` | `Maintenance` (100.0%) | 431,160 |
| `Agenda + Official Maintenance + GUDB` | `Maintenance` (100.0%) | 135,842 |
| `Official Maintenance` | `Maintenance` (100.0%) | 32,683 |
| `Official Maintenance + GUDB` | `Maintenance` (100.0%) | 3,103 |
