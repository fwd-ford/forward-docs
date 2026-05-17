# Cronograma oficial de manutencao - modelos Ford BR

> Pesquisa academica - FIAP-Ford Challenge 2026 (Projeto Ford Forward).
> Objetivo: alimentar a flag "veiculo em atraso de revisao" como regra de negocio (preditor de churn).
> Data da pesquisa: 2026-05-11.

## Resumo executivo

- **Modelos cobertos**: 8 de 8 (KA, FIESTA, ECOSPORT, FOCUS, RANGER, MAVERICK, TERRITORY, TRANSIT).
- **Intervalo padrao Ford BR (linha 2015+)**: **10.000 km ou 12 meses, o que ocorrer primeiro** (excecoes: Ranger 3.0 V6 2024+ e Maverick 2023+ FHEV = 16.000 km / 12 meses; Transit = 20.000 km / 12 meses).
- **1a revisao especial (linha 2015-2022)**: aos 6 meses ou 5.000 km (mao de obra cortesia). A partir de 2023 a Ford migrou para "Revisao Inteligente" - sem revisao obrigatoria aos 6 meses; o sistema de oil-life monitor avisa quando trocar.
- **Tolerancia oficial Ford BR**: +/- 1.000 km ou +/- 30 dias (sem perder garantia).
- **Revisoes criticas (geral)**: 20.000 km (filtro de combustivel) e 60.000 km (correia dentada, fluidos, embreagem em alguns modelos).
- **Range de precos por revisao** (val. 2025-2026, capitais BR):
  - Hatchs/sedas pequenos (Ka, Fiesta): R$ 400-1.200 por revisao.
  - SUVs medios (EcoSport, Territory, Focus): R$ 600-2.300 por revisao.
  - Picapes/utilitarios (Ranger, Maverick, Transit): R$ 900-2.000 por revisao.
- **Plano pre-pago Ford Protect** (2025): adesao passou de 10% para 15% das vendas - sinal de que a Ford ja entende que retencao na pos-venda e diferencial.

### Tabela mestre - intervalo padrao por modelo

| Modelo | Intervalo padrao | Cobertura tabela publica | Plano pre-pago Ford |
|---|---|---|---|
| KA (2014-2021) | 10.000 km / 12 meses (1a aos 6m/5k) | ate 60-80 mil km | Ford Protect |
| FIESTA (2014-2019) | 10.000 km / 12 meses (1a aos 6m/5k) | ate 30 mil km (garantia) + planos ate 50 mil | Ford Protect Advanced/Premium |
| ECOSPORT (2013-2022) | 10.000 km / 12 meses (1a aos 6m/5k) | ate 60-80 mil km | Ford Protect (3 ou 4 rev.) |
| FOCUS (2014-2019) | 10.000 km / 12 meses (1a aos 6m/5k) | ate 50-60 mil km | Ford Protect |
| RANGER 2.2/3.2 (2014-2022) | 10.000 km / 12 meses | ate 60 mil km | Revisao Preco Fixo |
| RANGER 3.0 V6 (2023+) | 16.000 km / 12 meses | 5 revisoes (Protect Plus) | Ford Protect Plus |
| MAVERICK ICE (2022-2024) | 10.000 km / 12 meses [Justos]; 16.000 km/12m [Ford oficial 2023+] | ate 60 mil km | Ford Protect |
| MAVERICK FHEV (2025+) | 16.000 km / 12 meses | Revisao Inteligente | Ford Protect |
| TERRITORY (2020-2026) | 10.000 km / 12 meses | ate 60 mil km | Revisao Preco Fixo + Protect |
| TRANSIT (2022+) | 20.000 km / 12 meses | ate 60 mil km (3 rev. cortesia 350 primeiras unidades) | Ford Protect Manutencao Premium |

> **Discrepancia notavel**: Maverick - Justos publica intervalo de 10k km, enquanto a pagina oficial Ford (Revisao Inteligente) diz 16k km. Hipotese: 10k km e o limite seguro do oleo conservador; 16k km e o limite do sistema Intelligent Oil Life. **Para a flag de churn, usar 12 meses ou 10k km** como gatilho (conservador, evita falsos positivos).

---

## Por modelo

### RANGER (2014-2026) - PRIORIDADE MAXIMA

#### Ranger 2.2 / 3.2 Turbodiesel (geracao 2013-2022)

Intervalo: **10.000 km ou 12 meses**, o que ocorrer primeiro.

Tabela com precos reais publicados (Garagem360, base 2020-2022):

| Revisao # | KM | Meses | Itens principais | Preco XLS 2.2 4x4 (BRL) | Preco Limited 3.2 4x4 (BRL) |
|---|---|---|---|---|---|
| 1a | 10.000 | 12 | Oleo, filtros, verificacoes basicas, lavagem | R$ 1.129 | R$ 1.199 |
| 2a | 20.000 | 24 | Oleo, filtros de ar e combustivel | R$ 1.129 | R$ 1.199 |
| 3a | 30.000 | 36 | Oleo, limpeza de injetores, embreagem | R$ 1.429 | R$ 1.499 |
| 4a | 40.000 | 48 | Oleo, correias, transmissao | R$ 1.219 | R$ 1.249 |
| 5a | 50.000 | 60 | Oleo, arrefecimento, direcao, suspensao | R$ 1.219 | R$ 1.249 |
| 6a | 60.000 | 72 | Revisao ampla, correia dentada, fluidos | R$ 1.649 | R$ 1.679 |
| **Total 60k km** |  |  |  | **R$ 7.384** | **R$ 8.074** |

**Cesta de pecas Ranger (referencia 2022)**: ~R$ 16.000 (XLS 2.2 ou Limited 3.2).

#### Ranger 3.0 V6 Turbodiesel (geracao 2023+ - "Nova Ranger")

Intervalo: **16.000 km ou 12 meses** (Ford Protect Plus - 5 revisoes).

Tabela detalhada por revisao nao publicada oficialmente em fonte aberta indexavel (Ford.com.br retorna 403 para scrapers). Estimativa de imprensa indica que cada revisao custa entre R$ 1.500 e R$ 2.300, com a de 60-80k km sendo a mais cara (~R$ 2.500+) por incluir trocas maiores.

**Fontes**:
- [Garagem360 - custos manutencao Ranger](https://garagem360.com.br/veja-custos-de-manutencao-revisao-e-seguro-da-ford-ranger/) - [indicativo]
- [Ford Brasil - Revisao Preco Fixo Ranger](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/ranger/) - [oficial, conteudo nao scraped]
- [Ford Brasil - Revisao Ford Ranger 2023+](https://www.ford.com.br/servico-ao-cliente/revisao-ford/ranger/) - [oficial]
- [Mobiauto - custos Ranger](https://www.mobiauto.com.br/revista/ford-ranger-custos-de-revisao-seguro-e-pecas-e-manutencao/1534) - [indicativo]

---

### MAVERICK (2022-2026)

#### Maverick ICE (2.0 EcoBoost e 2.5 Hybrid 2022-2024)

| Revisao # | KM | Meses | Itens principais | Preco indicativo (BRL) |
|---|---|---|---|---|
| 1a | 10.000 | 12 | Oleo, filtros, verificacoes basicas | R$ 1.208 |
| 2a | 20.000 | 24 | Oleo, filtros de ar e combustivel | R$ 1.208 |
| 3a | 30.000 | 36 | Oleo, limpeza de injetores | R$ 1.383 |
| 4a | 40.000 | 48 | Oleo, correias, transmissao | R$ 1.484 |
| 5a | 50.000 | 60 | Oleo, arrefecimento, direcao, suspensao | R$ 1.258 |
| 6a | 60.000 | 72 | Revisao ampla, correia, fluidos | R$ 1.893 |

> **Atencao - intervalo**: Justos publica 10k km / 12m. Ford oficial publica "Revisao Inteligente" baseada em oil-life monitor, com intervalo maximo de 16k km / 12m. **Para regra de negocio (flag churn), usar 10k km / 12m como gatilho conservador.**

#### Maverick FHEV / Hybrid AWD (2025+)

- Intervalo: **16.000 km ou 12 meses** (Revisao Inteligente).
- Garantia bateria de alta-voltagem: 8 anos.
- Garantia geral: 3 anos.
- Preco lancamento: R$ 239.900.
- Tabela detalhada por revisao nao publicada oficialmente em fonte aberta.

**Fontes**:
- [Ford Brasil - Maverick Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/maverick/) - [oficial]
- [Ford Brasil - Maverick FHEV](https://www.ford.com.br/servico-ao-cliente/revisao-ford/maverick-fhev/) - [oficial]
- [Justos - quanto custa manter Maverick](https://www.justos.com.br/blog/quanto-custa-manter-um-ford-maverick) - [indicativo, precos por revisao]
- [Ford media - Nova Maverick Hybrid AWD](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2025/11/nova-ford-maverick-hybrid-chega-mais-moderna--completa-e-com-tra.html) - [oficial]
- [Mobiauto - Maverick custos](https://www.mobiauto.com.br/revista/ford-maverick-custos-de-revisao-seguro-e-pecas-de-manutencao/1925) - [indicativo]

---

### TERRITORY (2020-2026)

Intervalo: **10.000 km ou 12 meses**.

| Revisao # | KM | Meses | Itens principais | Preco indicativo (BRL) |
|---|---|---|---|---|
| 1a | 10.000 | 12 | Oleo, filtros, verificacoes basicas | R$ 900 - R$ 1.200 |
| 2a | 20.000 | 24 | Oleo, filtros de ar e combustivel (critica) | R$ 1.000 - R$ 1.400 |
| 3a | 30.000 | 36 | Oleo, limpeza injetores | R$ 1.100 - R$ 1.700 |
| 4a | 40.000 | 48 | Oleo, correias, transmissao | R$ 1.200 - R$ 1.900 |
| 5a | 50.000 | 60 | Oleo, arrefecimento, direcao, suspensao | R$ 1.300 - R$ 2.000 |
| 6a | 60.000 | 72 | Revisao ampla, correia dentada, fluidos (critica) | R$ 1.500 - R$ 2.300 |

**Total ate 60k km**: ~R$ 15.000 (referencia 2025).

**Custo mensal total Territory 2025** (combustivel + IPVA + seguro + manutencao): R$ 1.830-2.530/mes.

**Fontes**:
- [Mercado Veiculos - Territory 2024](https://mercadoveiculos.com/info/revisao-ford-territory-2024) - [indicativo]
- [Ford Brasil - Territory Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/territory/) - [oficial]
- [Webmotors - revisoes Territory](https://www.webmotors.com.br/wm1/dinheiro-e-economia/quanto-custam-as-revisoes-do-ford-territory) - [indicativo, nao acessivel via scraper]
- [O Antagonista - custo mensal Territory 2025](https://oantagonista.com.br/ladooa/carros/quanto-custa-por-mes-ter-um-ford-territory-em-2025/) - [indicativo]

---

### TRANSIT (2022+)

Intervalo: **20.000 km ou 12 meses** (mais longo que outros modelos - perfil utilitario/comercial).

| Revisao # | KM | Meses | Itens principais | Status |
|---|---|---|---|---|
| 1a | 20.000 | 12 | Oleo motor, filtros, avaliacao sistemas | Cortesia para 350 primeiras unidades |
| 2a | 40.000 | 24 | Oleo, filtros, verificacao 60 itens | Cortesia (350 primeiras) |
| 3a | 60.000 | 36 | Oleo, filtros, fluidos | Cortesia (350 primeiras) |
| 4a+ | 80.000+ | 48+ | Programa Revisao Preco Fixo Ford | Preco fixo via concessionaria |

- **Lancamento (nov/2021)**: Ford Protect Manutencao Premium incluso para as 350 primeiras unidades = 3 revisoes + pecas de desgaste por 36 meses / 60.000 km, gratis.
- **Garantia padrao Transit 2026**: 2 anos.
- **Preco Transit 2026**: a partir de R$ 282.900 (Furgao R$ 297.900, Minibus R$ 354.900).
- **Custo total operacao 5 anos / 200.000 km**: ate R$ 90 mil menor que principal concorrente (claim Ford).

**Fontes**:
- [Ford Brasil - Transit Bus Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-ford/transit-bus/) - [oficial]
- [Ford Brasil - Transit Furgao](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/transit-furgao/) - [oficial]
- [Ford media - lancamento Transit pacote cortesia](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2021/11/03/ford-transit-tem-pacote-gratuito-de-revisao-e-pecas-como-oferta-.html) - [oficial]
- [Car.blog.br - Transit 2026](https://www.car.blog.br/2025/02/novo-ford-transit-2026-preco-parte-de-r.html) - [indicativo, precos lancamento]

---

### KA (2014-2021)

Intervalo: **10.000 km ou 12 meses** (a partir da linha 2015; antes era 7.500 km / 6 meses).

| Revisao # | KM | Meses | Itens principais | Preco indicativo (BRL) |
|---|---|---|---|---|
| 1a | 5.000 | 6 | Inspecao basica (mao de obra cortesia) | gratis / inclusa |
| 2a | 10.000 | 12 | Oleo Motorcraft 5W20, filtros, verificacoes | R$ 400 - R$ 500 |
| 3a | 20.000 | 24 | Oleo, filtros, velas, verificacao completa | R$ 550 - R$ 650 |
| 4a | 30.000 | 36 | Oleo, filtros, fluido freio, injecao | R$ 650 - R$ 750 |
| 5a | 40.000 | 48 | Oleo, filtros, correias, transmissao | R$ 800 - R$ 900 |
| 6a | 50.000 | 60 | Oleo, arrefecimento, direcao, suspensao | R$ 550 - R$ 650 |
| 7a | 60.000 | 72 | Revisao ampla, correia dentada (CRITICA) | R$ 1.000 - R$ 1.200 |
| 8a | 70.000 | 84 | Oleo, filtros | (kits disponiveis) |
| 9a | 80.000 | 96 | Oleo, filtros, velas | (kits disponiveis) |
| 10a | 100.000 | 120 | Oleo, filtros, correias, geral | (kits disponiveis) |

**Engine variants**: 1.0 12V Ti-VCT (3 cilindros), 1.5 16V Ti-VCT, 1.5 12V Dragon (3 cilindros, a partir 2018).

**Fontes**:
- [Mercado Veiculos - Ka 2020](https://mercadoveiculos.com/info/revisao-ford-ka-2020) - [indicativo, mai/2026]
- [Sua Oficina Online - tabela revisao Ka](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-ka/) - [indicativo]
- [Italia Ricambi - kits revisao Ka 2014-2021](https://www.italiaricambi.com.br/kit-revisao-ford-60000-km-72-meses-ford-ka-10-12v-2014-em-diante) - [indicativo - confirma intervalos]
- [Ford Brasil - KA Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/ka/) - [oficial]

---

### FIESTA (2014-2019) - "New Fiesta"

Intervalo: **10.000 km ou 12 meses** (1a aos 6m / 5k km na linha 2015+).

**Plano garantia (3 anos, 36 meses ou 30.000 km)** - precos publicados pela Ford no lancamento 2018:

| Revisao # | KM | Meses | Itens principais | Total 3 rev. 1.6 Sigma | Total 3 rev. EcoBoost |
|---|---|---|---|---|---|
| 1a | 10.000 | 12 | Oleo, filtros, verificacao | (incluso no total) | (incluso no total) |
| 2a | 20.000 | 24 | Oleo, filtros completos | (incluso no total) | (incluso no total) |
| 3a | 30.000 | 36 | Oleo, filtro combustivel, geral | (incluso no total) | (incluso no total) |
| **Total 3 rev. (publicado Ford 2018)** |  |  |  | **R$ 1.568** | **R$ 1.620** |

**Planos pre-pagos Ford Protect (lancamento 2018)**:
- Ford Protect Advanced (4 rev. ate 48m/40k km): R$ 2.966.
- Ford Protect Premium (5 rev. ate 60m/50k km): R$ 3.573.

> Medias por revisao: ~R$ 520 (1.6 Sigma) ou ~R$ 540 (EcoBoost). Sao **os precos mais baixos da linha Ford no Brasil**.

**Fontes**:
- [Car.blog.br - New Fiesta 2018](https://www.car.blog.br/2017/11/ford-new-fiesta-2018-consumo-precos-e.html) - [oficial via imprensa, precos publicados pela Ford]
- [Ford Brasil - Fiesta Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/new-fiesta-hatch/) - [oficial]
- [Sua Oficina Online - tabela revisao Fiesta](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-fiesta/) - [indicativo]

---

### ECOSPORT (2013-2022)

Intervalo: **10.000 km ou 12 meses** (1a aos 6m / 5k km na linha 2015+).

| Revisao # | KM | Meses | Itens principais | Preco indicativo (BRL) |
|---|---|---|---|---|
| 1a | 5.000 | 6 | Inspecao basica (mao de obra cortesia 2015+) | gratis / inclusa |
| 2a | 10.000 | 12 | Oleo, filtros, verificacoes | R$ 450 - R$ 600 |
| 3a | 20.000 | 24 | Oleo, filtros completos, velas | R$ 700 - R$ 850 |
| 4a | 30.000 | 36 | Oleo, filtros, fluido freio, injecao | R$ 850 - R$ 1.000 |
| 5a | 40.000 | 48 | Oleo, correias, transmissao | R$ 1.100 - R$ 1.300 |
| 6a | 50.000 | 60 | Oleo, arrefecimento, direcao, suspensao | R$ 750 - R$ 900 |
| 7a | 60.000 | 72 | Revisao ampla, correia dentada (CRITICA) | R$ 1.400 - R$ 1.700 |
| 8a-10a | 70k-100k | 84-120 | Trocas escalonadas | (kits Italia Ricambi) |

**Engine variants**: 1.5 Dragon (2018+), 1.5 Sigma (ate 2018), 2.0 Direct Flex (Storm/Titanium), 1.6 (descontinuado).

**Ford Protect EcoSport (lancamento 2018)**:
- 3 revisoes iniciais: R$ 1.703 (~R$ 567/revisao).
- 4 revisoes (ate 48m/40k km) + 1 ano garantia extra: R$ 2.820 (~R$ 705/revisao).

**Custo medio anual manutencao preventiva EcoSport**: R$ 1.500-2.500.

**Fontes**:
- [Mercado Veiculos - EcoSport 2020](https://mercadoveiculos.com/info/revisao-ford-ecosport-2020) - [indicativo]
- [Sua Oficina Online - tabela revisao EcoSport](https://www.suaoficinaonline.com.br/conteudo/plano-de-revisao-ford-ecosport/) - [indicativo]
- [Ford Brasil - EcoSport Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/ecosport/) - [oficial]
- [Ford media - EcoSport 2018 lancamento](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2017/07/24/ecosport-2018-oferece-as-versoes-mais-completas-em-conteudo--com.html) - [oficial - planos Ford Protect publicados]

---

### FOCUS (2014-2019)

Intervalo: **10.000 km ou 12 meses** (1a aos 6m / 5k km na linha 2015+).

**Encerramento**: Ford encerrou producao Focus no Brasil em 2019. Manutencao via concessionaria continua mas tabela atualizada nao publicada para anos pos-2020.

| Revisao # | KM | Meses | Itens principais | Preco indicativo (BRL) |
|---|---|---|---|---|
| 1a | 5.000 | 6 | Inspecao basica (mao de obra cortesia) | gratis / inclusa |
| 2a | 10.000 | 12 | Oleo, filtros, verificacoes | R$ 500 - R$ 700 |
| 3a | 20.000 | 24 | Oleo, filtros completos | R$ 650 - R$ 900 |
| 4a | 30.000 | 36 | Oleo, filtros, fluido freio | R$ 800 - R$ 1.100 |
| 5a | 40.000 | 48 | Oleo, correias, transmissao | R$ 1.000 - R$ 1.300 |
| 6a | 50.000 | 60 | Oleo, arrefecimento, suspensao | R$ 800 - R$ 1.100 |
| 7a | 60.000 | 72 | Revisao ampla, correia dentada (CRITICA) | R$ 1.400 - R$ 1.800 |

**Engine variants**: 1.6 Sigma, 2.0 Direct Flex Duratec, 2.0 GDI EcoBoost (Titanium).

**Fontes**:
- [Ford Brasil - Focus Preco Fixo](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/focus/) - [oficial]
- [Sua Oficina Online - tabela revisao Focus](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-focus/) - [indicativo]
- [Luna Seguros - quanto custa manter Focus](https://luna.ac/blog/quanto-custa-manter-um-ford-focus) - [indicativo, nao acessivel via scraper]
- [Italia Ricambi - kits Focus 2.0 16V 2013+](https://www.italiaricambi.com.br/kit-revisao-ford-50000-km-60-meses-ford-focus-20-16v-de-2013-em-diante) - [confirma intervalos]

---

## Padroes transversais

### O que e Ford BR sempre faz

1. **Intervalo padrao = 10.000 km ou 12 meses, o que ocorrer primeiro** (validado: confirmado pelo press release oficial Ford "Linha 2015 - novo plano de manutencao" via Autoentusiastas/Car.blog.br + paginas oficiais Ford.com.br).
2. **Excecoes ao padrao**:
   - **Transit**: 20.000 km / 12 meses (perfil utilitario, oleo de maior duracao).
   - **Ranger 3.0 V6 e Maverick FHEV (2023+)**: 16.000 km / 12 meses (Revisao Inteligente via oil-life monitor).
3. **1a revisao especial** (linha 2015-2022): aos 6 meses ou 5.000 km, mao de obra cortesia. Linha 2023+ (Revisao Inteligente) eliminou esta revisao obrigatoria.
4. **Tolerancia oficial**: +/- 1.000 km ou +/- 30 dias.
5. **Conteudo de toda revisao**: 60 itens verificados, troca de oleo e filtros, lavagem cortesia.

### Itens sempre presentes (em toda revisao)

- Oleo motor (Motorcraft, viscosidade conforme modelo - 5W20 em modelos pequenos, 5W30 no Territory).
- Filtros (oleo sempre; ar/combustivel em revisoes alternadas).
- Inspecao de freios (pastilhas, discos).
- Inspecao de suspensao e direcao.
- Fluido de arrefecimento, fluido de freio.

### Itens criticos por marco quilometrico

| Marco | Item critico | Por que importa para churn |
|---|---|---|
| 20k km / 24m | Filtro de combustivel | Falha aqui = engine miss = cliente vai para oficina nao-Ford |
| 40k km / 48m | Correias acessorias, transmissao | Sintomas de desgaste comecam aparecer aqui |
| 60k km / 72m | Correia dentada (Ka, EcoSport, Fiesta - motores Sigma) | Quebra = motor destruido = perda total = churn garantido |
| 80k km / 96m | Velas, fluido transmissao automatica | Cliente comeca a achar que carro "esta velho" |
| 100k km / 120m | Revisao geral, embreagem (manuais) | Decisao "consertar ou trocar" |

### Plano Ford Protect (pre-pago)

- **2024**: 10% das vendas com plano pre-pago.
- **2025**: passou de 15%.
- Tipos:
  - Ford Protect Manutencao (3 ou 4 revisoes incluso).
  - Ford Protect Advanced (estende garantia, ate 48m/40k km).
  - Ford Protect Premium (estende ate 60m/50k km).
  - Ford Protect Plus (Ranger 3.0 V6: 5 revisoes ate 80k km).
- **Insight para o projeto**: cliente que comprou Ford Protect tem **muito maior tendencia a voltar para a concessionaria**. Cruzar adesao Protect x churn = feature poderosa para modelo.

---

## Aplicacao para a flag "veiculo em atraso de revisao"

### Regra de negocio sugerida (para a plataforma Forward Service)

```
Para cada veiculo no dataset:
  intervalo_km = lookup_intervalo(modelo, ano)  // tabela mestre acima
  intervalo_meses = 12  // padrao Ford BR
  
  km_desde_ultima_revisao = km_atual - km_ultima_revisao
  meses_desde_ultima_revisao = hoje - data_ultima_revisao
  
  flag_atrasado = (
    km_desde_ultima_revisao > (intervalo_km + 1000)  // tolerancia oficial
    OR
    meses_desde_ultima_revisao > (intervalo_meses + 1)
  )
  
  // Severidade (para priorizacao de outreach):
  severidade = max(
    km_desde_ultima_revisao / intervalo_km,
    meses_desde_ultima_revisao / intervalo_meses
  )
  // > 1.5x = crítico (cliente provavelmente ja foi para oficina nao-Ford)
  // > 2.0x = perdido (churn quase certo - prox compra = outra marca)
```

### Hierarquia de risco

| Severidade | Acao Forward Service |
|---|---|
| 0.8-1.0 | Pre-aviso amigavel (push, email) |
| 1.0-1.3 | Lembrete + incentivo (cupom revisao) |
| 1.3-1.7 | Outreach proativo (concessionaria liga) |
| 1.7-2.5 | Recuperacao ativa (oferta especial Ford Protect) |
| > 2.5 | Cliente perdido provavel (nao desperdicar verba) |

---

## Fontes consolidadas

### Oficiais Ford BR (paginas indexadas, nem todas scrapaveis)
- [ford.com.br - Revisao Preco Fixo Ranger](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/ranger/) - acesso 2026-05-11
- [ford.com.br - Revisao Ford Ranger 2023+](https://www.ford.com.br/servico-ao-cliente/revisao-ford/ranger/) - acesso 2026-05-11
- [ford.com.br - Maverick](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/maverick/) - acesso 2026-05-11
- [ford.com.br - Maverick FHEV](https://www.ford.com.br/servico-ao-cliente/revisao-ford/maverick-fhev/) - acesso 2026-05-11
- [ford.com.br - Territory](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/territory/) - acesso 2026-05-11
- [ford.com.br - Transit Bus](https://www.ford.com.br/servico-ao-cliente/revisao-ford/transit-bus/) - acesso 2026-05-11
- [ford.com.br - Transit Furgao](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/transit-furgao/) - acesso 2026-05-11
- [ford.com.br - Fiesta](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/new-fiesta-hatch/) - acesso 2026-05-11
- [ford.com.br - EcoSport](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/ecosport/) - acesso 2026-05-11
- [ford.com.br - Focus](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/focus/) - acesso 2026-05-11
- [ford.com.br - KA](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/ka/) - acesso 2026-05-11
- [ford.com.br - termos e condicoes](https://www.ford.com.br/servico-ao-cliente/revisao-preco-fixo/termos-e-condicoes/) - acesso 2026-05-11

### Press releases Ford Brasil (oficiais)
- [Ford media - linha 2015 novo plano](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2014/08/13/ford-introduz-novo-plano-de-manutencao--mais-economico--para-tod.html) - acesso 2026-05-11
- [Ford media - Transit lancamento cortesia](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2021/11/03/ford-transit-tem-pacote-gratuito-de-revisao-e-pecas-como-oferta-.html) - acesso 2026-05-11
- [Ford media - EcoSport 2018](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2017/07/24/ecosport-2018-oferece-as-versoes-mais-completas-em-conteudo--com.html) - acesso 2026-05-11
- [Ford media - Maverick Hybrid AWD 2026](https://media.ford.com/content/fordmedia/fsa/br/pt/news/2025/11/nova-ford-maverick-hybrid-chega-mais-moderna--completa-e-com-tra.html) - acesso 2026-05-11

### Imprensa especializada
- [Mercado Veiculos - Ka 2020](https://mercadoveiculos.com/info/revisao-ford-ka-2020) - 2026-05-11
- [Mercado Veiculos - EcoSport 2020](https://mercadoveiculos.com/info/revisao-ford-ecosport-2020) - 2026-05-11
- [Mercado Veiculos - Maverick 2023](https://mercadoveiculos.com/info/revisao-ford-maverick-2023) - 2026-05-11
- [Mercado Veiculos - Ranger 2024](https://mercadoveiculos.com/info/revisao-ford-ranger-2024) - 2026-05-11
- [Mercado Veiculos - Territory 2024](https://mercadoveiculos.com/info/revisao-ford-territory-2024) - 2026-05-11
- [Car.blog.br - linha 2015 novo plano (cobertura imprensa)](https://www.car.blog.br/2014/08/ford-altera-plano-de-revisoes-de-seus.html) - 2026-05-11
- [Car.blog.br - New Fiesta 2018 precos publicados](https://www.car.blog.br/2017/11/ford-new-fiesta-2018-consumo-precos-e.html) - 2026-05-11
- [Car.blog.br - Transit 2026](https://www.car.blog.br/2025/02/novo-ford-transit-2026-preco-parte-de-r.html) - 2026-05-11
- [Autoentusiastas - Ford aumenta intervalos linha 2015](https://autoentusiastas.com.br/2014/08/ford-aumenta-os-intervalos-de-manutencao-de-toda-a-sua-linha/) - 2026-05-11
- [Garagem360 - custos manutencao Ranger](https://garagem360.com.br/veja-custos-de-manutencao-revisao-e-seguro-da-ford-ranger/) - 2026-05-11
- [Mobiauto - Ranger custos](https://www.mobiauto.com.br/revista/ford-ranger-custos-de-revisao-seguro-e-pecas-e-manutencao/1534) - 2026-05-11
- [Mobiauto - Maverick custos](https://www.mobiauto.com.br/revista/ford-maverick-custos-de-revisao-seguro-e-pecas-de-manutencao/1925) - 2026-05-11
- [Webmotors - revisoes Territory](https://www.webmotors.com.br/wm1/dinheiro-e-economia/quanto-custam-as-revisoes-do-ford-territory) - 2026-05-11
- [O Antagonista - custo Territory 2025](https://oantagonista.com.br/ladooa/carros/quanto-custa-por-mes-ter-um-ford-territory-em-2025/) - 2026-05-11
- [Justos - quanto custa Maverick](https://www.justos.com.br/blog/quanto-custa-manter-um-ford-maverick) - 2026-05-11
- [Luna Seguros - quanto custa Focus](https://luna.ac/blog/quanto-custa-manter-um-ford-focus) - 2026-05-11
- [Luna Seguros - quanto custa Maverick](https://luna.ac/blog/quanto-custa-manter-um-ford-maverick) - 2026-05-11
- [Sua Oficina Online - Ka](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-ka/) - 2026-05-11
- [Sua Oficina Online - Fiesta](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-fiesta/) - 2026-05-11
- [Sua Oficina Online - Focus](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-focus/) - 2026-05-11
- [Sua Oficina Online - EcoSport](https://www.suaoficinaonline.com.br/conteudo/plano-de-revisao-ford-ecosport/) - 2026-05-11
- [Sua Oficina Online - Ranger](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-ranger/) - 2026-05-11
- [Sua Oficina Online - Transit](https://www.suaoficinaonline.com.br/conteudo/plano-revisao-ford-transit/) - 2026-05-11
- [Italia Ricambi - kits revisao Ford diversos modelos](https://www.italiaricambi.com.br/) - 2026-05-11
- [Fordbarigui - adesao Ford Protect](https://www.fordbarigui.com.br/noticias/detalhes/593/revisao-pre-paga-cresce-na-preferencia-dos-clientes-da-ford) - 2026-05-11
- [Fordstudio - Ford Protect 15% vendas](https://www.fordstudio.com.br/noticias/detalhes/994/cresce-a-adesao-aos-planos-de-revisao-pre-paga-e-garantia-estendida-da-ford) - 2026-05-11

---

## Gaps e ressalvas

1. **Ford.com.br nao retorna conteudo para scrapers** (HTTP 403). Precos oficiais por revisao precisam ser obtidos manualmente via browser ou ligacao a concessionaria. Para o projeto: usar precos publicados em press releases (Fiesta 2018, EcoSport 2018) como ancora e estimativas da imprensa para os demais.
2. **Manuais do proprietario em PDF**: nao encontrei links publicos diretos. A Ford direciona via portal `fordservicecontent.com` (apos cadastro do VIN do cliente). Sem acesso anonimo.
3. **Discrepancia Maverick**: Justos diz 10k km / 12m; Ford oficial diz 16k km / 12m (Revisao Inteligente). Para a flag de churn, recomendamos **usar 10k km como gatilho conservador** (cobre tambem clientes em uso severo).
4. **Mercadoveiculos.com**: a estrutura de itens por revisao parece ser **template generico** (texto identico entre Ka, EcoSport, Territory, Maverick, Ranger). **Confiar apenas em km e intervalo**; descrever os itens via templates do manual do proprietario, nao pelo MV.
5. **Focus**: tabela de precos publicada para nenhum ano. Estimativas via Luna Seguros (nao acessivel via scraper).
6. **Edge, Fusion, Mustang, F-150**: lower priority, nao cobertos.
7. **Linha pre-2015 (Ka antigo, EcoSport ate 2014, Focus ate 2014)**: provavelmente intervalo de 7.500 km / 6 meses (plano antigo). Confirmar antes de aplicar a flag para veiculos > 2014.
