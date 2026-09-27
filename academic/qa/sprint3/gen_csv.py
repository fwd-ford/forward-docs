#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera backlog.csv para o recurso nativo "Import work items" do Azure Boards.

Alternativa ao azure_devops_import.py quando não é possível usar a REST API.

Formato (Microsoft Learn, "Import or update work items in bulk by using CSV files"):
  - coluna ID vazia para itens novos;
  - hierarquia por colunas Title 1..Title 4 (Epic > Feature > PBI > Task), cada filho
    logo abaixo do pai (o importador cria apenas links pai/filho);
  - State fica de fora por padrão: a documentação orienta não enviar State em itens novos
    (todos entram como New/To Do);
  - links predecessora/sucessora NÃO são suportados pelo CSV. Depois do import, rode
    azure_devops_import.py --steps workitems,links --sync-state para criar as predecessoras
    e aplicar os estados (o script reconhece os itens pela chave no título).

Uso:
  python gen_csv.py [--backlog backlog.json] [--output backlog.csv] [--project ForwardService] [--include-state]
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from azure_devops_import import (  # noqa: E402  (import após ajustar sys.path)
    BacklogError, load_backlog, render_acceptance, render_description,
)

COLUMNS = ["ID", "Work Item Type", "Title 1", "Title 2", "Title 3", "Title 4", "Priority", "Effort",
           "Business Value", "Remaining Work", "Activity", "Iteration Path", "Tags", "Description",
           "Acceptance Criteria"]


def build_rows(model, project_name, include_state=False):
    rows = []

    def row(item):
        d = item.data
        r = dict.fromkeys(COLUMNS + (["State"] if include_state else []), "")
        r["Work Item Type"] = item.type
        r["Title %d" % item.level] = item.title
        if item.type == "Task":
            r["Priority"] = item.parent.get("priority")
            r["Remaining Work"] = d.get("remaining_hours")
            r["Activity"] = d.get("activity")
        else:
            r["Priority"] = d.get("priority")
            r["Effort"] = d.get("effort")
            r["Business Value"] = d.get("business_value")
            r["Acceptance Criteria"] = render_acceptance(model, item)
        r["Iteration Path"] = "%s\\%s" % (project_name, d["iteration"]) if d.get("iteration") else project_name
        r["Tags"] = "; ".join(d.get("tags", []))
        r["Description"] = render_description(model, item)
        if include_state:
            r["State"] = d.get("state")
        return r

    def walk(item):
        rows.append(row(item))
        for child in sorted(item.children, key=lambda c: c.get("rank", 0)):
            walk(child)

    for epic in model.of_type("Epic"):
        walk(epic)
    return rows


def write_csv(rows, path, include_state=False):
    columns = COLUMNS + (["State"] if include_state else [])
    # utf-8-sig: o Excel reconhece os acentos; o importador do Azure Boards aceita CSV UTF-8.
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in columns})


def main(argv=None):
    p = argparse.ArgumentParser(description="Gera backlog.csv (Import work items do Azure Boards) a partir de backlog.json")
    p.add_argument("--backlog", default=os.path.join(HERE, "backlog.json"))
    p.add_argument("--output", default=os.path.join(HERE, "backlog.csv"))
    p.add_argument("--project", default=None, help="nome do projeto no Azure DevOps (padrão: o do backlog.json)")
    p.add_argument("--include-state", action="store_true",
                   help="inclui a coluna State (não recomendado para itens novos, veja a docstring)")
    args = p.parse_args(argv)
    try:
        model = load_backlog(args.backlog)
    except BacklogError as exc:
        print("[erro] %s" % exc)
        return 3
    project = args.project or model.project["name"]
    rows = build_rows(model, project, args.include_state)
    write_csv(rows, args.output, args.include_state)
    counts = {}
    for r in rows:
        counts[r["Work Item Type"]] = counts.get(r["Work Item Type"], 0) + 1
    print("[ok] %s gerado com %d linhas: %s" % (os.path.basename(args.output), len(rows),
                                                ", ".join("%s %d" % kv for kv in counts.items())))
    print("[info] Importe em Boards > Queries > Import work items. Depois rode azure_devops_import.py "
          "--steps workitems,links --sync-state para criar as predecessoras e aplicar os estados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
