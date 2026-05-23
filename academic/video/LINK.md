# QA-5 — Vídeo Pitch ForwardService

> **Status:** Aguardando gravação  
> **Deadline:** 23/05/2026  
> **Duração máxima:** 3 minutos (180 segundos)  
> **Requisito:** Os 4 integrantes devem aparecer no vídeo

---

## Link do Vídeo

```
[INSERIR LINK AQUI APÓS PUBLICAR]
```

> Publicar no **YouTube (não-listado)** ou **Google Drive (link público compartilhado)**.  
> Após publicar, colocar o link também no **Slide 1 da apresentação (PITCH.pptx)**.

---

## Setup Mínimo

- **Resolução:** 1080p (celular é suficiente)
- **Áudio:** limpo, sem barulho de fundo — use headset se possível
- **Cenário:** fundo neutro ou com logo ForwardService
- **Slide-card:** nome + RM de cada integrante no canto inferior durante sua fala

---

## Roteiro — Divisão 45 segundos por integrante

### 🎬 Abertura (5s — voz over ou texto animado)
> *"ForwardService — A Ford saiu da fábrica, não da sua vida."*

---

### 🎤 João Victor Franco — Problema + Diferenciação (45s)

**Fala sugerida:**
> "A Ford fechou suas fábricas no Brasil em 2021 — mas ainda tem 12 milhões de veículos circulando.  
> O problema? Só 4% desses veículos passam pela rede oficial. Os outros 96% vão para oficinas independentes.  
> Chamamos isso de Curva da Morte: a cada revisão, 30 a 40% dos clientes somem.  
> A ForwardService resolve isso com 4 pilares e 9 lógicas de negócio que nenhum CRM genérico replica."

**Mostrar:** gráfico da Curva da Morte (31% → 22% → 15% → 9%)

---

### 🎤 Lucca Borges — Inteligência: Dataset + ML (45s)

**Fala sugerida:**
> "Nossa solução começa com dados — 602 mil eventos reais de manutenção Ford, com 175 mil veículos únicos.  
> Usamos Machine Learning em 3 camadas: K-means para segmentar clientes em 4 perfis — Fiel, Econômico, Esquecido e Abandono.  
> XGBoost para prever o risco de cada cliente sair. E Survival Analysis para saber exatamente quando ele vai sumir.  
> O resultado: cada veículo Ford tem uma etiqueta, um termômetro de risco e uma ação sugerida — automaticamente."

**Mostrar:** tela do notebook com os 4 clusters + o score de churn

---

### 🎤 Ruan Melo — Arquitetura Técnica (45s)

**Fala sugerida:**
> "A arquitetura segue o padrão SOA: tudo passa pelo forward-api-java, nosso portão central em Java 17 com Spring Boot.  
> O mobile usa React Native — um único app, dois modos: Modo Ford para o atendente da concessionária,  
> e Modo Cliente para o dono do carro.  
> As ações automáticas saem pelo n8n integrado ao WhatsApp Business — 97% de taxa de abertura no Brasil.  
> Toda a infraestrutura roda na Azure, com PostgreSQL e Docker."

**Mostrar:** diagrama de arquitetura com os 5 componentes + seta do portão único

---

### 🎤 Rodrigo Jimenez (Roji) — Valor para Ford + Roadmap (45s)

**Fala sugerida:**
> "O impacto é mensurável. Cada campanha de WhatsApp retorna 300 reais para cada 1 investido — ROI de 300 para 1.  
> Com Ford Care, nosso plano pré-pago, retenção salta de 20% para 60% — o triplo.  
> O Quadro de Valor mostra: para a Ford, VIN Share crescente. Para o dealer, lista de leads priorizados todo dia.  
> Para o cliente de Ka e EcoSport, que se sentia abandonado — um lembrete, uma proposta, uma reconexão.  
> Sprint 2: Recall Gateway, Rede Invertida, Ponte Serviço-Venda.  
> ForwardService — a Ford não saiu da vida do seu cliente. Nós garantimos isso."

**Mostrar:** slide com o ROI 300:1 + tela do dashboard web

---

### 🎬 Encerramento (5s)
> *"ForwardService · Ford Challenge FIAP 2026 · github.com/fwd-ford"*

---

## Dicas de Edição

- **Ferramenta sugerida:** DaVinci Resolve (gratuito) / CapCut / Premiere
- **Cortes:** secos entre falantes (sem fade longo)
- **Slide-card:** texto com nome + RM no canto inferior esquerdo de cada fala
- **Música de fundo:** opcional — royalty-free (YouTube Audio Library ou Pixabay)
- **Exportar:** MP4, H.264, 1080p, bitrate ≥ 8 Mbps

---

## Checklist antes de publicar

- [ ] Vídeo ≤ 3 minutos
- [ ] Os 4 integrantes aparecem e falam
- [ ] Slide-card com nome + RM visível em cada fala
- [ ] Áudio limpo, sem eco ou barulho de fundo
- [ ] Link publicado (YouTube não-listado ou Google Drive público)
- [ ] Link inserido neste arquivo (campo acima)
- [ ] Link inserido no Slide 1 do PITCH.pptx
- [ ] Link salvo em `forward-docs/academic/video/LINK.md` ✅ (este arquivo)

---

## Fontes usadas no roteiro

- `forward-docs/project/00_BASE_FUNDACIONAL.md` — 4 pilares, 9 lógicas, personas João/Maria/Carlos
- `forward-docs/project/03_SOLUTION_DESIGN.md` v2.1 — "Um dia no ForwardService" (Parte 2)
- `forward-docs/project/02e_DATASET_OFICIAL_E_FONTES.md` — VIN Share, Curva da Morte real
