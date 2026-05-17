# Guia de API Keys — Ford Forward

Passo a passo detalhado para obter e configurar cada credencial no N8N.

---

## 1. WhatsApp Business Cloud API (Meta)

A integração principal do projeto. Permite enviar mensagens automatizadas para dealers e clientes.

### 1.1 Criar conta de desenvolvedor Meta

1. Acesse https://developers.facebook.com
2. Clique em **"Get Started"** (canto superior direito)
3. Logue com sua conta Facebook pessoal (ou crie uma)
4. Aceite os termos de desenvolvedor
5. Complete a verificação (email)

### 1.2 Criar o App

1. No dashboard do Meta for Developers, clique em **"Create App"**
   - URL direta: https://developers.facebook.com/apps/create/
2. Selecione o tipo: **"Other"** → **"Business"**
3. Preencha:
   - Display Name: `Ford Forward`
   - App Contact Email: seu email
   - Business Account: pode pular se não tem (seleciona "I don't want to connect...")
4. Clique **"Create App"**

### 1.3 Adicionar WhatsApp ao App

1. Na dashboard do app, seção **"Add products to your app"**
2. Encontre **"WhatsApp"** e clique **"Set Up"**
3. Se pedir pra criar/selecionar Business Portfolio, clique em **"Continue"** com a opção padrão

### 1.4 Obter credenciais de teste

1. No menu lateral, vá em **WhatsApp → API Setup**
   - URL: `https://developers.facebook.com/apps/<APP_ID>/whatsapp-business/wa-dev-console/`
2. Nessa tela você verá:

   **Temporary Access Token** (expira em 24h):
   ```
   EAAxxxxxxx...
   ```
   Copie esse token. Pra uso de teste é suficiente.

   **Phone Number ID** (identificador do número de envio sandbox):
   ```
   1234567890123456
   ```
   Copie esse ID.

   **WhatsApp Business Account ID**:
   ```
   9876543210123456
   ```
   Copie esse ID.

### 1.5 Registrar número de teste para receber mensagens

O sandbox da Meta só envia mensagens para números previamente autorizados.

1. Na mesma tela de **API Setup**, role até **"To"**
2. Clique **"Manage phone number list"**
3. Adicione seu número de celular pessoal (com DDI: +5511999999999)
4. Você vai receber um código de verificação por SMS
5. Confirme o código

### 1.6 Testar via curl (validar antes de colocar no N8N)

```bash
curl -X POST "https://graph.facebook.com/v21.0/<PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <TEMPORARY_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5511999999999",
    "type": "text",
    "text": { "body": "Teste Ford Forward - funciona!" }
  }'
```

Se retornar `"message_status": "accepted"`, está funcionando.

### 1.7 Configurar no N8N

1. Abra o N8N: http://localhost:5678
2. Vá em **Settings** (engrenagem no menu lateral) → **Credentials**
3. Clique **"Add Credential"** → busque **"WhatsApp Business Cloud"**
4. Preencha:
   - **Access Token**: o Temporary Access Token que você copiou
   - **Business Account ID**: o WhatsApp Business Account ID
5. Clique **"Save"**
6. No workflow, no node WhatsApp:
   - **Phone Number ID**: cole o Phone Number ID
   - **Recipient Phone Number**: seu número com DDI (5511999999999)
   - **Text Body**: a mensagem

### 1.8 Token permanente (para depois — não precisa agora)

O token temporário expira em 24h. Para ter um permanente:

1. Vá em https://business.facebook.com/settings/system-users
2. Crie um **System User** (tipo Admin)
3. Gere um token com permissões: `whatsapp_business_messaging`, `whatsapp_business_management`
4. Esse token **não expira** — use ele no N8N no lugar do temporário

---

## 2. Google Gemini (LLM gratuito)

Para gerar mensagens personalizadas, resumos de leads, ou enriquecer textos com IA.

### 2.1 Obter API Key

1. Acesse https://aistudio.google.com/apikey
2. Logue com sua conta Google
3. Clique **"Create API Key"**
4. Selecione qualquer projeto Google Cloud (ou crie um novo — é grátis)
5. A key será gerada:
   ```
   AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
6. Copie e guarde

### 2.2 Limites do free tier

- 60 requisições por minuto
- 1.500 requisições por dia
- Modelos: Gemini 2.0 Flash (rápido), Gemini 2.5 Pro (melhor qualidade)
- Mais que suficiente para projeto acadêmico

### 2.3 Testar via curl

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=<SUA_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Gere uma mensagem curta e amigável de lembrete de revisão para um cliente Ford Ka 2018, última revisão há 2 anos."}]
    }]
  }'
```

### 2.4 Configurar no N8N

1. **Settings → Credentials → Add Credential**
2. Busque **"Google Gemini"** (ou **"Google AI"**)
3. Preencha:
   - **API Key**: a key que você gerou
4. **Save**
5. No workflow, use o node **"Google Gemini Chat Model"** ou **"AI Agent"**
6. Selecione modelo: `gemini-2.0-flash` (rápido) ou `gemini-2.5-pro` (melhor)

---

## 3. OpenAI (alternativa paga)

Caso prefira GPT em vez de Gemini. Tem $5 de crédito grátis na primeira conta.

### 3.1 Criar conta e obter key

1. Acesse https://platform.openai.com/signup
2. Crie conta (email ou Google)
3. Vá em https://platform.openai.com/api-keys
4. Clique **"Create new secret key"**
5. Dê um nome: `ford-forward-n8n`
6. Copie a key:
   ```
   sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
   **Atenção:** a key só aparece uma vez. Se perder, gera outra.

### 3.2 Verificar créditos

1. Acesse https://platform.openai.com/settings/organization/billing/overview
2. Verifique se tem créditos disponíveis (contas novas ganham ~$5)
3. Se não tiver, precisa adicionar cartão e comprar créditos ($5 mínimo)

### 3.3 Configurar no N8N

1. **Settings → Credentials → Add Credential**
2. Busque **"OpenAI"**
3. Preencha:
   - **API Key**: a sk-proj-... que você copiou
4. **Save**
5. No workflow, use o node **"OpenAI"** ou **"OpenAI Chat Model"**
6. Modelo recomendado: `gpt-4o-mini` (barato e bom)

---

## 4. Anthropic Claude (alternativa paga)

### 4.1 Criar conta e obter key

1. Acesse https://console.anthropic.com/login
2. Crie conta
3. Vá em https://console.anthropic.com/settings/keys
4. Clique **"Create Key"**
5. Nome: `ford-forward-n8n`
6. Copie a key:
   ```
   sk-ant-apiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

### 4.2 Créditos

- Precisa adicionar cartão e comprar créditos ($5 mínimo)
- Modelo recomendado: `claude-sonnet-4-6` (bom custo-benefício)

### 4.3 Configurar no N8N

1. **Settings → Credentials → Add Credential**
2. Busque **"Anthropic"**
3. Cole a API key
4. **Save**

---

## 5. Supabase no N8N (opcional — já funciona via HTTP)

Se quiser usar o node nativo do Supabase em vez de HTTP Request.

### 5.1 Obter a Service Role Key

1. Acesse o Supabase Dashboard do projeto
2. Vá em **Settings → API**
3. Em **Project API Keys**, copie a **service_role key** (a secreta, NÃO a anon)
   ```
   eyJhbGciOiJIUzI1NiIs... (longa)
   ```
   **Cuidado:** essa key bypassa RLS. Só usar em server-to-server (N8N).

### 5.2 Configurar no N8N

1. **Settings → Credentials → Add Credential**
2. Busque **"Supabase"**
3. Preencha:
   - **Host**: `https://ysewoopjgdpvnkfhffgy.supabase.co`
   - **Service Role Key**: a key service_role
4. **Save**
5. Agora os nodes Supabase (Insert Row, Get Row, Update Row) funcionam direto

---

## Resumo: o que pegar agora vs depois

| Credencial | Quando | Prioridade |
|---|---|---|
| WhatsApp Business Cloud API | Agora | Alta — é o core da automação |
| Google Gemini | Agora | Média — grátis e fácil, enriquece mensagens |
| OpenAI | Depois (se precisar) | Baixa — só se Gemini não servir |
| Anthropic | Depois (se precisar) | Baixa — só se Gemini não servir |
| Supabase service_role | Opcional | Baixa — HTTP com X-API-Key já funciona |

## Checklist

- [ ] Meta Developer Account criada
- [ ] WhatsApp App criado + product adicionado
- [ ] Temporary Token obtido
- [ ] Phone Number ID copiado
- [ ] Número de teste registrado
- [ ] Teste via curl funcionou
- [ ] Credencial WhatsApp salva no N8N
- [ ] Google Gemini API Key gerada
- [ ] Credencial Gemini salva no N8N
- [ ] Workflow de teste executado com sucesso

---

## Segurança

- **NUNCA** commite API keys no código. Salve só dentro do N8N (credentials) ou em `.env` gitignored.
- Tokens temporários do WhatsApp expiram em 24h — pra demo/Sprint use, pra produção gere System User Token.
- A key do Gemini tem rate limit generoso mas não abuse — 1.500 req/dia é bastante pra demo.
- Service Role Key do Supabase **bypassa toda segurança RLS** — só server-to-server, nunca em frontend.
