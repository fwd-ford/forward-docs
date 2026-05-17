# Features comportamentais por VIN

**VINs com features derivadas:** 175,554
**Total de eventos:** 602,788
**CSV completo de features:** `tmp_research/official/data/vin_features.csv`

## Distribuicoes-chave

### Eventos por VIN
| Eventos | VINs | % |
|---:|---:|---:|
| 1 | 50,499 | 28.77% |
| 2 | 39,564 | 22.54% |
| 3 | 31,177 | 17.76% |
| 4 | 16,076 | 9.16% |
| 5 | 11,418 | 6.50% |
| 6 | 8,174 | 4.66% |
| 7 | 4,225 | 2.41% |
| 8 | 2,971 | 1.69% |
| 9 | 3,265 | 1.86% |
| 10 | 1,709 | 0.97% |
| 11 | 1,043 | 0.59% |
| 12 | 1,478 | 0.84% |
| 13 | 520 | 0.30% |
| 14 | 423 | 0.24% |
| 15 | 886 | 0.50% |

### Tenure (dias entre InvoiceDate/SalesDate e ultimo servico)
  mean=760.2 | p25=401 | median=669 | p75=1034 | min=4 | max=2945

### Gap medio entre servicos (dias)
  mean=240.8 | p25=140 | median=221 | p75=342 | min=0 | max=2023

### KM maximo registrado
  mean=52523.2 | p25=15371 | median=29508 | p75=48323 | min=1 | max=955388451

### Diversidade de dealers visitados
| Dealers distintos | VINs | % |
|---:|---:|---:|
| 1 | 127,654 | 72.71% |
| 2 | 38,015 | 21.65% |
| 3 | 7,796 | 4.44% |
| 4 | 1,628 | 0.93% |
| 5 | 333 | 0.19% |
| 6 | 81 | 0.05% |
| 7 | 29 | 0.02% |
| 8 | 11 | 0.01% |
| 9 | 5 | 0.00% |
| 10 | 1 | 0.00% |

## Implicacoes para ML

Cada VIN tem ate **20+ features derivadas** sem precisar de fonte externa.
As mais importantes para deteccao de churn:
- `days_since_last_service` (recencia)
- `gap_avg_days` x `gap_last_days` (acelerando ou retardando?)
- `dealers_distinct` (lealdade ao dealer)
- `service_types_distinct` (rico em comportamento ou unidimensional)
