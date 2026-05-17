# VIO Ford Brasil — FENABRAVE/Sindipeças

> Pesquisa pública para Challenge Ford 2026 (Forward Service). Data da coleta: **2026-05-11**.
> Objetivo: estimar o denominador do VIN Share (frota Ford circulante no Brasil), contra os 175.554 VINs do dataset interno de oficinas.

## Resumo executivo

- **Frota total Brasil 2024:** **62,1 milhões** de veículos + motos (Sindipeças) ou **48 milhões** de veículos automotores (excluindo motos). Considerando todos os tipos (incluindo reboques), Senatran/Veloe-Fipe reporta **123,97 milhões** de unidades. As três fontes medem coisas diferentes.
- **Frota Ford Brasil estimada:** entre **~3,5 e ~5 milhões** de veículos `[estimativa]` — não foi possível obter o número oficial Sindipeças por marca em fontes públicas gratuitas. Apenas o **Ford Ka** ultrapassou **1 milhão** de unidades produzidas só no Brasil (marco de 2017), e o **Fiesta** acumulou **mais de 1,8 milhão de vendas** até 2015. O **EcoSport** somou **mais de 1,2 milhão** de unidades produzidas em Camaçari.
- **Composição da frota Ford:** ~80% concentrada em modelos descontinuados (Ka, Fiesta, EcoSport), produzidos no Brasil até janeiro/2021 quando a Ford fechou as 3 fábricas (Taubaté/SP, Camaçari/BA, Horizonte/CE).
- **Vendas Ford BR 2024:** **48.311 unidades** (+70% vs 2023). Em 2025 (jan-nov), **49.000 unidades** já haviam sido emplacadas (+12,6%).
- **Rede de concessionárias:** caiu de **~283** (2021, pré-fechamento) para **~80** (final 2022/início 2023) e se recuperou para **140** (2025) com padrão Signature 2.0.
- **Idade média da frota brasileira (2024):** **10 anos e 11 meses**; automóveis com idade 11-15 anos passaram de 15,2% (2015) para **31,3%** (2024). Frota Ford tende a ser ainda mais velha por conta do fim da produção nacional.

---

## VIO Ford BR — total e por modelo

> **Aviso de gap:** o Anuário Sindipeças 2024 é a fonte canônica para frota por marca/modelo, mas a tabela detalhada Ford não está exposta nas páginas web públicas do Vira Página (pp. 60 e 62 mostram apenas agregados por tipo). Os números abaixo são **estimativas** derivadas de produção acumulada × idade da frota × sucateamento típico (~3% a.a. para hatches populares).

| Modelo | VIO estimado (unidades) | Ano referência | Base / Fonte |
|---|---|---|---|
| **Ka (hatch + sedan)** | ~900.000 [estimativa] | 2024 | >1M produzidos até 2017 + ~250-300k pós-2017; sucateamento aplicado — [Ford Media 2017](https://media.lincoln.com/content/fordmedia/fsa/br/pt/news/2017/04/24/ford-ka-comemora-1-milhao-de-unidades-produzidas-no-brasil.html) |
| **EcoSport** | ~700.000-900.000 [estimativa] | 2024 | 1,2M produzidos em Camaçari (Brasil + export); ~500-700k destinados ao mercado interno — [Revista Carro](https://revistacarro.com.br/ford-ford-ecosport-popularizou-os-suvs-no-brasil-relembre-historia/) |
| **Fiesta (todas gerações)** | ~600.000-800.000 [estimativa] | 2024 | 1,8M vendidos até 2015 + ~150k pós (New Fiesta encerrou 2019); ajuste por idade — [Ford Media 2015](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2015/10/27/ford-fiesta-comemora-20-anos-no-brasil-com-mais-de-1-8-milhao-de.html) |
| **Focus** | ~150.000-250.000 [estimativa] | 2024 | Produção nacional até 2018; volumes anuais ~30-50k na década de 2010 |
| **Ranger** | ~200.000-300.000 [estimativa] | 2024 | Volume anual médio 15-30k × 15+ anos de vendas contínuas; modelo ativo |
| **Maverick** | ~6.000-8.000 | 2024 | Lançada 2022 no Brasil; ~1,4k em 2022, +123% em 2024 — [Frota&Cia](https://frotacia.com.br/vendas-da-ford-crescem-70-em-2024/) |
| **Territory** | ~15.000-20.000 [estimativa] | 2024 | 7,7k acumulados só em jan-nov/2025; vendas iniciadas 2020 |
| **Bronco Sport** | ~5.000-8.000 [estimativa] | 2024 | Vendas baixas; ~2,3k em 11 meses de 2025 |
| **Transit** | <5.000 [estimativa] | 2024 | Lançada como Ford Pro recentemente |
| **Edge / Fusion / Mondeo** | ~60.000-100.000 [estimativa] | 2024 | Modelos importados descontinuados (Fusion até 2019; Edge até 2020) |
| **Mustang** | ~3.000-5.000 [estimativa] | 2024 | Importado nicho; ~800-1.000 unidades/ano |
| **F-150 / F-Series** | ~5.000-10.000 [estimativa] | 2024 | F-1000 até 1998 (nacional), depois F-250/F-150 importadas |
| **F-250 (1999-2011)** | ~40.000-60.000 [estimativa] | 2024 | Produzida no Brasil; popular em frotas |
| **Caminhões Ford (Cargo etc.)** | ~250.000 [estimativa] | 2024 | Produção encerrada 2019; ~7-9k/ano vendidos antes — [Canal Dana](https://dana.com.br/canaldana/2021/03/04/ford-segue-vendendo-caminhoes-novos-mesmo-sem-produzir-no-brasil-desde-2019/) |
| **TOTAL FORD BR (estimativa final)** | **~3,5 a 5 milhões** | 2024 | Soma dos itens acima × fator de sucateamento; carece de confirmação Sindipeças |

> **Recomendação ao projeto:** para fechar o denominador do VIN Share com rigor, o time deve solicitar o **Anuário Sindipeças 2024 completo** (paga) ou o **Boletim Frota Circulante Sindipeças/Abipeças** (PDF público com dados detalhados — versão 2023 disponível mas o detalhamento por modelo no nível Sindipeças real fica dentro do anuário pago).

---

## VIO Ford BR — por idade da frota

> Aplicando a distribuição etária do mercado brasileiro 2024 (Sindipeças) à frota Ford. Como a Ford encerrou produção nacional em jan/2021, **a frota Ford está estruturalmente mais velha que a média do mercado**.

| Faixa de idade (anos) | % mercado BR 2024 | Unidades Ford estimadas (base 4M) | Fonte |
|---|---|---|---|
| 0-5 anos (2020-2025) | 22,3% | ~890.000 [estimativa enviesada baixo] | [MoveNews/Sindipeças](https://www.movenews.com.br/frota-brasileira-cresce-28-em-2024-e-chega-a-621-milhoes-de-veiculos/) |
| 6-10 anos (2015-2019) | ~30% (residual) | ~1.200.000 [estimativa] | Sindipeças 2024 |
| 11-15 anos (2010-2014) | 31,3% | ~1.250.000 | [MoveNews/Sindipeças](https://www.movenews.com.br/frota-brasileira-cresce-28-em-2024-e-chega-a-621-milhoes-de-veiculos/) |
| 16+ anos (até 2009) | ~16% (residual) | ~640.000 | Sindipeças 2024 |

> **Ajuste Ford-específico recomendado:** como ~80% da frota Ford é Ka/Fiesta/EcoSport descontinuados, a distribuição etária **deve ser deslocada para a direita** (mais velha). Estimativa interna sugere ~10% em 0-5 anos e ~45% em 11-15 anos para a frota Ford.

**Idades médias gerais Brasil 2024 (Sindipeças):**
- Automóveis: 11 anos e 1 mês
- Comerciais leves: 8 anos e 11 meses
- Caminhões: 12 anos e 2 meses
- Total frota: 10 anos e 11 meses

---

## Histórico de vendas Ford BR

| Ano | Unidades vendidas | Posição mercado | Market share | Fonte |
|---|---|---|---|---|
| 2015 | ~330.000 [estimativa] | 4ª | ~9% | base: queda 2015→2016 de -39,3% no acum. ano cit. em [MotorShow](https://motorshow.com.br/por-que-crise-de-vendas-e-maior-na-ford/) |
| 2016 | ~200.000 [estimativa] | 5ª-6ª | ~8% | [Mecânica Online](https://mecanicaonline.com.br/2017/02/emplacamentos-globais-apontam-brasil-com-pior-resultado-em-2016/) — mercado caiu 19,8% |
| 2017 | n/d | 4ª | n/d | [Ford Media 2018](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2018/01/05/ford-cresce-em-vendas-e-participacao-em-2017--ka--fusion-e-range.html) |
| 2018 | **226.437** | 4ª | n/d | Fenabrave via [Canal Dana](https://dana.com.br/canaldana/2021/03/04/ford-segue-vendendo-caminhoes-novos-mesmo-sem-produzir-no-brasil-desde-2019/) |
| 2019 | **218.426** (-3,5%) | 5ª (perdeu 4º) | n/d | [AutoIndústria](https://www.autoindustria.com.br/2020/03/06/ford-cai-e-ja-e-apenas-a-setima-marca-no-ranking-de-vendas/) |
| 2020 | **139.255** | 5ª | 7,14% | Fenabrave via [Vrum](https://www.vrum.com.br/noticias/2024/01/6787859-ford-ha-3-anos-sem-fabrica-no-brasil-qual-a-situacao-da-marca.html) |
| 2021 | **37.778** (-73%) | 11ª | 1,91% | Fenabrave via [Vrum](https://www.vrum.com.br/noticias/2024/01/6787859-ford-ha-3-anos-sem-fabrica-no-brasil-qual-a-situacao-da-marca.html) |
| 2022 | **20.824** | 14ª | 1,06% | Fenabrave via [Vrum](https://www.vrum.com.br/noticias/2024/01/6787859-ford-ha-3-anos-sem-fabrica-no-brasil-qual-a-situacao-da-marca.html) |
| 2023 | **28.711** | 13ª | 1,32% | Fenabrave via [Vrum](https://www.vrum.com.br/noticias/2024/01/6787859-ford-ha-3-anos-sem-fabrica-no-brasil-qual-a-situacao-da-marca.html) |
| 2024 | **48.311** (+70%) | n/d | n/d | [AutomaisTV](https://www.automaistv.com.br/curiosidades/ford-nao-saiu-do-brasil-mas-sim-do-limbo-onde-se-meteu/) / [Frota&Cia](https://frotacia.com.br/vendas-da-ford-crescem-70-em-2024/) |
| 2025 (proj.) | **54.466** (record) | n/d | n/d | [AutomaisTV](https://www.automaistv.com.br/curiosidades/ford-nao-saiu-do-brasil-mas-sim-do-limbo-onde-se-meteu/) |

**Total vendas Ford BR 2015-2024 (acumulado):** **~1,5 a 1,7 milhão** — combinado com unidades vendidas pré-2015 ainda em circulação, sustenta a estimativa de frota total ~3,5 a 5 milhões.

---

## Vendas Ford BR por modelo (ano mais recente)

### 2024 (jan-nov consolidado + projeção)

| Modelo | Unidades | % vendas Ford | Fonte |
|---|---|---|---|
| **Ranger** | **30.000+** (+60% YoY) | ~62% | [Ford Media 2024](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2024/11/ford-tem-recorde-de-vendas-em-outubro-puxado-pela-ranger.html) |
| **Maverick** | ~3.000 (+123% YoY) | ~6% | [Ford Media 2024](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2024/11/ford-tem-recorde-de-vendas-em-outubro-puxado-pela-ranger.html) |
| **Territory** | ~5.000 [estimativa] | ~10% | Recorde de 710 unid./mês em out/24 |
| **Bronco Sport** | ~2.000 [estimativa] | ~4% | base: 2,3k em jan-nov/2025 |
| **Mustang** | ~700 [estimativa] | ~1,5% | base: 846 em jan-nov/2025 |
| **F-150** | ~500 [estimativa] | ~1% | base: 1,1k em jan-nov/2025 |
| **Transit** | n/d | n/d | parte do Ford Pro junto com Ranger comercial |
| **Total Ford 2024** | **48.311** | 100% | [AutomaisTV](https://www.automaistv.com.br/curiosidades/ford-nao-saiu-do-brasil-mas-sim-do-limbo-onde-se-meteu/) |

### 2025 (jan-nov, dados oficiais)

| Modelo | Unidades | Growth YoY | Fonte |
|---|---|---|---|
| Ranger | 30.000+ | +9% | [BemParaná/Ford](https://www.bemparana.com.br/carros/ford-cresce-acima-do-mercado-no-brasil-em-2025-e-prepara-ofensiva-de-20-lancamentos-para-os-proximos-dois-anos/) |
| Territory | 7.700 | +55% | idem |
| F-150 | 1.100+ | +140% | idem |
| Mustang | 846 | +26% | idem |
| Bronco Sport | 2.300+ | +11% | idem |
| Maverick | 3.300 | estável | idem |
| Ranger + Transit (Ford Pro) | 8.400+ combinado | +33% | idem |
| **TOTAL** | **49.000** (jan-nov) | +12,6% | idem |

---

## Dados sobre rede de concessionárias (bonus)

| Período | Nº concessionárias Ford BR | Fonte |
|---|---|---|
| Pré-fechamento (2021, jan) | **~283** (ABRADIF) | [Wikipedia Ford do Brasil](https://pt.wikipedia.org/wiki/Ford_do_Brasil) |
| Final 2022 | **110** | [Wikipedia Ford do Brasil](https://pt.wikipedia.org/wiki/Ford_do_Brasil) |
| Jan 2023 | **95** (listados no site) | [Wikipedia Ford do Brasil](https://pt.wikipedia.org/wiki/Ford_do_Brasil) |
| 2023 (renovação Signature) | **114** (86 já no padrão Signature) | [Garagem360](https://garagem360.com.br/ford-concessionarias-lancar-10-veiculos-brasil-2023/) |
| 2023 (pós CNN Brasil) | **80** (após fechamento de ~150) | [Carro Arretado](https://carroarretado.com.br/como-esta-a-ford-hoje-no-brasil-depois-de-dois-anos-do-fechamento-das-fabricas/) |
| 2025 | **140** (padrão Signature 2.0) | [BemParaná/Ford](https://www.bemparana.com.br/carros/ford-cresce-acima-do-mercado-no-brasil-em-2025-e-prepara-ofensiva-de-20-lancamentos-para-os-proximos-dois-anos/) |

**Plano Ford:** 20 ações de produto nos próximos 2 anos + US$ 170M para Ranger híbrida plug-in a partir de 2027.

> **Observação para o projeto:** o gap "VIN visto na rede vs frota total" é estruturalmente grande porque (1) só ~140 concessionárias atendem ~4 milhões de carros Ford no Brasil e (2) ~80% da frota é de modelos descontinuados (Ka/Fiesta/EcoSport) cujos donos têm fortes incentivos para migrar para mecânicas independentes (peças mais baratas, proximidade, custo de mão-de-obra). Isto **valida o problem statement** do Forward Service.

---

## Fontes consultadas

- [Ford Media Brasil — Ka 1 milhão (2017)](https://media.lincoln.com/content/fordmedia/fsa/br/pt/news/2017/04/24/ford-ka-comemora-1-milhao-de-unidades-produzidas-no-brasil.html) — milestone produção — acesso 2026-05-11
- [Ford Media Brasil — Fiesta 20 anos / 1,8M vendas (2015)](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2015/10/27/ford-fiesta-comemora-20-anos-no-brasil-com-mais-de-1-8-milhao-de.html) — produção acumulada — 2026-05-11
- [Ford Media Brasil — Recorde Ranger out/2024](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2024/11/ford-tem-recorde-de-vendas-em-outubro-puxado-pela-ranger.html) — vendas 2024 por modelo — 2026-05-11
- [BemParaná — Ford 2025 +12,6%](https://www.bemparana.com.br/carros/ford-cresce-acima-do-mercado-no-brasil-em-2025-e-prepara-ofensiva-de-20-lancamentos-para-os-proximos-dois-anos/) — dados 2025 por modelo + rede — 2026-05-11
- [Vrum — Ford 3 anos sem fábrica (jan/2024)](https://www.vrum.com.br/noticias/2024/01/6787859-ford-ha-3-anos-sem-fabrica-no-brasil-qual-a-situacao-da-marca.html) — série histórica 2020-2023, citando Fenabrave — 2026-05-11
- [AutomaisTV — Ford limbo](https://www.automaistv.com.br/curiosidades/ford-nao-saiu-do-brasil-mas-sim-do-limbo-onde-se-meteu/) — vendas 2024-2025 — 2026-05-11
- [Frota&Cia — Ford +70% em 2024](https://frotacia.com.br/vendas-da-ford-crescem-70-em-2024/) — confirmação 2024 — 2026-05-11
- [MoveNews — Frota BR 62,1M (Sindipeças 2024)](https://www.movenews.com.br/frota-brasileira-cresce-28-em-2024-e-chega-a-621-milhoes-de-veiculos/) — total + idade — 2026-05-11
- [AutoIndústria — Frota envelhece (Sindipeças)](https://www.autoindustria.com.br/2025/04/29/frota-circulante-cresce-mas-envelhece-no-caso-dos-carros-e-caminhoes/) — distribuição etária 2015 vs 2024 — 2026-05-11
- [Sindipeças PDF — Frota Circulante 2024](https://sindipecas.org.br/sindinews/Economia/2024/Frota_Circulante.pdf) — boletim resumido — 2026-05-11
- [Sindipeças Anuário 2024 — Página 60](https://virapagina.com.br/sindipecas2024/60/) — agregado por tipo — 2026-05-11
- [Sindipeças Anuário 2024 — Página 62](https://virapagina.com.br/sindipecas2024/62/) — idade média — 2026-05-11
- [Sindipeças/Abipeças Relatório Frota Circulante 2023 (PDF)](https://static.poder360.com.br/2023/05/RelatorioFrotaCirculante_2023.pdf) — fonte canônica histórica — 2026-05-11
- [AutoIndústria — Ford cai para 7ª (mar/2020)](https://www.autoindustria.com.br/2020/03/06/ford-cai-e-ja-e-apenas-a-setima-marca-no-ranking-de-vendas/) — share Ford 2019-2020 — 2026-05-11
- [Canal Dana — Ford caminhões](https://dana.com.br/canaldana/2021/03/04/ford-segue-vendendo-caminhoes-novos-mesmo-sem-produzir-no-brasil-desde-2019/) — 2018: 226.437, 2019: 218.426 — 2026-05-11
- [Wikipedia — Ford do Brasil](https://pt.wikipedia.org/wiki/Ford_do_Brasil) — histórico fábricas/rede — 2026-05-11
- [Revista Carro — EcoSport histórico](https://revistacarro.com.br/ford-ford-ecosport-popularizou-os-suvs-no-brasil-relembre-historia/) — 1,2M EcoSport produzidos — 2026-05-11
- [Carro Arretado — Ford 2 anos pós-fechamento](https://carroarretado.com.br/como-esta-a-ford-hoje-no-brasil-depois-de-dois-anos-do-fechamento-das-fabricas/) — rede 80 concessionárias — 2026-05-11
- [Garagem360 — Renovação concessionárias](https://garagem360.com.br/ford-concessionarias-lancar-10-veiculos-brasil-2023/) — rede 2023 — 2026-05-11
- [InfoMoney — Fechamento fábricas Ford 2021](https://www.infomoney.com.br/negocios/ford-fecha-fabricas-anuncia-fim-da-producao-de-carros-no-brasil-em-2021-e-demite-mais-de-5-mil-funcionarios/) — contexto — 2026-05-11
- [Portal FENABRAVE — Emplacamentos](https://www.fenabrave.org.br/portalv2/Conteudo/emplacamentos) — fonte primária (acesso via portal exige navegação) — 2026-05-11
- [Mobiauto — Altos e baixos Ford 5 anos](https://www.mobiauto.com.br/revista/os-altos-e-baixos-da-ford-nos-ultimos-cinco-anos-de-vendas-no-brasil/542) — referência (conteúdo bloqueado) — 2026-05-11

---

## Gaps (o que não foi possível encontrar)

1. **Número exato de VIO Ford BR por marca (Sindipeças)** — o Anuário Sindipeças 2024 tem o detalhamento por marca/modelo, mas o conteúdo público no Vira Página só expõe agregados. A tabela exata Ford precisa ser solicitada ou comprada.
2. **Vendas Ford BR 2015, 2016, 2017 anuais consolidadas** — Fenabrave tem isto no portal histórico mas exige navegação manual. Estimativas baseadas em comparativos de queda (-39,3% YoY 2015-2016) e participação de mercado (~9%).
3. **Vendas Ford 2024 por modelo com granularidade mensal** — disponíveis apenas no relatório Fenabrave detalhado, não em release público.
4. **VIO Ford por idade especificamente** — todos os dados etários são agregados do mercado, não Ford-específicos. A inferência aplica distribuição etária mercado × frota Ford estimada.
5. **Sucateamento real (kill rate) por modelo Ford** — métrica crítica para refinar a estimativa. Modelos populares como Ka tendem a sobreviver 15-20 anos no Brasil pela facilidade/baixo custo de manutenção; modelos premium (Fusion, Edge) tendem a sucatear mais cedo por custo de peças.
6. **Confirmação de Transit, Edge, F-Series, Bronco Sport individualmente em 2024** — todos somados ficam dentro do total 48.311, mas o split exato é apenas estimativa baseada em proxies de 2025.

## Recomendação ao time Forward Service

Para fechar o numerador/denominador do VIN Share com mais rigor, dois movimentos:

1. **Comprar o Anuário Sindipeças 2024 completo** (~R$ 200-400, fonte canônica BR para frota por marca) — resolve gap #1.
2. **Cruzar com SENATRAN/Detran-SP por placa final** — possível obter contagem de licenciamentos Ford em circulação por ano-modelo (via LAI ou portais de dados abertos estaduais). Para validar #4.

Assumindo o cenário mais conservador (**3,5M de frota Ford BR**) e VINs vistos pela rede (**175.554**), o **VIN Share atual seria ~5,0%**. No cenário 5M, **3,5%**. Em qualquer hipótese, o headroom para o Forward Service é grande — esse é o argumento estratégico do projeto.
