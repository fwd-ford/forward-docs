# Diretório de concessionárias Ford Brasil

> Coleta realizada em 2026-05-11 para o projeto Ford Forward (FIAP-Ford Challenge 2026).
> Objetivo: alimentar análise de "service deserts" cruzando densidade de eventos pós-venda
> (dataset 602k eventos / 435 `DealerCode`) com a rede física Ford no Brasil.

## Resumo executivo

- **80 concessionárias únicas** coletadas (de ~120 estimadas na rede oficial — cobertura ~67%).
- Cobertura geográfica: **25 das 27 UFs** (faltam apenas AM e SE no extrato ABRADIF).
- Todos os 80 registros incluem: nome (truncado em ~20 chars), endereço, cidade, UF, CEP e **latitude/longitude**.
- Fonte primária: **ABRADIF** (Associação Brasileira dos Distribuidores Ford) — o único catálogo
  estruturado e público que sobreviveu ao fim da produção Ford no Brasil em 2021.
- Domínio histórico `fordconcessionaria.com.br` **não resolve mais** (NXDOMAIN em 2026-05-11).
- Portal oficial `ford.com.br/localize-uma-concessionaria/` retorna **403** (anti-bot Cloudflare/Akamai).
- Rede CAOA Ford (`ford.caoa.com.br`) lista apenas **5 unidades CAOA-Ford** (todas em SP):
  Ceasa, Jabaquara, Campinas, Santos, Ibirapuera — é uma sub-rede, não a rede toda.

## Método

### 1. Sondagem das fontes oficiais

| Fonte | URL | Status | Resultado |
|---|---|---|---|
| Ford Brasil locator | `ford.com.br/localize-uma-concessionaria/` | HTTP 403 | bloqueado |
| fordconcessionaria.com.br | DNS | NXDOMAIN | domínio desativado |
| CAOA Ford | `ford.caoa.com.br/sitemap-branchlocations.xml` | HTTP 200 | apenas 5 unidades (sub-rede CAOA) |
| ABRADIF homepage | `abradif.com.br/` | HTTP 200 | **JSON inline com 93 entradas** |
| ABRADIF search | `abradif.com.br/conc_busca.php` (POST `tbusca=`) | HTTP 200 | mesmo formato, filtra por termo |
| ABRAFOR (caminhões) | `abrafor.com.br` | DNS NXDOMAIN | indisponível |

### 2. Extração ABRADIF

A página inicial executa `carregaBR()` em JavaScript, que injeta um array literal
`locationBR = [['<div><b>NOME</b><br>ENDEREÇO<br>CIDADE/UF - CEP: NNNN<br></div>','LAT','LON',idx], ...]`.

Esse array carrega todos os marcadores do mapa Google Maps de uma vez — não há endpoint
JSON segregado, é HTML estático. Parseado com regex (`tmp_research/_scrape/parse_abradif.py`).

**Total de requests externos: 7** (3 HEAD-equiv para verificar status + 4 buscas amostrais
no `conc_busca.php` para confirmar formato e completude). Bem dentro do orçamento de 50.

### 3. Deduplicação

O array bruto traz 93 entradas, mas várias estão repetidas (ex.: FENIX BELÉM aparece
4 vezes; SALOMÃO/BOA VISTA 3 vezes; VEPEL/CAMPINA GRANDE 3 vezes). Provavelmente são
"pins" duplicados por múltiplos serviços (vendas, peças, pós-venda) sob o mesmo CNPJ.
Dedupe por `(nome, cidade, uf, cep)` → **80 únicas**.

### 4. Tratamento de coordenadas

A maioria dos lat/lon vem com um sufixo `...197085` constante (ex.:
`-23.5305823197085`) — é um *jitter* fixo aplicado pela ABRADIF (provavelmente legado
de privacidade). Arredondado para 5 casas decimais (~1,1m de precisão), o suficiente
para análise em escala municipal.

## Distribuição por estado

| UF | N dealers | UF | N dealers |
|---|---|---|---|
| SP | 13 | TO | 2 |
| PR | 10 | DF | 2 |
| SC | 7  | RO | 2 |
| RS | 7  | RJ | 2 |
| MG | 7  | PE | 1 |
| GO | 6  | CE | 1 |
| MT | 3  | AC | 1 |
| BA | 3  | RN | 1 |
| MS | 3  | PI | 1 |
| PA | 2  | ES | 1 |
| AP | 1  | RR | 1 |
| AL | 1  | PB | 1 |
| MA | 1  | **AM, SE** | **0 (ausentes)** |

Sul + Sudeste = 49 dealers (61%). Norte + Centro-Oeste sub-representados
(15 dealers em 11 UFs, ~19%).

## Amostra de dealers coletados (primeiros 20, ordenado por UF/cidade)

| # | Nome (ABRADIF, truncado) | Cidade | UF |
|--|---|---|---|
| 1 | RECOL | Rio Branco | AC |
| 2 | LAGUNA | Maceió | AL |
| 3 | MOSELLI | Macapá | AP |
| 4 | BURITI BARREIRAS | Barreiras | BA |
| 5 | INDIANA - SALVADOR | Salvador | BA |
| 6 | ATLANTA | Vitória da Conquista | BA |
| 7 | CRASA SUL | Fortaleza | CE |
| 8 | BRASAL TAGUATINGA | Brasília | DF |
| 9 | SLAVIERO SIA | Brasília | DF |
| 10 | VIAFOR COLATINA | Colatina | ES |
| 11 | NAVESA - ANAPOLIS | Anápolis | GO |
| 12 | TRIAUTO - CATALAO | Catalão | GO |
| 13 | CIAASA. | Goiânia | GO |
| 14 | NAVESA - AUTOMOVEI | Goiânia | GO |
| 15 | REGIVEL - ITUMBIAR | Itumbiara | GO |
| 16 | REGIVEL - RIO VERD | Rio Verde | GO |
| 17 | DUVEL - SAO LUIS - | São Luís | MA |
| 18 | BH FOR - BELO HORI | Belo Horizonte | MG |
| 19 | BRASAUTO - GOV. VA | Governador Valadares | MG |
| 20 | ORIGINAL - MATRIZ | Juiz de Fora | MG |

Listagem completa em `tmp_research/official/data/ford_dealers.csv`.

## Cobertura

- **80 dealers únicos**, salvos em `ford_dealers.csv` com colunas:
  `dealer_name, city, uf, address, cep, phone, latitude, longitude, source_url`.
- Coordenadas presentes em **todos os 80 registros** (geocoding já feito pela ABRADIF).
- Telefones **não** coletados (campo vazio) — a página inicial não expõe.

## Gaps e limitações

### Cobertura incompleta vs. rede oficial
- **80 coletadas vs. ~120 oficiais** = gap de ~33%. Fontes de imprensa de jan/2025
  (CNN Brasil, Autopapo, ISTOÉ Dinheiro) reportam ~120 concessionárias Ford ativas
  no Brasil pós-2021. A ABRADIF representa associadas (não 100% obrigatório), o que
  explica o gap.
- **UFs ausentes:** AM (Amazonas) e SE (Sergipe) não aparecem. Em consultas anteriores
  Ford tinha presença em Manaus e Aracaju — possivelmente saíram da ABRADIF.

### Nomes truncados
- A ABRADIF guarda só os primeiros ~20 caracteres do nome no popup do mapa
  (ex.: "BH FOR - BELO HORI" = "BH FOR - BELO HORIZONTE"; "REGIVEL - RIO VERD" = 
  "REGIVEL - RIO VERDE"). Para nome legal/comercial completo seria necessário
  scraping individual de cada concessionária — não feito (excederia orçamento de calls).

### Telefones e horários ausentes
- Não disponíveis no payload. Estão em páginas individuais de cada concessionária
  (subdomínios próprios tipo `fancar.com.br`, `brasal.com.br`, `gruposinal.com.br`).

### DealerCode (numérico do dataset) → Nome
- **NÃO conseguimos mapear.** O dataset interno usa códigos como `4146, 2033, 2195`
  (435 únicos), mas a ABRADIF **não expõe** esses códigos — usa apenas índices sequenciais
  (1..93) que mudam a cada render. O mapeamento `DealerCode → dealer` é dado proprietário
  da Ford (interno ao DMS / sistema de garantia). Sem ele:
  - Não dá pra cruzar **diretamente** os 602k eventos com os 80 dealers nomeados.
  - **Workaround viável:** usar o campo `city`/`state` do dataset (se existir) ou
    inferir região por agrupamento de DealerCode → comparar densidades regionais
    com o mapa de 80 dealers para identificar service deserts em nível UF/região.

### Discrepância 435 vs. 80
- Dataset: 435 `DealerCode` únicos. Catálogo público: 80 dealers ativos. A diferença
  reflete o efeito do fechamento da fábrica em 2021 — antes Ford tinha ~283 pontos de
  venda; muitos DealerCodes do dataset representam concessionárias **hoje extintas**,
  o que é informação valiosa em si para o estudo de "service deserts" (regiões que
  perderam capilaridade).

## Próximos passos sugeridos (fora do escopo desta coleta)

1. **Geocoding complementar**: dos 80, todos já têm coords; para os ~40 faltantes da
   rede total, geocodificar pelo Nominatim/OSM a partir de cidade+UF.
2. **Cruzamento dataset↔catálogo via cidade/UF** (não via DealerCode): contar
   eventos por município e sobrepor ao mapa dos 80 dealers para identificar municípios
   "órfãos" (alta densidade de eventos, zero dealers num raio de N km).
3. **Validar UFs ausentes** (AM, SE): busca pontual no Google Maps por
   "concessionária Ford Manaus" e "concessionária Ford Aracaju" para confirmar/descartar
   sua existência atual.

## Fontes

- ABRADIF — Associação Brasileira dos Distribuidores Ford: <https://www.abradif.com.br/>
  (extração via array `locationBR` em `carregaBR()` na homepage).
- CAOA Ford sitemap branch locations: <https://ford.caoa.com.br/sitemap-branchlocations.xml>
  (5 unidades, complementar).
- Imprensa/contexto (estimativa de ~120 dealers em 2024-2025):
  - CNN Brasil — "Ford vai fechar 160 concessionárias..."
  - Autopapo — "No Brasil, 160 cidades podem ficar sem concessionárias Ford"
  - AgenciaDC News — "rede Ford ganha 16 posições e chega ao top 5 em ranking da Fenabrave"
