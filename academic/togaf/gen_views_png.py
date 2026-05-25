"""
Gera 6 PNGs representando as views TOGAF do ForwardService.
Usa Pillow — visual limpo com boxes coloridos e texto.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\Users\USER\Desktop\espm\forward-docs\academic\togaf\views"
os.makedirs(OUT, exist_ok=True)

# ── Cores ──────────────────────────────────────────────────────────────────────
FORD_DARK   = (0,   39,  74)
FORD_BLUE   = (30,  86, 160)
FORD_ORANGE = (249, 99,   2)
WHITE       = (255, 255, 255)
LIGHT_GRAY  = (240, 244, 248)
GRAY        = (100, 116, 135)
GREEN       = (39, 103, 73)
PURPLE      = (106, 70, 160)
TEAL        = (13, 110, 130)

W, H = 1600, 1000

def new_img():
    img = Image.new("RGB", (W, H), LIGHT_GRAY)
    d = ImageDraw.Draw(img)
    return img, d

def try_font(size):
    for name in ["arial.ttf", "calibri.ttf", "DejaVuSans.ttf", "FreeSans.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except:
            pass
    return ImageFont.load_default()

def header(d, title, subtitle, bg=FORD_DARK):
    d.rectangle([0, 0, W, 90], fill=bg)
    d.rectangle([0, 90, W, 96], fill=FORD_ORANGE)
    d.text((20, 14), title, fill=WHITE, font=try_font(30))
    d.text((20, 55), subtitle, fill=(200, 210, 220), font=try_font(17))

def box(d, x, y, w, h, bg, text_lines, title_color=WHITE, body_color=WHITE, accent=FORD_ORANGE):
    d.rectangle([x, y, x+w, y+h], fill=bg)
    d.rectangle([x, y, x+w, y+5], fill=accent)
    font_t = try_font(14)
    font_b = try_font(12)
    cy = y + 12
    for i, line in enumerate(text_lines):
        clr = title_color if i == 0 else body_color
        fnt = font_t if i == 0 else font_b
        d.text((x + 8, cy), line, fill=clr, font=fnt)
        cy += 18 if i == 0 else 15

def arrow(d, x1, y1, x2, y2, color=FORD_ORANGE, width=2):
    d.line([x1, y1, x2, y2], fill=color, width=width)
    # arrowhead
    import math
    angle = math.atan2(y2-y1, x2-x1)
    size = 10
    d.polygon([
        (x2, y2),
        (int(x2 - size*math.cos(angle - 0.5)), int(y2 - size*math.sin(angle - 0.5))),
        (int(x2 - size*math.cos(angle + 0.5)), int(y2 - size*math.sin(angle + 0.5))),
    ], fill=color)

def footer(d, text):
    d.rectangle([0, H-40, W, H], fill=FORD_DARK)
    d.text((20, H-26), text, fill=(180,190,200), font=try_font(13))

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — Motivation
# ══════════════════════════════════════════════════════════════════════════════
img, d = new_img()
header(d, "1. Motivation View — Drivers, Goals, Requirements",
          "ArchiMate 3.1 · ForwardService · Ford Challenge FIAP 2026")

# Stakeholders
for i, (name,) in enumerate([
    ("Ford Brasil (Diretoria)",),
    ("Concessionária (Dealer)",),
    ("Cliente Ford",),
    ("Gestor Regional Ford",),
]):
    box(d, 20, 110+i*95, 240, 80, FORD_DARK,
        ["Stakeholder", name], accent=FORD_ORANGE)

# Drivers
for i, (name,) in enumerate([
    ("Churn pós-garantia",),
    ("VIN Share ~4%",),
    ("3,4M Recalls pendentes",),
    ("Frota 80% descontinuada",),
]):
    box(d, 280, 110+i*95, 240, 80, TEAL,
        ["Driver", name], accent=(100,200,200))
    arrow(d, 260, 150+i*95, 280, 150+i*95)

# Goals
goals = [
    "Aumentar VIN Share ≥ 8%",
    "Reduzir churn pós-venda",
    "ROI mensurável (Closed-Loop)",
    "Escalar cobertura (Fluxo Simpl.)",
]
for i, g in enumerate(goals):
    box(d, 540, 110+i*95, 260, 80, GREEN,
        ["Goal", g], accent=(100,220,150))
    arrow(d, 520, 150+i*95, 540, 150+i*95)

# Requirements
reqs = [
    "REQ-01: Latência API p95 < 300ms",
    "REQ-02: Disponibilidade ≥ 99%",
    "REQ-03: AUC classificador ≥ 0,82",
    "REQ-04: Falsos positivos < 10%",
    "REQ-05: LGPD — pseudonimizado",
    "REQ-06: Onboarding < 15 min",
    "REQ-07: WhatsApp entrega < 30s",
]
for i, r in enumerate(reqs):
    box(d, 820, 110+i*125, 360, 108, FORD_BLUE,
        ["Requirement", r], accent=FORD_ORANGE)

# Principles
for i, p in enumerate(["SOA — Portão Único", "Flywheel de Dados", "Proatividade sobre reatividade"]):
    box(d, 1200, 110+i*145, 370, 120, PURPLE,
        ["Principle", p], accent=(200,150,255))

footer(d, "ForwardService.archimate · View 1: Motivation · ArchiMate 3.1 · QA-4 · Sprint 1 · 2026")
img.save(os.path.join(OUT, "01_motivation_view.png"))
print("✓ 01_motivation_view.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — Business View
# ══════════════════════════════════════════════════════════════════════════════
img, d = new_img()
header(d, "2. Business View — AS-IS × TO-BE",
          "Processo pós-venda atual vs ForwardService")

# AS-IS box
d.rectangle([20, 110, 380, 360], fill=(60,20,20))
d.text((30, 120), "AS-IS: Pós-Venda Ford (sem plataforma)", fill=(255,150,150), font=try_font(16))
for i, txt in enumerate([
    "• Cliente some após garantia — sem aviso",
    "• Dealer age de forma reativa, sem dados",
    "• Sem segmentação — todos tratados igual",
    "• Sem ROI medido por campanha",
    "• 96% da frota vai para independentes",
]):
    d.text((35, 148+i*32), txt, fill=(255,200,200), font=try_font(14))

# Actors
actors = ["Atendente", "Gerente de Serviço", "Diretor Regional", "Cliente Ativo", "Gestor de Retenção"]
for i, a in enumerate(actors):
    box(d, 20, 380+i*100, 180, 85, FORD_DARK, ["BusinessActor", a])

# TO-BE processes
procs = [
    ("Segmentar Clientes", "K-means 4 perfis diário"),
    ("Priorizar Leads", "Pulse Leads: risco × LSV"),
    ("Disparar Ação", "n8n + WhatsApp personalizado"),
    ("Medir ROI", "Closed-Loop ROI em R$"),
    ("Recall como Porta", "3,4M pendentes → oportunidade"),
    ("Agendamento Digital", "App ou WhatsApp — 1 toque"),
]
for i, (name, desc) in enumerate(procs):
    bx = 420 + (i % 3) * 370
    by = 110 + (i // 3) * 230
    box(d, bx, by, 340, 200, FORD_BLUE, ["BusinessProcess", name, desc], accent=FORD_ORANGE)
    if i < len(procs)-1 and i % 3 < 2:
        arrow(d, bx+340, by+100, bx+370, by+100)

# Business objects
objs = ["VIN (Vehicle ID)", "Score de Churn", "Perfil de Segmento", "Ação Recomendada", "IHC — Saúde do Dealer"]
for i, o in enumerate(objs):
    box(d, 420 + i*225, 600, 200, 80, TEAL, ["BusinessObject", o], accent=(100,200,200))

# Services
srvs = ["Serviço de Scoring", "Serviço de Leads", "Serviço de Notificação", "Serviço de Agendamento"]
for i, s in enumerate(srvs):
    box(d, 420 + i*285, 710, 260, 80, GREEN, ["BusinessService", s], accent=(100,220,150))

footer(d, "ForwardService.archimate · View 2: Business · ArchiMate 3.1 · QA-4 · Sprint 1 · 2026")
img.save(os.path.join(OUT, "02_business_view.png"))
print("✓ 02_business_view.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 3 — Application View
# ══════════════════════════════════════════════════════════════════════════════
img, d = new_img()
header(d, "3. Application View — Componentes de Software",
          "SOA: tudo passa pelo forward-api-java (portão único)")

# Camadas horizontais
layers = [
    ("Experience Layer", 110, TEAL),
    ("Performance Console", 110, TEAL),
    ("Action Engine", 110, TEAL),
    ("", 0, None),
    ("Backend Core (Portão Único)", 300, FORD_DARK),
    ("Intelligence Hub", 300, GREEN),
    ("", 0, None),
    ("Data Layer", 500, PURPLE),
]

# Components
comps = [
    ("forward-mobile\n(React Native/Expo)", 20, 110, 340, 160, TEAL),
    ("forward-web\n(SvelteKit)", 380, 110, 280, 160, TEAL),
    ("n8n (Action Engine)\n(Docker self-hosted)", 680, 110, 280, 160, TEAL),
]
for name, x, y, w, h, bg in comps:
    lines = name.split("\n")
    box(d, x, y, w, h, bg, ["ApplicationComponent"] + lines, accent=FORD_ORANGE)

# API Java (big center)
d.rectangle([20, 300, 1580, 480], fill=FORD_DARK)
d.rectangle([20, 300, 1580, 306], fill=FORD_ORANGE)
d.text((30, 312), "ApplicationComponent: forward-api-java — Java 17 + Spring Boot 3.2 (PORTÃO ÚNICO)", fill=WHITE, font=try_font(17))
interfaces = ["REST API (OpenAPI/Swagger)", "SOAP / WSDL (GetVehicle)", "Auth/RBAC (JWT HS256)", "Audit Trail", "Scoring Service", "Lead Prioritization", "Notification Service", "Analytics Service"]
for i, iface in enumerate(interfaces):
    bx = 30 + i * 195
    box(d, bx, 340, 180, 120, FORD_BLUE, ["«interface»", iface], accent=(100,150,255))

# ML
box(d, 980, 110, 280, 160, GREEN,
    ["ApplicationComponent", "forward-ml", "(Python · scikit-learn)"], accent=(100,220,150))

# Arrows (mobile/web/n8n → api)
for cx in [190, 520, 820]:
    arrow(d, cx, 270, cx, 300)

# DB
d.rectangle([20, 510, 1580, 640], fill=PURPLE)
d.rectangle([20, 510, 1580, 516], fill=FORD_ORANGE)
d.text((30, 522), "DataObject Layer: Supabase / PostgreSQL 16", fill=WHITE, font=try_font(17))
tables = ["vin_features.csv", "client_segments", "client_scores", "recommended_actions", "executed_actions", "conversations", "audit_log"]
for i, t in enumerate(tables):
    box(d, 30 + i*220, 548, 200, 75, (80,40,120), ["«table»", t], accent=FORD_ORANGE)

# Arrow api → db
arrow(d, 800, 480, 800, 510)
# Arrow api → ml
arrow(d, 1100, 480, 1100, 270)

footer(d, "ForwardService.archimate · View 3: Application · ArchiMate 3.1 · QA-4 · Sprint 1 · 2026")
img.save(os.path.join(OUT, "03_application_view.png"))
print("✓ 03_application_view.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 4 — Technology View
# ══════════════════════════════════════════════════════════════════════════════
img, d = new_img()
header(d, "4. Technology View — Infraestrutura Azure, Docker, Postgres",
          "Azure VM + Supabase/Neon + Vercel · Custo estimado Sprint 1: $15–35/mês")

# Azure boundary
d.rectangle([20, 110, 960, 900], fill=(10,30,60))
d.rectangle([20, 110, 960, 116], fill=FORD_ORANGE)
d.text((30, 120), "☁  Azure Cloud — VM Standard_B1s ou B2s", fill=WHITE, font=try_font(18))

# Docker
d.rectangle([40, 155, 940, 880], fill=(15,50,90))
d.text((50, 163), "🐳  Docker Engine", fill=(100,200,255), font=try_font(16))

# Containers
containers = [
    ("forward-api-java\n(Java 17 / Spring Boot 3.2)\nREST + SOAP · JWT · Flyway", 60, 200, 400, 250, FORD_DARK),
    ("n8n (Action Engine)\n(Node.js self-hosted)\nWhatsApp workflows", 480, 200, 380, 250, TEAL),
    ("forward-ml\n(Python 3.11)\nK-means · XGBoost · Survival\nCron 02h diário", 60, 490, 400, 280, GREEN),
    ("Cron Linux\nrun_segmenter.py\n1×/dia · 02h00", 480, 490, 380, 280, (80,60,20)),
]
for name, x, y, w, h, bg in containers:
    lines = name.split("\n")
    box(d, x, y, w, h, bg, ["«container»"] + lines, accent=FORD_ORANGE)

# External
# Supabase
d.rectangle([980, 110, 1580, 380], fill=(60,20,80))
d.rectangle([980, 110, 1580, 116], fill=FORD_ORANGE)
d.text((990, 120), "☁  Supabase Cloud / Neon (PostgreSQL 16)", fill=WHITE, font=try_font(16))
box(d, 995, 155, 570, 200, PURPLE, ["SystemSoftware", "PostgreSQL 16", "Banco gerenciado · Fonte da verdade", "Flyway migrations · ≤$25/mês"], accent=(200,100,255))

# Vercel
d.rectangle([980, 400, 1580, 600], fill=(20,50,20))
d.rectangle([980, 400, 1580, 406], fill=FORD_ORANGE)
d.text((990, 410), "☁  Vercel / Netlify (forward-web)", fill=WHITE, font=try_font(16))
box(d, 995, 445, 570, 130, GREEN, ["Node", "forward-web (SvelteKit)", "Dashboard corporativo Ford · Free tier", "Build + deploy automático via GitHub Actions"], accent=(100,255,150))

# Meta / WhatsApp
d.rectangle([980, 620, 1580, 800], fill=(20,50,80))
d.text((990, 635), "☁  Meta — WhatsApp Business API", fill=WHITE, font=try_font(16))
box(d, 995, 670, 570, 110, FORD_BLUE, ["TechnologyInterface", "WhatsApp Business API", "97% abertura · ROI 300:1", "1.000 msgs/mês free tier (Sprint 1)"], accent=FORD_ORANGE)

# Expo
d.rectangle([980, 820, 1580, 970], fill=(30,30,60))
d.text((990, 832), "☁  Expo EAS (forward-mobile)", fill=WHITE, font=try_font(16))
box(d, 995, 862, 570, 90, FORD_DARK, ["Artifact", "forward-mobile.apk / .ipa", "30 builds/mês free · Push notifications via Expo API"], accent=FORD_ORANGE)

# Arrows
arrow(d, 960, 325, 980, 260)   # java → postgres
arrow(d, 960, 340, 980, 500)   # java → vercel (web consome api)
arrow(d, 700, 325, 980, 700)   # n8n → whatsapp

footer(d, "ForwardService.archimate · View 4: Technology · ArchiMate 3.1 · QA-4 · Sprint 1 · 2026")
img.save(os.path.join(OUT, "04_technology_view.png"))
print("✓ 04_technology_view.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 5 — Requirements View (Quality)
# ══════════════════════════════════════════════════════════════════════════════
img, d = new_img()
header(d, "5. Requirements View — Requisitos de Qualidade",
          "Cada requisito realizado por componentes específicos (Realization)")

reqs_detail = [
    ("REQ-01", "Latência API p95 < 300ms",       "forward-api-java · HikariCP · Azure B-series", FORD_DARK),
    ("REQ-02", "Disponibilidade ≥ 99%",           "Docker + health checks · Azure SLA · Postgres managed", FORD_DARK),
    ("REQ-03", "AUC classificador ≥ 0,82",        "forward-ml · XGBoost · target engenheirado (days > 365)", GREEN),
    ("REQ-04", "Falsos positivos churn < 10%",    "forward-ml · K-means Silhouette > 0,4 · threshold tunável", GREEN),
    ("REQ-05", "LGPD — dados pseudonimizados",    "VIN_Hash SHA1+salt · audit_log · sem PII no ML", PURPLE),
    ("REQ-06", "Onboarding atendente < 15 min",   "forward-mobile · UX dual-mode · Expo i18n", TEAL),
    ("REQ-07", "Entrega WhatsApp < 30s",           "n8n · WhatsApp Business API · templates pré-aprovados", TEAL),
]

for i, (code, name, impl, bg) in enumerate(reqs_detail):
    row = i % 4
    col = i // 4
    x = 20 + col * 810
    y = 115 + row * 215

    # Req box
    box(d, x, y, 380, 190, bg, ["Requirement", f"{code}: {name}", "", impl], accent=FORD_ORANGE)

    # Realization arrow → principle
    arrow(d, x+380, y+95, x+420, y+95)

    # Principle box
    principles = [
        "SOA — Portão Único", "SOA — Portão Único", "Flywheel de Dados", "Flywheel de Dados",
        "Proatividade", "SOA — Portão Único", "SOA — Portão Único",
    ]
    box(d, x+420, y+50, 350, 90, FORD_BLUE, ["Principle", principles[i]], accent=(100,150,255))

footer(d, "ForwardService.archimate · View 5: Requirements (Quality) · ArchiMate 3.1 · QA-4 · Sprint 1 · 2026")
img.save(os.path.join(OUT, "05_requirements_view.png"))
print("✓ 05_requirements_view.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 6 — Monitoring View
# ══════════════════════════════════════════════════════════════════════════════
img, d = new_img()
header(d, "6. Monitoring View — Observabilidade e Alertas",
          "Grafana · audit_log · ML Monitor · Cron segmentador")

monitors = [
    ("Grafana Dashboard",         "Latência API · throughput · erros · n8n\nConectado ao forward-api-java", FORD_BLUE, 20, 115),
    ("Alert: API p95 > 300ms",    "Dispara quando SLA de latência é quebrado\n→ notifica equipe no Slack/email", FORD_ORANGE, 20, 330),
    ("Alert: Disponibilidade <99%","Downtime > SLA → alerta imediato\n→ 7h15 downtime/ano é o limite", FORD_ORANGE, 20, 545),
    ("audit_log viewer",          "Interface para revisar trilha LGPD\nQuem acessou o quê e quando", PURPLE, 540, 115),
    ("ML Model Monitor",          "AUC mensal · drift de dados · Silhouette\nRetrein triggered se AUC < 0,78", GREEN, 540, 330),
    ("Cron segmentador 02h",      "run_segmenter.py roda às 02h\nEscreve em client_segments · 175k VINs/dia", TEAL, 540, 545),
]

for name, desc, bg, x, y in monitors:
    box(d, x, y, 480, 190, bg, ["«assessment»", name, "", desc], accent=FORD_ORANGE)

# Observed components
obs = [
    ("forward-api-java",   1080, 115),
    ("forward-ml",         1080, 280),
    ("audit_log (tabela)", 1080, 445),
    ("client_segments",    1080, 610),
    ("Azure VM (B-series)",1080, 775),
    ("Docker Engine",      1350, 115),
    ("GitHub Actions CI",  1350, 280),
]
for name, x, y in obs:
    box(d, x, y, 220, 130, FORD_DARK, ["Component", name])

# Arrows
for (_, _, _, mx, my), (_, ox, oy) in zip(monitors, obs):
    arrow(d, mx+480, my+95, ox, oy+65)

footer(d, "ForwardService.archimate · View 6: Monitoring · ArchiMate 3.1 · QA-4 · Sprint 1 · 2026")
img.save(os.path.join(OUT, "06_monitoring_view.png"))
print("✓ 06_monitoring_view.png")

print("\n✅ 6 PNGs gerados em:", OUT)
