#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa o plano do ForwardService (backlog.json) para o Azure DevOps.

Cria, de forma idempotente (itens já existentes são reconhecidos pela chave no título e não são
duplicados; numa reexecução só a hierarquia e as predecessoras que faltarem são completadas, e
--sync-fields / --sync-state também alinham campos e estado ao backlog.json):
  1. o projeto com o processo Scrum (ou valida o processo de um projeto existente);
  2. as sprints (iterações) com datas e a seleção delas no time padrão;
  3. a Definition of Done nas colunas do board de Backlog items;
  4. épicos, features, PBIs e tarefas com hierarquia (pai/filho), sprint,
     prioridade, esforço, valor de negócio, critérios de aceite e tags;
  5. os links predecessora/sucessora entre itens;
  6. consultas compartilhadas e a wiki do projeto;
  7. (opcional) o acesso do professor: Basic + Project Administrators.

Uso:
  python azure_devops_import.py --org https://dev.azure.com/<org> --project ForwardService \
      [--professor profelias.bernardo@fiap.com.br] [--dry-run]

O PAT vem da variável de ambiente AZDO_PAT ou é digitado de forma oculta (getpass).
O PAT nunca é impresso nem gravado em disco.

Somente biblioteca padrão do Python 3 (urllib, json, base64, getpass, argparse).

Referências (Microsoft Learn, REST API 7.1) conferidas para cada chamada:
  Projects - Create/Get ............ /rest/api/azure/devops/core/projects
  Processes - List ................. /rest/api/azure/devops/core/processes/list
  Operations - Get ................. /rest/api/azure/devops/operations/operations/get
  Classification Nodes ............. /rest/api/azure/devops/wit/classification-nodes
  Iterations (team settings) ....... /rest/api/azure/devops/work/iterations
  Boards / Columns ................. /rest/api/azure/devops/work/boards, /work/columns
  Work Item Types Field - List ..... /rest/api/azure/devops/wit/work-item-types-field/list
  Work Items - Create/Update ....... /rest/api/azure/devops/wit/work-items
  Wiql - Query By Wiql ............. /rest/api/azure/devops/wit/wiql/query-by-wiql
  Work Items - Get Work Items Batch  /rest/api/azure/devops/wit/work-items/get-work-items-batch
  Queries - Create/Get ............. /rest/api/azure/devops/wit/queries
  Wikis / Pages .................... /rest/api/azure/devops/wiki
  User Entitlements ................ /rest/api/azure/devops/memberentitlementmanagement/user-entitlements
  Link types ....................... /azure/devops/boards/queries/link-type-reference
"""
from __future__ import annotations

import argparse
import base64
import getpass
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict

API_VERSION = "7.1"
# Id do processo Scrum de sistema (Processes - List; exemplo oficial de Projects - Create).
SCRUM_PROCESS_TYPE_ID = "6b724908-ef14-45cf-84f8-768b5384da45"
# Link types (Link type reference): Hierarchy-Reverse = Parent; Dependency-Reverse = Predecessor.
LINK_PARENT = "System.LinkTypes.Hierarchy-Reverse"
LINK_PREDECESSOR = "System.LinkTypes.Dependency-Reverse"

TYPE_ORDER = ["Epic", "Feature", "Product Backlog Item", "Task"]
STATE_FLOW = {
    "Epic": ["New", "In Progress", "Done"],
    "Feature": ["New", "In Progress", "Done"],
    "Product Backlog Item": ["New", "Approved", "Committed", "Done"],
    "Task": ["To Do", "In Progress", "Done"],
}
INITIAL_STATE = {t: states[0] for t, states in STATE_FLOW.items()}

F_TITLE = "System.Title"
F_DESCRIPTION = "System.Description"
F_ACCEPTANCE = "Microsoft.VSTS.Common.AcceptanceCriteria"
F_PRIORITY = "Microsoft.VSTS.Common.Priority"
F_EFFORT = "Microsoft.VSTS.Scheduling.Effort"
F_BUSINESS_VALUE = "Microsoft.VSTS.Common.BusinessValue"
F_REMAINING = "Microsoft.VSTS.Scheduling.RemainingWork"
F_ACTIVITY = "Microsoft.VSTS.Common.Activity"
F_ITERATION = "System.IterationPath"
F_TAGS = "System.Tags"
F_BACKLOG_PRIORITY = "Microsoft.VSTS.Common.BacklogPriority"
F_START = "Microsoft.VSTS.Scheduling.StartDate"
F_TARGET = "Microsoft.VSTS.Scheduling.TargetDate"
F_STATE = "System.State"
F_ASSIGNED = "System.AssignedTo"
F_HISTORY = "System.History"

KEY_RE = re.compile(r"^\[(EP-\d{2}|FT-\d{2}\.\d|PBI-\d{3}|TSK-\d+\.\d{2})\]")

EXIT_OK, EXIT_PARTIAL, EXIT_FATAL, EXIT_INVALID = 0, 1, 2, 3

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BACKLOG = os.path.join(HERE, "backlog.json")

ARCHIMATE_REQUIREMENTS = OrderedDict([
    ("REQ-01", "REQ-01: Latência API p95 < 300ms"),
    ("REQ-02", "REQ-02: Disponibilidade ≥ 99%"),
    ("REQ-03", "REQ-03: AUC classificador ≥ 0,82"),
    ("REQ-04", "REQ-04: Falsos positivos churn < 10%"),
    ("REQ-05", "REQ-05: LGPD — dados pseudonimizados"),
    ("REQ-06", "REQ-06: Onboarding atendente < 15 min"),
    ("REQ-07", "REQ-07: Entrega WhatsApp < 30s"),
])

ALL_STEPS = ["project", "iterations", "board", "workitems", "links", "queries", "wiki", "professor"]


class BacklogError(Exception):
    """backlog.json inválido."""


class FatalError(Exception):
    """Erro que impede continuar (acesso, projeto, processo)."""


class HttpError(Exception):
    def __init__(self, status, message, method, url):
        super().__init__("HTTP %s em %s %s: %s" % (status, method, _strip_query(url), message))
        self.status = status
        self.message = message
        self.method = method
        self.url = url


def _strip_query(url):
    return url.split("?", 1)[0]


# ---------------------------------------------------------------------------
# Saída no console
# ---------------------------------------------------------------------------
class Console:
    """Mensagens em pt-BR com prefixos estáveis; nunca recebe o PAT."""

    def __init__(self, stream=None, verbose=False):
        self.stream = stream or sys.stdout
        self.verbose = verbose

    def _w(self, prefix, msg):
        self.stream.write("%s %s\n" % (prefix, msg))
        self.stream.flush()

    def title(self, msg):
        self.stream.write("\n== %s ==\n" % msg)
        self.stream.flush()

    def ok(self, msg):
        self._w("[ok]", msg)

    def created(self, msg):
        self._w("[criado]", msg)

    def updated(self, msg):
        self._w("[atualizado]", msg)

    def skip(self, msg):
        self._w("[existe]", msg)

    def info(self, msg):
        self._w("[info]", msg)

    def plan(self, msg):
        self._w("[dry-run]", msg)

    def warn(self, msg):
        self._w("[aviso]", msg)

    def error(self, msg):
        self._w("[erro]", msg)

    def debug(self, msg):
        if self.verbose:
            self._w("[debug]", msg)


class Summary:
    def __init__(self):
        self.counts = OrderedDict()
        self.errors = []
        self.warnings = []

    def inc(self, what, n=1):
        self.counts[what] = self.counts.get(what, 0) + n

    def error(self, msg):
        self.errors.append(msg)

    def warning(self, msg):
        self.warnings.append(msg)


# ---------------------------------------------------------------------------
# Cliente HTTP (urllib)
# ---------------------------------------------------------------------------
class Response:
    def __init__(self, status, headers, data):
        self.status = status
        self.headers = headers
        self.data = data

    def header(self, name):
        if self.headers is None:
            return None
        return self.headers.get(name)


class Client:
    """Cliente mínimo da REST API do Azure DevOps.

    - Autenticação Basic com usuário vazio e o PAT como senha (base64 de ":PAT").
    - Em dry-run, só executa GET; POST/PATCH/PUT/DELETE são registrados e não enviados.
    - Repete requisições em 429/5xx respeitando Retry-After.
    """

    def __init__(self, pat, console, dry_run=False, max_retries=4, sleep=time.sleep, timeout=60):
        self._auth = None
        if pat:
            token = base64.b64encode((":" + pat).encode("utf-8")).decode("ascii")
            self._auth = "Basic " + token
        self.console = console
        self.dry_run = dry_run
        self.max_retries = max_retries
        self.sleep = sleep
        self.timeout = timeout
        self.skipped_writes = []

    @property
    def online(self):
        return self._auth is not None

    def request(self, method, url, body=None, content_type="application/json", headers=None):
        method = method.upper()
        if self.dry_run and method != "GET":
            self.skipped_writes.append((method, url))
            self.console.debug("dry-run: %s %s não enviado" % (method, _strip_query(url)))
            return None
        if not self.online:
            raise FatalError("Sem PAT: defina AZDO_PAT ou execute com --dry-run para o modo offline.")
        hdrs = {
            "Authorization": self._auth,
            "Accept": "application/json",
            "User-Agent": "fwd-ford-azure-devops-import/1.0",
        }
        if headers:
            hdrs.update(headers)
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            hdrs["Content-Type"] = content_type
        attempt = 0
        while True:
            attempt += 1
            self.console.debug("%s %s" % (method, _strip_query(url)))
            req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    status = resp.status
                    raw = resp.read()
                    resp_headers = resp.headers
            except urllib.error.HTTPError as exc:
                status = exc.code
                try:
                    raw = exc.read()
                except OSError:
                    raw = b""
                finally:
                    exc.close()
                resp_headers = exc.headers
                if (status == 429 or status >= 500) and attempt <= self.max_retries:
                    wait = _retry_after(resp_headers, attempt)
                    self.console.warn("HTTP %s em %s; nova tentativa em %ss" % (status, _strip_query(url), wait))
                    self.sleep(wait)
                    continue
                raise HttpError(status, _error_message(raw), method, url)
            except urllib.error.URLError as exc:
                if attempt <= self.max_retries:
                    wait = min(2 ** attempt, 20)
                    self.console.warn("Falha de rede (%s); nova tentativa em %ss" % (exc.reason, wait))
                    self.sleep(wait)
                    continue
                raise HttpError(0, "falha de rede: %s" % exc.reason, method, url)
            ctype = (resp_headers.get("Content-Type") or "") if resp_headers else ""
            if status == 203 or "text/html" in ctype:
                # O Azure DevOps devolve 203 + página HTML de login quando o PAT é inválido.
                raise HttpError(401, "autenticação recusada (resposta HTML/203): confira o PAT, os escopos e a organização", method, url)
            payload = None
            if raw:
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except ValueError:
                    payload = raw.decode("utf-8", "replace")
            return Response(status, resp_headers, payload)


def _retry_after(headers, attempt):
    value = headers.get("Retry-After") if headers else None
    try:
        return max(0, min(int(float(value)), 60))
    except (TypeError, ValueError):
        return min(2 ** attempt, 20)


def _error_message(raw):
    if not raw:
        return "(sem corpo)"
    try:
        body = json.loads(raw.decode("utf-8"))
        if isinstance(body, dict):
            return body.get("message") or body.get("Message") or json.dumps(body, ensure_ascii=False)[:300]
        return str(body)[:300]
    except ValueError:
        return raw.decode("utf-8", "replace")[:300]


# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------
def q(segment):
    return urllib.parse.quote(str(segment), safe="")


class Urls:
    def __init__(self, org_url, project, entitlement_base=None):
        parsed = urllib.parse.urlparse(org_url.strip())
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise FatalError("--org inválido: use https://dev.azure.com/<organizacao>")
        host = parsed.netloc.lower()
        path = parsed.path.strip("/")
        if host.endswith(".visualstudio.com"):
            self.org_name = host.split(".")[0]
            self.org = "https://dev.azure.com/%s" % self.org_name
        else:
            if not path:
                raise FatalError("--org precisa incluir o nome da organização: https://dev.azure.com/<organizacao>")
            self.org_name = path.split("/")[-1]
            self.org = "%s://%s/%s" % (parsed.scheme, parsed.netloc, path)
        self.project = project
        self.p = "%s/%s" % (self.org, q(project))
        if entitlement_base:
            self.vsaex = entitlement_base.rstrip("/")
        elif urllib.parse.urlparse(self.org).netloc.lower() == "dev.azure.com":
            self.vsaex = "https://vsaex.dev.azure.com/%s" % q(self.org_name)
        else:
            self.vsaex = self.org

    @staticmethod
    def with_params(base, **params):
        params = OrderedDict((k, v) for k, v in params.items() if v is not None)
        params["api-version"] = API_VERSION
        return base + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    # O primeiro argumento chama-se route (e não path) porque a wiki usa o parâmetro de query "path".
    def api(self, route, **params):
        return self.with_params(self.org + "/_apis/" + route, **params)

    def papi(self, route, **params):
        return self.with_params(self.p + "/_apis/" + route, **params)

    def tapi(self, team, route, **params):
        return self.with_params("%s/%s/_apis/%s" % (self.p, q(team), route), **params)

    def workitem_ref(self, wid):
        return "%s/_apis/wit/workItems/%s" % (self.org, wid)

    # Links do portal (formato usual das telas do Azure Boards).
    def web_project(self):
        return self.p

    def web_backlog(self, team, level="Backlog items"):
        return "%s/_backlogs/backlog/%s/%s" % (self.p, q(team), q(level))

    def web_board(self, team, level="Backlog items"):
        return "%s/_boards/board/t/%s/%s" % (self.p, q(team), q(level))

    def web_taskboard(self, team, sprint):
        return "%s/_sprints/taskboard/%s/%s/%s" % (self.p, q(team), q(self.project), q(sprint))

    def web_sprint_backlog(self, team, sprint):
        return "%s/_sprints/backlog/%s/%s/%s" % (self.p, q(team), q(self.project), q(sprint))

    def web_query(self, query_id):
        return "%s/_queries/query/%s/" % (self.p, query_id)

    def web_wiki(self, wiki_name):
        return "%s/_wiki/wikis/%s" % (self.p, q(wiki_name))

    def web_workitem(self, wid):
        return "%s/_workitems/edit/%s" % (self.p, wid)


# ---------------------------------------------------------------------------
# Modelo (backlog.json)
# ---------------------------------------------------------------------------
class Item:
    __slots__ = ("key", "type", "data", "parent", "children", "level")

    def __init__(self, key, type_, data, parent, level):
        self.key = key
        self.type = type_
        self.data = data
        self.parent = parent
        self.children = []
        self.level = level

    def get(self, name, default=None):
        return self.data.get(name, default)

    @property
    def title(self):
        return "[%s] %s" % (self.key, self.data["title"])


class Model:
    def __init__(self, raw, path):
        self.raw = raw
        self.path = path
        self.project = raw["project"]
        self.conventions = raw["conventions"]
        self.iterations = raw["iterations"]
        self.iteration_by_name = {i["name"]: i for i in self.iterations}
        self.items = OrderedDict()
        self.team = {m["key"]: m for m in raw["project"]["team"]}
        for epic in raw["epics"]:
            e = self._add(epic, "Epic", None, 1)
            for feat in epic["features"]:
                f = self._add(feat, "Feature", e, 2)
                for pbi in feat["pbis"]:
                    p = self._add(pbi, "Product Backlog Item", f, 3)
                    for task in pbi.get("tasks", []):
                        self._add(task, "Task", p, 4)

    def _add(self, data, type_, parent, level):
        key = data["key"]
        if key in self.items:
            raise BacklogError("chave duplicada: %s" % key)
        if data.get("type", type_) != type_:
            raise BacklogError("%s: tipo %s inesperado" % (key, data.get("type")))
        it = Item(key, type_, data, parent, level)
        self.items[key] = it
        if parent:
            parent.children.append(it)
        return it

    def of_type(self, type_):
        items = [i for i in self.items.values() if i.type == type_]
        return sorted(items, key=lambda i: i.get("rank", 0))

    def creation_order(self):
        out = []
        for t in TYPE_ORDER:
            out.extend(self.of_type(t))
        return out

    def sprint_totals(self):
        totals = OrderedDict((i["name"], 0) for i in self.iterations)
        for p in self.of_type("Product Backlog Item"):
            if p.get("iteration"):
                totals[p.get("iteration")] += p.get("effort", 0)
        return totals

    def owner_name(self, key):
        m = self.team.get(key)
        return m["name"] if m else key


def load_backlog(path):
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as exc:
        raise BacklogError("não foi possível ler %s: %s" % (path, exc))
    model = Model(raw, path)
    validate_model(model)
    return model


def validate_model(model):
    errors = []
    scale = set(model.conventions.get("planning_poker_scale", [1, 2, 3, 5, 8, 13, 21]))
    iters = set(model.iteration_by_name)
    for it in model.items.values():
        d = it.data
        if len(it.title) > 255:
            errors.append("%s: título com mais de 255 caracteres" % it.key)
        state = d.get("state")
        if state not in STATE_FLOW[it.type]:
            errors.append("%s: estado inválido %r para %s" % (it.key, state, it.type))
        if d.get("priority") not in (1, 2, 3, 4) and it.type != "Task":
            errors.append("%s: prioridade deve ser 1 a 4" % it.key)
        if d.get("iteration") and d["iteration"] not in iters:
            errors.append("%s: sprint desconhecida %r" % (it.key, d["iteration"]))
        for tag in d.get("tags", []):
            if "," in tag or ";" in tag or tag.startswith("@") or len(tag) > 400:
                errors.append("%s: tag inválida %r" % (it.key, tag))
        if it.type == "Product Backlog Item":
            if d.get("effort") not in scale:
                errors.append("%s: esforço fora da escala Planning Poker" % it.key)
            story = d.get("story") or {}
            if not all(story.get(k) for k in ("como", "quero", "para")):
                errors.append("%s: história incompleta (Como/quero/para)" % it.key)
            tipos = {c.get("tipo") for c in (d.get("acceptance") or {}).get("cenarios", [])}
            if "feliz" not in tipos or not tipos & {"erro", "borda"}:
                errors.append("%s: critérios BDD precisam de caminho feliz e de erro/borda" % it.key)
        if it.type == "Task":
            if not isinstance(d.get("remaining_hours"), (int, float)) or d.get("activity") not in model.conventions.get("activities", []):
                errors.append("%s: tarefa sem horas ou atividade válida" % it.key)
        for pred in d.get("predecessors", []):
            if pred not in model.items:
                errors.append("%s: predecessora inexistente %s" % (it.key, pred))
            elif model.items[pred].type != it.type:
                errors.append("%s: predecessora %s de outro tipo" % (it.key, pred))
    # ciclo nas dependências
    graph = {k: list(i.get("predecessors", [])) for k, i in model.items.items()}
    visiting, done = set(), set()

    def visit(node, stack):
        if node in done:
            return
        if node in visiting:
            errors.append("ciclo de dependência: %s" % " -> ".join(stack + [node]))
            return
        visiting.add(node)
        for nxt in graph.get(node, []):
            if nxt in graph:
                visit(nxt, stack + [node])
        visiting.discard(node)
        done.add(node)

    for k in graph:
        visit(k, [])
    if errors:
        raise BacklogError("backlog.json inválido:\n  - " + "\n  - ".join(errors))


# ---------------------------------------------------------------------------
# Renderização HTML (campos rich-text do Azure Boards)
# ---------------------------------------------------------------------------
def esc(text):
    return html.escape(str(text), quote=False)


TIPO_LABEL = {"feliz": "caminho feliz", "erro": "erro", "borda": "caso de borda"}


def render_gherkin_html(acc):
    if not acc:
        return ""
    parts = ["<p><b>Funcionalidade:</b> %s</p>" % esc(acc["funcionalidade"])]
    for n, sc in enumerate(acc.get("cenarios", []), start=1):
        lines = ["<b>Cenário %d: %s</b> <i>(%s)</i>" % (n, esc(sc["titulo"]), TIPO_LABEL.get(sc["tipo"], sc["tipo"]))]
        for step in sc["passos"]:
            kw, _, rest = step.partition(" ")
            lines.append("&nbsp;&nbsp;<b>%s</b> %s" % (esc(kw), esc(rest)))
        parts.append("<p>%s</p>" % "<br>".join(lines))
    return "".join(parts)


def render_gherkin_text(acc):
    if not acc:
        return ""
    out = ["Funcionalidade: %s" % acc["funcionalidade"]]
    for sc in acc.get("cenarios", []):
        out.append("")
        out.append("  Cenário: %s (%s)" % (sc["titulo"], TIPO_LABEL.get(sc["tipo"], sc["tipo"])))
        for step in sc["passos"]:
            out.append("    %s" % step)
    return "\n".join(out)


def _ul(items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(i) for i in items)


def _ol(items):
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % esc(i) for i in items)


def _sprint_label(model, name):
    if not name:
        return "Backlog futuro (sem sprint)"
    it = model.iteration_by_name.get(name)
    if not it:
        return name
    return "%s (%s a %s)" % (name, _br_date(it["start"]), _br_date(it["finish"]))


def _br_date(iso):
    y, m, d = iso[:10].split("-")
    return "%s/%s/%s" % (d, m, y)


def _req_label(req):
    return ARCHIMATE_REQUIREMENTS.get(req, req)


def _key_list(model, keys):
    out = []
    for k in keys:
        it = model.items.get(k)
        out.append("%s %s" % (k, it.data["title"]) if it else k)
    return out


def render_description(model, item):
    d = item.data
    dod = model.raw["definition_of_done"]
    parts = []
    if item.type == "Product Backlog Item":
        st = d["story"]
        parts.append("<p><b>História de usuário</b><br>Como <b>%s</b>, quero <b>%s</b>, para <b>%s</b>.</p>"
                     % (esc(st["como"]), esc(st["quero"]), esc(st["para"])))
        parts.append("<p><b>Contexto técnico</b><br>%s</p>" % esc(d.get("context", "")))
        plan = [
            "Sprint: %s" % _sprint_label(model, d.get("iteration")),
            "Prioridade: %s (MoSCoW) = Priority %s" % (d["moscow"], d["priority"]),
            "Esforço: %s pontos (Planning Poker, Fibonacci). Valor de negócio: %s" % (d["effort"], d["business_value"]),
            "Responsável: %s" % model.owner_name(d.get("owner")),
            "Ordem de implementação no backlog: %sº" % d.get("rank"),
            "Predecessoras: %s" % ("; ".join(_key_list(model, d.get("predecessors", []))) or "nenhuma"),
        ]
        parts.append("<p><b>Planejamento</b></p>" + _ul(plan))
        trace = ["Elementos ArchiMate: %s" % ("; ".join(d.get("archimate", [])) or "n/a"),
                 "Requisitos de qualidade: %s" % ("; ".join(_req_label(r) for r in d.get("requirements", [])) or "nenhum específico"),
                 "Feature: %s. Épico: %s" % (item.parent.title, item.parent.parent.title)]
        parts.append("<p><b>Rastreabilidade TOGAF/ArchiMate</b></p>" + _ul(trace))
        parts.append("<p><b>Critérios de Pronto (DoD)</b></p>" + _ol(list(dod["Product Backlog Item"]) + list(d.get("dod_extra", []))))
        if d.get("evidence"):
            parts.append("<p><b>Evidência de entrega</b><br>%s</p>" % esc(d["evidence"]))
    elif item.type == "Task":
        parts.append("<p>%s</p>" % esc(d.get("description", "")))
        plan = [
            "Atividade: %s" % d["activity"],
            "Estimativa: %s h. Restante: %s h. Complexidade: %s pontos (Fibonacci)" % (d["estimate_hours"], d["remaining_hours"], d["complexity_points"]),
            "Responsável: %s" % model.owner_name(d.get("owner")),
            "Predecessoras técnicas: %s" % ("; ".join(_key_list(model, d.get("predecessors", []))) or "nenhuma"),
            "PBI: %s" % item.parent.title,
        ]
        parts.append(_ul(plan))
        parts.append("<p><b>Critérios de Pronto da tarefa</b></p>" + _ol(dod["Task"]))
    elif item.type == "Feature":
        parts.append("<p><b>Objetivo</b><br>%s</p>" % esc(d["objective"]))
        parts.append("<p><b>Persona principal:</b> %s</p>" % esc(d["persona"]))
        kids = ["%s (%s, %s pts, %s)" % (c.title, c.get("iteration") or "backlog futuro", c.get("effort"), c.get("state")) for c in item.children]
        parts.append("<p><b>PBIs</b></p>" + _ul(kids))
        trace = ["Elementos ArchiMate: %s" % "; ".join(d.get("archimate", [])),
                 "Requisitos de qualidade: %s" % ("; ".join(_req_label(r) for r in d.get("requirements", [])) or "nenhum específico"),
                 "Épico: %s" % item.parent.title,
                 "Esforço total: %s pontos. Prioridade: %s (Priority %s)" % (d["effort"], d["moscow"], d["priority"])]
        parts.append("<p><b>Rastreabilidade e planejamento</b></p>" + _ul(trace))
        parts.append("<p><b>Critérios de Pronto (DoD da Feature)</b></p>" + _ol(dod["Feature"]))
    else:  # Epic
        parts.append("<p><b>Objetivo</b><br>%s</p>" % esc(d["objective"]))
        parts.append("<p><b>Hipótese de valor</b><br>%s</p>" % esc(d["value_hypothesis"]))
        parts.append("<p><b>Métricas de sucesso</b></p>" + _ul(d.get("success_metrics", [])))
        kids = ["%s (%s pts, %s)" % (c.title, c.get("effort"), c.get("state")) for c in item.children]
        parts.append("<p><b>Features</b></p>" + _ul(kids))
        trace = ["Pilar: %s" % d.get("pillar", ""),
                 "Elementos ArchiMate: %s" % "; ".join(d.get("archimate", [])),
                 "Requisitos de qualidade: %s" % ("; ".join(_req_label(r) for r in d.get("requirements", [])) or "nenhum específico"),
                 "Esforço total: %s pontos. Prioridade: %s (Priority %s)" % (d["effort"], d["moscow"], d["priority"])]
        parts.append("<p><b>Rastreabilidade e planejamento</b></p>" + _ul(trace))
        parts.append("<p><b>Critérios de Pronto (DoD do Épico)</b></p>" + _ol(dod["Epic"]))
    parts.append("<p><i>Chave de rastreio %s, gerada a partir de forward-docs/academic/qa/sprint3/backlog.json.</i></p>" % esc(item.key))
    return "".join(parts)


def render_acceptance(model, item):
    d = item.data
    if item.type in ("Product Backlog Item", "Feature"):
        return render_gherkin_html(d.get("acceptance"))
    if item.type == "Epic":
        return "<p><b>Critérios de aceite do épico</b></p>" + _ul(d.get("acceptance_list", []))
    return ""


def iteration_path(model, name):
    project = model.project["name"]
    return "%s\\%s" % (project, name) if name else project


def _date_field(iso):
    # Meio-dia UTC evita que o portal mostre o dia anterior no fuso de Brasília.
    return "%sT12:00:00Z" % iso[:10]


def desired_fields(model, item, project_name, assign_map):
    d = item.data
    fields = OrderedDict()
    fields[F_TITLE] = item.title
    fields[F_DESCRIPTION] = render_description(model, item)
    if item.type != "Task":
        fields[F_ACCEPTANCE] = render_acceptance(model, item)
        fields[F_EFFORT] = d.get("effort")
        fields[F_BUSINESS_VALUE] = d.get("business_value")
        fields[F_PRIORITY] = d.get("priority")
    else:
        fields[F_PRIORITY] = item.parent.get("priority")
        fields[F_REMAINING] = d.get("remaining_hours")
        fields[F_ACTIVITY] = d.get("activity")
    fields[F_BACKLOG_PRIORITY] = d.get("backlog_priority")
    if item.type in ("Epic", "Feature"):
        if d.get("start_date"):
            fields[F_START] = _date_field(d["start_date"])
        if d.get("target_date"):
            fields[F_TARGET] = _date_field(d["target_date"])
    fields[F_ITERATION] = "%s\\%s" % (project_name, d["iteration"]) if d.get("iteration") else project_name
    fields[F_TAGS] = "; ".join(d.get("tags", []))
    owner = d.get("owner")
    if assign_map and owner and assign_map.get(owner):
        fields[F_ASSIGNED] = assign_map[owner]
    return OrderedDict((k, v) for k, v in fields.items() if v is not None and v != "")


# ---------------------------------------------------------------------------
# Importador
# ---------------------------------------------------------------------------
class Importer:
    def __init__(self, args, model, client, urls, console, summary):
        self.args = args
        self.model = model
        self.client = client
        self.urls = urls
        self.c = console
        self.s = summary
        self.project = None
        self.project_id = None
        self.team_id = None
        self.team_name = model.project.get("default_team") or (args.project + " Team")
        self.iteration_ids = {}
        self.type_fields = {}
        self.existing = {}          # key -> {"id", "rev", "fields", "relations"}
        self.ids = {}               # key -> id
        self.new_keys = set()
        self.query_ids = OrderedDict()
        self.wiki = None
        self.warned_fields = set()
        self.lag_retries_left = 12   # orçamento total de novas tentativas por atraso de propagação da sprint
        self.assign_map = {}
        if args.assign_map:
            with open(args.assign_map, encoding="utf-8") as fh:
                self.assign_map = json.load(fh)

    @property
    def dry(self):
        return self.args.dry_run

    @property
    def online(self):
        return self.client.online

    # ---------------- 1. acesso e projeto ----------------
    def step_project(self):
        self.c.title("1/8 Organização e projeto (processo Scrum)")
        if not self.online:
            self.c.plan("modo offline: sem PAT, nenhuma chamada HTTP será feita")
            self.c.plan("verificaria o acesso em GET %s" % _strip_query(self.urls.api("projects")))
            self.c.plan("criaria o projeto %r com o processo Scrum (templateTypeId %s) se ele não existir" % (self.args.project, SCRUM_PROCESS_TYPE_ID))
            return
        try:
            self.client.request("GET", self.urls.api("projects", **{"$top": 1}))
        except HttpError as exc:
            if exc.status in (401, 403):
                raise FatalError("Acesso negado à organização %s (HTTP %s). Confira se o PAT está válido, se foi criado para esta organização e se tem os escopos pedidos no PLANO (Work Items, Project and Team, Wiki, Member Entitlement Management)." % (self.urls.org, exc.status))
            if exc.status == 404:
                raise FatalError("Organização não encontrada: %s" % self.urls.org)
            raise FatalError(str(exc))
        self.c.ok("acesso à organização %s confirmado" % self.urls.org)
        project = self._get_project()
        if project is None:
            if self.dry:
                self.c.plan("projeto %r não existe: seria criado com o processo Scrum" % self.args.project)
                return
            project = self._create_project()
        else:
            self.c.skip("projeto %r já existe (id %s)" % (project["name"], project["id"]))
            self._check_scrum(project)
        self.project = project
        self.project_id = project["id"]
        team = project.get("defaultTeam") or {}
        if team.get("id"):
            self.team_id = team["id"]
            self.team_name = team.get("name") or self.team_name
        self.c.ok("time padrão: %s" % self.team_name)

    def _get_project(self):
        try:
            r = self.client.request("GET", self.urls.api("projects/%s" % q(self.args.project), includeCapabilities="true"))
            return r.data
        except HttpError as exc:
            if exc.status == 404:
                return None
            raise FatalError("Falha ao consultar o projeto: %s" % exc)

    def _scrum_process_id(self):
        try:
            r = self.client.request("GET", self.urls.api("process/processes"))
            for proc in (r.data or {}).get("value", []):
                if proc.get("name") == "Scrum":
                    return proc["id"]
        except HttpError as exc:
            self.c.warn("não foi possível listar os processos (%s); usando o id padrão do Scrum" % exc.status)
        return SCRUM_PROCESS_TYPE_ID

    def _create_project(self):
        process_id = self._scrum_process_id()
        body = {
            "name": self.args.project,
            "description": self.model.project.get("description", ""),
            "visibility": "private",
            "capabilities": {
                "versioncontrol": {"sourceControlType": "Git"},
                "processTemplate": {"templateTypeId": process_id},
            },
        }
        try:
            r = self.client.request("POST", self.urls.api("projects"), body)
        except HttpError as exc:
            raise FatalError("Não foi possível criar o projeto: %s" % exc)
        op = r.data or {}
        self.c.info("criação do projeto enfileirada (operação %s)" % op.get("id"))
        deadline = time.monotonic() + self.args.poll_timeout
        status = op.get("status")
        while status not in ("succeeded", "failed", "cancelled"):
            if time.monotonic() > deadline:
                raise FatalError("Tempo esgotado aguardando a criação do projeto; rode o script de novo em alguns minutos.")
            self.client.sleep(self.args.poll_interval)
            try:
                status = (self.client.request("GET", self.urls.api("operations/%s" % op.get("id"))).data or {}).get("status")
            except HttpError as exc:
                self.c.warn("falha ao consultar a operação (%s); tentando de novo" % exc.status)
        if status != "succeeded":
            raise FatalError("A criação do projeto terminou com status %s" % status)
        project = None
        for _ in range(10):
            project = self._get_project()
            if project and project.get("state", "wellFormed") == "wellFormed":
                break
            self.client.sleep(self.args.poll_interval)
        if not project:
            raise FatalError("Projeto criado mas não encontrado na consulta seguinte")
        self.c.created("projeto %r criado com o processo Scrum" % project["name"])
        self.s.inc("projeto criado")
        return project

    def _check_scrum(self, project):
        tmpl = ((project.get("capabilities") or {}).get("processTemplate") or {})
        name = tmpl.get("templateName")
        type_id = tmpl.get("templateTypeId")
        if name == "Scrum" or (type_id or "").lower() == SCRUM_PROCESS_TYPE_ID:
            self.c.ok("processo do projeto: Scrum")
            return
        # Processo herdado do Scrum: aceita se o tipo Product Backlog Item existe.
        try:
            self.client.request("GET", self.urls.papi("wit/workitemtypes/%s" % q("Product Backlog Item")))
            self.c.warn("processo %r não é o Scrum de sistema, mas tem Product Backlog Item (herdado do Scrum); seguindo" % name)
            self.s.warning("processo herdado: %s" % name)
        except HttpError:
            raise FatalError("O projeto %r usa o processo %r, não o Scrum. Crie o projeto com o processo Scrum ou use --project com outro nome; nada foi alterado." % (project.get("name"), name))

    # ---------------- 2. sprints ----------------
    def step_iterations(self):
        self.c.title("2/8 Sprints (iterações) e seleção no time")
        wanted = self.model.iterations
        if not self.online or not self.project_id:
            for it in wanted:
                self.c.plan("criaria ou atualizaria %s: %s a %s" % (it["name"], it["start"], it["finish"]))
            self.c.plan("adicionaria as %d sprints ao time %s" % (len(wanted), self.team_name))
            return
        root = self.client.request("GET", self.urls.papi("wit/classificationnodes/Iterations", **{"$depth": 2})).data or {}
        children = {c.get("name"): c for c in (root.get("children") or [])}
        for it in wanted:
            # Datas de sprint são "date-only, correct unadjusted at midnight in UTC" (TeamIterationAttributes,
            # Microsoft Learn); os exemplos de Classification Nodes usam o mesmo formato T00:00:00Z.
            attrs = {"startDate": "%sT00:00:00Z" % it["start"], "finishDate": "%sT00:00:00Z" % it["finish"]}
            node = children.get(it["name"])
            try:
                if node is None:
                    if self.dry:
                        self.c.plan("criaria a sprint %s (%s a %s)" % (it["name"], it["start"], it["finish"]))
                        continue
                    r = self.client.request("POST", self.urls.papi("wit/classificationnodes/Iterations"), {"name": it["name"], "attributes": attrs})
                    node = r.data
                    self.c.created("sprint %s (%s a %s)" % (it["name"], it["start"], it["finish"]))
                    self.s.inc("sprints criadas")
                else:
                    cur = node.get("attributes") or {}
                    same = (str(cur.get("startDate", ""))[:10] == it["start"] and str(cur.get("finishDate", ""))[:10] == it["finish"])
                    if same:
                        self.c.skip("sprint %s com as datas corretas" % it["name"])
                    elif self.dry:
                        self.c.plan("atualizaria as datas da sprint %s" % it["name"])
                    else:
                        r = self.client.request("PATCH", self.urls.papi("wit/classificationnodes/Iterations/%s" % q(it["name"])), {"attributes": attrs})
                        node = r.data or node
                        self.c.updated("datas da sprint %s (%s a %s)" % (it["name"], it["start"], it["finish"]))
                        self.s.inc("sprints atualizadas")
                if node and node.get("identifier"):
                    self.iteration_ids[it["name"]] = node["identifier"]
            except HttpError as exc:
                self.c.error("sprint %s: %s" % (it["name"], exc))
                self.s.error("sprint %s: %s" % (it["name"], exc))
        team = self.team_id or self.team_name
        try:
            r = self.client.request("GET", self.urls.tapi(team, "work/teamsettings/iterations"))
            data = r.data or {}
            selected = {x.get("id") for x in (data.get("value") or data.get("values") or [])}
        except HttpError as exc:
            self.c.error("não foi possível ler as sprints do time: %s" % exc)
            self.s.error("sprints do time: %s" % exc)
            return
        for it in wanted:
            ident = self.iteration_ids.get(it["name"])
            if not ident:
                continue
            if ident in selected:
                self.c.skip("%s já selecionada no time" % it["name"])
                continue
            if self.dry:
                self.c.plan("adicionaria %s ao time" % it["name"])
                continue
            try:
                self.client.request("POST", self.urls.tapi(team, "work/teamsettings/iterations"), {"id": ident})
                self.c.created("%s adicionada ao time %s" % (it["name"], self.team_name))
                self.s.inc("sprints adicionadas ao time")
            except HttpError as exc:
                self.c.error("adicionar %s ao time: %s" % (it["name"], exc))
                self.s.error("time/%s: %s" % (it["name"], exc))

    # ---------------- 3. DoD no board ----------------
    def step_board(self):
        self.c.title("3/8 Definition of Done nas colunas do board")
        dor = self.model.raw["definition_of_ready"]
        dod = self.model.raw["definition_of_done"]["Product Backlog Item"]
        texts = self.model.conventions.get("board_column_texts") or {
            "Approved": "Pronto para a sprint (Definition of Ready):\n" + "\n".join("- " + x for x in dor),
            "Committed": "Definition of Done do PBI:\n" + "\n".join("- " + x for x in dod),
        }
        if not self.online or not self.project_id:
            self.c.plan("gravaria a DoR na coluna Approved e a DoD na coluna Committed do board Backlog items")
            return
        team = self.team_id or self.team_name
        try:
            boards = (self.client.request("GET", self.urls.tapi(team, "work/boards")).data or {}).get("value", [])
            board = next((b for b in boards if (b.get("name") or "").lower() == "backlog items"), None)
            board = board or next((b for b in boards if "backlog" in (b.get("name") or "").lower()), None)
            if not board:
                self.c.warn("board de Backlog items não encontrado; DoD fica apenas na wiki")
                return
            ref = board.get("id") or board.get("name")
            cols = (self.client.request("GET", self.urls.tapi(team, "work/boards/%s/columns" % q(ref))).data or {}).get("value", [])
            changed = False
            for col in cols:
                if col.get("columnType") == "inProgress" and col.get("name") in texts:
                    if (col.get("description") or "") != texts[col["name"]]:
                        col["description"] = texts[col["name"]]
                        changed = True
            if not changed:
                self.c.skip("DoR e DoD já registradas nas colunas do board")
                return
            if self.dry:
                self.c.plan("atualizaria as colunas Approved/Committed com DoR e DoD")
                return
            self.client.request("PUT", self.urls.tapi(team, "work/boards/%s/columns" % q(ref)), cols)
            self.c.updated("DoR (Approved) e DoD (Committed) gravadas no board %s" % board.get("name"))
            self.s.inc("colunas do board atualizadas")
        except HttpError as exc:
            self.c.warn("não foi possível gravar a DoD no board (%s); ela continua na wiki e em cada PBI" % exc)
            self.s.warning("board DoD: %s" % exc)

    # ---------------- 4. itens de trabalho ----------------
    def _load_type_fields(self):
        for t in TYPE_ORDER:
            if not self.online or not self.project_id:
                self.type_fields[t] = None
                continue
            try:
                r = self.client.request("GET", self.urls.papi("wit/workitemtypes/%s/fields" % q(t)))
                self.type_fields[t] = {f.get("referenceName") for f in (r.data or {}).get("value", [])}
            except HttpError as exc:
                if exc.status == 404:
                    raise FatalError("O tipo %r não existe no projeto: o processo não é Scrum." % t)
                self.c.warn("não foi possível listar os campos de %s (%s); todos os campos serão enviados" % (t, exc.status))
                self.type_fields[t] = None

    def _lookup_existing(self):
        if not self.online or not self.project_id:
            return
        if self.dry:
            self.c.plan("dry-run: a consulta WIQL (POST) não é executada; itens existentes não são verificados")
            return
        tag = self.model.conventions.get("import_tag", "fwd-import")
        wiql = ("SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project "
                "AND [System.Tags] CONTAINS '%s' ORDER BY [System.Id]" % tag)
        r = self.client.request("POST", self.urls.papi("wit/wiql"), {"query": wiql})
        ids = [w["id"] for w in (r.data or {}).get("workItems", [])]
        for i in range(0, len(ids), 200):
            chunk = ids[i:i + 200]
            rb = self.client.request("POST", self.urls.papi("wit/workitemsbatch"), {"ids": chunk, "$expand": "Relations", "errorPolicy": "Omit"})
            for wi in (rb.data or {}).get("value", []):
                if not wi:
                    continue
                fields = wi.get("fields") or {}
                m = KEY_RE.match(fields.get(F_TITLE, ""))
                if not m:
                    continue
                key = m.group(1)
                if key in self.existing:
                    self.c.warn("chave %s aparece em mais de um item (ids %s e %s); usando o menor" % (key, self.existing[key]["id"], wi["id"]))
                    continue
                self.existing[key] = {"id": wi["id"], "rev": wi.get("rev"), "fields": fields, "relations": wi.get("relations") or []}
        self.c.info("%d itens deste plano já existem no projeto" % len(self.existing))

    def _ops_for(self, item):
        project_name = (self.project or {}).get("name") or self.args.project
        fields = desired_fields(self.model, item, project_name, self.assign_map)
        allowed = self.type_fields.get(item.type)
        ops = []
        for ref, value in fields.items():
            if allowed is not None and ref not in allowed:
                if (item.type, ref) not in self.warned_fields:
                    self.warned_fields.add((item.type, ref))
                    self.c.warn("campo %s não existe em %s neste processo; ignorado" % (ref, item.type))
                    self.s.warning("campo ausente: %s/%s" % (item.type, ref))
                continue
            ops.append({"op": "add", "path": "/fields/%s" % ref, "value": value})
        ops.append({"op": "add", "path": "/fields/%s" % F_HISTORY,
                    "value": "Importado de backlog.json (chave %s) pelo azure_devops_import.py." % item.key})
        return ops

    def step_workitems(self):
        self.c.title("4/8 Épicos, features, PBIs e tarefas")
        self._load_type_fields()
        self._lookup_existing()
        order = self.model.creation_order()
        fake_id = 0
        for item in order:
            parent_id = self.ids.get(item.parent.key) if item.parent else None
            if item.key in self.existing:
                ex = self.existing[item.key]
                self.ids[item.key] = ex["id"]
                self.c.skip("%s %s (#%s)" % (item.type, item.title, ex["id"]))
                self.s.inc("itens já existentes")
                self._ensure_parent(item, ex)
                if self.args.sync_fields:
                    self._sync_fields(item, ex)
                if self.args.sync_state:
                    self._ensure_state(item, ex["id"], (ex["fields"] or {}).get(F_STATE))
                continue
            ops = self._ops_for(item)
            if item.parent:
                if parent_id is None and not self.dry:
                    self.c.error("%s: pai %s não foi criado; item ignorado" % (item.key, item.parent.key))
                    self.s.error("%s sem pai" % item.key)
                    continue
                ops.append({"op": "add", "path": "/relations/-", "value": {
                    "rel": LINK_PARENT, "url": self.urls.workitem_ref(parent_id if parent_id is not None else 0),
                    "attributes": {"comment": "Hierarquia de backlog.json"}}})
            url = self.urls.papi("wit/workitems/$%s" % q(item.type), suppressNotifications="true" if self.args.suppress_notifications else None)
            if self.dry:
                fake_id += 1
                self.ids[item.key] = "novo-%d" % fake_id
                self.new_keys.add(item.key)
                extra = item.get("iteration") or "sem sprint"
                self.c.plan("criaria %s %s [%s, %s]" % (item.type, item.title, extra, item.get("state")))
                self.s.inc("itens que seriam criados")
                continue
            try:
                r = self._create_with_retry(url, ops)
                wid = (r.data or {}).get("id")
                self.ids[item.key] = wid
                self.new_keys.add(item.key)
                self.c.created("%s %s (#%s)" % (item.type, item.title, wid))
                self.s.inc("itens criados")
                self._ensure_state(item, wid, INITIAL_STATE[item.type])
            except HttpError as exc:
                self.c.error("%s: %s" % (item.key, exc))
                self.s.error("criar %s: %s" % (item.key, exc.message))

    def _sync_fields(self, item, existing):
        """Regrava no Azure só os campos que divergem do backlog.json (opção --sync-fields)."""
        current = existing.get("fields") or {}
        ops = []
        for op in self._ops_for(item):
            ref = op["path"][len("/fields/"):]
            if ref != F_HISTORY and not _same_value(ref, current.get(ref), op["value"]):
                ops.append(op)
        if not ops:
            return
        names = ", ".join(op["path"][len("/fields/"):] for op in ops)
        try:
            self.client.request("PATCH", self.urls.papi("wit/workitems/%s" % existing["id"]), ops,
                                content_type="application/json-patch+json")
            self.c.updated("%s: %s" % (item.key, names))
            self.s.inc("itens com campos atualizados")
        except HttpError as exc:
            self.c.error("campos de %s: %s" % (item.key, exc))
            self.s.error("campos %s: %s" % (item.key, exc.message))

    def _create_with_retry(self, url, ops, attempts=4):
        """Cria o item; repete se a sprint recém-criada ainda não propagou (TF401347 / IterationPath)."""
        for n in range(1, attempts + 1):
            try:
                return self.client.request("POST", url, ops, content_type="application/json-patch+json")
            except HttpError as exc:
                lag = exc.status == 400 and ("TF401347" in exc.message or "IterationPath" in exc.message)
                if not lag or n == attempts or self.lag_retries_left <= 0:
                    raise
                self.lag_retries_left -= 1
                self.c.warn("sprint ainda não disponível para itens (%s); nova tentativa em 5s" % exc.message[:80])
                self.client.sleep(5)

    def _ensure_parent(self, item, existing):
        if not item.parent:
            return
        parent_id = self.ids.get(item.parent.key)
        if parent_id is None:
            return
        rels = [r for r in existing.get("relations", []) if r.get("rel") == LINK_PARENT]
        if any(_rel_target(r) == str(parent_id) for r in rels):
            return
        if rels:
            self.c.warn("%s já tem outro pai (#%s); a hierarquia não foi alterada" % (item.key, _rel_target(rels[0])))
            self.s.warning("%s com outro pai" % item.key)
            return
        if self.dry:
            self.c.plan("ligaria %s ao pai %s" % (item.key, item.parent.key))
            return
        try:
            self.client.request("PATCH", self.urls.papi("wit/workitems/%s" % existing["id"]), [
                {"op": "add", "path": "/relations/-", "value": {"rel": LINK_PARENT, "url": self.urls.workitem_ref(parent_id),
                                                                "attributes": {"comment": "Hierarquia de backlog.json"}}}],
                content_type="application/json-patch+json")
            self.c.updated("%s ligado ao pai %s" % (item.key, item.parent.key))
            self.s.inc("links pai/filho adicionados")
        except HttpError as exc:
            self.c.error("pai de %s: %s" % (item.key, exc))
            self.s.error("pai %s: %s" % (item.key, exc.message))

    def _ensure_state(self, item, wid, current):
        target = item.get("state")
        if not target or target == current:
            return
        if self.dry:
            self.c.plan("mudaria o estado de %s para %s" % (item.key, target))
            return
        flow = STATE_FLOW[item.type]
        try:
            self._patch_state(wid, target)
        except HttpError as exc:
            # Se a transição direta for recusada, percorre os estados intermediários.
            if exc.status == 400 and current in flow and target in flow and flow.index(target) > flow.index(current) + 1:
                try:
                    for st in flow[flow.index(current) + 1:flow.index(target) + 1]:
                        self._patch_state(wid, st)
                except HttpError as exc2:
                    self.c.error("estado de %s: %s" % (item.key, exc2))
                    self.s.error("estado %s: %s" % (item.key, exc2.message))
                    return
            else:
                self.c.error("estado de %s: %s" % (item.key, exc))
                self.s.error("estado %s: %s" % (item.key, exc.message))
                return
        self.c.updated("%s -> %s" % (item.key, target))
        self.s.inc("estados definidos")

    def _patch_state(self, wid, state):
        self.client.request("PATCH", self.urls.papi("wit/workitems/%s" % wid),
                            [{"op": "add", "path": "/fields/%s" % F_STATE, "value": state}],
                            content_type="application/json-patch+json")

    # ---------------- 5. predecessoras ----------------
    def step_links(self):
        self.c.title("5/8 Dependências (predecessora -> sucessora)")
        total = 0
        for item in self.model.creation_order():
            preds = item.get("predecessors", [])
            if not preds:
                continue
            wid = self.ids.get(item.key)
            if wid is None:
                self.c.warn("%s não existe; dependências ignoradas" % item.key)
                continue
            existing_rel = []
            if item.key in self.existing:
                existing_rel = self.existing[item.key].get("relations", [])
            have = {_rel_target(r) for r in existing_rel if r.get("rel") == LINK_PREDECESSOR}
            missing = []
            for pk in preds:
                pid = self.ids.get(pk)
                if pid is None:
                    self.c.warn("%s: predecessora %s não existe; link ignorado" % (item.key, pk))
                    continue
                if str(pid) in have:
                    continue
                missing.append((pk, pid))
            if not missing:
                continue
            total += len(missing)
            if self.dry or not self.online:
                self.c.plan("%s teria como predecessoras %s" % (item.key, ", ".join(pk for pk, _ in missing)))
                continue
            ops = [{"op": "add", "path": "/relations/-", "value": {
                "rel": LINK_PREDECESSOR, "url": self.urls.workitem_ref(pid),
                "attributes": {"comment": "Predecessora (%s) conforme backlog.json" % pk}}} for pk, pid in missing]
            try:
                self.client.request("PATCH", self.urls.papi("wit/workitems/%s" % wid), ops, content_type="application/json-patch+json")
                self.c.created("%s <- predecessoras %s" % (item.key, ", ".join(pk for pk, _ in missing)))
                self.s.inc("links predecessora", len(missing))
            except HttpError as exc:
                self.c.error("dependências de %s: %s" % (item.key, exc))
                self.s.error("links %s: %s" % (item.key, exc.message))
        if total == 0:
            self.c.skip("todas as dependências já existem")

    # ---------------- 6. consultas ----------------
    def queries_spec(self):
        project = self.args.project
        cols = "[System.Id], [System.WorkItemType], [System.Title], [System.State], [System.IterationPath], [Microsoft.VSTS.Common.Priority], [Microsoft.VSTS.Scheduling.Effort], [System.Tags]"
        return OrderedDict([
            ("01 Backlog ordenado (PBIs por ordem de implementação)",
             "SELECT %s FROM WorkItems WHERE [System.TeamProject] = @project AND [System.WorkItemType] = 'Product Backlog Item' "
             "AND [System.Tags] CONTAINS 'fwd-import' ORDER BY [Microsoft.VSTS.Common.BacklogPriority] ASC" % cols),
            ("02 Hierarquia de épicos, features e PBIs",
             "SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.Effort], [System.IterationPath] "
             "FROM WorkItemLinks WHERE ([Source].[System.TeamProject] = @project AND [Source].[System.WorkItemType] = 'Epic') "
             "AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward') "
             # Consultas em árvore (MODE Recursive) não aceitam ORDER BY nem ASOF (WIQL syntax, Microsoft Learn).
             "AND ([Target].[System.WorkItemType] IN ('Feature', 'Product Backlog Item')) MODE (Recursive)"),
            ("03 Dependências (item e suas predecessoras)",
             "SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State], [System.IterationPath] "
             "FROM WorkItemLinks WHERE ([Source].[System.TeamProject] = @project AND [Source].[System.Tags] CONTAINS 'fwd-import') "
             "AND ([System.Links.LinkType] = 'System.LinkTypes.Dependency-Reverse') "
             "AND ([Target].[System.Tags] CONTAINS 'fwd-import') ORDER BY [System.Id] ASC MODE (MustContain)"),
            ("04 Sprint 3 PBIs e tarefas",
             "SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State], [System.AssignedTo], [Microsoft.VSTS.Common.Activity], "
             "[Microsoft.VSTS.Scheduling.RemainingWork], [Microsoft.VSTS.Scheduling.Effort] FROM WorkItemLinks "
             "WHERE ([Source].[System.TeamProject] = @project AND [Source].[System.WorkItemType] = 'Product Backlog Item' "
             "AND [Source].[System.IterationPath] = '%s\\Sprint 3') AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward') "
             "AND ([Target].[System.WorkItemType] = 'Task') ORDER BY [Microsoft.VSTS.Common.BacklogPriority] ASC MODE (MayContain)" % project),
            ("05 Release plan (PBIs por sprint)",
             "SELECT %s FROM WorkItems WHERE [System.TeamProject] = @project AND [System.WorkItemType] = 'Product Backlog Item' "
             "AND [System.Tags] CONTAINS 'fwd-import' ORDER BY [System.IterationPath] ASC, [Microsoft.VSTS.Common.BacklogPriority] ASC" % cols),
            ("06 MoSCoW Must (Priority 1)",
             "SELECT %s FROM WorkItems WHERE [System.TeamProject] = @project AND [System.WorkItemType] = 'Product Backlog Item' "
             "AND [Microsoft.VSTS.Common.Priority] = 1 ORDER BY [Microsoft.VSTS.Common.BacklogPriority] ASC" % cols),
        ])

    def step_queries(self):
        self.c.title("6/8 Consultas compartilhadas")
        folder = self.args.query_folder
        spec = self.queries_spec()
        if not self.online or not self.project_id:
            self.c.plan("criaria a pasta Shared Queries/%s com %d consultas" % (folder, len(spec)))
            for name in spec:
                self.c.plan("  consulta: %s" % name)
            return
        folder_path = "Shared Queries/%s" % folder
        folder_url = self.urls.papi("wit/queries/%s" % "/".join(q(s) for s in folder_path.split("/")), **{"$depth": 1})
        children = {}
        try:
            fdata = self.client.request("GET", folder_url).data or {}
            children = {ch.get("name"): ch.get("id") for ch in (fdata.get("children") or [])}
            self.c.skip("pasta %s" % folder_path)
        except HttpError as exc:
            if exc.status != 404:
                self.c.error("consultas: %s" % exc)
                self.s.error("consultas: %s" % exc.message)
                return
            if self.dry:
                self.c.plan("criaria a pasta %s" % folder_path)
            else:
                try:
                    self.client.request("POST", self.urls.papi("wit/queries/%s" % q("Shared Queries")), {"name": folder, "isFolder": True})
                    self.c.created("pasta %s" % folder_path)
                    self.s.inc("pastas de consulta")
                except HttpError as exc2:
                    self.c.error("pasta de consultas: %s" % exc2)
                    self.s.error("pasta de consultas: %s" % exc2.message)
                    return
        for name, wiql in spec.items():
            if name in children:
                self.query_ids[name] = children[name]
                self.c.skip("consulta %s" % name)
                continue
            if self.dry:
                self.c.plan("criaria a consulta %s" % name)
                continue
            try:
                r = self.client.request("POST", self.urls.papi("wit/queries/%s" % "/".join(q(s) for s in folder_path.split("/"))),
                                        {"name": name, "wiql": wiql})
                self.query_ids[name] = (r.data or {}).get("id")
                self.c.created("consulta %s" % name)
                self.s.inc("consultas criadas")
            except HttpError as exc:
                self.c.error("consulta %s: %s" % (name, exc))
                self.s.error("consulta %s: %s" % (name, exc.message))

    # ---------------- 7. wiki ----------------
    def step_wiki(self):
        self.c.title("7/8 Wiki do projeto")
        ids = {k: v for k, v in self.ids.items() if isinstance(v, int)}
        pages = render_wiki_pages(self.model, self.urls, self.team_name, ids, self.query_ids,
                                  query_folder=self.args.query_folder, links=self.online and bool(self.project_id))
        if self.args.export_wiki:
            export_wiki(pages, self.args.export_wiki, self.c)
        if not self.online or not self.project_id:
            self.c.plan("criaria a wiki do projeto e %d páginas:" % len(pages))
            for path in pages:
                self.c.plan("  %s" % path)
            return
        try:
            wikis = (self.client.request("GET", self.urls.papi("wiki/wikis")).data or {}).get("value", [])
        except HttpError as exc:
            self.c.error("wiki: %s" % exc)
            self.s.error("wiki: %s" % exc.message)
            return
        wiki = next((w for w in wikis if w.get("type") == "projectWiki"), None)
        if wiki is None:
            if self.dry:
                self.c.plan("criaria a wiki %s.wiki e as páginas %s" % (self.args.project, ", ".join(pages)))
                return
            try:
                wiki = self.client.request("POST", self.urls.papi("wiki/wikis"), {
                    "type": "projectWiki", "name": "%s.wiki" % self.args.project, "projectId": self.project_id}).data
                self.c.created("wiki %s" % wiki.get("name"))
                self.s.inc("wiki criada")
            except HttpError as exc:
                self.c.error("criar wiki: %s" % exc)
                self.s.error("criar wiki: %s" % exc.message)
                return
        else:
            self.c.skip("wiki %s" % wiki.get("name"))
        self.wiki = wiki
        wiki_ref = wiki.get("id") or wiki.get("name")
        for path, content in pages.items():
            page_url = self.urls.papi("wiki/wikis/%s/pages" % q(wiki_ref), path=path, includeContent="true")
            etag = None
            current = None
            try:
                r = self.client.request("GET", page_url)
                etag = r.header("ETag")
                current = (r.data or {}).get("content") if isinstance(r.data, dict) else None
            except HttpError as exc:
                if exc.status != 404:
                    self.c.error("página %s: %s" % (path, exc))
                    self.s.error("página %s: %s" % (path, exc.message))
                    continue
            if current is not None and current.strip() == content.strip():
                self.c.skip("página %s sem mudanças" % path)
                continue
            if self.dry:
                self.c.plan("%s a página %s" % ("atualizaria" if etag else "criaria", path))
                continue
            put_url = self.urls.papi("wiki/wikis/%s/pages" % q(wiki_ref), path=path)
            headers = {"If-Match": etag} if etag else None
            try:
                self.client.request("PUT", put_url, {"content": content}, headers=headers)
                if etag:
                    self.c.updated("página %s" % path)
                    self.s.inc("páginas atualizadas")
                else:
                    self.c.created("página %s" % path)
                    self.s.inc("páginas criadas")
            except HttpError as exc:
                self.c.error("página %s: %s" % (path, exc))
                self.s.error("página %s: %s" % (path, exc.message))

    # ---------------- 8. professor ----------------
    def step_professor(self):
        self.c.title("8/8 Acesso do professor")
        email = self.args.professor
        if not email:
            self.c.info("--professor não informado; passo ignorado")
            return
        if not self.online or not self.project_id:
            self.c.plan("adicionaria %s com acesso Basic (express) e grupo Project Administrators no projeto" % email)
            return
        try:
            self._grant_professor(email)
        except HttpError as exc:
            self.c.error("não foi possível configurar o acesso do professor: %s" % exc)
            self.s.error("professor: %s" % exc.message)
            self._manual_professor_steps(email)

    def _grant_professor(self, email):
        search = self.urls.with_params(self.urls.vsaex + "/_apis/userentitlements", **{"$filter": "name eq '%s'" % email, "select": "License,Projects"})
        items = (self.client.request("GET", search).data or {}).get("items") or []
        user = next((u for u in items if email.lower() in {
            str((u.get("user") or {}).get("principalName", "")).lower(),
            str((u.get("user") or {}).get("mailAddress", "")).lower()}), None)
        if user is None:
            if self.dry:
                self.c.plan("adicionaria %s (Basic + Project Administrators)" % email)
                return
            body = {
                "accessLevel": {"licensingSource": "account", "accountLicenseType": "express"},
                "extensions": [],
                "user": {"principalName": email, "subjectKind": "user"},
                "projectEntitlements": [{"group": {"groupType": "projectAdministrator"}, "projectRef": {"id": self.project_id}}],
            }
            r = self.client.request("POST", self.urls.with_params(self.urls.vsaex + "/_apis/userentitlements"), body)
            data = r.data or {}
            result = data.get("operationResult") or {}
            if data.get("isSuccess") is False or result.get("isSuccess") is False:
                errs = result.get("errors") or data.get("errors") or []
                self.c.error("o Azure DevOps recusou o convite: %s" % json.dumps(errs, ensure_ascii=False)[:400])
                self.s.error("professor: convite recusado")
                self._manual_professor_steps(email)
                return
            self.c.created("%s convidado com acesso Basic e como Project Administrator" % email)
            self.s.inc("professor convidado")
            return
        ops = []
        lic = ((user.get("accessLevel") or {}).get("accountLicenseType") or "").lower()
        if lic in ("", "none", "stakeholder"):
            ops.append({"from": "", "op": "replace", "path": "/accessLevel",
                        "value": {"accountLicenseType": "express", "licensingSource": "account"}})
        is_admin = any(((pe.get("projectRef") or {}).get("id") == self.project_id
                        and ((pe.get("group") or {}).get("groupType") == "projectAdministrator"))
                       for pe in (user.get("projectEntitlements") or []))
        if not is_admin:
            ops.append({"from": "", "op": "add", "path": "/projectEntitlements",
                        "value": {"group": {"groupType": "projectAdministrator"}, "projectRef": {"id": self.project_id}}})
        if not ops:
            self.c.skip("%s já tem acesso Basic e é Project Administrator" % email)
            return
        if self.dry:
            self.c.plan("ajustaria o acesso de %s (%d operação(ões))" % (email, len(ops)))
            return
        r = self.client.request("PATCH", self.urls.with_params(self.urls.vsaex + "/_apis/userentitlements/%s" % q(user.get("id"))),
                                ops, content_type="application/json-patch+json")
        data = r.data or {}
        if data.get("isSuccess") is False:
            self.c.error("o Azure DevOps recusou a alteração de acesso: %s" % json.dumps(data.get("operationResults"), ensure_ascii=False)[:400])
            self.s.error("professor: alteração recusada")
            self._manual_professor_steps(email)
            return
        self.c.updated("acesso de %s ajustado (Basic + Project Administrators)" % email)
        self.s.inc("professor atualizado")

    def _manual_professor_steps(self, email):
        steps = [
            "Passo a passo manual para dar acesso ao professor:",
            "  1. Abra %s e entre em Organization settings (engrenagem no canto inferior esquerdo)." % self.urls.org,
            "  2. Users > Add users.",
            "  3. Users or Service Principals: %s" % email,
            "  4. Access level: Basic.",
            "  5. Add to projects: %s. Azure DevOps Groups: Project Administrators." % self.args.project,
            "  6. Marque Send email invites e clique em Add.",
            "  7. Se o projeto já existir para ele com outro grupo: Project settings > Permissions > Project Administrators > Members > Add.",
            "  Se a organização estiver ligada ao Microsoft Entra ID e o e-mail for de outro domínio, habilite antes",
            "  Organization settings > Policies > External guest access (ou convide-o como convidado no Entra ID).",
        ]
        for line in steps:
            self.c.info(line)

    # ---------------- links finais ----------------
    def print_links(self):
        self.c.title("Links para colar no Teams")
        u = self.urls
        team = self.team_name
        lines = [
            ("Projeto", u.web_project()),
            ("Backlog de PBIs (ordem de implementação)", u.web_backlog(team)),
            ("Backlog de Épicos", u.web_backlog(team, "Epics")),
            ("Board (Kanban) de PBIs", u.web_board(team)),
            ("Sprint 3: backlog da sprint", u.web_sprint_backlog(team, "Sprint 3")),
            ("Sprint 3: taskboard", u.web_taskboard(team, "Sprint 3")),
        ]
        if self.wiki:
            lines.append(("Wiki", u.web_wiki(self.wiki.get("name") or "%s.wiki" % self.args.project)))
        else:
            lines.append(("Wiki", "%s/_wiki" % u.p))
        for name, qid in self.query_ids.items():
            if qid:
                lines.append(("Consulta %s" % name, u.web_query(qid)))
        lines.append(("Consultas compartilhadas", "%s/_queries/all" % u.p))
        for label, link in lines:
            self.c.info("%s: %s" % (label, link))


def _norm_text(value):
    """Normaliza texto/HTML para comparação: entidades, variações de <br> e espaços."""
    s = html.unescape(str(value))
    s = re.sub(r"<br\s*/?>", "<br>", s, flags=re.IGNORECASE)
    return " ".join(s.split())


def _same_value(ref, current, desired):
    """Compara o valor gravado no Azure com o do backlog.json sem acusar diferenças só de formato."""
    if current is None:
        return desired in (None, "")
    if ref == F_TAGS:
        def tagset(v):
            return {t.strip().lower() for t in str(v).split(";") if t.strip()}
        return tagset(current) == tagset(desired)
    if isinstance(desired, (int, float)) and not isinstance(desired, bool):
        try:
            return abs(float(current) - float(desired)) < 1e-9
        except (TypeError, ValueError):
            return False
    if ref in (F_START, F_TARGET):
        return str(current)[:10] == str(desired)[:10]
    if isinstance(current, dict):  # campo de identidade (Assigned To) volta como IdentityRef
        names = {str(current.get(k, "")).lower() for k in ("uniqueName", "displayName")}
        return str(desired).lower() in names
    return _norm_text(current) == _norm_text(desired)


def _rel_target(rel):
    return str(rel.get("url", "")).rstrip("/").rsplit("/", 1)[-1]


# ---------------------------------------------------------------------------
# Wiki (Markdown gerado de backlog.json)
# ---------------------------------------------------------------------------
WIKI_PAGES = [
    "/Visão Geral do Plano",
    "/Definition of Done",
    "/Critérios de Priorização (MoSCoW) e Estimativa (Planning Poker)",
    "/Release Plan e Roadmap",
    "/Sprint 3 — Detalhamento",
    "/Rastreabilidade TOGAF e ArchiMate",
    "/BDD — Guia de Critérios de Aceite",
]


def _ref(item, ids):
    wid = ids.get(item.key) if ids else None
    return "#%s %s" % (wid, item.key) if wid else item.key


def _md(text):
    """Texto vindo do backlog.json em Markdown: escapa < e > (senão viram tags HTML)."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _md_cell(text):
    return _md(text).replace("|", "\\|").replace("\n", " ")


def _page(lines):
    """Junta as linhas da página sem linhas em branco duplicadas no fim (markdownlint MD012/MD047)."""
    return "\n".join(lines).rstrip("\n") + "\n"


def _num(value, digits=1):
    return ("%%.%df" % digits % value).replace(".", ",")


def render_wiki_pages(model, urls, team, ids=None, query_ids=None, query_folder="ForwardService - Plano", links=True):
    ids = ids or {}
    query_ids = query_ids or {}
    raw = model.raw
    pbis = model.of_type("Product Backlog Item")
    tasks = model.of_type("Task")
    totals = model.sprint_totals()
    pages = OrderedDict()

    # 1. Visão geral ---------------------------------------------------------
    lines = ["# Visão geral do plano ForwardService", "",
             _md(raw["project"]["description"]), "",
             "Processo: **Scrum**. Fonte única do plano: `forward-docs/academic/qa/sprint3/backlog.json`, "
             "publicado por `azure_devops_import.py` (REST API 7.1).", "",
             "## Time", "",
             "| Integrante | RM | Papel |", "| --- | --- | --- |"]
    for m in raw["project"]["team"]:
        lines.append("| %s | %s | %s |" % (_md_cell(m["name"]), m["rm"], _md_cell(m["role"])))
    lines += ["", "## Números do backlog", "",
              "| Nível | Quantidade |", "| --- | --- |",
              "| Épicos | %d |" % len(model.of_type("Epic")),
              "| Features | %d |" % len(model.of_type("Feature")),
              "| PBIs | %d |" % len(pbis),
              "| Tarefas da Sprint 3 | %d |" % len(tasks), "",
              "## Sprints", "",
              "| Sprint | Início | Fim | Status | Pontos | Objetivo |", "| --- | --- | --- | --- | --- | --- |"]
    for it in model.iterations:
        lines.append("| %s | %s | %s | %s | %d | %s |" % (it["name"], _br_date(it["start"]), _br_date(it["finish"]),
                                                     it["status"], totals[it["name"]], _md_cell(it["goal"])))
    lines += ["", "## Como navegar", "",
              "- **Boards > Backlogs**: PBIs na ordem de implementação; troque o nível para Features ou Epics no seletor.",
              "- Itens concluídos (Sprints 1 e 2) ficam ocultos no backlog; ligue **View options > Completed child items** "
              "ou use as consultas abaixo.",
              "- **Boards > Sprints**: backlog e taskboard da Sprint 3 com as tarefas, horas restantes e responsáveis.",
              "- **Boards > Queries > Shared Queries > %s**: consultas prontas." % _md(query_folder), ""]
    if links:
        lines += ["## Atalhos", "",
                  "- [Backlog de PBIs](%s)" % urls.web_backlog(team),
                  "- [Backlog de Épicos](%s)" % urls.web_backlog(team, "Epics"),
                  "- [Board de PBIs](%s)" % urls.web_board(team),
                  "- [Taskboard da Sprint 3](%s)" % urls.web_taskboard(team, "Sprint 3"), ""]
    if query_ids and links:
        lines += ["## Consultas", ""]
        for name, qid in query_ids.items():
            if qid:
                lines.append("- [%s](%s)" % (_md(name), urls.web_query(qid)))
        lines.append("")
    lines += ["## Páginas desta wiki", ""]
    for path in WIKI_PAGES[1:]:
        lines.append("- %s" % path.strip("/"))
    pages[WIKI_PAGES[0]] = _page(lines)

    # 2. Definition of Done --------------------------------------------------
    dod = raw["definition_of_done"]
    lines = ["# Definition of Done", "",
             "A DoD vale para todo o time e é verificada na Sprint Review pelo Product Owner. "
             "Cada PBI repete a DoD na descrição (seção Critérios de Pronto) e soma critérios específicos. "
             "No board de Backlog items, a coluna Approved mostra a Definition of Ready e a coluna Committed mostra a DoD.", "",
             "## Definition of Ready (entrada na sprint)", ""]
    lines += ["%d. %s" % (n, _md(x)) for n, x in enumerate(raw["definition_of_ready"], start=1)]
    for level, label in (("Product Backlog Item", "PBI"), ("Feature", "Feature"), ("Epic", "Épico"), ("Task", "Tarefa")):
        lines += ["", "## DoD de %s" % label, ""]
        lines += ["%d. %s" % (n, _md(x)) for n, x in enumerate(dod[level], start=1)]
    if raw.get("definition_of_done_evolution"):
        lines += ["", "## Evolução da DoD", "", "| Sprints | DoD vigente |", "| --- | --- |"]
        for ev in raw["definition_of_done_evolution"]:
            lines.append("| %s | %s |" % (_md_cell(ev["sprints"]), _md_cell(ev["note"])))
    pages[WIKI_PAGES[1]] = _page(lines)

    # 3. Priorização e estimativa -------------------------------------------
    conv = model.conventions
    lines = ["# Critérios de priorização (MoSCoW) e estimativa (Planning Poker)", "",
             "## MoSCoW (obrigatoriedade, necessidade e opcionalidade)", "",
             "| MoSCoW | Priority no Azure | Critério |", "| --- | --- | --- |"]
    for k, prio in conv["moscow_to_priority"].items():
        lines.append("| %s | %s | %s |" % (k, prio, _md_cell(conv["moscow_criteria"][k])))
    dist = OrderedDict((k, [0, 0]) for k in conv["moscow_to_priority"])
    for p in pbis:
        dist[p.get("moscow")][0] += 1
        dist[p.get("moscow")][1] += p.get("effort")
    lines += ["", "Distribuição dos PBIs:", "", "| MoSCoW | PBIs | Pontos |", "| --- | --- | --- |"]
    for k, (n, pts) in dist.items():
        lines.append("| %s | %d | %d |" % (k, n, pts))
    lines += ["", "## Planning Poker", "",
              "Escala: %s (Fibonacci modificada)." % ", ".join(str(x) for x in conv["planning_poker_scale"]), ""]
    lines += ["- %s" % _md(r) for r in conv["planning_poker_rules"]]
    ref = model.items.get(conv["reference_story"])
    if ref:
        lines += ["", "História de referência: **%s %s** (%d pontos)." % (ref.key, _md(ref.get("title")), ref.get("effort"))]
    ranges = OrderedDict()
    for p in pbis:
        ranges.setdefault(p.get("moscow"), []).append(p.get("business_value"))
    lines += ["", "## Valor de negócio", "",
              "Business Value de 1 a 100, definido pelo PO a partir do Quadro de Valor; desempata itens com a mesma prioridade.", "",
              "| MoSCoW | Faixa de Business Value |", "| --- | --- |"]
    for k, bvs in ranges.items():
        lines.append("| %s | %d a %d |" % (k, min(bvs), max(bvs)))
    lines.append("")
    pages[WIKI_PAGES[2]] = _page(lines)

    # 4. Release plan --------------------------------------------------------
    vals = list(totals.values())
    mean = sum(vals) / float(len(vals))
    lines = ["# Release plan e roadmap", "",
             "## Releases", "", "| Release | Sprints | Data | Pontos |", "| --- | --- | --- | --- |"]
    for rel in raw["releases"]:
        pts = sum(totals[s] for s in rel["sprints"]) if rel["sprints"] else sum(p.get("effort") for p in pbis if not p.get("iteration"))
        lines.append("| %s | %s | %s | %d |" % (rel["name"], ", ".join(rel["sprints"]) or "sem sprint",
                                             _br_date(rel["date"]) if rel["date"] else "a definir", pts))
    lines += ["", "## Pontos por sprint (balanceamento)", "",
              "| Sprint | Pontos | Desvio da média |", "| --- | --- | --- |"]
    for name, pts in totals.items():
        lines.append("| %s | %d | %s%% |" % (name, pts, ("+" if pts >= mean else "") + _num((pts - mean) * 100.0 / mean, 0)))
    lines += ["", "Média de %s pontos por sprint; maior/menor = %s (limite adotado: 1,20)." % (_num(mean), _num(max(vals) / float(min(vals)), 2)), "",
              "## Roadmap", "", "```mermaid", "gantt", "    title Roadmap ForwardService 2026", "    dateFormat YYYY-MM-DD",
              "    axisFormat %d/%m"]
    for rel in raw["releases"]:
        if not rel["sprints"]:
            continue
        lines.append("    section %s" % rel["key"])
        for s in rel["sprints"]:
            it = model.iteration_by_name[s]
            state = "done, " if it["status"] == "Concluída" else ("active, " if it["status"] == "Em andamento" else "")
            lines.append("    %s (%d pts) :%s%s, %s, %s" % (s, totals[s], state, s.replace(" ", "").lower(), it["start"], it["finish"]))
    lines += ["```", ""]
    for it in model.iterations:
        lines += ["## %s (%s a %s)" % (it["name"], _br_date(it["start"]), _br_date(it["finish"])), "",
                  "Objetivo: %s" % _md(it["goal"]), "",
                  "| PBI | Título | MoSCoW | Pontos | Estado |", "| --- | --- | --- | --- | --- |"]
        for p in [x for x in pbis if x.get("iteration") == it["name"]]:
            lines.append("| %s | %s | %s | %d | %s |" % (_ref(p, ids), _md_cell(p.get("title")), p.get("moscow"), p.get("effort"), p.get("state")))
        lines += ["", "Total: **%d pontos**." % totals[it["name"]], ""]
    lines += ["## Backlog futuro (Won't have now)", "", "| PBI | Título | Pontos |", "| --- | --- | --- |"]
    for p in [x for x in pbis if not x.get("iteration")]:
        lines.append("| %s | %s | %d |" % (_ref(p, ids), _md_cell(p.get("title")), p.get("effort")))
    lines += ["", "## Mapa de dependências entre PBIs", "", "```mermaid", "graph LR"]
    for p in pbis:
        for pred in p.get("predecessors", []):
            lines.append("    %s --> %s" % (pred.replace("-", ""), p.key.replace("-", "")))
    lines += ["```", ""]
    pages[WIKI_PAGES[3]] = _page(lines)

    # 5. Sprint 3 -------------------------------------------------------------
    s3 = model.iteration_by_name.get("Sprint 3")
    s3_pbis = [p for p in pbis if p.get("iteration") == "Sprint 3"]
    est = sum(t.get("estimate_hours") for t in tasks)
    rem = sum(t.get("remaining_hours") for t in tasks)
    done_pts = sum(p.get("effort") for p in s3_pbis if p.get("state") == "Done")
    lines = ["# Sprint 3 — Detalhamento", "",
             "Período: %s a %s (sprint atual). Objetivo: %s" % (_br_date(s3["start"]), _br_date(s3["finish"]), _md(s3["goal"])), "",
             "- PBIs: %d, total de %d pontos (%d pontos já em Done)." % (len(s3_pbis), totals["Sprint 3"], done_pts),
             "- Tarefas: %d, estimativa de %d h e %d h restantes." % (len(tasks), est, rem),
             "- Itens não concluídos no fim da sprint voltam ao Sprint Planning da Sprint 4 (carry-over reavaliado pelo PO).",
             "- O processo Scrum só tem o campo Remaining Work na tarefa: a estimativa original fica na descrição da tarefa e na tabela abaixo.",
             "- Burndown e capacidade: Boards > Sprints > Sprint 3 > Analytics e Capacity.", "",
             "## PBIs da sprint", "",
             "| PBI | Título | Responsável | Pontos | Estado | Predecessoras |", "| --- | --- | --- | --- | --- | --- |"]
    for p in s3_pbis:
        lines.append("| %s | %s | %s | %d | %s | %s |" % (_ref(p, ids), _md_cell(p.get("title")), model.owner_name(p.get("owner")),
                                                        p.get("effort"), p.get("state"), ", ".join(p.get("predecessors", [])) or "-"))
    lines += ["", "## Tarefas", "",
              "| Tarefa | PBI | Título | Atividade | Estimativa (h) | Restante (h) | Complexidade | Estado | Responsável | Predecessoras |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for t in tasks:
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            _ref(t, ids), t.parent.key, _md_cell(t.get("title")), t.get("activity"), t.get("estimate_hours"),
            t.get("remaining_hours"), t.get("complexity_points"), t.get("state"), model.owner_name(t.get("owner")),
            ", ".join(t.get("predecessors", [])) or "-"))
    by_act = OrderedDict()
    by_owner = OrderedDict()
    for t in tasks:
        a = by_act.setdefault(t.get("activity"), [0, 0])
        a[0] += t.get("estimate_hours")
        a[1] += t.get("remaining_hours")
        o = by_owner.setdefault(model.owner_name(t.get("owner")), [0, 0])
        o[0] += t.get("estimate_hours")
        o[1] += t.get("remaining_hours")
    lines += ["", "## Horas por atividade", "", "| Atividade | Estimativa (h) | Restante (h) |", "| --- | --- | --- |"]
    for k, (e, r) in by_act.items():
        lines.append("| %s | %d | %d |" % (k, e, r))
    lines += ["", "## Horas por integrante", "", "| Integrante | Estimativa (h) | Restante (h) |", "| --- | --- | --- |"]
    for k, (e, r) in by_owner.items():
        lines.append("| %s | %d | %d |" % (k, e, r))
    lines += ["", "## Dependências técnicas entre tarefas", "", "```mermaid", "graph LR"]
    for t in tasks:
        for pred in t.get("predecessors", []):
            lines.append("    %s --> %s" % (pred.replace("-", "").replace(".", "_"), t.key.replace("-", "").replace(".", "_")))
    lines += ["```", ""]
    pages[WIKI_PAGES[4]] = _page(lines)

    # 6. Rastreabilidade ------------------------------------------------------
    lines = ["# Rastreabilidade TOGAF e ArchiMate", "",
             "Os nomes abaixo são exatamente os elementos do modelo `academic/togaf/gen_archimate.py` "
             "(ForwardService.archimate). Cada item carrega as tags `ArchiMate:<elemento>` e `REQ-xx` "
             "(nas tags, vírgula vira ponto porque o Azure DevOps não aceita vírgula em tag).", "",
             "## Épicos x camadas e elementos", "",
             "| Épico | Pilar | Elementos ArchiMate | Requisitos |", "| --- | --- | --- | --- |"]
    for e in model.of_type("Epic"):
        lines.append("| %s | %s | %s | %s |" % (_ref(e, ids) + " " + _md_cell(e.get("title")), _md_cell(e.get("pillar")),
                                              _md_cell("; ".join(e.get("archimate", []))), ", ".join(e.get("requirements", [])) or "-"))
    lines += ["", "## Requisitos de qualidade (Requirements View)", "", "| Requisito | PBIs que realizam ou evidenciam |", "| --- | --- |"]
    for req, label in ARCHIMATE_REQUIREMENTS.items():
        keys = [p.key for p in pbis if req in p.get("requirements", [])]
        lines.append("| %s | %s |" % (_md_cell(label), ", ".join(keys) or "-"))
    element_map = OrderedDict()
    for p in pbis:
        for el in p.get("archimate", []):
            element_map.setdefault(el, []).append(p.key)
    lines += ["", "## Elemento ArchiMate x PBIs", "", "| Elemento | PBIs |", "| --- | --- |"]
    for el in sorted(element_map, key=lambda s: s.lower()):
        lines.append("| %s | %s |" % (_md_cell(el), ", ".join(element_map[el])))
    lines.append("")
    pages[WIKI_PAGES[5]] = _page(lines)

    # 7. Guia BDD -------------------------------------------------------------
    example = model.items.get("PBI-018") or (pbis[0] if pbis else None)
    lines = ["# BDD — Guia de critérios de aceite", "",
             "Todo PBI tem a história no formato `Como <persona>, quero <ação>, para <benefício>` e critérios de aceite "
             "em Gherkin em português, no campo Acceptance Criteria do Azure Boards.", "",
             "## Convenções", "",
             "- Palavras-chave: Funcionalidade, Cenário, Dado, Quando, Então, E, Mas.",
             "- Cada PBI tem pelo menos um cenário de **caminho feliz** e um de **erro** ou **borda**.",
             "- Um comportamento por cenário, em linguagem de negócio, sem detalhes de tela.",
             "- Resultados observáveis e mensuráveis (status HTTP, mensagem, tempo, registro em auditoria).",
             "- Personas do mapa de personas: Atendente, Gerente de Serviço, Diretor Regional, Cliente Ford, Analista ML e outras.",
             "- Critérios de qualidade citam o requisito ArchiMate (por exemplo REQ-01 ou REQ-06).",
             "- Os cenários da API viram testes executáveis (PBI-057, Cucumber-JVM com Gherkin em português).", "",
             "## Personas", "", "| Persona | Elemento ArchiMate | Uso |", "| --- | --- | --- |"]
    for per in raw.get("personas", []):
        lines.append("| %s | %s | %s |" % (_md_cell(per["nome"]), _md_cell(per["archimate"]), _md_cell(per["uso"])))
    if example:
        st = example.get("story")
        lines += ["", "## Exemplo completo (%s)" % example.key, "",
                  "Como **%s**, quero **%s**, para **%s**." % (_md(st["como"]), _md(st["quero"]), _md(st["para"])), "",
                  "```gherkin", "# language: pt", render_gherkin_text(example.get("acceptance")), "```", ""]
    lines += ["## Checklist de revisão do critério", "",
              "- O cenário pode ser verificado por alguém de fora do time?",
              "- Existe cenário de erro para cada regra de negócio ou de segurança?",
              "- O resultado esperado é único e sem ambiguidade?",
              "- O critério não descreve a implementação (como), só o comportamento (o quê)?", ""]
    pages[WIKI_PAGES[6]] = _page(lines)
    return pages


def export_wiki(pages, directory, console):
    os.makedirs(directory, exist_ok=True)
    for n, (path, content) in enumerate(pages.items(), start=1):
        ascii_name = unicodedata.normalize("NFKD", path.strip("/")).encode("ascii", "ignore").decode("ascii")
        name = re.sub(r"[^0-9A-Za-z]+", "-", ascii_name).strip("-")
        fname = os.path.join(directory, "%02d-%s.md" % (n, name))
        with open(fname, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        console.info("wiki exportada: %s" % fname)


# ---------------------------------------------------------------------------
# Plano (dry-run)
# ---------------------------------------------------------------------------
def print_backlog_overview(model, console):
    console.title("Backlog validado")
    counts = OrderedDict((t, len(model.of_type(t))) for t in TYPE_ORDER)
    console.info("arquivo: %s" % os.path.relpath(model.path))
    console.info("épicos %d, features %d, PBIs %d, tarefas %d" % tuple(counts.values()))
    totals = model.sprint_totals()
    vals = list(totals.values())
    mean = sum(vals) / float(len(vals))
    for name, pts in totals.items():
        console.info("%s: %d pontos (%s%% da média)" % (name, pts, ("+" if pts >= mean else "") + _num((pts - mean) * 100.0 / mean, 0)))
    console.info("média %s pontos; maior/menor = %s" % (_num(mean), _num(max(vals) / float(min(vals)), 2)))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(
        description="Importa o plano do ForwardService (backlog.json) para o Azure DevOps (Boards + Wiki). "
                    "PAT via variável AZDO_PAT ou digitação oculta.")
    p.add_argument("--org", required=True, help="URL da organização, ex.: https://dev.azure.com/minha-org")
    p.add_argument("--project", default="ForwardService", help="nome do projeto (padrão: ForwardService)")
    p.add_argument("--backlog", default=DEFAULT_BACKLOG, help="caminho do backlog.json")
    p.add_argument("--professor", help="e-mail do professor: acesso Basic + Project Administrators")
    p.add_argument("--dry-run", action="store_true", help="não altera nada; sem PAT roda totalmente offline")
    p.add_argument("--steps", default="all", help="passos separados por vírgula: %s (padrão: all)" % ",".join(ALL_STEPS))
    p.add_argument("--sync-state", action="store_true", help="também ajusta o estado de itens que já existiam")
    p.add_argument("--sync-fields", action="store_true",
                   help="também regrava os campos (título, descrição, critérios, prioridade, esforço, sprint, tags...) "
                        "de itens que já existiam e divergem do backlog.json")
    p.add_argument("--assign-map", help="JSON {\"JOTA\": \"email\", ...} para preencher Assigned To")
    p.add_argument("--suppress-notifications", action="store_true",
                   help="usa suppressNotifications=true (exige a permissão Suppress notifications for work item updates)")
    p.add_argument("--query-folder", default="ForwardService - Plano", help="pasta em Shared Queries")
    p.add_argument("--export-wiki", help="grava as páginas da wiki geradas nesta pasta (útil com --dry-run)")
    p.add_argument("--entitlement-url", help="base da API de entitlements (padrão: https://vsaex.dev.azure.com/<org>)")
    p.add_argument("--poll-timeout", type=int, default=240, help="segundos aguardando a criação do projeto")
    p.add_argument("--poll-interval", type=float, default=3.0, help="intervalo entre consultas da operação")
    p.add_argument("--max-retries", type=int, default=4, help="tentativas em 429/5xx")
    p.add_argument("--verbose", action="store_true", help="mostra cada requisição (sem cabeçalhos)")
    return p


def main(argv=None, env=None, out=None, sleep=time.sleep, prompt=getpass.getpass):
    env = os.environ if env is None else env
    stream = out or sys.stdout
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    console = Console(stream, verbose=args.verbose)
    summary = Summary()
    steps = ALL_STEPS if args.steps.strip() == "all" else [s.strip() for s in args.steps.split(",") if s.strip()]
    unknown = [s for s in steps if s not in ALL_STEPS]
    if unknown:
        console.error("passos desconhecidos: %s" % ", ".join(unknown))
        return EXIT_INVALID
    try:
        model = load_backlog(args.backlog)
    except BacklogError as exc:
        console.error(str(exc))
        return EXIT_INVALID
    try:
        urls = Urls(args.org, args.project, args.entitlement_url)
    except FatalError as exc:
        console.error(str(exc))
        return EXIT_INVALID

    pat = (env.get("AZDO_PAT") or "").strip()
    if not pat and not args.dry_run:
        try:
            pat = prompt("PAT do Azure DevOps (a digitação fica oculta): ").strip()
        except (EOFError, KeyboardInterrupt):
            pat = ""
        if not pat:
            console.error("PAT não informado. Defina AZDO_PAT ou digite o token quando solicitado.")
            return EXIT_FATAL

    console.title("ForwardService -> Azure DevOps (%s)" % ("DRY-RUN" if args.dry_run else "execução real"))
    console.info("organização: %s | projeto: %s | passos: %s" % (urls.org, args.project, ", ".join(steps)))
    print_backlog_overview(model, console)

    client = Client(pat or None, console, dry_run=args.dry_run, max_retries=args.max_retries, sleep=sleep)
    imp = Importer(args, model, client, urls, console, summary)
    exit_code = EXIT_OK
    try:
        if "project" in steps or any(s in steps for s in ALL_STEPS[1:]):
            imp.step_project()
        for name in ALL_STEPS[1:]:
            if name in steps:
                getattr(imp, "step_" + name)()
    except FatalError as exc:
        console.error(str(exc))
        summary.error(str(exc))
        exit_code = EXIT_FATAL
    except HttpError as exc:
        console.error("falha inesperada: %s" % exc)
        summary.error(str(exc))
        exit_code = EXIT_FATAL

    if exit_code != EXIT_FATAL and imp.project_id:
        imp.print_links()
    console.title("Resumo")
    for k, v in summary.counts.items():
        console.info("%s: %d" % (k, v))
    if args.dry_run and not client.online:
        console.info("modo offline: nenhuma requisição HTTP foi enviada")
    elif args.dry_run:
        console.info("requisições de escrita não enviadas (dry-run): %d" % len(client.skipped_writes))
    for w in summary.warnings:
        console.warn(w)
    for e in summary.errors:
        console.error(e)
    if summary.errors and exit_code == EXIT_OK:
        exit_code = EXIT_PARTIAL
    console.info("concluído com código %d (%s)" % (exit_code, {0: "sucesso", 1: "concluído com erros não fatais", 2: "erro fatal", 3: "entrada inválida"}[exit_code]))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
