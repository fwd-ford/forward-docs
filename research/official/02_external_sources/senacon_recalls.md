# Campanhas de recall Ford Brasil

> Pesquisa para Ford Forward (Recall Gateway) — Challenge FIAP-Ford 2026
> Acesso: 2026-05-11
> Janela investigada: 2015 – 2026-05 (priorizando ultimos 5 anos)

---

## Resumo executivo

- **~12 campanhas Ford no Brasil identificadas** com base em fontes abertas (Ford BR oficial, Procon-SP, imprensa especializada, releases Senacon), das quais ~9 sao **abertas** ou recentes (2024-2026).
- **2025 foi um ano atipico:** segundo reportagem Garagem360, a Ford somou **104 recalls no ano de 2025** (todos os mercados globalmente) — o **quintuplo do 2o colocado (Stellantis, 21)**. No Brasil, a Checkprice mapeou **4 campanhas Ford** em 2025 entre 20 campanhas totais do setor automotivo brasileiro.
- **Modelos mais afetados (Brasil, ultimos 5 anos):** Bronco Sport, Maverick, Mustang, Ranger (mais recentes); Territory, EcoSport, Edge, Fusion, Troller T4 (historico).
- **Universo total da Senacon (1S/2024):** 58 campanhas automotivas convocaram **1.125.627 unidades** so no 1o semestre de 2024.
- **Estoque de recalls pendentes (Senatran/Senacon, set/2024):** **~3,4 milhoes** de veiculos com recall nao atendido no Brasil.
- **Adesao media setorial Brasil:** ~40% nos ultimos anos. Dos 701 recalls Brasil 2019-2024, **189 (27%) ficaram abaixo de 10%** de atendimento e **103 (15%) entre 10-40%**.
- **Numero exato de veiculos Ford afetados no Brasil nao foi divulgado** publicamente para a maioria das campanhas — fonte primaria (portal Senacon `consumidor.gov.br/pages/recall`) **exige autenticacao** para consulta por fabricante, o que e um gap conhecido desta pesquisa.

---

## Top campanhas mais recentes (com detalhe)

| # | Modelo | Anos modelo | Data anuncio | Defeito (resumo) | Universo BR | Status | Codigo |
|---|---|---|---|---|---|---|---|
| 1 | Bronco Sport / Maverick Black / Maverick Tremor | 2025 | 2026-03-26 | Valvula EGR defeituosa - perda de potencia ate 20 km/h, vibracao, falha de partida | N/D | Aberto — agendamento Q4 2026 | N/D |
| 2 | Bronco Sport | 2025 | 2025-12-22 | Painel digital de instrumentos com falha de calibracao (tela pode nao ligar) | N/D | Aberto | N/D |
| 3 | E-Transit | 2022, 2024, 2025, 2026 | 2025-11-05 | Modulo motor/transmissao mal calibrado causa superaquecimento da bateria 12V, gases na cabine | N/D | Aberto — agendamento Q1 2026 | N/D |
| 4 | Mustang | 2024, 2025 | 2025-09-30 | Infiltracao de agua no BCM (Body Control Module) - lampadas externas falham, descarga de bateria | N/D | Aberto — servico desde 2025-10-06 | N/D |
| 5 | Ranger / Ranger Raptor | 2024, 2025, 2026 | 2025-09-08 (notif. global) | Airbag de cortina lateral rasga ao acionar | 100.900 global (BR n/d) | Aberto | 25C41 (Ford) / 25V541 (NHTSA) |
| 6 | Ranger / Ranger Raptor | 2024, 2025 | 2025-05-20 | Sistema antiesmagamento dos vidros dianteiros falha | N/D | Aberto | N/D |
| 7 | EcoSport, Edge, Fusion, Mustang, Ranger, Bronco Sport | EcoSport 20-21; Edge 19-20; Fusion 19; Mustang 20-23; Ranger 20-21; Bronco Sport 21-24 | 2024-2025 | Camera de re mostra tela preta / congelada / fica ligada apos sair de re | N/D | Aberto — update SW ~40 min | N/D |
| 8 | Mustang | 2021, 2023 | 2024-07-30 | Modulo da caixa de direcao eletrica mal calibrado — resistencia ou movimento inesperado | **4** unidades (chassi divulgado) | Aberto — servico desde 2024-11-29 | N/D |
| 9 | Territory | 2021 | 2021-02-25 | Conversor catalitico oscila — emissoes acima do limite legal | ~4.160 chassis (MTP00009-MTP04168) | Fechado (provavel) | N/D |
| 10 | Troller T4 | 2015, 2016 | 2017-05-30 (anuncio) / 2017-07-20 (servico) | Atrito entre linha de freio dianteira direita e fixador da mangueira do intercooler — vazamento de fluido | N/D (chassis FH400017-FH402280 e GH400001-GH401387) | Fechado | N/D |
| 11 | EcoSport (motor 1.5L) | 2018, 2019 | ~2019-2021 | Campanha de seguranca (motor 1.5L) | N/D | Fechado (provavel) | N/D |
| 12 | Fusion, Edge | Fusion 2006-2012; Edge 2009-2010 | ~2017-2022 | Recall mundial Takata — inflador do airbag do motorista pode romper e lancar fragmentos | N/D BR | Aberto (parcial — reposicao continua globalmente) | N/D |

> Observacoes:
> - **Codigos Senacon nao disponiveis em fontes publicas indexadas** para a maioria das campanhas — o portal `consumidor.gov.br/pages/recall` redireciona para tela de login. Recomenda-se consulta direta ao Senacon via Lei de Acesso a Informacao (LAI) para obter os numeros de campanha oficiais e universos por chassi.
> - **Universos de veiculos** na maioria nao foram divulgados pela Ford Brasil — fonte indireta (Checkprice, 2025) confirma "nao totalmente especificado" para campanhas Ford/Fiat.
> - **Recall Mustang BCM 2024-2025** ja esta em servico (out/2025), uma janela ativa para o ForwardService usar como gancho de reconexao.

---

## Lista completa

Dataset estruturado: [`../data/ford_recalls.csv`](../data/ford_recalls.csv)

12 linhas, colunas conforme spec: `campaign_code, announce_date, model, years_affected, defect_brief, universe_count, adhesion_rate, status, source_url`.

---

## Contexto setorial (Brasil)

### Volume Senacon

| Metrica | Valor | Fonte |
|---|---|---|
| Total recalls Brasil 2019-2024 (5 anos) | **701 campanhas** | Senacon, via Agencia Gov / Senatran |
| Veiculos convocados 1S/2024 | **1.125.627** unidades em 58 campanhas | Senacon |
| Estoque atual de recalls pendentes Brasil | **~3,4 milhoes** veiculos (set/2024) | Senatran |
| Recalls Brasil 2025 (amostra Checkprice) | **20 campanhas** mapeadas em fontes abertas | Checkprice / press |

### Adesao media

| Faixa | % das 701 campanhas 2019-2024 |
|---|---|
| < 10% | **27%** (189 campanhas) |
| 10-40% | **15%** (103 campanhas) |
| 40-100% | **58%** (estimativa por exclusao) |
| **Media estimada Brasil** | **~40%** dos proprietarios convocados comparecem (Senacon) |

### Ranking de fabricantes — 2025

| Posicao | Fabricante | Recalls 2025 (global) | Fonte |
|---|---|---|---|
| 1 | **Ford** | **104** | Garagem360, citando NHTSA |
| 2 | Stellantis | 21 | Garagem360 |
| - | Top 6 (Stellantis+VW+GM+Mercedes+Honda+Hyundai) combinados | 77 | Garagem360 |

Brasil-especifico 2025 (Checkprice):
- Fiat: 9
- **Ford: 4**
- Honda: 2
- BMW: 2
- Chevrolet: 1
- Ram: 2

### Top defeitos mais comuns no Brasil 2025 (UsadosBR)

1. **Airbags Takata** e similares (>300 mil veiculos)
2. Sistema de freio (vazamento / sensor)
3. Cinto de seguranca / ISOFIX
4. Bomba de combustivel
5. Software do ECU
6. Suspensao
7. Direcao eletrica
8. Farois e eletrica
9. Cambio automatico
10. Capo / porta-malas

> Os defeitos #5 (ECU/SW), #7 (direcao eletrica) e #8 (farois/BCM) aparecem todos na lista Ford 2024-2025 — sao **defeitos de cresta atual da industria**, nao Ford-especificos.

### Endurecimento regulatorio (relevante para Recall Gateway)

- A partir de 2024-2025, **recall nao atendido em ate 1 ano consta no CRLV** e **bloqueia licenciamento / transferencia** (CTB).
- Isto cria pressao de mercado **a favor do gancho "Recall Gateway"** do Ford Forward — proprietario tem incentivo regulatorio para responder a convocacao.

---

## Fontes

| Fonte | URL | Data acesso |
|---|---|---|
| consumidor.gov.br/pages/recall (Senacon — portal principal) | https://www.consumidor.gov.br/pages/recall/ | 2026-05-11 (exigiu login — gap) |
| gov.br/mj/.../recall (MJ/Senacon) | https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/recall | 2026-05-11 (404 na URL especifica) |
| Ford Brasil — Recall Mustang 2024-2025 | https://www.ford.com.br/servico-ao-cliente/recall/2025/ford-mustang-modelo-2024-2025/ | 2026-05-11 |
| Ford Brasil — Recall Territory 2021 | https://www.ford.com.br/servico-ao-cliente/recall/2021/ford-territory-modelo-2021/ | 2026-05-11 |
| Ford Brasil — Airbag Takata | https://www.ford.com.br/recall-airbag-takata/ | 2026-05-11 |
| Procon-SP — Recall Ford (Troller T4 2015-2016) | https://www.procon.sp.gov.br/recall-ford-2/ | 2026-05-11 |
| Procon-SP — Territory 2021 | https://www.procon.sp.gov.br/ford-comunica-recall-de-modelos-territory-2021/ | 2026-05-11 (via search) |
| Grupo Sentinela — recall Mustang 24-25 | https://www.gruposentinela.com.br/recall-ford-mustang-modelos-2024-e-2025/ | 2026-05-11 |
| Grupo Sentinela — recall E-Transit 22/24/25/26 | https://www.gruposentinela.com.br/recall-ford-e-transit-modelos-2022-2024-2025-e-2026/ | 2026-05-11 |
| MixVale — Ranger antiesmagamento 24-25 | https://www.mixvale.com.br/2025/05/20/ford-convoca-recall-de-ranger-2024-e-2025-por-falha-no-sistema-antiesmagamento/amp/ | 2026-05-11 |
| MixVale — Bronco Sport painel | https://www.mixvale.com.br/2025/12/22/ford-convoca-recall-do-bronco-sport-2025-por-falha-no-painel-digital-de-instrumentos/ | 2026-05-11 |
| GaragemSE — Bronco Sport / Maverick EGR (2026-03) | https://garagemse.com.br/ford-recall-bronco-sport-maverick-2025-valvula-egr/ | 2026-05-11 |
| Garagem360 — Ford lider de recalls 2025 (104) | https://garagem360.com.br/deu-ruim-ford-dispara-no-ranking-de-recalls-e-ja-soma-104-convocacoes-em-2025/ | 2026-05-11 |
| Checkprice Blog — Recalls Brasil 2025 (analise tecnica) | https://www.checkpriceblog.com.br/post/recalls-de-ve%C3%ADculos-no-brasil-em-2025-uma-an%C3%A1lise-t%C3%A9cnica | 2026-05-11 |
| Autopapo — Ford lider recall 2025 | https://autopapo.com.br/curta/ford-lider-recall/ | 2026-05-11 |
| Autopapo — Territory emissoes | https://autopapo.com.br/noticia/recall-ford-territory-emissoes/ | 2026-05-11 |
| Motor Show — Ford EcoSport/Edge/Fusion/Mustang/Ranger/Bronco | https://motorshow.com.br/recall-ford-chama-unidades-de-ecosport-edge-fusion-mustang-ranger-e-bronco | 2026-05-11 |
| Conexao Automotiva — Mustang 2021-2023 modulo direcao | https://www.conexaoautomotivabr.com/2026/02/ford-convoca-recall-que-envolve-o.html | 2026-05-11 |
| Agencia Gov / Senatran — Recall explicado (out/2024) | https://agenciagov.ebc.com.br/noticias/202410/voce-sabe-o-que-e-e-como-funciona-o-recall-a-senatran-tira-suas-duvidas | 2026-05-11 |
| Senacon — Importancia do recall | https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-alerta-proprietarios-de-veiculos-para-importancia-de-fazer-recall | 2026-05-11 |
| UsadosBR — Top 10 recalls Brasil 2025 | https://blog.usadosbr.com/top-10-recalls-mais-comuns-no-brasil-em-2025-e-como-evita-los/ | 2026-05-11 |
| Tabela FIPE Brasil — Recalls Ford | https://www.tabelafipebrasil.com/recall/carros/ford | 2026-05-11 (HTTP 403) |
| CNN Brasil — Ford 694 mil veiculos risco incendio | https://www.cnnbrasil.com.br/economia/negocios/ford-recolhe-mais-de-694-mil-veiculos-com-risco-de-incendio/ | 2026-05-11 |
| Banda B — Ford Bronco Sport/Maverick motor | https://www.bandab.com.br/nacional/recall-ford-modelos-carros-brasil-defeito-motor/ | 2026-05-11 |

---

## Gaps

1. **Codigos oficiais Senacon (numero de campanha)** nao foram obtidos para nenhuma das 12 campanhas — exigem consulta autenticada ao portal `consumidor.gov.br/pages/recall` ou pedido LAI ao Ministerio da Justica. **Acao recomendada:** abrir LAI requisitando relacao Ford completa 2015-2026.
2. **Universos por campanha (Brasil)** sao mantidos confidenciais pela Ford BR — so o numero global aparece em alguns casos (ex: Ranger 100.900 globalmente). Sem dados BR-especificos nao da para calcular adesao por campanha.
3. **Taxas de adesao por campanha Ford** nao foram localizadas publicamente. So existe a media setorial (~40%) e a distribuicao Senacon de 701 campanhas. **Acao:** combinar com nosso dataset Itau-Ford (500k registros) para inferir adesao por modelo via cruzamento data-servico × data-anuncio-recall.
4. **Campanhas pre-2017** (Fusion/EcoSport/Ka 2010-2016) so aparecem fragmentadas em imprensa. Sem cobertura indexada confiavel.
5. **Distribuicao geografica** das campanhas Ford no Brasil (concentracao por estado/concessionaria) nao foi mapeada — relevante para Recall Gateway segmentar acionamento por regiao.
6. **Custo medio por recall (para Ford BR)** nao localizado em fonte publica — usar referencias do mercado USA (US$30-60/veiculo) so para sizing inicial.

### Como esta pesquisa alimenta o Recall Gateway

- **Tag service-event** como "visita de recall": precisamos do cruzamento campaign × VIN (ou pelo menos campaign × modelo × ano × faixa de chassi). **Faixas de chassi** estao publicas para Troller T4, Territory 2021, Mustang 2021-2023 e Bronco Sport/Maverick 2025 — suficiente para piloto.
- **Calcular adesao por campanha:** com 500k registros do dataset Itau-Ford e a lista de 12 campanhas acima, e viavel produzir uma estimativa de adesao Ford BR — comparar com a media setorial de 40%.
- **Identificar VINs com recall pendente:** sem o codigo Senacon nem o universo oficial, o melhor proxy hoje e o **filtro modelo+ano+data-de-fabricacao** contra a lista acima. Documentar no DOC 06 como limitacao explicita.
