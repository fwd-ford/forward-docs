# -*- coding: utf-8 -*-
"""Testes do azure_devops_import.py contra um Azure DevOps falso (http.server + unittest).

O servidor falso implementa as rotas da REST API 7.1 usadas pelo script, guarda cada
requisição (método, caminho, query, cabeçalhos e corpo) e simula o comportamento
relevante do Azure DevOps: links recíprocos (Parent/Child, Predecessor/Successor),
estados válidos por tipo, ETag nas páginas da wiki, 203/401 sem autenticação e 429.

Execução (na pasta academic/qa/sprint3):
    python -m unittest discover -s tests -v
"""
from __future__ import annotations

import base64
import contextlib
import copy
import csv
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SPRINT3 = os.path.dirname(HERE)
sys.path.insert(0, SPRINT3)

import azure_devops_import as adi  # noqa: E402
import gen_csv  # noqa: E402

BACKLOG = os.path.join(SPRINT3, "backlog.json")
ARCHIMATE_SCRIPT = os.path.normpath(os.path.join(SPRINT3, "..", "..", "togaf", "gen_archimate.py"))
PAT = "dummy-pat-de-teste-nao-real"  # valor fictício (allowlist do gitleaks: dummy)
ORG = "fakeorg"
PROJECT = "ForwardService"
PROFESSOR = "profelias.bernardo@fiap.com.br"
SCRUM_ID = adi.SCRUM_PROCESS_TYPE_ID
AGILE_ID = "adcc42ab-9882-485e-a3ed-7678f01f66bc"

SCRUM_TYPES = {
    "Epic": ["New", "In Progress", "Done", "Removed"],
    "Feature": ["New", "In Progress", "Done", "Removed"],
    "Product Backlog Item": ["New", "Approved", "Committed", "Done", "Removed"],
    "Task": ["To Do", "In Progress", "Done", "Removed"],
    "Bug": ["New", "Approved", "Committed", "Done", "Removed"],
}
COMMON_FIELDS = ["System.Id", "System.Title", "System.State", "System.Description", "System.IterationPath",
                 "System.AreaPath", "System.Tags", "System.AssignedTo", "System.History",
                 "Microsoft.VSTS.Common.Priority", "Microsoft.VSTS.Common.BacklogPriority"]
TYPE_FIELDS = {
    "Epic": COMMON_FIELDS + ["Microsoft.VSTS.Common.AcceptanceCriteria", "Microsoft.VSTS.Scheduling.Effort",
                             "Microsoft.VSTS.Common.BusinessValue", "Microsoft.VSTS.Scheduling.StartDate",
                             "Microsoft.VSTS.Scheduling.TargetDate"],
    "Feature": COMMON_FIELDS + ["Microsoft.VSTS.Common.AcceptanceCriteria", "Microsoft.VSTS.Scheduling.Effort",
                                "Microsoft.VSTS.Common.BusinessValue", "Microsoft.VSTS.Scheduling.StartDate",
                                "Microsoft.VSTS.Scheduling.TargetDate"],
    # BusinessValue omitido de propósito: o script deve filtrar campos que o tipo não tem.
    "Product Backlog Item": COMMON_FIELDS + ["Microsoft.VSTS.Common.AcceptanceCriteria", "Microsoft.VSTS.Scheduling.Effort"],
    "Task": COMMON_FIELDS + ["Microsoft.VSTS.Scheduling.RemainingWork", "Microsoft.VSTS.Common.Activity"],
}
RECIPROCAL = {
    "System.LinkTypes.Hierarchy-Reverse": "System.LinkTypes.Hierarchy-Forward",
    "System.LinkTypes.Hierarchy-Forward": "System.LinkTypes.Hierarchy-Reverse",
    "System.LinkTypes.Dependency-Reverse": "System.LinkTypes.Dependency-Forward",
    "System.LinkTypes.Dependency-Forward": "System.LinkTypes.Dependency-Reverse",
}


class MockState:
    """Estado em memória do Azure DevOps falso."""

    def __init__(self, project_exists=False, process="Scrum", preexisting_sprints=("Sprint 1", "Sprint 2", "Sprint 3"),
                 fail_titles=(), throttle_first_wiql=False, entitlement_exists=False):
        self.lock = threading.Lock()
        self.requests = []
        self.base = None
        self.projects = {}
        self.operations = {}
        self.team_iterations = []
        self.work_items = {}
        self.next_id = 1000
        self.query_root = {"id": str(uuid.uuid4()), "name": "Shared Queries", "isFolder": True, "children": []}
        self.wikis = []
        self.pages = {}
        self.fail_titles = set(fail_titles)
        self.throttle_first_wiql = throttle_first_wiql
        self.entitlements = []
        self.columns = [
            {"id": str(uuid.uuid4()), "name": "New", "itemLimit": 0, "stateMappings": {"Product Backlog Item": "New", "Bug": "New"}, "columnType": "incoming"},
            {"id": str(uuid.uuid4()), "name": "Approved", "itemLimit": 5, "stateMappings": {"Product Backlog Item": "Approved", "Bug": "Approved"}, "isSplit": False, "description": "", "columnType": "inProgress"},
            {"id": str(uuid.uuid4()), "name": "Committed", "itemLimit": 5, "stateMappings": {"Product Backlog Item": "Committed", "Bug": "Committed"}, "isSplit": False, "description": "", "columnType": "inProgress"},
            {"id": str(uuid.uuid4()), "name": "Done", "itemLimit": 0, "stateMappings": {"Product Backlog Item": "Done", "Bug": "Done"}, "columnType": "outgoing"},
        ]
        self.iteration_root = {"id": 1, "identifier": str(uuid.uuid4()), "name": PROJECT, "structureType": "iteration",
                               "hasChildren": True, "children": []}
        for n, name in enumerate(preexisting_sprints, start=2):
            self.iteration_root["children"].append({"id": n, "identifier": str(uuid.uuid4()), "name": name,
                                                    "structureType": "iteration", "hasChildren": False})
        if project_exists:
            self._make_project(process)
        if entitlement_exists:
            self.entitlements.append({"id": str(uuid.uuid4()), "user": {"principalName": PROFESSOR, "mailAddress": PROFESSOR},
                                      "accessLevel": {"accountLicenseType": "stakeholder"}, "projectEntitlements": []})

    # ----- helpers -----
    def _make_project(self, process="Scrum"):
        pid = str(uuid.uuid4())
        types = dict(SCRUM_TYPES) if process == "Scrum" else {"Epic": [], "Feature": [], "User Story": [], "Task": []}
        self.projects[PROJECT] = {
            "id": pid, "name": PROJECT, "state": "wellFormed",
            "capabilities": {"processTemplate": {"templateName": process, "templateTypeId": SCRUM_ID if process == "Scrum" else AGILE_ID},
                             "versioncontrol": {"sourceControlType": "Git"}},
            "defaultTeam": {"id": str(uuid.uuid4()), "name": PROJECT + " Team"},
            "types": types,
        }
        return self.projects[PROJECT]

    def project(self):
        return self.projects.get(PROJECT)

    def items_of(self, type_):
        return [w for w in self.work_items.values() if w["fields"]["System.WorkItemType"] == type_]

    def by_key(self):
        out = {}
        for w in self.work_items.values():
            m = adi.KEY_RE.match(w["fields"]["System.Title"])
            if m:
                out[m.group(1)] = w
        return out

    def wi_url(self, wid):
        return "%s/%s/_apis/wit/workItems/%s" % (self.base, ORG, wid)

    def writes(self, since=0):
        return [r for r in self.requests[since:] if r["method"] != "GET"]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # silencia o log do http.server
        pass

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def do_PATCH(self):
        self._handle("PATCH")

    def do_PUT(self):
        self._handle("PUT")

    def do_DELETE(self):
        self._handle("DELETE")

    def _send(self, status, body=None, headers=None):
        raw = b"" if body is None else json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if raw:
            self.wfile.write(raw)

    def _handle(self, method):
        state = self.server.state
        parsed = urllib.parse.urlparse(self.path)
        query = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        body = None
        if raw:
            try:
                body = json.loads(raw.decode("utf-8"))
            except ValueError:
                body = raw.decode("utf-8", "replace")
        segs = [urllib.parse.unquote(s) for s in parsed.path.strip("/").split("/")]
        with state.lock:
            state.requests.append({"method": method, "path": parsed.path, "segs": segs, "query": query,
                                   "headers": {k.lower(): v for k, v in self.headers.items()}, "body": body})
            expected = "Basic " + base64.b64encode((":" + PAT).encode()).decode()
            if self.headers.get("Authorization") != expected:
                return self._send(401, {"message": "TF400813: não autorizado"})
            if query.get("api-version") != "7.1":
                return self._send(400, {"message": "api-version ausente ou diferente de 7.1"})
            try:
                status, out, headers = route(state, method, segs, query, body, self.headers)
            except Exception as exc:  # pragma: no cover - ajuda a depurar o mock
                status, out, headers = 500, {"message": "mock: %r" % (exc,)}, None
        self._send(status, out, headers)


def route(st, method, segs, query, body, headers):
    assert segs[0] == ORG, segs
    s = segs[1:]
    # ---- nível organização ----
    if s[:2] == ["_apis", "projects"]:
        if method == "GET" and len(s) == 2:
            return 200, {"count": len(st.projects), "value": [{"id": p["id"], "name": p["name"]} for p in st.projects.values()]}, None
        if method == "GET" and len(s) == 3:
            p = st.projects.get(s[2])
            if not p:
                return 404, {"message": "TF200016: projeto não existe"}, None
            out = {k: v for k, v in p.items() if k != "types"}
            return 200, out, None
        if method == "POST" and len(s) == 2:
            assert body["capabilities"]["processTemplate"]["templateTypeId"] == SCRUM_ID
            op = str(uuid.uuid4())
            st.operations[op] = {"polls": 0, "name": body["name"]}
            return 202, {"id": op, "status": "queued", "url": "%s/%s/_apis/operations/%s" % (st.base, ORG, op)}, None
    if s[:2] == ["_apis", "operations"] and method == "GET":
        op = st.operations[s[2]]
        op["polls"] += 1
        if op["polls"] >= 2 and not st.project():
            st._make_project("Scrum")
        return 200, {"id": s[2], "status": "succeeded" if op["polls"] >= 2 else "inProgress"}, None
    if s[:3] == ["_apis", "process", "processes"] and method == "GET":
        return 200, {"count": 2, "value": [{"id": SCRUM_ID, "name": "Scrum"}, {"id": AGILE_ID, "name": "Agile"}]}, None
    if s[:2] == ["_apis", "userentitlements"]:
        return route_entitlements(st, method, s, query, body)
    # ---- nível projeto ----
    proj = st.projects.get(s[0])
    if not proj:
        return 404, {"message": "projeto não encontrado"}, None
    if s[1] == "_apis":
        return route_project(st, proj, method, s[2:], query, body, headers)
    # ---- nível time ----
    team = s[1]
    assert team in (proj["defaultTeam"]["id"], proj["defaultTeam"]["name"]), team
    rest = s[3:]
    if rest[:3] == ["work", "teamsettings", "iterations"]:
        if method == "GET":
            vals = [{"id": i} for i in st.team_iterations]
            return 200, {"count": len(vals), "value": vals}, None
        if method == "POST":
            assert body["id"] not in st.team_iterations
            st.team_iterations.append(body["id"])
            return 201, {"id": body["id"]}, None
    if rest[:2] == ["work", "boards"]:
        if len(rest) == 2 and method == "GET":
            return 200, {"count": 3, "value": [{"id": "b1", "name": "Backlog items"}, {"id": "b2", "name": "Features"}, {"id": "b3", "name": "Epics"}]}, None
        if len(rest) == 4 and rest[3] == "columns":
            if method == "GET":
                return 200, {"count": len(st.columns), "value": copy.deepcopy(st.columns)}, None
            if method == "PUT":
                assert isinstance(body, list) and {c["id"] for c in body} == {c["id"] for c in st.columns}
                st.columns = copy.deepcopy(body)
                return 200, {"count": len(body), "value": body}, None
    return 404, {"message": "rota de time desconhecida %s" % "/".join(rest)}, None


def route_project(st, proj, method, s, query, body, headers):
    if s[:2] == ["wit", "workitemtypes"]:
        type_ = s[2]
        if type_ not in proj["types"]:
            return 404, {"message": "tipo inexistente"}, None
        if len(s) == 3:
            return 200, {"name": type_}, None
        fields = [{"referenceName": f, "name": f} for f in TYPE_FIELDS.get(type_, COMMON_FIELDS)]
        return 200, {"count": len(fields), "value": fields}, None
    if s[:3] == ["wit", "classificationnodes", "Iterations"]:
        children = st.iteration_root["children"]
        if method == "GET":
            return 200, copy.deepcopy(st.iteration_root), None
        if method == "POST":
            assert all(c["name"] != body["name"] for c in children)
            node = {"id": 100 + len(children), "identifier": str(uuid.uuid4()), "name": body["name"],
                    "structureType": "iteration", "hasChildren": False, "attributes": body.get("attributes")}
            children.append(node)
            return 201, node, None
        if method == "PATCH":
            node = next(c for c in children if c["name"] == s[3])
            node["attributes"] = body["attributes"]
            return 200, node, None
    if s[:2] == ["wit", "wiql"] and method == "POST":
        if st.throttle_first_wiql:
            st.throttle_first_wiql = False
            return 429, {"message": "TF400733: throttled"}, {"Retry-After": "0"}
        assert "@project" in body["query"]
        tag = re.search(r"CONTAINS '([^']+)'", body["query"]).group(1)
        ids = sorted(w["id"] for w in st.work_items.values() if tag in w["fields"].get("System.Tags", ""))
        return 200, {"queryType": "flat", "workItems": [{"id": i, "url": st.wi_url(i)} for i in ids]}, None
    if s[:2] == ["wit", "workitemsbatch"] and method == "POST":
        assert len(body["ids"]) <= 200
        out = []
        for i in body["ids"]:
            w = copy.deepcopy(st.work_items[i])
            if str(body.get("$expand", "")).lower() not in ("relations", "all"):
                w.pop("relations", None)
            out.append(w)
        return 200, {"count": len(out), "value": out}, None
    if s[:2] == ["wit", "workitems"] and method == "POST" and s[2].startswith("$"):
        type_ = s[2][1:]
        if type_ not in proj["types"]:
            return 404, {"message": "tipo inexistente"}, None
        if headers.get("Content-Type") != "application/json-patch+json":
            return 415, {"message": "Content-Type deve ser application/json-patch+json"}, None
        title = next(o["value"] for o in body if o["path"] == "/fields/System.Title")
        if title in st.fail_titles:
            return 400, {"message": "TF401320: falha simulada para %s" % title}, None
        st.next_id += 1
        wid = st.next_id
        w = {"id": wid, "rev": 1, "fields": {"System.WorkItemType": type_, "System.State": SCRUM_TYPES[type_][0],
                                              "System.TeamProject": PROJECT}, "relations": [], "url": st.wi_url(wid)}
        st.work_items[wid] = w
        err = apply_patch(st, w, body)
        if err:
            del st.work_items[wid]
            return 400, {"message": err}, None
        return 200, copy.deepcopy(w), None
    if s[:2] == ["wit", "workitems"] and method == "PATCH":
        if headers.get("Content-Type") != "application/json-patch+json":
            return 415, {"message": "Content-Type deve ser application/json-patch+json"}, None
        w = st.work_items[int(s[2])]
        err = apply_patch(st, w, body)
        if err:
            return 400, {"message": err}, None
        w["rev"] += 1
        return 200, copy.deepcopy(w), None
    if s[:2] == ["wit", "queries"]:
        path = s[2:]
        node = st.query_root
        assert path[0] == "Shared Queries"
        for name in path[1:]:
            node = next((c for c in node["children"] if c["name"] == name), None)
            if node is None:
                return 404, {"message": "consulta não encontrada"}, None
        if method == "GET":
            out = {k: v for k, v in node.items() if k != "children"}
            out["children"] = [{"id": c["id"], "name": c["name"]} for c in node["children"]]
            return 200, out, None
        if method == "POST":
            assert node.get("isFolder")
            assert all(c["name"] != body["name"] for c in node["children"])
            if not body.get("isFolder"):
                assert body["wiql"].strip().upper().startswith("SELECT")
                if "MODE (RECURSIVE)" in body["wiql"].upper():
                    assert "ORDER BY" not in body["wiql"].upper(), "consulta em árvore não aceita ORDER BY"
            child = {"id": str(uuid.uuid4()), "name": body["name"], "isFolder": bool(body.get("isFolder")),
                     "wiql": body.get("wiql"), "children": []}
            node["children"].append(child)
            return 201, {k: v for k, v in child.items() if k != "children"}, None
    if s[:2] == ["wiki", "wikis"]:
        if len(s) == 2:
            if method == "GET":
                return 200, {"count": len(st.wikis), "value": st.wikis}, None
            if method == "POST":
                assert body["type"] == "projectWiki" and body["projectId"] == proj["id"]
                wiki = {"id": str(uuid.uuid4()), "name": body["name"], "type": "projectWiki", "projectId": proj["id"]}
                st.wikis.append(wiki)
                return 201, wiki, None
        if len(s) == 4 and s[3] == "pages":
            path = query["path"]
            page = st.pages.get(path)
            if method == "GET":
                if not page:
                    return 404, {"message": "WikiPageNotFoundException"}, None
                return 200, {"path": path, "content": page["content"]}, {"ETag": page["etag"]}
            if method == "PUT":
                if_match = headers.get("If-Match")
                if page and if_match != page["etag"]:
                    return 412, {"message": "versão divergente"}, None
                if not page and if_match:
                    return 404, {"message": "página não existe"}, None
                etag = '"%s"' % uuid.uuid4().hex
                st.pages[path] = {"content": body["content"], "etag": etag}
                return (200 if page else 201), {"path": path}, {"ETag": etag}
    return 404, {"message": "rota de projeto desconhecida %s" % "/".join(s)}, None


def route_entitlements(st, method, s, query, body):
    if method == "GET" and len(s) == 2:
        needle = re.search(r"name eq '([^']+)'", query.get("$filter", ""))
        items = [e for e in st.entitlements if not needle or needle.group(1).lower() in e["user"]["principalName"].lower()]
        return 200, {"items": copy.deepcopy(items), "totalCount": len(items)}, None
    if method == "POST" and len(s) == 2:
        assert body["accessLevel"] == {"licensingSource": "account", "accountLicenseType": "express"}
        assert body["user"]["subjectKind"] == "user"
        ent = {"id": str(uuid.uuid4()), "user": {"principalName": body["user"]["principalName"], "mailAddress": body["user"]["principalName"]},
               "accessLevel": body["accessLevel"], "projectEntitlements": body["projectEntitlements"]}
        st.entitlements.append(ent)
        return 200, {"isSuccess": True, "operationResult": {"isSuccess": True, "errors": [], "userId": ent["id"]}, "userEntitlement": ent}, None
    if method == "PATCH" and len(s) == 3:
        ent = next(e for e in st.entitlements if e["id"] == s[2])
        for op in body:
            if op["path"] == "/accessLevel":
                ent["accessLevel"] = op["value"]
            elif op["path"] == "/projectEntitlements":
                ent["projectEntitlements"].append(op["value"])
        return 200, {"isSuccess": True, "operationResults": [{"isSuccess": True, "errors": []}], "userEntitlement": ent}, None
    return 404, {"message": "rota de entitlements desconhecida"}, None


def apply_patch(st, w, ops):
    type_ = w["fields"]["System.WorkItemType"]
    for op in ops:
        assert op["op"] == "add", op
        path = op["path"]
        if path.startswith("/fields/"):
            ref = path[len("/fields/"):]
            if ref not in TYPE_FIELDS[type_] and ref != "System.History":
                return "TF51535: campo %s não existe em %s" % (ref, type_)
            if ref == "System.State" and op["value"] not in SCRUM_TYPES[type_]:
                return "estado %s inválido para %s" % (op["value"], type_)
            if ref != "System.History":
                w["fields"][ref] = op["value"]
        elif path == "/relations/-":
            rel = op["value"]
            target = int(rel["url"].rstrip("/").rsplit("/", 1)[-1])
            if target not in st.work_items:
                return "TF201036: item de destino %s não existe" % target
            if any(r["rel"] == rel["rel"] and r["url"] == rel["url"] for r in w["relations"]):
                return "TF201035: o link já existe"
            if rel["rel"] == "System.LinkTypes.Hierarchy-Reverse" and any(r["rel"] == rel["rel"] for r in w["relations"]):
                return "TF201036: o item já tem um pai"
            w["relations"].append({"rel": rel["rel"], "url": rel["url"], "attributes": rel.get("attributes", {})})
            other = st.work_items[target]
            other["relations"].append({"rel": RECIPROCAL[rel["rel"]], "url": st.wi_url(w["id"]), "attributes": {}})
        else:
            return "caminho de patch não suportado: %s" % path
    return None


class MockServer:
    def __init__(self, state):
        self.state = state
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.httpd.state = state
        self.port = self.httpd.server_address[1]
        state.base = "http://127.0.0.1:%d" % self.port
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    @property
    def org_url(self):
        return "http://127.0.0.1:%d/%s" % (self.port, ORG)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()


def run_main(org_url, *extra, pat=PAT, dry_run=False):
    argv = ["--org", org_url, "--project", PROJECT, "--backlog", BACKLOG, "--poll-interval", "0"] + list(extra)
    if dry_run:
        argv.append("--dry-run")
    out = io.StringIO()
    env = {"AZDO_PAT": pat} if pat else {}
    code = adi.main(argv, env=env, out=out, sleep=lambda s: None, prompt=lambda msg: "")
    return code, out.getvalue()


def load_json():
    with open(BACKLOG, encoding="utf-8") as fh:
        return json.load(fh)


class ImportFlowTest(unittest.TestCase):
    """Execução completa contra o mock: criação do projeto até o professor."""

    @classmethod
    def setUpClass(cls):
        cls.model = adi.load_backlog(BACKLOG)
        cls.state = MockState(project_exists=False)
        cls.server = MockServer(cls.state).__enter__()
        cls.code, cls.out = run_main(cls.server.org_url, "--professor", PROFESSOR)
        cls.first_run_requests = len(cls.state.requests)

    @classmethod
    def tearDownClass(cls):
        cls.server.__exit__(None, None, None)

    def test_exit_code_and_summary(self):
        self.assertEqual(self.code, 0, self.out[-3000:])
        self.assertIn("itens criados: 123", self.out)
        self.assertNotIn("[erro]", self.out)

    def test_every_request_is_authenticated_and_versioned(self):
        expected = "Basic " + base64.b64encode((":" + PAT).encode()).decode()
        for r in self.state.requests:
            self.assertEqual(r["headers"].get("authorization"), expected, r["path"])
            self.assertEqual(r["query"].get("api-version"), "7.1", r["path"])

    def test_pat_is_never_printed(self):
        self.assertNotIn(PAT, self.out)
        token = base64.b64encode((":" + PAT).encode()).decode()
        self.assertNotIn(token, self.out)

    def test_project_created_with_scrum_and_polled(self):
        posts = [r for r in self.state.requests if r["method"] == "POST" and r["segs"][1:] == ["_apis", "projects"]]
        self.assertEqual(len(posts), 1)
        body = posts[0]["body"]
        self.assertEqual(body["capabilities"]["processTemplate"]["templateTypeId"], SCRUM_ID)
        self.assertEqual(body["capabilities"]["versioncontrol"]["sourceControlType"], "Git")
        self.assertEqual(posts[0]["headers"].get("content-type"), "application/json")
        polls = [r for r in self.state.requests if r["segs"][1:3] == ["_apis", "operations"]]
        self.assertGreaterEqual(len(polls), 2)

    def test_iterations_created_or_updated_with_dates(self):
        nodes = {c["name"]: c for c in self.state.iteration_root["children"]}
        for it in self.model.iterations:
            node = nodes[it["name"]]
            self.assertEqual(node["attributes"]["startDate"], it["start"] + "T00:00:00Z")
            self.assertEqual(node["attributes"]["finishDate"], it["finish"] + "T00:00:00Z")
        patched = [r for r in self.state.requests if r["method"] == "PATCH" and "classificationnodes" in r["segs"]]
        created = [r for r in self.state.requests if r["method"] == "POST" and "classificationnodes" in r["segs"]]
        self.assertEqual(sorted(r["segs"][-1] for r in patched), ["Sprint 1", "Sprint 2", "Sprint 3"])
        self.assertEqual(sorted(r["body"]["name"] for r in created), ["Sprint 4", "Sprint 5", "Sprint 6"])
        self.assertEqual(len(self.state.team_iterations), 6)

    def test_board_columns_receive_dor_and_dod(self):
        cols = {c["name"]: c for c in self.state.columns}
        self.assertIn("Definition of Ready", cols["Approved"]["description"])
        self.assertIn("Definition of Done", cols["Committed"]["description"])

    def test_counts_by_type(self):
        self.assertEqual(len(self.state.items_of("Epic")), 8)
        self.assertEqual(len(self.state.items_of("Feature")), 21)
        self.assertEqual(len(self.state.items_of("Product Backlog Item")), 60)
        self.assertEqual(len(self.state.items_of("Task")), 34)

    def test_create_requests_use_json_patch(self):
        creates = [r for r in self.state.requests if r["method"] == "POST" and len(r["segs"]) > 4 and r["segs"][4] == "workitems"]
        self.assertEqual(len(creates), 123)
        for r in creates:
            self.assertEqual(r["headers"].get("content-type"), "application/json-patch+json")
            self.assertIsInstance(r["body"], list)
            paths = {op["path"] for op in r["body"]}
            self.assertIn("/fields/System.Title", paths)
            self.assertIn("/fields/System.IterationPath", paths)
            self.assertIn("/fields/System.Tags", paths)
            self.assertIn("/fields/Microsoft.VSTS.Common.BacklogPriority", paths)
            for op in r["body"]:
                self.assertEqual(op["op"], "add")

    def test_pbi_fields_and_field_filtering(self):
        creates = [r for r in self.state.requests if r["method"] == "POST" and r["segs"][-1] == "$Product Backlog Item"]
        self.assertEqual(len(creates), 60)
        for r in creates:
            paths = {op["path"]: op.get("value") for op in r["body"]}
            self.assertIn("/fields/Microsoft.VSTS.Common.AcceptanceCriteria", paths)
            self.assertIn("Funcionalidade", paths["/fields/Microsoft.VSTS.Common.AcceptanceCriteria"])
            self.assertIn("Critérios de Pronto (DoD)", paths["/fields/System.Description"])
            self.assertIn(paths["/fields/Microsoft.VSTS.Scheduling.Effort"], (1, 2, 3, 5, 8, 13, 21))
            self.assertIn(paths["/fields/Microsoft.VSTS.Common.Priority"], (1, 2, 3, 4))
            # BusinessValue não existe no PBI do mock: o script precisa filtrar.
            self.assertNotIn("/fields/Microsoft.VSTS.Common.BusinessValue", paths)
        features = [r for r in self.state.requests if r["method"] == "POST" and r["segs"][-1] == "$Feature"]
        self.assertTrue(all("/fields/Microsoft.VSTS.Common.BusinessValue" in {op["path"] for op in r["body"]} for r in features))
        self.assertIn("campo Microsoft.VSTS.Common.BusinessValue não existe em Product Backlog Item", self.out)

    def test_task_fields(self):
        by_key = self.state.by_key()
        for t in self.model.of_type("Task"):
            w = by_key[t.key]
            self.assertEqual(w["fields"]["Microsoft.VSTS.Scheduling.RemainingWork"], t.get("remaining_hours"))
            self.assertEqual(w["fields"]["Microsoft.VSTS.Common.Activity"], t.get("activity"))
            self.assertEqual(w["fields"]["System.IterationPath"], PROJECT + "\\Sprint 3")

    def test_hierarchy_relations(self):
        by_key = self.state.by_key()
        for key, item in self.model.items.items():
            w = by_key[key]
            parents = [r for r in w["relations"] if r["rel"] == adi.LINK_PARENT]
            if item.parent is None:
                self.assertEqual(parents, [], key)
            else:
                self.assertEqual(len(parents), 1, key)
                self.assertTrue(parents[0]["url"].endswith("/_apis/wit/workItems/%s" % by_key[item.parent.key]["id"]), key)

    def test_predecessor_relations(self):
        by_key = self.state.by_key()
        total = 0
        for key, item in self.model.items.items():
            got = sorted(int(r["url"].rsplit("/", 1)[-1]) for r in by_key[key]["relations"] if r["rel"] == adi.LINK_PREDECESSOR)
            want = sorted(by_key[p]["id"] for p in item.get("predecessors", []))
            self.assertEqual(got, want, key)
            total += len(want)
        self.assertGreater(total, 80)

    def test_states_match_backlog(self):
        by_key = self.state.by_key()
        for key, item in self.model.items.items():
            self.assertEqual(by_key[key]["fields"]["System.State"], item.get("state"), key)

    def test_iteration_paths(self):
        by_key = self.state.by_key()
        for key, item in self.model.items.items():
            want = PROJECT + ("\\" + item.get("iteration") if item.get("iteration") else "")
            self.assertEqual(by_key[key]["fields"]["System.IterationPath"], want, key)

    def test_queries_created(self):
        folder = next(c for c in self.state.query_root["children"] if c["name"] == "ForwardService - Plano")
        self.assertEqual(len(folder["children"]), 6)
        for q in folder["children"]:
            self.assertIn("@project", q["wiql"])

    def test_wiki_pages_created_with_ids(self):
        self.assertEqual(len(self.state.wikis), 1)
        self.assertEqual(sorted(self.state.pages), sorted(adi.WIKI_PAGES))
        sprint3 = self.state.pages["/Sprint 3 — Detalhamento"]["content"]
        pbi18 = self.state.by_key()["PBI-018"]["id"]
        self.assertIn("#%s PBI-018" % pbi18, sprint3)
        self.assertIn("TSK-3.34", sprint3)
        self.assertIn("```mermaid", self.state.pages["/Release Plan e Roadmap"]["content"])

    def test_professor_entitlement(self):
        posts = [r for r in self.state.requests if r["method"] == "POST" and r["segs"][1:] == ["_apis", "userentitlements"]]
        self.assertEqual(len(posts), 1)
        body = posts[0]["body"]
        self.assertEqual(body["user"]["principalName"], PROFESSOR)
        self.assertEqual(body["accessLevel"]["accountLicenseType"], "express")
        pe = body["projectEntitlements"][0]
        self.assertEqual(pe["group"]["groupType"], "projectAdministrator")
        self.assertEqual(pe["projectRef"]["id"], self.state.project()["id"])

    def test_links_printed(self):
        self.assertIn("_sprints/taskboard/ForwardService%20Team/ForwardService/Sprint%203", self.out)
        self.assertIn("_backlogs/backlog/ForwardService%20Team/Backlog%20items", self.out)

    def test_zz_rerun_is_idempotent(self):
        # Executa de novo contra o mesmo estado: nada novo pode ser criado.
        before_items = len(self.state.work_items)
        before_pages = {k: v["etag"] for k, v in self.state.pages.items()}
        start = len(self.state.requests)
        code, out = run_main(self.server.org_url, "--professor", PROFESSOR)
        self.assertEqual(code, 0, out[-3000:])
        writes = self.state.writes(start)
        # Leituras via POST (WIQL e batch) são permitidas; qualquer outra escrita não.
        unexpected = [(r["method"], r["path"]) for r in writes
                      if not (r["method"] == "POST" and r["segs"][-1] in ("wiql", "workitemsbatch"))]
        self.assertEqual(unexpected, [])
        self.assertEqual(len(self.state.work_items), before_items)
        self.assertEqual({k: v["etag"] for k, v in self.state.pages.items()}, before_pages)
        self.assertIn("itens já existentes: 123", out)


class DryRunTest(unittest.TestCase):
    def test_dry_run_with_pat_makes_only_get_requests(self):
        state = MockState(project_exists=True)
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url, "--professor", PROFESSOR, dry_run=True)
        self.assertEqual(code, 0, out[-2000:])
        self.assertTrue(state.requests, "o dry-run com PAT deve consultar o estado atual")
        self.assertEqual([r for r in state.requests if r["method"] != "GET"], [])
        self.assertEqual(state.work_items, {})
        self.assertIn("[dry-run]", out)

    def test_dry_run_without_pat_is_offline(self):
        state = MockState(project_exists=True)
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url, dry_run=True, pat=None)
        self.assertEqual(code, 0, out[-2000:])
        self.assertEqual(state.requests, [])
        self.assertIn("modo offline", out)
        self.assertIn("itens que seriam criados: 123", out)

    def test_cli_subprocess_dry_run(self):
        env = dict(os.environ)
        env.pop("AZDO_PAT", None)
        env["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.run([sys.executable, os.path.join(SPRINT3, "azure_devops_import.py"),
                               "--org", "https://dev.azure.com/exemplo", "--dry-run"],
                              capture_output=True, text=True, encoding="utf-8", env=env, timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stdout[-2000:] + proc.stderr[-2000:])
        self.assertIn("DRY-RUN", proc.stdout)


class ResilienceTest(unittest.TestCase):
    def test_existing_project_with_other_process_aborts(self):
        state = MockState(project_exists=True, process="Agile")
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url)
        self.assertEqual(code, adi.EXIT_FATAL)
        self.assertIn("Scrum", out)
        self.assertEqual([r for r in state.requests if r["method"] != "GET"], [])

    def test_invalid_pat_is_reported(self):
        state = MockState(project_exists=True)
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url, pat="pat-errado")
        self.assertEqual(code, adi.EXIT_FATAL)
        self.assertIn("Acesso negado", out)
        self.assertNotIn("pat-errado", out)

    def test_one_failure_does_not_stop_the_import(self):
        title = "[PBI-040] Vídeo pitch técnico (até 6 minutos)"
        state = MockState(project_exists=True, fail_titles=[title])
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url)
        self.assertEqual(code, adi.EXIT_PARTIAL)
        self.assertEqual(len(state.work_items), 122)
        self.assertIn("PBI-040", out)
        self.assertIn("predecessora PBI-040 não existe", out)

    def test_throttling_is_retried(self):
        state = MockState(project_exists=True, throttle_first_wiql=True)
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url, "--steps", "workitems")
        self.assertEqual(code, 0, out[-2000:])
        wiql = [r for r in state.requests if r["segs"][-1] == "wiql"]
        self.assertEqual(len(wiql), 2)
        self.assertIn("HTTP 429", out)

    def test_existing_professor_is_promoted(self):
        state = MockState(project_exists=True, entitlement_exists=True)
        with MockServer(state) as srv:
            code, out = run_main(srv.org_url, "--steps", "professor", "--professor", PROFESSOR)
        self.assertEqual(code, 0, out[-2000:])
        patches = [r for r in state.requests if r["method"] == "PATCH" and "userentitlements" in r["segs"]]
        self.assertEqual(len(patches), 1)
        self.assertEqual(patches[0]["headers"].get("content-type"), "application/json-patch+json")
        paths = [op["path"] for op in patches[0]["body"]]
        self.assertEqual(paths, ["/accessLevel", "/projectEntitlements"])


class BacklogContentTest(unittest.TestCase):
    """Regras de conteúdo exigidas pela rubrica, verificadas sobre backlog.json."""

    @classmethod
    def setUpClass(cls):
        cls.model = adi.load_backlog(BACKLOG)
        cls.raw = load_json()

    def test_sizes(self):
        self.assertTrue(7 <= len(self.model.of_type("Epic")) <= 8)
        self.assertTrue(18 <= len(self.model.of_type("Feature")) <= 24)
        self.assertTrue(45 <= len(self.model.of_type("Product Backlog Item")) <= 60)
        tasks = self.model.of_type("Task")
        self.assertTrue(25 <= len(tasks) <= 35)
        self.assertTrue(all(t.get("iteration") == "Sprint 3" for t in tasks))

    def test_sprint_balance(self):
        totals = self.model.sprint_totals()
        vals = list(totals.values())
        self.assertLessEqual(max(vals) / float(min(vals)), 1.2, totals)
        self.assertEqual(totals, self.raw["sprint_totals_points"])

    def test_bdd_and_dod_everywhere(self):
        for p in self.model.of_type("Product Backlog Item"):
            acc = p.get("acceptance")
            self.assertTrue(acc["funcionalidade"])
            kinds = {c["tipo"] for c in acc["cenarios"]}
            self.assertIn("feliz", kinds, p.key)
            self.assertTrue(kinds & {"erro", "borda"}, p.key)
            for c in acc["cenarios"]:
                words = [s.split(" ", 1)[0] for s in c["passos"]]
                self.assertTrue(words[0].startswith("Dad"), p.key)
                self.assertIn("Quando", words, p.key)
                self.assertIn("Então", words, p.key)
            self.assertTrue(p.get("dod_extra"), p.key)
        for f in self.model.of_type("Feature"):
            self.assertTrue(f.get("acceptance")["cenarios"], f.key)
        for e in self.model.of_type("Epic"):
            self.assertTrue(e.get("acceptance_list"), e.key)
        for level in ("Epic", "Feature", "Product Backlog Item", "Task"):
            self.assertTrue(self.raw["definition_of_done"][level])

    def test_priority_matches_moscow(self):
        mapping = self.raw["conventions"]["moscow_to_priority"]
        for p in self.model.of_type("Product Backlog Item"):
            self.assertEqual(p.get("priority"), mapping[p.get("moscow")], p.key)
            if p.get("moscow") == "Won't":
                self.assertIsNone(p.get("iteration"), p.key)

    def test_archimate_names_exist_in_model(self):
        with open(ARCHIMATE_SCRIPT, encoding="utf-8") as fh:
            src = fh.read()
        names = set(re.findall(r'^el\(f_\w+,\s*"\w+",\s*"([^"]+)"', src, flags=re.M))
        self.assertGreater(len(names), 50)
        for it in self.model.items.values():
            for el in it.get("archimate", []) or []:
                self.assertIn(el, names, "%s: %s" % (it.key, el))
            for req in it.get("requirements", []) or []:
                self.assertIn(adi.ARCHIMATE_REQUIREMENTS[req], names)

    def test_backlog_order_respects_dependencies(self):
        for it in self.model.items.values():
            for pred in it.get("predecessors", []):
                self.assertLess(self.model.items[pred].get("rank"), it.get("rank"), (it.key, pred))

    def test_rollups(self):
        for f in self.model.of_type("Feature"):
            self.assertEqual(f.get("effort"), sum(c.get("effort") for c in f.children), f.key)
        for e in self.model.of_type("Epic"):
            self.assertEqual(e.get("effort"), sum(c.get("effort") for c in e.children), e.key)
        for p in self.model.of_type("Product Backlog Item"):
            if p.get("state") == "Done":
                self.assertTrue(all(t.get("state") == "Done" for t in p.children), p.key)
        for t in self.model.of_type("Task"):
            self.assertLessEqual(t.get("remaining_hours"), t.get("estimate_hours"))
            if t.get("state") == "Done":
                self.assertEqual(t.get("remaining_hours"), 0, t.key)

    def test_invalid_backlog_is_rejected(self):
        raw = load_json()
        pbi = raw["epics"][0]["features"][0]["pbis"][0]
        pbi["effort"] = 4
        pbi["predecessors"] = ["PBI-999"]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "backlog.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(raw, fh, ensure_ascii=False)
            with self.assertRaises(adi.BacklogError) as ctx:
                adi.load_backlog(path)
        self.assertIn("Planning Poker", str(ctx.exception))
        self.assertIn("PBI-999", str(ctx.exception))

    def test_dependency_cycle_is_rejected(self):
        raw = load_json()
        pbis = [p for e in raw["epics"] for f in e["features"] for p in f["pbis"]]
        first = next(p for p in pbis if p["key"] == "PBI-001")
        first["predecessors"] = ["PBI-027"]  # PBI-027 depende de PBI-001
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "backlog.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(raw, fh, ensure_ascii=False)
            with self.assertRaises(adi.BacklogError) as ctx:
                adi.load_backlog(path)
        self.assertIn("ciclo", str(ctx.exception))


class CsvTest(unittest.TestCase):
    def test_csv_hierarchy_and_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "backlog.csv")
            with contextlib.redirect_stdout(io.StringIO()) as captured:
                self.assertEqual(gen_csv.main(["--output", path]), 0)
            self.assertIn("123 linhas", captured.getvalue())
            with open(path, encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), 123)
        self.assertEqual(list(rows[0].keys()), gen_csv.COLUMNS)
        self.assertNotIn("State", rows[0])
        level_of = {"Epic": 1, "Feature": 2, "Product Backlog Item": 3, "Task": 4}
        prev_level = 0
        for r in rows:
            self.assertEqual(r["ID"], "")
            filled = [n for n in range(1, 5) if r["Title %d" % n]]
            self.assertEqual(filled, [level_of[r["Work Item Type"]]])
            self.assertLessEqual(filled[0], prev_level + 1, "filho precisa vir logo abaixo do pai")
            prev_level = filled[0]
            self.assertTrue(r["Iteration Path"].startswith(PROJECT))
            self.assertIn("fwd-import", r["Tags"])
        tasks = [r for r in rows if r["Work Item Type"] == "Task"]
        self.assertTrue(all(r["Remaining Work"] != "" and r["Activity"] for r in tasks))
        pbis = [r for r in rows if r["Work Item Type"] == "Product Backlog Item"]
        self.assertTrue(all("Funcionalidade" in r["Acceptance Criteria"] for r in pbis))


if __name__ == "__main__":
    unittest.main(verbosity=2)
