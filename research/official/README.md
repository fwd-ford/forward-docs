# research/official/

Pesquisas executadas em **2026-05-11** sobre o dataset oficial Ford (`vin_share_Desafio_02.xlsx`) e suas fontes complementares.

Conteúdo consolidado em [../../project/02e_DATASET_OFICIAL_E_FONTES.md](../../project/02e_DATASET_OFICIAL_E_FONTES.md).

## Estrutura

### `01_internal_analysis/`
Análises diretas sobre o dataset oficial (sem fonte externa):
- `inventory.md` — schema completo, distribuições por coluna, missing rates
- `geography.md` — cobertura geográfica (100% BRA)
- `codebook_inferred.md` — cross-tabs dos campos Service* pra inferir codebook
- `behavioral_features.md` — engenharia de features comportamentais (20+ por VIN)
- `sha1_reversal_test.md` — teste de reversão do `VIN_Hash` (5M tentativas, 0 matches)

### `02_external_sources/`
Pesquisas em fontes públicas brasileiras:
- `fenabrave_vio.md` — frota Ford BR (VIO) via FENABRAVE/Sindipeças
- `ford_dealers.md` — diretório de 80 dealers Ford geocodificados (ABRADIF)
- `fipe_values.md` — valores FIPE por modelo×ano (API Parallelum)
- `senacon_recalls.md` — 12 campanhas de recall Ford BR
- `manuals_maintenance.md` — cronograma oficial de manutenção Ford BR

## Bibliografia

Todas as URLs citadas em [../../project/02e_REFERENCIAS.md](../../project/02e_REFERENCIAS.md) (90+ fontes organizadas por tema).

## Para uso acadêmico

Cada pesquisa cita fonte URL + data de acesso por número. Fontes 🟢 (oficiais — Ford, FENABRAVE, Senacon, FIPE) podem ser usadas com confiança em entregáveis avaliativos. Fontes 🟡 (imprensa) servem como secundárias.
