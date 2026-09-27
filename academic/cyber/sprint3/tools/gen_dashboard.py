# Generates observability/dashboards/forwardservice-overview.json:
#   python gen_dashboard.py ../observability/dashboards/forwardservice-overview.json
"""Generates the Grafana dashboard JSON (forwardservice-overview.json).

Panels are declared once here and reused by gen_mock.py so the static mock
(screenshot) and the importable dashboard always share titles, queries and
thresholds.
"""
import json
import sys

PROM = {"type": "prometheus", "uid": "${ds_prom}"}
LOKI = {"type": "loki", "uid": "${ds_loki}"}
APP = 'application="$app"'
NOT_PROBES = 'uri!~"/actuator.*|/health|/ready"'

# Each panel: kind, title, grid (x, y, w, h), unit, thresholds [(value, color)], targets [(expr, legend)],
# plus "desc" (Portuguese description shown in Grafana) and "status" (implemented / planned source).
ROWS = [
    ("SLO da API (REQ-01 latência p95 < 300 ms, REQ-02 disponibilidade >= 99%)", 0),
    ("Erros e segurança da API (autenticação, autorização, rate limit)", 13),
    ("ML: scoring de churn (forward-ml)", 30),
    ("Mobile (forward-mobile)", 38),
    ("IoT: telemetria de veículos conectados (proposto)", 44),
    ("DevSecOps: achados de código e dependências", 51),
]

PANELS = [
    # ---- Row: SLO -------------------------------------------------------------------------
    dict(kind="stat", title="Latência p95 da API (5 min)", grid=(0, 1, 6, 5), unit="s",
         thresholds=[(None, "green"), (0.25, "orange"), (0.3, "red")],
         targets=[(f'histogram_quantile(0.95, sum by (le) (rate(http_server_requests_seconds_bucket{{{APP}, {NOT_PROBES}}}[5m])))', "p95")],
         desc="REQ-01: p95 abaixo de 300 ms. Fonte: Micrometer http.server.requests (histograma habilitado)."),
    dict(kind="stat", title="Disponibilidade 30 dias (sonda /health)", grid=(6, 1, 6, 5), unit="percentunit",
         thresholds=[(None, "red"), (0.99, "orange"), (0.995, "green")],
         targets=[('avg_over_time(probe_success{job="blackbox-forward-api"}[30d])', "disponibilidade")],
         desc="REQ-02: disponibilidade >= 99% medida por sonda sintética (blackbox exporter) em /health a cada 30 s."),
    dict(kind="stat", title="Error budget restante (30 dias)", grid=(12, 1, 6, 5), unit="percentunit",
         thresholds=[(None, "red"), (0.25, "orange"), (0.5, "green")],
         targets=[('1 - ((1 - avg_over_time(probe_success{job="blackbox-forward-api"}[30d])) / 0.01)', "budget")],
         desc="Orçamento de erro do SLO de 99%: 1% de 30 dias = 7 h 12 min de indisponibilidade tolerada por mês."),
    dict(kind="stat", title="Taxa de erro 5xx (5 min)", grid=(18, 1, 6, 5), unit="percentunit",
         thresholds=[(None, "green"), (0.01, "orange"), (0.02, "red")],
         targets=[(f'sum(rate(http_server_requests_seconds_count{{{APP}, outcome="SERVER_ERROR"}}[5m])) / sum(rate(http_server_requests_seconds_count{{{APP}}}[5m]))', "5xx")],
         desc="Fração de respostas 5xx sobre o total de requisições."),
    dict(kind="timeseries", title="Latência p95 por rota (API)", grid=(0, 6, 12, 7), unit="s",
         thresholds=[(None, "green"), (0.3, "red")], threshold_line=True,
         targets=[(f'histogram_quantile(0.95, sum by (le, uri) (rate(http_server_requests_seconds_bucket{{{APP}, {NOT_PROBES}}}[5m])))', "{{uri}}")],
         desc="p95 por endpoint; linha vermelha = limite do REQ-01."),
    dict(kind="timeseries", title="Latência p95 na borda Fly.io (sem instrumentação)", grid=(12, 6, 12, 7), unit="s",
         thresholds=[(None, "green"), (0.3, "red")], threshold_line=True,
         targets=[('histogram_quantile(0.95, sum by (le) (rate(fly_edge_http_response_time_seconds_bucket{app="forward-api-java"}[5m])))', "edge p95")],
         desc="Métrica nativa do Fly.io (Prometheus gerenciado): mede o SLO mesmo antes da instrumentação Micrometer."),
    # ---- Row: API security ----------------------------------------------------------------
    dict(kind="timeseries", title="Respostas 4xx e 5xx (req/s)", grid=(0, 14, 8, 8), unit="reqps",
         thresholds=[(None, "green")],
         targets=[(f'sum by (outcome) (rate(http_server_requests_seconds_count{{{APP}, outcome=~"CLIENT_ERROR|SERVER_ERROR"}}[5m]))', "{{outcome}}")],
         desc="Erros de cliente (4xx) e de servidor (5xx)."),
    dict(kind="timeseries", title="401 e 403 por minuto", grid=(8, 14, 8, 8), unit="short",
         thresholds=[(None, "green"), (60, "red")], threshold_line=True,
         targets=[(f'sum by (status) (rate(http_server_requests_seconds_count{{{APP}, status=~"401|403"}}[5m])) * 60', "HTTP {{status}}")],
         desc="Picos de 401 indicam token inválido em massa; picos de 403 indicam sondagem de autorização (BOLA/BFLA)."),
    dict(kind="timeseries", title="Falhas de login por minuto (por motivo)", grid=(16, 14, 8, 8), unit="short",
         thresholds=[(None, "green"), (20, "red")], threshold_line=True,
         targets=[('sum by (reason) (rate(forward_auth_login_total{result="failure"}[5m])) * 60', "{{reason}}")],
         desc="Contador do endpoint de login (JWT emitido pela API). Base para detectar brute force e credential stuffing."),
    dict(kind="timeseries", title="Rate limit: respostas 429 por minuto", grid=(0, 22, 8, 8), unit="short",
         thresholds=[(None, "green"), (60, "red")], threshold_line=True,
         targets=[(f'sum(rate(http_server_requests_seconds_count{{{APP}, status="429"}}[5m])) * 60', "429/min")],
         desc="RateLimitFilter (Bucket4j, 60 req/min por IP + sub)."),
    dict(kind="logs", title="Eventos de segurança (logs JSON no Loki)", grid=(8, 22, 16, 8),
         targets=[('{app="forward-api"} | json | event=~"auth\\\\..*|authz\\\\..*|ratelimit\\\\..*|admin\\\\..*"', "")],
         desc="Logs estruturados (LogstashEncoder) filtrados pelo campo event; correlação por request_id."),
    # ---- Row: ML ----------------------------------------------------------------------------
    dict(kind="timeseries", title="Drift do score (PSI vs baseline de treino)", grid=(0, 31, 8, 7), unit="short",
         thresholds=[(None, "green"), (0.1, "orange"), (0.25, "red")], threshold_line=True,
         targets=[('max by (model_version) (forward_ml_score_psi{model="churn_scorer_v3"})', "{{model_version}}")],
         desc="Population Stability Index do churn_probability por lote de scoring. > 0,25 = drift relevante."),
    dict(kind="stat", title="AUC monitorada (REQ-03 >= 0,82)", grid=(8, 31, 4, 7), unit="short", decimals=3,
         thresholds=[(None, "red"), (0.78, "orange"), (0.82, "green")],
         targets=[('forward_ml_auc{model="churn_scorer_v3"}', "AUC")],
         desc="AUC recalculada mensalmente com rótulos maduros; < 0,78 dispara retreino (Monitoring View TOGAF)."),
    dict(kind="stat", title="Horas desde o último scoring", grid=(12, 31, 4, 7), unit="h", decimals=1,
         thresholds=[(None, "green"), (24, "orange"), (26, "red")],
         targets=[('(time() - forward_ml_scoring_last_success_timestamp_seconds) / 3600', "horas")],
         desc="Job diário de scoring; atraso > 26 h gera alerta."),
    dict(kind="timeseries", title="Clientes por faixa de risco (último lote)", grid=(16, 31, 8, 7), unit="short",
         thresholds=[(None, "green")],
         targets=[('sum by (tier) (forward_ml_scored_customers)', "{{tier}}")],
         desc="Distribuição das faixas de risco; mudança brusca sem mudança de negócio indica drift ou envenenamento de dados."),
    # ---- Row: Mobile -----------------------------------------------------------------------
    dict(kind="stat", title="Sessões sem crash (24 h)", grid=(0, 39, 6, 5), unit="percentunit", decimals=2,
         thresholds=[(None, "red"), (0.99, "orange"), (0.995, "green")],
         targets=[('forward_mobile_crash_free_sessions_ratio', "crash-free")],
         desc="Crash-free sessions exportado do crash reporting (Sentry/EAS) para o Prometheus."),
    dict(kind="timeseries", title="Erros de API vistos pelo app (por minuto)", grid=(6, 39, 10, 5), unit="short",
         thresholds=[(None, "green")],
         targets=[('sum by (status) (rate(forward_mobile_api_errors_total[5m])) * 60', "HTTP {{status}}")],
         desc="Erros HTTP registrados pelo cliente mobile (ApiError em lib/api.ts)."),
    dict(kind="timeseries", title="Crashes por versão do app (1 h)", grid=(16, 39, 8, 5), unit="short",
         thresholds=[(None, "green")],
         targets=[('sum by (app_version) (increase(forward_mobile_crashes_total[1h]))', "{{app_version}}")],
         desc="Regressões por release (EAS Update / APK)."),
    # ---- Row: IoT --------------------------------------------------------------------------
    dict(kind="timeseries", title="Atraso de ingestão da telemetria p95", grid=(0, 45, 8, 6), unit="s",
         thresholds=[(None, "green"), (60, "red")], threshold_line=True,
         targets=[('histogram_quantile(0.95, sum by (le) (rate(forward_telemetry_ingest_lag_seconds_bucket[5m])))', "lag p95")],
         desc="Tempo entre o timestamp do veículo e a gravação no banco."),
    dict(kind="timeseries", title="MQTT: falhas de autenticação e ACL negadas", grid=(8, 45, 8, 6), unit="short",
         thresholds=[(None, "green"), (10, "red")], threshold_line=True,
         targets=[('sum(rate(forward_mqtt_auth_failures_total[5m])) * 60', "auth falhou/min"),
                  ('sum(rate(forward_mqtt_acl_denied_total[5m])) * 60', "ACL negada/min")],
         desc="Certificado inválido, revogado ou publicação fora do próprio tópico."),
    dict(kind="stat", title="Dispositivos conectados", grid=(16, 45, 8, 6), unit="short",
         thresholds=[(None, "green")],
         targets=[('sum(forward_mqtt_connected_clients)', "conectados")],
         desc="Conexões MQTT ativas (mTLS)."),
    # ---- Row: DevSecOps --------------------------------------------------------------------
    dict(kind="bargauge", title="Achados abertos por severidade (code scanning)", grid=(0, 52, 12, 6), unit="short",
         thresholds=[(None, "green"), (1, "orange"), (5, "red")],
         targets=[('sum by (severity) (forward_devsecops_open_alerts)', "{{severity}}")],
         desc="Exporter que lê a API de code scanning da org (SARIF do pipeline DevSecOps)."),
    dict(kind="stat", title="Idade do achado crítico mais antigo (dias)", grid=(12, 52, 12, 6), unit="d",
         thresholds=[(None, "green"), (3, "orange"), (7, "red")],
         targets=[('max(forward_devsecops_oldest_open_alert_age_days{severity="critical"})', "dias")],
         desc="SLA de correção: crítico em até 7 dias (plano de segurança contínua)."),
]


def thresholds(steps):
    return {"mode": "absolute", "steps": [{"color": c, "value": v} for v, c in steps]}


def build():
    panels = []
    pid = 1
    for title, y in ROWS:
        panels.append({"type": "row", "title": title, "id": 100 + pid, "collapsed": False,
                       "gridPos": {"h": 1, "w": 24, "x": 0, "y": y}, "panels": []})
        pid += 1
    for p in PANELS:
        x, y, w, h = p["grid"]
        panel = {
            "id": pid,
            "type": p["kind"],
            "title": p["title"],
            "description": p["desc"],
            "gridPos": {"h": h, "w": w, "x": x, "y": y},
            "datasource": LOKI if p["kind"] == "logs" else PROM,
            "targets": [
                {"refId": chr(65 + i), "expr": expr, "legendFormat": legend,
                 "datasource": LOKI if p["kind"] == "logs" else PROM}
                for i, (expr, legend) in enumerate(p["targets"])
            ],
        }
        pid += 1
        if p["kind"] == "logs":
            panel["options"] = {"showTime": True, "wrapLogMessage": True, "sortOrder": "Descending",
                                "enableLogDetails": True, "prettifyLogMessage": False}
        else:
            defaults = {"unit": p.get("unit", "short"), "thresholds": thresholds(p["thresholds"]),
                        "color": {"mode": "thresholds" if p["kind"] != "timeseries" else "palette-classic"}}
            if "decimals" in p:
                defaults["decimals"] = p["decimals"]
            if p["kind"] == "timeseries":
                defaults["custom"] = {
                    "drawStyle": "line", "lineWidth": 2, "fillOpacity": 10, "showPoints": "never",
                    "thresholdsStyle": {"mode": "line+area" if p.get("threshold_line") else "off"},
                }
                panel["options"] = {"legend": {"displayMode": "list", "placement": "bottom", "showLegend": True},
                                    "tooltip": {"mode": "multi", "sort": "desc"}}
            elif p["kind"] == "stat":
                panel["options"] = {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
                                    "colorMode": "background", "graphMode": "area", "justifyMode": "center",
                                    "textMode": "value"}
            elif p["kind"] == "bargauge":
                panel["options"] = {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
                                    "orientation": "horizontal", "displayMode": "gradient", "showUnfilled": True}
            panel["fieldConfig"] = {"defaults": defaults, "overrides": []}
        panels.append(panel)

    return {
        "title": "ForwardService: visão geral de SLO, segurança, ML, mobile e IoT",
        "uid": "forwardservice-overview",
        "description": "Dashboard do plano de monitoramento da entrega Cybersecurity Sprint 3 (FIAP x Ford). "
                       "Métricas forward_* são instrumentação planejada; veja ENTREGA_CYBER_SPRINT3.md seção 3.",
        "tags": ["forwardservice", "ford", "slo", "security", "devsecops"],
        "timezone": "America/Sao_Paulo",
        "editable": True,
        "graphTooltip": 1,
        "schemaVersion": 39,
        "version": 1,
        "refresh": "1m",
        "time": {"from": "now-24h", "to": "now"},
        "annotations": {"list": [
            {"builtIn": 1, "datasource": {"type": "grafana", "uid": "-- Grafana --"}, "enable": True,
             "hide": True, "iconColor": "rgba(0, 211, 255, 1)", "name": "Annotations & Alerts", "type": "dashboard"},
            {"datasource": PROM, "enable": True, "iconColor": "red", "name": "Deploys (Fly.io)",
             "expr": 'changes(fly_instance_up{app="forward-api-java"}[2m]) > 0', "step": "60s",
             "titleFormat": "deploy/restart"},
        ]},
        "templating": {"list": [
            {"name": "ds_prom", "label": "Prometheus", "type": "datasource", "query": "prometheus",
             "current": {}, "hide": 0, "refresh": 1},
            {"name": "ds_loki", "label": "Loki", "type": "datasource", "query": "loki",
             "current": {}, "hide": 0, "refresh": 1},
            {"name": "app", "label": "Aplicação (Micrometer application tag)", "type": "custom",
             "query": "forward-api", "current": {"text": "forward-api", "value": "forward-api"},
             "options": [{"selected": True, "text": "forward-api", "value": "forward-api"}], "hide": 0},
        ]},
        "links": [
            {"title": "Plano de monitoramento (seção 3)", "type": "link", "targetBlank": True,
             "url": "https://github.com/fwd-ford/forward-docs/blob/main/academic/cyber/sprint3/ENTREGA_CYBER_SPRINT3.md"},
        ],
        "panels": panels,
    }


if __name__ == "__main__":
    out = sys.argv[1]
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(build(), fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("written", out, "panels:", len(PANELS))
