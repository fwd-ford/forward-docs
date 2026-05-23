"""
QA-4 — Gerador do arquivo ForwardService.archimate
Formato: XML do Archi (The Open Group ArchiMate Tool)
Versão compatível: Archi 4.x (.archimate single-file XML)

Views geradas:
  1. Motivation View    — drivers, stakeholders, goals, requirements
  2. Business View      — as-is (churn) × to-be (ForwardService)
  3. Application View   — componentes de software
  4. Technology View    — infra Azure, Docker, Postgres
  5. Requirements View  — requisitos de qualidade (extra)
  6. Monitoring View    — Grafana, audit_log, alertas (extra)
"""
import uuid, textwrap
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

NS = "http://www.archimatetool.com/archimate"
XSI = "http://www.w3.org/2001/XMLSchema-instance"

def uid():
    return "id-" + uuid.uuid4().hex[:12]

def pretty(elem):
    raw = tostring(elem, encoding="unicode")
    return minidom.parseString(raw).toprettyxml(indent="  ")

# ── Model root ─────────────────────────────────────────────────────────────────
model = Element("archimate:model", {
    "xmlns:xsi": XSI,
    "xmlns:archimate": NS,
    "name": "ForwardService — Ford Challenge FIAP 2026",
    "id": uid(),
    "version": "4.10.0",
})

# ── Folders ────────────────────────────────────────────────────────────────────
def folder(parent, name, type_, id_=None):
    f = SubElement(parent, "folder", {"name": name, "id": id_ or uid()})
    if type_:
        f.set("type", type_)
    return f

f_motivation = folder(model, "Motivation",   "motivation")
f_strategy   = folder(model, "Strategy",     "strategy")
f_business   = folder(model, "Business",     "business")
f_application= folder(model, "Application",  "application")
f_technology = folder(model, "Technology",   "technology")
f_impl       = folder(model, "Implementation","implementation_migration")
f_other      = folder(model, "Other",        "other")
f_relations  = folder(model, "Relations",    "relations")
f_views      = folder(model, "Views",        "diagrams")

# ── Helper to create elements ──────────────────────────────────────────────────
elements = {}  # name → id

def el(parent, xsi_type, name, doc=""):
    e = SubElement(parent, "element", {
        "xsi:type": f"archimate:{xsi_type}",
        "name": name,
        "id": uid(),
    })
    if doc:
        SubElement(e, "documentation").text = doc
    elements[name] = e.get("id")
    return e

def rel(parent, xsi_type, src_name, tgt_name, name=""):
    src = elements.get(src_name)
    tgt = elements.get(tgt_name)
    if not src or not tgt:
        return None
    r = SubElement(parent, "element", {
        "xsi:type": f"archimate:{xsi_type}",
        "id": uid(),
        "source": src,
        "target": tgt,
    })
    if name:
        r.set("name", name)
    return r

# ══════════════════════════════════════════════════════════════════════════════
# MOTIVATION ELEMENTS
# ══════════════════════════════════════════════════════════════════════════════
el(f_motivation, "Stakeholder", "Ford Brasil (Diretoria)", "Diretoria executiva — quer VIN Share crescente e ROI mensurável")
el(f_motivation, "Stakeholder", "Concessionária (Dealer)", "145 dealers ativos — precisa de leads priorizados e IHC")
el(f_motivation, "Stakeholder", "Cliente Ford",            "Dono de veículo Ford — quer lembrete proativo e experiência simplificada")
el(f_motivation, "Stakeholder", "Gestor Regional Ford",    "Compara performance de dealers por UF")
el(f_motivation, "Stakeholder", "Equipe ForwardService",   "4 desenvolvedores FIAP — entregam plataforma")

el(f_motivation, "Driver", "Churn pós-garantia", "Retenção despenca de 82% para 20-40% ao término da garantia (Cox Automotive 2025)")
el(f_motivation, "Driver", "VIN Share baixo",   "Apenas ~3,5-5% da frota Ford usa a rede oficial — 95% vai para independentes")
el(f_motivation, "Driver", "3,4M Recalls pendentes", "Taxa de atendimento de recalls no Brasil: ~40%. Novo CTB bloqueia licenciamento")
el(f_motivation, "Driver", "Frota descontinuada", "80% da frota são Ka/Fiesta/EcoSport — sem app, sem lembrete oficial")

el(f_motivation, "Goal", "Aumentar VIN Share",      "Meta: VIN Share ≥ 8% em 24 meses (base: ~3,5-5%)")
el(f_motivation, "Goal", "Reduzir churn pós-venda", "Aumentar taxa de retorno pós-1ª revisão de 71% para ≥ 80%")
el(f_motivation, "Goal", "ROI mensurável",          "Cada ação rastreada do disparo ao resultado financeiro em R$")
el(f_motivation, "Goal", "Escalar cobertura",       "Alcançar clientes de modelos descontinuados via Fluxo Simplificado")

el(f_motivation, "Requirement", "REQ-01: Latência API p95 < 300ms",     "Performance: endpoint p95 abaixo de 300ms")
el(f_motivation, "Requirement", "REQ-02: Disponibilidade ≥ 99%",        "SLA: no máximo 7h15 de downtime por ano")
el(f_motivation, "Requirement", "REQ-03: AUC classificador ≥ 0,82",     "ML: XGBoost com target engenheirado — dias_sem_revisão > 365")
el(f_motivation, "Requirement", "REQ-04: Falsos positivos churn < 10%", "Qualidade do modelo de segmentação K-means")
el(f_motivation, "Requirement", "REQ-05: LGPD — dados pseudonimizados", "VIN_Hash SHA1 + salt. Sem PII reversível no pipeline ML")
el(f_motivation, "Requirement", "REQ-06: Onboarding atendente < 15 min","UX: atendente operacional sem treinamento longo")
el(f_motivation, "Requirement", "REQ-07: Entrega WhatsApp < 30s",        "n8n + Meta Business API: confirmação em 30 segundos")

el(f_motivation, "Principle", "SOA — Portão Único",         "Tudo passa pelo forward-api-java. Mobile/Web não falam direto com banco ou ML")
el(f_motivation, "Principle", "Flywheel de Dados",           "Cada ciclo de ação gera dado que melhora o modelo. Precisão cresce com uso")
el(f_motivation, "Principle", "Proatividade sobre reatividade","A plataforma age antes do cliente sair — não espera ele sumir")

# Motivation Relations
rel(f_relations, "Association",   "Ford Brasil (Diretoria)", "Aumentar VIN Share")
rel(f_relations, "Association",   "Concessionária (Dealer)", "Reduzir churn pós-venda")
rel(f_relations, "Association",   "Cliente Ford",            "Escalar cobertura")
rel(f_relations, "Influence",     "Churn pós-garantia",      "Aumentar VIN Share",      "impulsiona")
rel(f_relations, "Influence",     "VIN Share baixo",         "ROI mensurável",           "necessita")
rel(f_relations, "Realization",   "REQ-01: Latência API p95 < 300ms", "ROI mensurável")
rel(f_relations, "Realization",   "REQ-03: AUC classificador ≥ 0,82", "Reduzir churn pós-venda")
rel(f_relations, "Realization",   "REQ-05: LGPD — dados pseudonimizados", "Escalar cobertura")

# ══════════════════════════════════════════════════════════════════════════════
# BUSINESS ELEMENTS
# ══════════════════════════════════════════════════════════════════════════════
el(f_business, "BusinessActor",   "Atendente",           "Func. da concessionária — usa app mobile Modo Ford")
el(f_business, "BusinessActor",   "Gerente de Serviço",  "Gerencia leads e NPS do dealer")
el(f_business, "BusinessActor",   "Diretor Regional",    "Usa dashboard web para visão macro")
el(f_business, "BusinessActor",   "Cliente Ativo",       "Dono de Ford que ainda usa a rede")
el(f_business, "BusinessActor",   "Cliente Churned",     "Dono de Ford que parou de usar a rede")

el(f_business, "BusinessRole",    "Gestor de Retenção",  "Responsável por campanhas de reativação")
el(f_business, "BusinessRole",    "Analista ML",         "Opera e retreina os modelos de segmentação/classificação")

el(f_business, "BusinessProcess", "Processo AS-IS: Pós-Venda Ford", "Processo atual: sem proatividade, sem segmentação, sem ROI rastreável")
el(f_business, "BusinessProcess", "Segmentar Clientes",  "K-means cego sobre 175k VINs — 4 perfis: Fiel/Econômico/Esquecido/Abandono")
el(f_business, "BusinessProcess", "Priorizar Leads",     "Pulse Leads: ordenar por risco × LSV — lista diária para o atendente")
el(f_business, "BusinessProcess", "Disparar Ação",       "CommEngine: WhatsApp personalizado via n8n no momento crítico")
el(f_business, "BusinessProcess", "Medir ROI",           "Closed-Loop ROI: rastrear ação → resposta → agendamento → receita em R$")
el(f_business, "BusinessProcess", "Recall como Porta",   "Recall Gateway: transformar recall pendente em oportunidade de reconexão")
el(f_business, "BusinessProcess", "Agendamento Digital", "Cliente agenda pelo app ou WhatsApp em 1 toque")

el(f_business, "BusinessService", "Serviço de Scoring",  "API que devolve segmento + score de churn + ação sugerida por VIN")
el(f_business, "BusinessService", "Serviço de Leads",    "API que devolve lista priorizada para o dealer do dia")
el(f_business, "BusinessService", "Serviço de Notificação", "Dispara WhatsApp/push/email via n8n")
el(f_business, "BusinessService", "Serviço de Agendamento","Registra e confirma revisão no banco")

el(f_business, "BusinessObject",  "VIN (Vehicle ID)",       "Número de chassi pseudonimizado — unidade de análise central do sistema")
el(f_business, "BusinessObject",  "Score de Churn",         "Probabilidade 0-100 de abandono de um VIN. Atualizado 1×/dia.")
el(f_business, "BusinessObject",  "Perfil de Segmento",     "Fiel | Econômico | Esquecido | Abandono — saída do K-means")
el(f_business, "BusinessObject",  "Ação Recomendada",       "O que fazer com o cliente: whatsapp | ligação | email | deixar quieto")
el(f_business, "BusinessObject",  "IHC — Saúde do Dealer",  "Score 0-100 da concessionária (VIN Share 25% + Conversão 20% + NPS 15% + outros)")

# Business Relations
rel(f_relations, "Assignment",    "Atendente",              "Priorizar Leads")
rel(f_relations, "Assignment",    "Gerente de Serviço",     "Medir ROI")
rel(f_relations, "Assignment",    "Diretor Regional",       "IHC — Saúde do Dealer")
rel(f_relations, "Triggering",    "Segmentar Clientes",     "Priorizar Leads")
rel(f_relations, "Triggering",    "Priorizar Leads",        "Disparar Ação")
rel(f_relations, "Triggering",    "Disparar Ação",          "Medir ROI")
rel(f_relations, "Triggering",    "Medir ROI",              "Segmentar Clientes", "feedback loop (Flywheel)")
rel(f_relations, "Serving",       "Serviço de Scoring",     "Priorizar Leads")
rel(f_relations, "Serving",       "Serviço de Leads",       "Priorizar Leads")
rel(f_relations, "Association",   "VIN (Vehicle ID)",       "Score de Churn")
rel(f_relations, "Association",   "VIN (Vehicle ID)",       "Perfil de Segmento")
rel(f_relations, "Association",   "Score de Churn",         "Ação Recomendada")

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION ELEMENTS
# ══════════════════════════════════════════════════════════════════════════════
el(f_application, "ApplicationComponent", "forward-api-java",
   "Backend core — Java 17 + Spring Boot 3.2. Portão único: REST + SOAP. JWT/RBAC. Flyway. SpringDoc OpenAPI.")
el(f_application, "ApplicationComponent", "forward-ml",
   "Serviço de ML — Python. K-means (segmentador) + XGBoost (classificador) + Kaplan-Meier (survival). Roda 1×/dia via cron.")
el(f_application, "ApplicationComponent", "forward-mobile",
   "App React Native/Expo. Dual-mode: Modo Ford (atendente) + Modo Cliente. 3 telas Sprint 1.")
el(f_application, "ApplicationComponent", "forward-web",
   "Dashboard SvelteKit. Cockpit Ford corporativo. Read-only. Chart.js/visx. Consome só forward-api-java.")
el(f_application, "ApplicationComponent", "n8n (Action Engine)",
   "Orquestrador low-code self-hosted. Inbound: webhook WhatsApp → Java. Outbound: Java → WhatsApp template.")
el(f_application, "ApplicationComponent", "Supabase / PostgreSQL",
   "Banco gerenciado. Fonte da verdade. Só forward-api-java e segmentador batch escrevem.")

el(f_application, "ApplicationInterface",  "REST API (OpenAPI)",    "Endpoints públicos: /clients, /leads, /scores, /classify, /analytics")
el(f_application, "ApplicationInterface",  "SOAP / WSDL",           "Operação GetVehicle — requisito SOA (Prof. Salatiel). WSDL exposto.")
el(f_application, "ApplicationInterface",  "WebSocket Push",         "Notificações em tempo real para o app mobile (push notifications)")
el(f_application, "ApplicationInterface",  "WhatsApp Business API",  "Integração Meta — templates aprovados, 97% abertura, ROI 300:1")

el(f_application, "ApplicationService",   "Scoring Service",        "Calcula segmento + score + ação sugerida via ML")
el(f_application, "ApplicationService",   "Lead Prioritization",    "Gera lista diária Pulse Leads por dealer")
el(f_application, "ApplicationService",   "Notification Service",   "Orquestra envio via n8n (WhatsApp/email/push)")
el(f_application, "ApplicationService",   "Analytics Service",      "Agrega KPIs para dashboard web (IHC, VIN Share, Curva da Morte)")
el(f_application, "ApplicationService",   "Auth/RBAC Service",      "JWT HS256 + roles: attendant/manager/dealer_owner/ford_regional/ford_admin")
el(f_application, "ApplicationService",   "Audit Trail Service",    "Registra acesso e ações em audit_log (LGPD)")

el(f_application, "DataObject", "vin_features.csv",  "175k VINs × 20+ features comportamentais — input pro ML")
el(f_application, "DataObject", "client_segments",   "Tabela: etiqueta + segmento por VIN. Atualizada 1×/dia pelo segmentador")
el(f_application, "DataObject", "client_scores",     "Tabela: score 0-100 + probabilidades por VIN + versão do modelo")
el(f_application, "DataObject", "recommended_actions","Tabela: ação sugerida, motivo, template, status (pending/dispatched/done)")
el(f_application, "DataObject", "audit_log",         "Trilha completa: quem acessou o quê, quando, antes/depois (LGPD)")

# Application Relations
rel(f_relations, "Serving",       "forward-api-java",        "forward-mobile",         "REST")
rel(f_relations, "Serving",       "forward-api-java",        "forward-web",            "REST")
rel(f_relations, "Serving",       "forward-api-java",        "n8n (Action Engine)",    "REST (ordens)")
rel(f_relations, "Serving",       "n8n (Action Engine)",     "forward-api-java",       "webhook events")
rel(f_relations, "Serving",       "forward-api-java",        "forward-ml",             "HTTP interno")
rel(f_relations, "Access",        "forward-ml",              "vin_features.csv",       "lê")
rel(f_relations, "Access",        "forward-ml",              "client_segments",        "escreve 1×/dia")
rel(f_relations, "Access",        "forward-api-java",        "client_scores",          "lê/escreve")
rel(f_relations, "Access",        "forward-api-java",        "recommended_actions",    "lê/escreve")
rel(f_relations, "Access",        "forward-api-java",        "audit_log",              "escreve sempre")
rel(f_relations, "Realization",   "forward-api-java",        "REST API (OpenAPI)")
rel(f_relations, "Realization",   "forward-api-java",        "SOAP / WSDL")
rel(f_relations, "Composition",   "forward-api-java",        "Auth/RBAC Service")
rel(f_relations, "Composition",   "forward-api-java",        "Audit Trail Service")
rel(f_relations, "Composition",   "forward-api-java",        "Scoring Service")
rel(f_relations, "Composition",   "forward-api-java",        "Lead Prioritization")
rel(f_relations, "Composition",   "forward-api-java",        "Notification Service")
rel(f_relations, "Composition",   "forward-api-java",        "Analytics Service")

# ══════════════════════════════════════════════════════════════════════════════
# TECHNOLOGY ELEMENTS
# ══════════════════════════════════════════════════════════════════════════════
el(f_technology, "Node",          "Azure VM (B-series)",  "Standard_B1s ou B2s — hospeda Java + n8n + ML Python via Docker")
el(f_technology, "Node",          "Supabase Cloud / Neon","Banco PostgreSQL 16 gerenciado — free/pro tier")
el(f_technology, "Node",          "Vercel / Netlify",     "Hospedagem estática do forward-web (free tier)")

el(f_technology, "SystemSoftware","Docker Engine",        "Containeriza forward-api-java + n8n + ML script na Azure VM")
el(f_technology, "SystemSoftware","PostgreSQL 16",        "Banco relacional — fonte da verdade de todo o sistema")
el(f_technology, "SystemSoftware","JVM (Java 17)",        "Runtime do Spring Boot 3.2 — HikariCP, Flyway, SpringDoc")
el(f_technology, "SystemSoftware","Python 3.11",          "Runtime ML — scikit-learn, pandas, lifelines, matplotlib")
el(f_technology, "SystemSoftware","n8n (Docker)",         "Orquestrador de workflows low-code — self-hosted na VM")

el(f_technology, "TechnologyInterface", "HTTPS / TLS 1.2+", "Toda comunicação externa criptografada. HTTPS forçado.")
el(f_technology, "TechnologyInterface", "WhatsApp Business API (Meta)", "Entrega de mensagens para clientes — 97% abertura no BR")
el(f_technology, "TechnologyInterface", "Expo Push API",    "Notificações push para app mobile via Expo")
el(f_technology, "TechnologyInterface", "GitHub Actions CI","Pipeline de build + teste automático a cada PR")

el(f_technology, "CommunicationNetwork", "Azure VNet",    "Rede privada que isola VM + banco + n8n internamente")
el(f_technology, "CommunicationNetwork", "Internet / CDN","Tráfego externo — mobile, web, WhatsApp webhook")

el(f_technology, "Artifact", "forward-api-java.jar",     "Build artefato Spring Boot — deployado via Docker na VM")
el(f_technology, "Artifact", "forward-mobile.apk/.ipa",  "Bundle Expo — publicado via EAS Build (30 builds/mês free)")
el(f_technology, "Artifact", "forward-web (static)",     "Build SvelteKit — deployado no Vercel/Netlify")
el(f_technology, "Artifact", "ML models (pickle/joblib)","Modelos treinados persistidos no filesystem da VM")
el(f_technology, "Artifact", "Flyway migrations",        "Versionamento do schema PostgreSQL — entrega obrigatória SOA")

# Technology Relations
rel(f_relations, "Serving",       "Azure VM (B-series)",   "forward-api-java")
rel(f_relations, "Serving",       "Azure VM (B-series)",   "n8n (Action Engine)")
rel(f_relations, "Serving",       "Azure VM (B-series)",   "forward-ml")
rel(f_relations, "Serving",       "Supabase Cloud / Neon", "PostgreSQL 16")
rel(f_relations, "Composition",   "Docker Engine",         "forward-api-java.jar")
rel(f_relations, "Composition",   "Docker Engine",         "n8n (Docker)")
rel(f_relations, "Association",   "Azure VNet",            "Azure VM (B-series)")
rel(f_relations, "Association",   "Azure VNet",            "Supabase Cloud / Neon")
rel(f_relations, "Realization",   "forward-api-java.jar",  "forward-api-java")
rel(f_relations, "Realization",   "forward-mobile.apk/.ipa","forward-mobile")
rel(f_relations, "Realization",   "ML models (pickle/joblib)","forward-ml")
rel(f_relations, "Realization",   "Flyway migrations",     "PostgreSQL 16")
rel(f_relations, "Association",   "HTTPS / TLS 1.2+",      "REST API (OpenAPI)")
rel(f_relations, "Association",   "HTTPS / TLS 1.2+",      "SOAP / WSDL")

# ══════════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION ELEMENTS (Monitoring View extras)
# ══════════════════════════════════════════════════════════════════════════════
el(f_impl, "WorkPackage", "Sprint 1 — Entrega 24/05/2026", "ML + Java + Mobile + Web + n8n + Infra + QA")
el(f_impl, "Deliverable", "PITCH.pptx",         "QA-1: Apresentação 15 slides")
el(f_impl, "Deliverable", "CANVAS.pdf",         "QA-2: Business Model Canvas")
el(f_impl, "Deliverable", "QUADRO_DE_VALOR.pdf","QA-3: Quadro de Valor com métricas negócio + qualidade")
el(f_impl, "Deliverable", "ForwardService.archimate","QA-4: Arquitetura TOGAF/Archi")
el(f_impl, "Deliverable", "VIDEO_PITCH.mp4",    "QA-5: Vídeo ≤3min com 4 integrantes")

# ══════════════════════════════════════════════════════════════════════════════
# OTHER (Monitoring)
# ══════════════════════════════════════════════════════════════════════════════
el(f_other, "Assessment", "Grafana Dashboard",        "Monitor de latência, throughput, erros da API Java + n8n")
el(f_other, "Assessment", "Alert: API p95 > 300ms",   "Alerta quando latência ultrapassa SLA — dispara para equipe")
el(f_other, "Assessment", "Alert: Disponibilidade <99%","Alerta de downtime — SLA: no máximo 7h15/ano")
el(f_other, "Assessment", "audit_log viewer",         "Interface interna para revisar trilha de auditoria LGPD")
el(f_other, "Assessment", "ML Model Monitor",         "Monitora AUC, drift de dados, qualidade do segmentador mensalmente")
el(f_other, "Assessment", "Cron segmentador 02h",     "Job Linux que roda run_segmenter.py 1×/dia e escreve em client_segments")

# ══════════════════════════════════════════════════════════════════════════════
# VIEWS / DIAGRAMS
# ══════════════════════════════════════════════════════════════════════════════

def view(parent, name, viewpoint=""):
    v = SubElement(parent, "element", {
        "xsi:type": "archimate:ArchimateDiagramModel",
        "name": name,
        "id": uid(),
    })
    if viewpoint:
        v.set("viewpoint", viewpoint)
    return v

def child(parent, elem_name, x, y, w=120, h=55):
    eid = elements.get(elem_name)
    if not eid:
        return None
    c = SubElement(parent, "child", {
        "xsi:type": "archimate:DiagramObject",
        "id": uid(),
        "archimateElement": eid,
    })
    b = SubElement(c, "bounds", {"x": str(x), "y": str(y), "width": str(w), "height": str(h)})
    return c

# View 1: Motivation
v1 = view(f_views, "1. Motivation View — Drivers, Goals, Requirements", "motivation")
child(v1, "Ford Brasil (Diretoria)",       12, 12, 130, 55)
child(v1, "Concessionária (Dealer)",       12, 80, 130, 55)
child(v1, "Cliente Ford",                  12,148, 130, 55)
child(v1, "Churn pós-garantia",           160, 12, 130, 55)
child(v1, "VIN Share baixo",              160, 80, 130, 55)
child(v1, "3,4M Recalls pendentes",       160,148, 130, 55)
child(v1, "Frota descontinuada",          160,216, 130, 55)
child(v1, "Aumentar VIN Share",           310, 12, 130, 55)
child(v1, "Reduzir churn pós-venda",      310, 80, 130, 55)
child(v1, "ROI mensurável",               310,148, 130, 55)
child(v1, "Escalar cobertura",            310,216, 130, 55)
child(v1, "REQ-01: Latência API p95 < 300ms", 460, 12, 160, 55)
child(v1, "REQ-02: Disponibilidade ≥ 99%",    460, 80, 160, 55)
child(v1, "REQ-03: AUC classificador ≥ 0,82", 460,148, 160, 55)
child(v1, "REQ-04: Falsos positivos churn < 10%",460,216, 160, 55)
child(v1, "REQ-05: LGPD — dados pseudonimizados",460,284, 160, 55)
child(v1, "SOA — Portão Único",           640, 12, 130, 55)
child(v1, "Flywheel de Dados",            640, 80, 130, 55)
child(v1, "Proatividade sobre reatividade",640,148, 130, 55)

# View 2: Business
v2 = view(f_views, "2. Business View — AS-IS × TO-BE")
child(v2, "Processo AS-IS: Pós-Venda Ford", 12, 12, 160, 70)
child(v2, "Segmentar Clientes",            200, 12, 130, 55)
child(v2, "Priorizar Leads",               350, 12, 130, 55)
child(v2, "Disparar Ação",                 500, 12, 130, 55)
child(v2, "Medir ROI",                     650, 12, 130, 55)
child(v2, "Recall como Porta",             800, 12, 130, 55)
child(v2, "Atendente",                     200,100, 100, 55)
child(v2, "Gerente de Serviço",            350,100, 100, 55)
child(v2, "Diretor Regional",              500,100, 100, 55)
child(v2, "VIN (Vehicle ID)",              200,180, 120, 55)
child(v2, "Score de Churn",                350,180, 120, 55)
child(v2, "Perfil de Segmento",            500,180, 120, 55)
child(v2, "Ação Recomendada",             650,180, 120, 55)
child(v2, "IHC — Saúde do Dealer",         800,180, 140, 55)
child(v2, "Serviço de Scoring",            200,260, 130, 55)
child(v2, "Serviço de Leads",              350,260, 130, 55)
child(v2, "Serviço de Notificação",        500,260, 130, 55)
child(v2, "Serviço de Agendamento",        650,260, 130, 55)

# View 3: Application
v3 = view(f_views, "3. Application View — Componentes de Software", "layered")
child(v3, "forward-mobile",               12,  12, 140, 70)
child(v3, "forward-web",                  170, 12, 140, 70)
child(v3, "n8n (Action Engine)",          328, 12, 140, 70)
child(v3, "forward-api-java",             12, 120, 300, 70)
child(v3, "forward-ml",                   328,120, 140, 70)
child(v3, "Supabase / PostgreSQL",        12, 220, 460, 70)
child(v3, "REST API (OpenAPI)",           12, 310, 140, 55)
child(v3, "SOAP / WSDL",                  170,310, 140, 55)
child(v3, "WhatsApp Business API",        328,310, 140, 55)
child(v3, "Auth/RBAC Service",            12, 380, 140, 55)
child(v3, "Audit Trail Service",          170,380, 140, 55)
child(v3, "Scoring Service",              328,380, 140, 55)
child(v3, "client_segments",              12, 460, 130, 55)
child(v3, "client_scores",                160,460, 130, 55)
child(v3, "recommended_actions",          308,460, 160, 55)
child(v3, "audit_log",                    486,460, 130, 55)

# View 4: Technology
v4 = view(f_views, "4. Technology View — Infra Azure, Docker, Postgres", "layered")
child(v4, "Azure VM (B-series)",          12,  12, 200, 90)
child(v4, "Supabase Cloud / Neon",        230, 12, 200, 90)
child(v4, "Vercel / Netlify",             448, 12, 180, 90)
child(v4, "Docker Engine",               12, 120, 200, 55)
child(v4, "PostgreSQL 16",               230,120, 200, 55)
child(v4, "JVM (Java 17)",               12, 190, 200, 55)
child(v4, "Python 3.11",                 230,190, 200, 55)
child(v4, "n8n (Docker)",                448,190, 180, 55)
child(v4, "HTTPS / TLS 1.2+",            12, 270, 200, 55)
child(v4, "WhatsApp Business API (Meta)",230,270, 220, 55)
child(v4, "GitHub Actions CI",           470,270, 160, 55)
child(v4, "Azure VNet",                  12, 350, 220, 55)
child(v4, "forward-api-java.jar",        12, 430, 160, 55)
child(v4, "Flyway migrations",           190,430, 160, 55)
child(v4, "ML models (pickle/joblib)",   368,430, 160, 55)
child(v4, "forward-mobile.apk/.ipa",    546,430, 170, 55)

# View 5: Requirements (Quality)
v5 = view(f_views, "5. Requirements View — Requisitos de Qualidade", "requirements_realization")
child(v5, "REQ-01: Latência API p95 < 300ms",   12,  12, 200, 55)
child(v5, "REQ-02: Disponibilidade ≥ 99%",       12,  80, 200, 55)
child(v5, "REQ-03: AUC classificador ≥ 0,82",    12, 148, 200, 55)
child(v5, "REQ-04: Falsos positivos churn < 10%",12, 216, 200, 55)
child(v5, "REQ-05: LGPD — dados pseudonimizados",12, 284, 200, 55)
child(v5, "REQ-06: Onboarding atendente < 15 min",12,352, 200, 55)
child(v5, "REQ-07: Entrega WhatsApp < 30s",      12, 420, 200, 55)
child(v5, "forward-api-java",                    240, 12, 160, 55)
child(v5, "forward-ml",                          240, 80, 160, 55)
child(v5, "Supabase / PostgreSQL",               240,148, 160, 55)
child(v5, "forward-mobile",                      240,216, 160, 55)
child(v5, "n8n (Action Engine)",                 240,284, 160, 55)
child(v5, "Auth/RBAC Service",                   240,352, 160, 55)
child(v5, "Audit Trail Service",                 240,420, 160, 55)
child(v5, "SOA — Portão Único",                  440, 12, 160, 55)
child(v5, "Flywheel de Dados",                   440, 80, 160, 55)
child(v5, "Proatividade sobre reatividade",      440,148, 160, 55)

# View 6: Monitoring
v6 = view(f_views, "6. Monitoring View — Observabilidade e Alertas")
child(v6, "Grafana Dashboard",              12,  12, 160, 55)
child(v6, "Alert: API p95 > 300ms",         12,  80, 160, 55)
child(v6, "Alert: Disponibilidade <99%",    12, 148, 160, 55)
child(v6, "audit_log viewer",               12, 216, 160, 55)
child(v6, "ML Model Monitor",               12, 284, 160, 55)
child(v6, "Cron segmentador 02h",           12, 352, 160, 55)
child(v6, "forward-api-java",               200, 12, 160, 55)
child(v6, "forward-ml",                     200, 80, 160, 55)
child(v6, "audit_log",                      200,148, 160, 55)
child(v6, "client_segments",                200,216, 160, 55)
child(v6, "Azure VM (B-series)",            380, 12, 160, 55)
child(v6, "Docker Engine",                  380, 80, 160, 55)
child(v6, "GitHub Actions CI",              380,148, 160, 55)

# ── Write file ─────────────────────────────────────────────────────────────────
out = r"C:\Users\USER\Desktop\espm\forward-docs\academic\togaf\ForwardService.archimate"
xml_str = pretty(model)
# Fix namespace prefix issue
xml_str = xml_str.replace('ns0:', 'archimate:').replace(':ns0=', ':archimate=')
xml_str = xml_str.replace("<?xml version=\"1.0\" ?>", '<?xml version="1.0" encoding="UTF-8"?>')

with open(out, "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"ForwardService.archimate salvo em {out}")
print(f"Elementos criados: {len(elements)}")
print("Views:")
for v in [v1, v2, v3, v4, v5, v6]:
    print(f"  {v.get('name')}")
