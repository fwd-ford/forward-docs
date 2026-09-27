// Regenerates ENTREGA_CYBER_SPRINT3.html (self-contained) and, with Edge/Chrome, the PDF.
//
//   cd academic/cyber/sprint3/tools && npm install
//   node build_html.mjs ../ENTREGA_CYBER_SPRINT3.md ../ENTREGA_CYBER_SPRINT3.html \
//     https://github.com/fwd-ford/forward-docs/blob/main/academic/cyber/sprint3/
//   msedge --headless=new --no-pdf-header-footer \
//     --print-to-pdf=../ENTREGA_CYBER_SPRINT3.pdf file:///<abs-path>/ENTREGA_CYBER_SPRINT3.html
//
// Builds a self-contained HTML (images embedded as base64 PNG) from the Markdown
// deliverable. Heading ids use github-slugger so the table of contents and the
// runbook anchors behave exactly like on github.com.
import fs from "node:fs";
import path from "node:path";
import { Marked } from "marked";
import GithubSlugger from "github-slugger";

const [, , mdPath, outPath, repoBase] = process.argv;
const baseDir = path.dirname(mdPath);
const md = fs.readFileSync(mdPath, "utf8");
const slugger = new GithubSlugger();

const marked = new Marked({ gfm: true });
marked.use({
  renderer: {
    heading({ tokens, depth, text }) {
      const inner = this.parser.parseInline(tokens);
      const plain = text.replace(/[*`]/g, "");
      const id = slugger.slug(plain);
      const cls = depth === 2 && /^([1-4]\.|Anexos)/.test(plain) ? ' class="section-break"' : "";
      return `<h${depth} id="${id}"${cls}>${inner}</h${depth}>\n`;
    },
    image({ href, title, text }) {
      let src = href;
      if (!/^(https?:|data:)/.test(href)) {
        const file = path.join(baseDir, href);
        const b64 = fs.readFileSync(file).toString("base64");
        src = `data:image/png;base64,${b64}`;
      }
      const t = title ? ` title="${title}"` : "";
      return `<img src="${src}" alt="${text}"${t}>`;
    },
    link({ href, title, tokens }) {
      const inner = this.parser.parseInline(tokens);
      let url = href;
      // Relative links point to files of this deliverable: make them absolute so the
      // PDF works outside the repository.
      if (!/^(https?:|#|mailto:)/.test(href)) {
        url = new URL(href, repoBase).toString();
      }
      const t = title ? ` title="${title}"` : "";
      return `<a href="${url}"${t}>${inner}</a>`;
    },
  },
});

const body = marked.parse(md);
const css = `
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
:root { --ink:#1f2328; --muted:#59636e; --line:#d1d9e0; --accent:#003478; --accent2:#1e5bb8; --bg-code:#f6f8fa; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: var(--ink); background:#fff;
       font-size: 10.5pt; line-height: 1.5; max-width: 980px; margin: 0 auto; padding: 24px 28px; }
h1 { font-size: 26pt; color: var(--accent); margin: 40mm 0 10mm; line-height: 1.15; border-bottom: 3px solid var(--accent); padding-bottom: 6mm; }
h2 { font-size: 16pt; color: var(--accent); border-bottom: 2px solid var(--line); padding-bottom: 4px; margin-top: 28px; }
h3 { font-size: 12.5pt; color: var(--accent2); margin-top: 22px; }
h2.section-break { break-before: page; page-break-before: always; }
h2, h3 { break-after: avoid; page-break-after: avoid; }
.cover { font-size: 12pt; break-after: page; page-break-after: always; }
.cover table { width: 60%; }
p, li { orphans: 3; widows: 3; }
a { color: var(--accent2); text-decoration: none; word-break: break-word; }
blockquote { margin: 12px 0; padding: 8px 14px; border-left: 4px solid var(--accent2); background: #f3f7fd; color: #2b3440; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px; font-size: 8.8pt; line-height: 1.35; }
th, td { border: 1px solid var(--line); padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #eef3fa; color: #0b2d5b; }
tr { break-inside: avoid; page-break-inside: avoid; }
code { font-family: Consolas, "Cascadia Mono", monospace; font-size: 8.8pt; background: var(--bg-code); padding: 1px 4px; border-radius: 3px; word-break: break-word; }
pre { background: var(--bg-code); border: 1px solid var(--line); border-radius: 6px; padding: 10px 12px; white-space: pre-wrap; word-break: break-all; font-size: 8.2pt; line-height: 1.4; break-inside: auto; }
pre code { background: none; padding: 0; font-size: inherit; }
img { max-width: 100%; height: auto; display: block; margin: 12px auto 4px; border: 1px solid var(--line); border-radius: 4px; break-inside: avoid; page-break-inside: avoid; }
p > em:only-child { display: block; text-align: center; color: var(--muted); font-size: 9pt; margin-top: 0; }
.doc-footer { margin-top: 32px; color: var(--muted); font-size: 8.5pt; border-top: 1px solid var(--line); padding-top: 8px; }
@media screen { body { box-shadow: 0 0 0 1px #eee; } }
`;
const html = `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entrega Cybersecurity Sprint 3: ForwardService</title>
<style>${css}</style>
</head>
<body>
${body}
<div class="doc-footer">Gerado a partir de ENTREGA_CYBER_SPRINT3.md (forward-docs, academic/cyber/sprint3) em 27/09/2026. Imagens incorporadas; links relativos apontam para a branch main do repositório.</div>
</body>
</html>
`;
fs.writeFileSync(outPath, html, "utf8");
console.log("written", outPath, (html.length / 1024).toFixed(0) + " KiB");
