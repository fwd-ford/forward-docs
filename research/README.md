# research/

Trabalhos de pesquisa do projeto Ford Forward — análises internas de datasets e levantamento de fontes externas.

## Estrutura

### `official/` — Pós-dataset oficial Ford (11/05/2026)

Material gerado entre 11-17/05/2026 após recebimento do `vin_share_Desafio_02.xlsx` oficial via coordenação FIAP.

#### `01_internal_analysis/`
5 markdowns de análise interna do dataset oficial:
- `inventory.md` — schema completo, distribuições por coluna, taxa de missing
- `geography.md` — distribuição por Country (100% BRA confirmado)
- `codebook_inferred.md` — cross-tabs de ServiceType × ServiceCode × ServiceRepairTypeCode
- `behavioral_features.md` — descrição das 20+ features comportamentais por VIN
- `sha1_reversal_test.md` — teste de reversão do VIN_Hash (5M tentativas, 0 matches)

#### `02_external_sources/`
5 markdowns de pesquisa em fontes externas públicas:
- `fenabrave_vio.md` — VIO Ford BR (frota em circulação)
- `ford_dealers.md` — diretório de 80 concessionárias geocodificadas
- `fipe_values.md` — 95 valores FIPE por modelo×ano
- `senacon_recalls.md` — 12 campanhas de recall Ford BR
- `manuals_maintenance.md` — cronograma oficial de manutenção

### Documentos consolidados (na pasta `project/`)

- **`project/02e_DATASET_OFICIAL_E_FONTES.md`** — relatório master consolidando tudo
- **`project/02e_REFERENCIAS.md`** — bibliografia organizada (90+ URLs)
- **`project/FOLLOW_UP_2026-05-17_DATASET_OFICIAL.md`** — comunicação pro grupo

## Dados estruturados (em `forward-ml/data/`)

- `forward-ml/data/processed/vin_features.csv` — 175k VINs × 20+ features (input ML)
- `forward-ml/data/processed/profile.json` — perfil quantitativo
- `forward-ml/data/external/fipe_values.csv` — valores FIPE
- `forward-ml/data/external/ford_dealers.csv` — dealers geocodificados
- `forward-ml/data/external/ford_recalls.csv` — campanhas de recall
- `forward-ml/data/external/maintenance_schedules.csv` — cronograma de manutenção

## Reprodutibilidade

Scripts em `forward-ml/scripts/`:
- `inspect_xlsx.py` — inspeção estrutural
- `profile_dataset.py` — gera `profile.json`
- `internal_analysis.py` — gera os 5 markdowns de análise interna + `vin_features.csv`
