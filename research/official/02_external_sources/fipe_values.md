# Tabela FIPE — modelos Ford no dataset

> Coleta para o componente "Valor de mercado" do **Lifetime Service Value (LSV)** do projeto Ford Forward (FIAP-Ford Challenge 2026).

## Resumo executivo

- **API usada:** Parallelum FIPE API v1 (`https://parallelum.com.br/fipe/api/v1/`)
- **Marca:** Ford (codigo `22`)
- **Mês de referência FIPE:** **maio de 2026** (uniforme em todas as consultas)
- **Cobertura:** 71 de 95 combinações modelo×ano alvo possuem valor FIPE válido (≈75%). As 24 ausentes são casos legítimos sem entrada FIPE (modelo não comercializado naquele ano no Brasil) — todas marcadas como `n/a` no CSV com justificativa.
- **Data de coleta:** 2026-05-11
- **Trims agregados:** quando havia múltiplas versões para o mesmo ano×modelo, calculou-se média aritmética simples e registou-se min/max + `n_versions`.

## Range de valores por modelo (BRL)

| Modelo | Min FIPE | Max FIPE | Anos cobertos no FIPE | Ticket médio |
|---|---:|---:|---|---:|
| KA | R$ 38.005 | R$ 64.282 | 2017–2021 (5/5) | ~R$ 47k |
| FIESTA | R$ 50.911 | R$ 58.041 | 2017–2019 (3/3) | ~R$ 55k |
| ECOSPORT | R$ 58.773 | R$ 85.193 | 2017–2021 (5/6, falta 2022) | ~R$ 72k |
| FOCUS | R$ 57.070 | R$ 67.111 | 2017–2019 (3/3) | ~R$ 60k |
| RANGER | R$ 128.915 | R$ 318.395 | 2017–2026 (10/10) | ~R$ 195k |
| MAVERICK | R$ 152.785 | R$ 219.612 | 2022–2026 (5/5) | ~R$ 183k |
| TERRITORY | R$ 112.601 | R$ 193.043 | 2021–2026 (6/7, falta 2020) | ~R$ 152k |
| TRANSIT | R$ 230.108 | R$ 266.010 | 2023–2026 (4/5, falta 2022) | ~R$ 248k |
| EDGE | R$ 121.638 | R$ 189.793 | 2017–2020 (4/4) | ~R$ 158k |
| FUSION/MONDEO | R$ 96.243 | R$ 132.640 | 2017–2019 (3/3) | ~R$ 111k |
| MUSTANG | R$ 346.106 | R$ 609.262 | 2018–2025 (7/10, falta 2017/2020/2026) | ~R$ 448k |
| F-150 | R$ 357.816 | R$ 523.848 | 2023–2025 (3/10) | ~R$ 444k |
| BRONCO SPORT | R$ 149.321 | R$ 234.910 | 2021–2025 (5/6, falta 2026) | ~R$ 184k |
| MUSTANG MACH-E | R$ 327.599 | R$ 417.599 | 2023–2025 (3/5) | ~R$ 384k |
| F-SERIES | R$ 128.915 | R$ 523.848 | 2017–2025 (proxy) | ver notas |

## Tabela completa

A tabela completa (95 linhas) está em CSV: [`../data/fipe_values.csv`](../data/fipe_values.csv).

Colunas: `model, year, fipe_mean_brl, fipe_min_brl, fipe_max_brl, n_versions, reference_month, source`.

### Amostra (top 10 maiores FIPE)

| Modelo | Ano | FIPE médio | Versões |
|---|---|---:|:--|
| MUSTANG | 2025 | R$ 567.895 | GT Performance + Dark Horse |
| F-150 | 2025 | R$ 518.664 | Lariat + L. Black + Tremor |
| F-150 | 2024 | R$ 449.154 | Lariat + Lariat Black |
| MUSTANG MACH-E | 2025 | R$ 417.599 | GT Performance |
| F-150 | 2023 | R$ 361.262 | Lariat + Platinum |
| MUSTANG MACH-E | 2024 | R$ 406.563 | GT Performance |
| RANGER | 2026 | R$ 279.551 | Limited V6 + XLT V6 + Black |
| RANGER | 2025 | R$ 259.307 | + Raptor R$415k |
| RANGER | 2024 | R$ 258.350 | Limited V6 + XLT V6 (nova geração) |
| TRANSIT | 2026 | R$ 266.010 | Furgão 2.0 Aut |

## Implicação direta para LSV

A diferença Ka×Ranger Limited V6 confirma a tese do briefing:

- Ka 2017 (R$ 38k) — base de manutenção barata
- Ranger Limited V6 2026 (R$ 318k) — **8.4×** mais valioso como ativo, justifica prioridade de lead

**Spread observado:** R$ 38.005 (Ka 2017) → R$ 609.262 (Mustang Dark Horse 2025) = fator 16× entre menor e maior FIPE no portfólio.

## Notas técnicas

### F-SERIES vs F-150
- A categoria F-SERIES no dataset Ford foi tratada como **família ampla** (inclui Ranger + F-150).
- Para 2017–2022 usei **Ranger como proxy** (F-150 não tinha oferta nacional nesse período após a saída em 2014).
- Para 2023+ usei **F-150 oficial** (importação relançada 2023).
- Se o time preferir tratar F-SERIES apenas como F-150 importado pesado, basta filtrar `model == 'F-150'` no CSV.

### Modelos sem FIPE encontrado (justificativa)
- **TERRITORY 2020:** lançamento no Brasil só em meados de 2020 como linha 2021, sem entrada FIPE explícita para 2020.
- **ECOSPORT 2022:** linha descontinuada em 2021 (fábrica de Camaçari encerrada), sem 2022 FIPE.
- **TRANSIT 2022:** Transit teve hiato — relançada em 2023, sem oferta 2022.
- **MUSTANG 2017/2020:** sem oferta nacional regular nesses anos (2020 teve apenas Black Shadow esporádico).
- **F-150 2017–2022:** F-150 saiu do Brasil em 2014; só voltou via importação em 2023.
- **BRONCO SPORT 2026, MUSTANG MACH-E 2026:** entrada de linha 2026 ainda não publicada na FIPE até maio/2026.
- **F-SERIES 2026:** mesma razão (F-150 2026 ainda não publicado).

### Variação por trim — magnitude observada

| Modelo×Ano | Trim base | Trim topo | Spread % |
|---|---:|---:|---:|
| Ka 2021 (SE vs Freestyle 1.5) | R$ 49.625 | R$ 64.282 | +30% |
| EcoSport 2021 (SE vs Titanium) | R$ 73.979 | R$ 85.193 | +15% |
| Ranger 2021 (Storm vs Limited 3.2 vs Tropivan) | R$ 156k | R$ 207k | +33% |
| Ranger 2025 (Black vs Limited V6 vs XLT V6 vs Raptor) | R$ 208k | R$ 415k | +99% |
| F-150 2025 (Lariat vs L.Black vs Tremor) | R$ 509k | R$ 523k | +3% |
| Mustang 2025 (GT Performance vs Dark Horse) | R$ 526k | R$ 609k | +16% |

**Implicação:** para LSV preciso, usar trim quando o VIN traz essa info (campo `DESCRICAO_MODELO`); cair para `fipe_mean_brl` quando só houver modelo+ano. O spread médio (~25%) está dentro da banda aceitável para um proxy.

### Decimal/moeda
- Valores armazenados como **inteiros (BRL sem centavos)** para facilitar joins SQL.
- Quem precisar do valor exato consulta o endpoint Parallelum diretamente — a API retorna formato `R$ 123.456,00`.

## Fontes

- **Parallelum FIPE API v1** — `https://parallelum.com.br/fipe/api/v1/carros/marcas/22/...`
  - Documentação: `https://deividfortuna.github.io/fipe/`
  - Data de acesso: **2026-05-11**
  - Mês de referência FIPE retornado: **maio de 2026**
  - Limites: API pública gratuita, sem autenticação; observados sporadic HTTP 500 em rajada — usado fallback de re-query.
- **Códigos consultados** (rastreabilidade): coluna `source` no CSV traz o(s) `cod` de modelo Parallelum por linha — permite reproduzir qualquer valor em segundos.
- **FIPE oficial** (`https://veiculos.fipe.org.br`): não usado diretamente (form com ViewState JSF), mas Parallelum espelha os mesmos dados.

---

**Próximo passo sugerido:** join desta tabela com o dataset 500k usando `(MODELO_NORM, ANO_FABRICACAO)` para hidratar campo `fipe_brl` na pipeline de ML/segmentação, e usar no cálculo de `lsv_score` junto com tickets de serviço.
