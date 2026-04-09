# Challenge Ford x FIAP 2026 - Analise Consolidada

> Documento gerado a partir do PDF oficial "Ford FIAP 2026: Kick-off do Projeto"
> Data de referencia: 09/04/2026 | Deadline unica: **24/05/2026**

---

## 1. Visao Geral do Programa

O programa **Ford & FIAP: Dados na Pratica** conecta estudantes de tecnologia a desafios reais de negocios da Ford. Lideres da Ford trazem cases focados em **dados** para otimizar decisoes operacionais e melhorar a experiencia do cliente.

### Regras Estruturais
- Grupos de **3 a 5 integrantes**, mesma turma
- Sem troca de grupo durante o semestre
- **1 unica Sprint** neste semestre, valendo para notas 1 e 2
- Entrega via **tarefas no Microsoft Teams**
- A nota da Challenge e a **media das entregas de todas as disciplinas** e TODAS as disciplinas recebem essa nota
- Scrum Master: **Prof. Yan Coelho** (proyan.coelho@fiap.com.br)

---

## 2. Os Dois Desafios da Ford

A Ford apresentou **dois desafios distintos**. Cada equipe deve escolher um deles como direcionamento.

---

### DESAFIO 01 - Inteligencia Competitiva Automotiva

#### Dor da Ford
A Ford precisa compreender rapidamente como os veiculos concorrentes se posicionam em termos de **preco** e **pacotes de equipamentos oferecidos**. Hoje, obter o valor percebido pelo cliente em relacao a concorrencia exige dados precisos e extremamente organizados - e isso nao e trivial.

#### O que deve ser criado
Uma **ferramenta / modelo / solucao** que permita receber dados tecnicos da concorrencia a partir de uma entrada simples e gerar uma **lista padronizada de especificacoes**.

#### Abordagem tecnica
Livre: IA, modelos hibridos, regras, automacao, outras solucoes.

#### Entradas obrigatorias
O usuario deve poder definir **livremente** a lista de equipamentos / atributos tecnicos que deseja pesquisar, juntamente com:
- **Marca**
- **Modelo**
- **Versao**

#### Saida obrigatoria
- Uma lista de especificacoes tecnicas
- Formato da lista **sempre o mesmo**, independentemente do veiculo
- Campos claros, organizados e comparaveis
- Se alguma informacao nao existir, deve ficar **explicito** (ex: vazio / nao disponivel)

#### Validacao da solucao
- Utilizar a **Ford Ranger Raptor** como caso de teste
- A solucao deve entregar corretamente todas as especificacoes tecnicas apresentadas no slide da Ranger Raptor
- Se os dados forem entregues de forma clara, organizada e consistente = solucao operando corretamente

#### Analise da Dor
| Aspecto | Detalhe |
|---|---|
| **Problema central** | Dificuldade de coletar e padronizar dados tecnico-competitivos de veiculos rivais |
| **Quem sofre** | Equipes de inteligencia de mercado / pricing / produto da Ford |
| **Impacto** | Decisoes de posicionamento de preco e pacotes de equipamentos ficam lentas ou imprecisas |
| **O que nao existe hoje (implicito)** | Uma ferramenta automatizada que normalize specs de diferentes marcas em formato comparavel |

---

### DESAFIO 02 - Impulsionando o VIN Share na America do Sul

#### Dor da Ford
Reter clientes no servico de **pos-venda** e crucial para o sucesso e sustentabilidade do negocio. O indicador-chave e o **VIN Share** (Service Share): a porcentagem de veiculos Ford que utilizam a **rede oficial** para manutencoes. Clientes estao abandonando a rede oficial.

#### O que deve ser criado
Ferramentas e metodologias que permitam as **concessionarias**:

**A) Analise e Visualizacao de Dados**
- Dashboards e relatorios interativos com granularidade do Service Share por: concessionaria, modelo de veiculo, idade do veiculo, tipo de servico e outras variaveis
- Identificar padroes, tendencias e anomalias no comportamento de servico dos clientes em nivel de concessionaria

**B) Geracao de Leads e Modelagem Preditiva**
- Algoritmos/modelos preditivos que identifiquem veiculos com alta probabilidade de precisar de servico OU que estejam em risco de sair da rede Ford
- Sistemas para gerar leads de servico proativos e personalizados para concessionarias, usando: dados de veiculos conectados, historico de manutencao, status da garantia e outras fontes

**C) Otimizacao da Jornada do Cliente**
- Usar insights para otimizar comunicacoes: lembretes de servico, ofertas, agendamento
- Solucoes que integrem dados de diferentes fontes para criar **visao 360 graus** do cliente e do veiculo
- Experiencia pos-venda mais fluida e personalizada

#### Analise da Dor
| Aspecto | Detalhe |
|---|---|
| **Problema central** | Perda de clientes no pos-venda para oficinas nao-autorizadas |
| **Quem sofre** | Rede de concessionarias Ford + Ford como marca (receita de servicos) |
| **Indicador-chave** | VIN Share / Service Share |
| **Impacto** | Perda de receita recorrente, menor fidelizacao, menor LTV do cliente |
| **O que falta** | Visibilidade granular dos dados, capacidade preditiva, comunicacao proativa |

---

## 3. Entregaveis por Disciplina (Sprint Unica)

Cada disciplina tem criterios especificos de avaliacao. Todas contribuem para a nota final.

---

### 3.1 Arquitetura Orientada a Servicos e Web Services

| Criterio | Peso |
|---|---|
| **Integracao por Web Services** | **50%** |
| - Desenho de arquitetura com componentes | 10% |
| - Implementacao de APIs RESTful ou SOAP | 20% |
| - Uso adequado de metodos HTTP | 10% |
| - Documentacao das APIs (README ou Swagger) | 10% |
| **Arquitetura SOA** | **20%** |
| - Organizacao modular (servicos independentes e reutilizaveis) | 10% |
| - Separacao clara entre camadas (apresentacao, servico, dados) | 10% |
| **Padroes e Boas Praticas** | **15%** |
| - Adocao de padroes (REST, SOAP, JSON, XML, WSDL) | 8% |
| - Tratamento adequado de erros e excecoes | 7% |
| **Conexao com banco de dados** | **15%** |
| - Dependencias e configuracoes para conexao | 8% |
| - Controle de migracoes | 7% |

**Ponto-chave:** O peso mais forte (20%) esta na implementacao real de APIs. Swagger/documentacao e desenho de arquitetura somam 20% adicionais. A disciplina exige codigo funcional, nao apenas documentacao.

---

### 3.2 Mobile Development and IoT

**Tecnologia obrigatoria:** React Native com Expo

**Requisitos:**
- App mobile **multiplataforma** (iOS e Android)
- Interface clara, navegacao intuitiva
- Integracao com **pelo menos uma fonte de dados externa via API**
- Consumo de dados relevantes (APIs externas, datasets simulados ou servicos proprios)
- Demonstrar dominio de: componentes React Native, gerenciamento de estado, navegacao com Expo Router, consumo de APIs assincronas

**Diferenciais:**
- Notificacoes
- Armazenamento local
- Integracao com sensores do dispositivo

**Criterios de avaliacao:**
- Qualidade tecnica da implementacao
- Consistencia da experiencia do usuario
- Aderencia ao problema de negocio da Ford
- Prototipagem visual consistente
- Codigo organizado
- Narrativa clara de produto

**Obs:** O app deve demonstrar de forma clara como contribui para o desafio escolhido (1 ou 2).

---

### 3.3 Testing, Compliance and Quality Assurance

Entrega com **tres componentes principais** + arquitetura TOGAF:

#### A) Pitch de Projeto
- Nome do projeto e identificacao da equipe
- Qual o problema a resolver
- Se o desafio e exclusivo da Ford ou presente em diversas empresas (com estatisticas)
- Descricao da solucao proposta (objetivos, recursos, requisitos)
- Benchmarking: solucoes similares no mercado
- Diferenciacoes competitivas
- Roadmap de etapas (o que entregar nas Sprints 3 e 4)
- **Obrigatorio incluir:** criterios de qualidade (performance, seguranca, usabilidade), principais riscos e impactos no negocio, metricas de sucesso (tempo de resposta, disponibilidade, satisfacao do usuario)

#### B) Quadro Business Canvas
- Clientes, canais, proposta de valor, atividades-chave, recursos-chave, parceiros, custos, fontes de receita/reducao de custo
- **Obrigatorio incluir:** analise de impactos de falhas na cadeia de valor (operacionais, financeiros, reputacionais) e custos associados a qualidade (retrabalho, manutencao, suporte, incidentes em producao)

#### C) Quadro de Valor
- Stakeholders, expectativas, entregas prometidas, metricas/indicadores, prioridade
- **Obrigatorio incluir para cada beneficio:** uma metrica de negocio (produtividade, reducao de custos) E uma metrica de qualidade (tempo de resposta, disponibilidade, confiabilidade)

#### D) Arquitetura TOGAF/Archi
- Ferramenta: **Archi** (formato .archimate)
- Visao da Arquitetura (estrategica e requisitos)
- Arquitetura de Negocio (mudanca no processo da Ford)
- Arquitetura de Sistema (componentes de software e comunicacoes)
- Arquitetura de Tecnologia (infraestrutura)
- **Obrigatorio incluir:** como a arquitetura contribui para a qualidade e mecanismos de monitoramento em producao

#### Formato de Entrega
- Apresentacao: **10-15 slides**, com nome e RM no slide 1
- Video de pitch: **ate 3 minutos** (link no slide 1)
- Arquivo .archimate
- Todos os integrantes devem participar do video
- Enviar tudo junto pelo Teams

---

### 3.4 Cybersecurity (100 pontos)

| Categoria | Pontos | Itens |
|---|---|---|
| **1. Seguranca de Entrada e Validacao de Dados** | **20** | Validacao de entradas; sanitizacao (SQLi, XSS, command injection); normalizacao de parametros de API (marca, modelo, versao); limitacao de tamanho/formato; tratamento seguro de erros (sem stack trace) |
| **2. Autenticacao e Autorizacao** | **20** | Autenticacao segura (JWT, OAuth2) com expiracao e assinatura forte; RBAC (analistas, admins, usuarios comuns) |
| **3. Protecao de APIs e Servicos** | **20** | HTTPS/TLS 1.2+; Rate limiting e throttling; CORS correto; Assinatura/verificacao de integridade de payloads |
| **4. Seguranca de Dados e Privacidade** | **25** | Criptografia em repouso; politica de retencao/descarte; anonimizacao/pseudonimizacao (ML e dashboards); protecao contra exposicao acidental (logs, dumps, endpoints nao documentados) |
| **5. Monitoramento, Logs e Auditoria** | **15** | Logs estruturados sem dados sensiveis; monitoramento de eventos suspeitos; trilha de auditoria para acoes criticas |

**Ponto-chave:** O maior peso (25 pts) esta em Seguranca de Dados e Privacidade. Isso se alinha fortemente com o Desafio 02 (dados de clientes, historico de manutencao, leads).

---

### 3.5 Inteligencia Artificial & Machine Learning

**Tema:** Segmentacao e Classificacao de Clientes Ford (Dados Sinteticos)

**Objetivo:** Aumentar a retencao de clientes na rede oficial de manutencao.

#### Duas Frentes Complementares

**Frente 1 - Segmentacao Comportamental (Nao Supervisionada)**
- Usar **Base 1** (historico completo pos-compra)
- Tecnicas de clustering
- Identificar perfis reais de clientes

**Frente 2 - Classificacao Preditiva (Supervisionada)**
- Usar **Base 2** (apenas dados do momento da compra)
- Transformar clusters em variavel-alvo
- Prever perfil de novos clientes no momento da compra

#### Hipotese Inicial de Perfis (a ser validada pelos dados)
| Perfil | Comportamento |
|---|---|
| **Cliente Fiel** | Retorna consistentemente a rede oficial, independente de preco |
| **Cliente de Abandono** | Faz no maximo a 1a revisao e sai da rede para opcoes mais baratas |
| **Cliente Esquecido** | Perde o timing da manutencao, tenta retornar e se frustra |
| **Cliente Economico** | Mantem relacao com a rede, mas e altamente sensivel a preco/promocoes |

#### REGRA CRITICA - DATA LEAKAGE
> Na etapa de classificacao, e **TERMINANTEMENTE PROIBIDO** utilizar qualquer variavel que represente comportamento futuro do cliente (revisoes realizadas, tempo ate manutencao, gastos, indicadores pos-compra). Isso invalida completamente o modelo.

#### Pipeline de Entregas
1. **Preparacao dos dados** - analise exploratoria, tratamento de missing values, inconsistencias, variaveis categoricas
2. **Segmentacao** (Base 1) - escolha e justificativa de variaveis, tecnica de clustering, definicao de numero de segmentos
3. **Interpretacao** - perfis de negocio claros (nada de "Cluster 0", "Cluster 1")
4. **Estrategias de retencao** por segmento - coerencia entre comportamento e acao
5. **Classificacao** (Base 2) - tratamento de variaveis, treino/teste, avaliacao (accuracy, precision, recall, F1, matriz de confusao)
6. **Leitura executiva** - segmentos identificados, risco de evasao, sensibilidade a acoes comerciais, capacidade preditiva, aplicacao pratica na concessionaria

#### Entregaveis Finais
- **Jupyter Notebook (.ipynb)** com todo o desenvolvimento tecnico
- **Relatorio em PDF** com principais achados

#### O que reprova
- Usar variaveis futuras na classificacao
- Misturar Base 1 e Base 2 indevidamente
- Clusters sem interpretacao de negocio
- Conclusoes sem suporte analitico

---

## 4. Mapa de Conexao: Desafios x Disciplinas

| Disciplina | Desafio 01 (Inteligencia Competitiva) | Desafio 02 (VIN Share / Pos-venda) |
|---|---|---|
| **Arq. Servicos/Web Services** | APIs para buscar e padronizar specs de veiculos | APIs para integrar dados de manutencao, leads e dashboards |
| **Mobile** | App para consultar/comparar especificacoes tecnicas | App para concessionaria gerenciar leads, agendar servicos |
| **Testing/QA** | Pitch + Canvas + TOGAF da solucao escolhida | Pitch + Canvas + TOGAF da solucao escolhida |
| **Cybersecurity** | Proteger dados de scraping, APIs de consulta | Proteger dados de clientes, historico, LGPD |
| **IA/ML** | (menos aderente diretamente) | Segmentacao e classificacao de clientes - **perfeita aderencia** |

**Observacao critica:** A disciplina de IA/ML esta 100% alinhada ao Desafio 02 (retencao de clientes). Se o grupo escolher o Desafio 01, o trabalho de IA/ML ainda sera sobre segmentacao de clientes (e o enunciado do professor), mas o restante das disciplinas pode ser direcionado ao Desafio 01.

---

## 5. Oportunidades de Solucao e Insights Estrategicos

### Para o Desafio 01
- **Web scraping inteligente** + LLM para extrair e padronizar specs de sites de montadoras
- Pipeline: entrada (marca/modelo/versao + atributos) -> busca automatizada -> normalizacao -> saida padronizada
- Possibilidade de usar IA generativa para interpretar fichas tecnicas em formatos heterogeneos
- Validacao clara: se a Ranger Raptor sai correta, a solucao funciona

### Para o Desafio 02
- **Plataforma integrada** concessionaria: dashboard de VIN Share + sistema de leads preditivos + automacao de comunicacao
- O trabalho de IA/ML ja entrega o motor analitico (segmentacao + classificacao)
- O app mobile pode ser a interface do concessionario para acessar leads e agendar contatos
- A API conecta tudo: dados de veiculos conectados, historico, garantia

### Avaliacao Estrategica: Qual Desafio Escolher?

| Criterio | Desafio 01 | Desafio 02 |
|---|---|---|
| Alinhamento com IA/ML | Baixo (IA/ML e sobre pos-venda) | **Total** |
| Complexidade tecnica | Media (scraping + normalizacao) | Alta (pipeline completo de dados) |
| Impacto de negocio demonstravel | Medio | **Alto** (retencao = receita recorrente) |
| Coerencia entre disciplinas | Precisa adaptar IA/ML | **Todas as disciplinas convergem** |
| Risco de execucao | Depende de fontes externas de dados | Dados sinteticos fornecidos pelo professor |

---

## 6. Pontos de Atencao Criticos

### Prazo
- **Unica Sprint**: 24/05/2026 (faltam ~45 dias a partir de hoje)
- Nao ha segunda chance. Tudo deve ser entregue junto.

### Nota
- A media das entregas de TODAS as disciplinas compoe a nota
- Uma disciplina fraca puxa todas as outras para baixo

### IA/ML - Armadilhas
- Data leakage e eliminatorio
- Base 1 (segmentacao) e Base 2 (classificacao) nao podem ser misturadas
- Clusters devem ter nomes de negocio, nao numericos

### Testing/QA - Volume de trabalho
- E a disciplina com maior volume de entregaveis: Pitch, Canvas, Quadro de Valor, Arquitetura TOGAF, video de 3 min
- Requer ferramenta Archi (arquivo .archimate)
- Todos os integrantes devem aparecer no video

### Cybersecurity - Implementacao Real
- Nao basta documentar; os criterios exigem implementacao (JWT, RBAC, HTTPS, rate limiting, criptografia)
- O maior peso (25 pts) e em privacidade de dados - considerar LGPD

### Mobile - Stack Definida
- **React Native com Expo** e obrigatorio (nao ha escolha de tecnologia)
- Deve consumir pelo menos uma API externa
- Expo Router para navegacao

### Arquitetura - APIs Funcionais
- 50% da nota e integracao por web services
- APIs devem estar documentadas (Swagger e o padrao)
- Banco de dados com migracoes controladas

---

## 7. Estrutura dos Dois Tipos de Entregaveis

### Entregaveis por Disciplina (obrigatorios para nota)
Sao as entregas especificas que cada professor definiu. Devem ser feitas independentemente de resolverem a dor da Ford diretamente. Cada uma tem rubrica propria e contribui para a media geral.

### Entregavel Livre (produto final)
A solucao que o grupo escolhe construir para de fato resolver o problema da Ford. Pode ser o proprio conjunto integrado das entregas por disciplina, ou algo completamente diferente. O formato e livre. O foco e resolver o problema de forma concreta e demonstravel.

**A inteligencia esta em fazer os dois convergirem:** construir uma solucao unica onde cada entrega por disciplina e uma "fatia" do produto final, evitando retrabalho e maximizando coerencia.

---

## 8. Checklist de Entregas (24/05/2026)

- [ ] **Arq. Servicos/Web Services**: APIs RESTful/SOAP + Swagger + desenho de arquitetura + banco com migracoes
- [ ] **Mobile**: App React Native/Expo multiplataforma + integracao API + navegacao
- [ ] **Testing/QA**: Apresentacao 10-15 slides + video pitch 3min + Canvas + Quadro de Valor + arquivo .archimate
- [ ] **Cybersecurity**: Implementacao de seguranca (validacao, JWT/OAuth2, RBAC, HTTPS, rate limiting, criptografia, logs)
- [ ] **IA/ML**: Jupyter Notebook (.ipynb) + Relatorio PDF (segmentacao Base 1 + classificacao Base 2)
- [ ] Tudo enviado via **Microsoft Teams**

---

*Documento consolidado para uso interno do grupo. Base para planejamento e execucao do Challenge Ford x FIAP 2026.*
