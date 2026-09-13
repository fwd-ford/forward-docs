# Rodar o ForwardService local

Guia para quem chega do zero: banco, API Java e app no simulador, na sua máquina, sem conta em nuvem. Tempo estimado: 40 min na primeira vez (a maior parte é download e o primeiro build do app).

> Enquanto a leva L0 não entra na `main`, use as branches `feat/access-model` (forward-infra), `feat/claims-bound-db-session` (forward-api-java) e `rebuild/foundation` (forward-mobile). O [ESTADO-E-PLANO](../produto/ESTADO-E-PLANO.md) diz quando isso muda.

## 1. Pré-requisitos

| Ferramenta | Para quê | Observação |
| --- | --- | --- |
| Docker Desktop | Supabase local e a API Java | deixe o limite de memória em torno de 4 GB (Settings, Resources) |
| Node 24 | scripts, Supabase CLI e o app | `fnm` ou `nvm`; cada repo tem `.nvmrc` |
| Git e GitHub CLI (`gh`) | clonar e abrir PR | `gh auth login` com a sua conta |
| Xcode com um simulador de iPhone (macOS) | rodar o app no iOS | abra o Xcode uma vez para aceitar a licença |
| Android Studio com um emulador (Windows, Linux ou macOS) | rodar o app no Android | alternativa ao iOS |

Não é preciso instalar Java: a API compila e roda dentro do Docker.

## 2. Clonar os repos lado a lado

Os scripts esperam os três repos na mesma pasta:

```bash
mkdir -p ~/code/fwd-ford && cd ~/code/fwd-ford
gh repo clone fwd-ford/forward-infra
gh repo clone fwd-ford/forward-api-java
gh repo clone fwd-ford/forward-mobile
```

## 3. Banco e API

```bash
cd forward-infra
npm install
npm run secrets:init
npm run stack:up
```

| Comando | O que faz |
| --- | --- |
| `npm run secrets:init` | cria uma vez os arquivos `.env.local`, sem imprimir nenhum segredo |
| `npm run stack:up` | sobe o Supabase (banco, Auth, REST), liga a senha do papel `forward_api`, sobe a API em `http://127.0.0.1:18080` e escreve o `.env.local` do app |

Depois, crie os usuários de teste. Isso vale para a primeira vez e para depois de todo `db reset`. A senha fica no `forward-infra/.env.local`, na variável `DEV_USERS_PASSWORD`:

```bash
set -a; . ./.env.local; set +a
node scripts/seed-users.mjs
```

Confira se está tudo de pé:

```bash
npm run stack:status
```

Esperado: `auth 200`, `rest 200`, `api 200`.

| Usuário | Papel |
| --- | --- |
| `agent.a@example.com` | consultora da concessionária F0001 |
| `agent.a2@example.com` | outra consultora da F0001 |
| `manager.a@example.com` | gerente da F0001 |
| `agent.b@example.com` | consultora da F0002 (serve para provar o isolamento) |
| `admin@example.com` | admin |

A senha de todos é a `DEV_USERS_PASSWORD` do seu `.env.local`.

## 4. App no simulador

A primeira vez compila o app nativo (10 a 20 min). Antes, pare a API para liberar memória:

```bash
cd ../forward-infra && npm run stack:pre-build-ios
cd ../forward-mobile
npm install
npx expo run:ios
```

No Android, use `npx expo run:android`.

Depois do build, volte a subir a API e deixe o servidor do app rodando:

```bash
cd ../forward-infra && npm run stack:up
cd ../forward-mobile && npx expo start --dev-client
```

Mudanças de JavaScript entram sozinhas. Só é preciso compilar de novo quando uma dependência nativa muda.

Entre com um dos usuários. Em modo de desenvolvimento há duas telas auxiliares:
- `forwardservice://dev/diagnostics` compara o que o Supabase e a API dizem sobre você;
- `forwardservice://dev/catalog` mostra o design system.

## 5. Testes de cada repo

| Repo | Comando | O que roda |
| --- | --- | --- |
| forward-infra | `npx supabase db reset && npx supabase test db` | migrations, seed e testes pgTAP de acesso |
| forward-api-java | `docker run --rm -v "$PWD":/src -v "$HOME/.m2":/root/.m2 -w /src eclipse-temurin:17-jdk-noble ./mvnw -B spotless:check verify -P quality` | formatação, Checkstyle, SpotBugs e testes |
| forward-mobile | `npm run check` | typecheck, lint, formatação, travessões e testes |

## 6. Problemas conhecidos

| Sintoma | Causa | Solução |
| --- | --- | --- |
| O Docker some no meio do build do app | o macOS matou a VM do Docker por falta de memória | `npm run stack:pre-build-ios` antes do build e limite de 4 GB no Docker |
| `supabase start` trava esperando o Studio | o Studio é pesado e desnecessário | o `stack:up` já exclui o Studio; se travar, reinicie o Docker Desktop |
| CocoaPods falha com `Encoding::CompatibilityError` | locale do terminal | `export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` antes do `expo run:ios` |
| Mudança de código não aparece no app | Metro rodando com `CI=1` (sem watch) | rode `npx expo start --dev-client` sem `CI` |
| O primeiro toque depois do login não funciona | popup "Salvar senha?" do iOS | toque em "Agora não" |
| A API responde 403 `no_membership` | usuário sem vínculo | rode o `seed-users.mjs` de novo |
| A API não sobe (`/ready` 503) | senha do `forward_api` diferente entre os `.env.local` | `npm run secrets:init` avisa a divergência; depois `npm run stack:up` |

Achou outro? Abra uma issue no forward-docs com o sintoma e o que resolveu, e acrescente a linha aqui.
