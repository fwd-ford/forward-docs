# Generates the static dashboard mock (synthetic data) used for the prints:
#   python gen_mock.py ../observability/mock
"""Static HTML mock of forwardservice-overview.json with synthetic data.

Docker was not available on the build machine, so Grafana + Prometheus could
not run locally. This renders the same panels (titles, thresholds, layout)
from gen_dashboard.PANELS with synthetic series, clearly labelled as such.
Two panels use real numbers (DevSecOps findings, model AUC) and say so.
"""
import html
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen_dashboard import PANELS, ROWS  # noqa: E402

random.seed(42)
COLORS = {"green": "#73BF69", "orange": "#FF9830", "red": "#F2495C", "blue": "#5794F2",
          "purple": "#B877D9", "yellow": "#FADE2A", "cyan": "#8AB8FF"}
PALETTE = ["#73BF69", "#FADE2A", "#5794F2", "#FF9830", "#F2495C", "#B877D9", "#8AB8FF"]
N = 288  # 24 h, 5 min step
UNIT_H = 34  # px per grid unit
WIDTH = 1500


def series(base, noise, spikes=(), floor=0.0, daily=0.0):
    out = []
    for i in range(N):
        hour = i / 12.0
        v = base + daily * math.sin((hour - 9) / 24 * 2 * math.pi) + random.gauss(0, noise)
        for center, height, width in spikes:
            v += height * math.exp(-((i - center) ** 2) / (2 * width ** 2))
        out.append(max(floor, v))
    return out


# Synthetic data keyed by panel title. Values are illustrative only.
DATA = {
    "Latência p95 da API (5 min)": {"stat": 0.212, "spark": series(0.19, 0.012, [(168, 0.15, 3)], daily=0.03)},
    "Disponibilidade 30 dias (sonda /health)": {"stat": 0.9962, "spark": series(0.9962, 0.0002)},
    "Error budget restante (30 dias)": {"stat": 0.62, "spark": [0.9 - i * 0.28 / N for i in range(N)]},
    "Taxa de erro 5xx (5 min)": {"stat": 0.004, "spark": series(0.004, 0.0015, [(170, 0.012, 4)])},
    "Latência p95 por rota (API)": {"lines": {
        "/api/v1/leads": series(0.21, 0.015, [(168, 0.16, 3)], daily=0.03),
        "/api/v1/service-events": series(0.24, 0.02, [(168, 0.12, 3)], daily=0.02),
        "/api/v1/scores/{customerId}": series(0.15, 0.01, daily=0.02),
        "/api/v1/customers/{id}": series(0.12, 0.01, daily=0.015),
        "/soap/vehicles": series(0.19, 0.015, daily=0.02),
    }},
    "Latência p95 da sonda sintética (/health, de fora)": {"lines": {
        "sonda p95": series(0.23, 0.015, [(168, 0.17, 3)], daily=0.03)}},
    "Respostas 4xx e 5xx (req/s)": {"lines": {
        "CLIENT_ERROR": series(0.12, 0.03, [(157, 1.6, 2)], daily=0.05),
        "SERVER_ERROR": series(0.006, 0.003, [(170, 0.05, 3)])}},
    "401 e 403 por minuto": {"lines": {
        "HTTP 401": series(3.0, 1.0, [(157, 92, 2)], daily=1.5),
        "HTTP 403": series(1.2, 0.5, [(160, 14, 2)])}},
    "Falhas de login por minuto (por motivo)": {"lines": {
        "invalid_credentials": series(0.9, 0.4, [(157, 33, 2)]),
        "disabled": series(0.05, 0.05, [(158, 1, 2)])}},
    "Rate limit: respostas 429 por minuto": {"lines": {"429/min": series(0.4, 0.3, [(158, 44, 2)])}},
    "Drift do score (PSI vs baseline de treino)": {"lines": {"v3": [0.043 if i >= 72 else 0.038 for i in range(N)]}},
    "AUC monitorada (REQ-03 >= 0,82)": {"stat": 0.907, "real": "AUC 0,9073 em resultados/metrics.json"},
    "Horas desde o último scoring": {"stat": 7.2},
    "Clientes por faixa de risco (último lote)": {"lines": {
        "baixo": [71240] * N, "médio": [38110] * N, "alto": [22010] * N, "crítico": [12254] * N}},
    "Sessões sem crash (24 h)": {"stat": 0.9971, "spark": series(0.9971, 0.0006)},
    "Erros de API vistos pelo app (por minuto)": {"lines": {
        "HTTP 401": series(0.6, 0.3, [(157, 3, 3)]), "HTTP 500": series(0.05, 0.05, [(170, 1.2, 3)])}},
    "Crashes por versão do app (1 h)": {"lines": {
        "0.1.0": series(0.4, 0.3, floor=0), "0.1.1": series(0.1, 0.1, floor=0)}},
    "Atraso de ingestão da telemetria p95": {"lines": {"lag p95": series(11, 2.5, [(200, 40, 4)], daily=3)}},
    "MQTT: falhas de autenticação e ACL negadas": {"lines": {
        "auth falhou/min": series(0.4, 0.3, [(220, 13, 2)]), "ACL negada/min": series(0.05, 0.05, [(222, 6, 2)])}},
    "Dispositivos conectados": {"stat": 1284, "spark": series(1284, 30, daily=180)},
    "Achados abertos por severidade (code scanning)": {"bars": [("critical", 7), ("high", 59), ("medium", 83), ("low", 10)],
                                                        "real": "totais reais do pipeline DevSecOps em 27/09/2026"},
    "Idade do achado crítico mais antigo (dias)": {"stat": 0.2, "real": "achados criados em 27/09/2026"},
}

LOG_LINES = [
    ("13:14:03", "WARN", 'ratelimit.rejected bucket=global key_type=ip limit=60 window=PT1M path=/api/v1/leads'),
    ("13:12:40", "WARN", 'authz.denied role=ATENDENTE required_role=GESTOR PATCH /api/v1/leads/7e2d9c14.../assignee'),
    ("13:09:15", "WARN", 'auth.token_rejected reason=token_invalid src_ip=91.240.118.7 path=/api/v1/customers/...'),
    ("13:09:02", "WARN", 'auth.token_rejected reason=token_expired path=/api/v1/leads'),
    ("13:05:48", "WARN", 'auth.login_failed reason=invalid_credentials username_hash=sha256:e3b9a1c47f02 src_ip=45.155.205.12'),
    ("13:05:47", "WARN", 'auth.login_failed reason=invalid_credentials failures_last_5m=17 src_ip=45.155.205.12'),
    ("13:02:11", "INFO", 'auth.login_succeeded role=ATENDENTE user_id=8f14e45f-... src_ip=177.92.18.44'),
]


def threshold_color(thresholds, value):
    color = thresholds[0][1]
    for v, c in thresholds[1:]:
        if v is not None and value >= v:
            color = c
    return COLORS.get(color, color)


def fmt(value, unit, decimals=None):
    if unit == "s":
        return f"{value:.0f} s" if value >= 2 else f"{value * 1000:.0f} ms"
    if unit == "percentunit":
        d = 2 if decimals is None else decimals
        return f"{value * 100:.{d}f}%".replace(".", ",")
    if unit == "h":
        return f"{value:.1f} h".replace(".", ",")
    if unit == "d":
        return f"{value:.1f} d".replace(".", ",")
    if isinstance(value, float) and value < 10:
        return f"{value:.3f}".replace(".", ",")
    return f"{value:,.0f}".replace(",", ".")


def spark_svg(values, w, h, color):
    lo, hi = min(values), max(values)
    rng = (hi - lo) or 1
    pts = " ".join(f"{i * w / (len(values) - 1):.1f},{h - (v - lo) / rng * h * 0.8 - 2:.1f}" for i, v in enumerate(values))
    return (f'<svg class="spark" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
            f'<polyline points="{pts}" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="2"/></svg>')


def timeseries_svg(lines, w, h, unit, thresholds, threshold_line):
    pad_l, pad_b, pad_t, pad_r = 58, 22, 8, 26
    allv = [v for vals in lines.values() for v in vals]
    tvals = [v for v, _ in thresholds if v is not None] if threshold_line else []
    hi = max(allv + tvals) * 1.12 or 1
    lo = 0
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for k in range(5):
        y = pad_t + ih - k * ih / 4
        val = lo + k * (hi - lo) / 4
        label = fmt(val, unit) if unit in ("s",) else (f"{val:,.0f}".replace(",", ".") if val >= 100 else f"{val:.2f}".replace(".", ","))
        out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w - pad_r}" y2="{y:.1f}" stroke="#2c3235" stroke-width="1"/>')
        out.append(f'<text x="{pad_l - 6}" y="{y + 4:.1f}" text-anchor="end" class="axis">{label}</text>')
    for k, hh in enumerate(["00:00", "06:00", "12:00", "18:00", "24:00"]):
        x = pad_l + k * iw / 4
        out.append(f'<text x="{x:.1f}" y="{h - 4}" text-anchor="middle" class="axis">{hh}</text>')
    if threshold_line:
        for v, c in thresholds:
            if v is None:
                continue
            y = pad_t + ih - (v - lo) / (hi - lo) * ih
            col = COLORS.get(c, c)
            out.append(f'<rect x="{pad_l}" y="{pad_t}" width="{iw}" height="{max(0, y - pad_t):.1f}" fill="{col}" opacity="0.06"/>')
            out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w - pad_r}" y2="{y:.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 4"/>')
    for idx, (name, vals) in enumerate(lines.items()):
        col = PALETTE[idx % len(PALETTE)]
        pts = " ".join(f"{pad_l + i * iw / (len(vals) - 1):.1f},{pad_t + ih - (v - lo) / (hi - lo) * ih:.1f}"
                       for i, v in enumerate(vals))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"/>')
    out.append("</svg>")
    legend = "".join(f'<span class="lg"><i style="background:{PALETTE[i % len(PALETTE)]}"></i>{html.escape(n)}</span>'
                     for i, n in enumerate(lines))
    return "".join(out) + f'<div class="legend">{legend}</div>'


def panel_html(p):
    x, y, w, h = p["grid"]
    pw = w * (WIDTH - 24) / 24 - 8
    ph = h * UNIT_H - 8
    data = DATA.get(p["title"], {})
    real = data.get("real")
    badge = f'<span class="real">dado real: {html.escape(real)}</span>' if real else ""
    body = ""
    if p["kind"] == "stat":
        value = data.get("stat", 0)
        color = threshold_color(p["thresholds"], value)
        spark = spark_svg(data["spark"], int(pw - 16), int(ph * 0.35), color) if "spark" in data else ""
        body = (f'<div class="stat" style="background:{color}"><div class="big">{fmt(value, p.get("unit"), p.get("decimals"))}</div>'
                f'{spark}</div>')
    elif p["kind"] == "timeseries":
        body = timeseries_svg(data.get("lines", {"-": [0] * N}), int(pw - 16), int(ph - 58),
                              p.get("unit"), p["thresholds"], p.get("threshold_line", False))
    elif p["kind"] == "bargauge":
        bars = data.get("bars", [])
        mx = max(v for _, v in bars) or 1
        rows = []
        for name, v in bars:
            col = threshold_color(p["thresholds"], v)
            if name == "critical":
                col = COLORS["red"]
            rows.append(f'<div class="bar"><span class="bn">{name}</span><span class="bt"><span style="width:{v / mx * 100:.0f}%;'
                        f'background:linear-gradient(90deg,{COLORS["green"]},{col})"></span></span><span class="bv">{v}</span></div>')
        body = "".join(rows)
    elif p["kind"] == "logs":
        body = "".join(f'<div class="log"><span class="lt">{t}</span><span class="lv {lv.lower()}">{lv}</span>'
                       f'<span class="lm">{html.escape(m)}</span></div>' for t, lv, m in LOG_LINES)
    return (f'<div class="panel" style="grid-column:{x + 1} / span {w};grid-row:{y + 1} / span {h}">'
            f'<div class="ptitle">{html.escape(p["title"])}{badge}</div><div class="pbody">{body}</div></div>')


def page(rows_filter, title_suffix):
    rows = [(t, y) for t, y in ROWS if t in rows_filter]
    ys = sorted(y for _, y in rows)
    y0 = ys[0]
    # rows included end where the next excluded row starts
    all_y = sorted(y for _, y in ROWS) + [60]
    y_end = min(v for v in all_y if v > max(ys))
    parts = []
    for t, y in rows:
        parts.append(f'<div class="row" style="grid-column:1 / span 24;grid-row:{y - y0 + 1} / span 1">{html.escape(t)}</div>')
    for p in PANELS:
        x, y, w, h = p["grid"]
        if y0 <= y < y_end:
            q = dict(p)
            q["grid"] = (x, y - y0, w, h)
            parts.append(panel_html(q))
    height_units = y_end - y0
    css = f"""
    *{{box-sizing:border-box}} body{{margin:0;background:#111217;color:#ccccdc;font-family:Inter,'Segoe UI',Arial,sans-serif;width:{WIDTH}px}}
    .top{{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid #2c3235;background:#181b1f}}
    .top h1{{font-size:20px;margin:0;color:#e0e0ea;font-weight:600}} .top .meta{{font-size:13px;color:#9fa7b3}}
    .warn{{margin:10px 12px 0;padding:10px 14px;border:1px solid #FF9830;background:rgba(255,152,48,.12);color:#FFB357;font-size:15px;border-radius:4px;font-weight:600}}
    .grid{{display:grid;grid-template-columns:repeat(24,1fr);grid-auto-rows:{UNIT_H}px;gap:8px;padding:12px}}
    .row{{font-size:16px;font-weight:600;color:#e0e0ea;display:flex;align-items:center;border-bottom:1px solid #2c3235}}
    .panel{{background:#181b1f;border:1px solid #2c3235;border-radius:3px;display:flex;flex-direction:column;overflow:hidden}}
    .ptitle{{font-size:14px;font-weight:600;padding:7px 10px 4px;color:#d8d9e0;display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
    .real{{font-size:11px;font-weight:600;color:#73BF69;border:1px solid #73BF69;border-radius:3px;padding:0 5px}}
    .pbody{{flex:1;padding:4px 8px 6px;position:relative}}
    .stat{{height:100%;border-radius:3px;display:flex;flex-direction:column;justify-content:center;align-items:center;position:relative}}
    .big{{font-size:40px;font-weight:600;color:#fff;z-index:1}} .spark{{position:absolute;bottom:4px;left:8px}}
    .axis{{font-size:11px;fill:#9fa7b3}} .legend{{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;padding-top:2px}}
    .lg i{{display:inline-block;width:14px;height:4px;margin-right:5px;vertical-align:middle;border-radius:2px}}
    .bar{{display:flex;align-items:center;gap:10px;margin:6px 4px}} .bn{{width:70px;font-size:13px}} .bv{{width:40px;font-size:18px;font-weight:600;text-align:right}}
    .bt{{flex:1;height:22px;background:#22252b;border-radius:2px;overflow:hidden}} .bt span{{display:block;height:100%}}
    .log{{font-family:Consolas,'Cascadia Mono',monospace;font-size:12.5px;padding:3px 0;border-bottom:1px solid #22252b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
    .lt{{color:#9fa7b3;margin-right:10px}} .lv{{margin-right:10px;font-weight:700}} .lv.warn{{color:#FF9830}} .lv.info{{color:#73BF69}} .lm{{color:#d8d9e0}}
    """
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Mock forwardservice-overview</title>
<style>{css}</style></head><body>
<div class="top"><h1>ForwardService: visão geral de SLO, segurança, ML, mobile e IoT {html.escape(title_suffix)}</h1>
<div class="meta">uid forwardservice-overview · últimas 24 h · America/Sao_Paulo</div></div>
<div class="warn">SIMULAÇÃO COM DADOS SINTÉTICOS: layout, consultas e limites do dashboard real
(observability/dashboards/forwardservice-overview.json); valores ilustrativos, exceto painéis marcados como "dado real".</div>
<div class="grid" style="grid-template-rows:repeat({height_units},{UNIT_H}px)">{''.join(parts)}</div>
</body></html>"""


if __name__ == "__main__":
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    titles = [t for t, _ in ROWS]
    pages = {
        "dashboard-mock-1-api.html": (titles[0:2], "(1/2)"),
        "dashboard-mock-2-ml-mobile-iot.html": (titles[2:6], "(2/2)"),
    }
    for name, (rows, suffix) in pages.items():
        (out_dir / name).write_text(page(rows, suffix), encoding="utf-8")
        print("written", out_dir / name)
