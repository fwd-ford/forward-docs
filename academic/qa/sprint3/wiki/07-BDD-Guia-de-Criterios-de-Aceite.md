# BDD — Guia de critérios de aceite

Todo PBI tem a história no formato `Como <persona>, quero <ação>, para <benefício>` e critérios de aceite em Gherkin em português, no campo Acceptance Criteria do Azure Boards.

## Convenções

- Palavras-chave: Funcionalidade, Cenário, Dado, Quando, Então, E, Mas.
- Cada PBI tem pelo menos um cenário de **caminho feliz** e um de **erro** ou **borda**.
- Um comportamento por cenário, em linguagem de negócio, sem detalhes de tela.
- Resultados observáveis e mensuráveis (status HTTP, mensagem, tempo, registro em auditoria).
- Personas do mapa de personas: Atendente, Gerente de Serviço, Diretor Regional, Cliente Ford, Analista ML e outras.
- Critérios de qualidade citam o requisito ArchiMate (por exemplo REQ-01 ou REQ-06).
- Os cenários da API viram testes executáveis (PBI-057, Cucumber-JVM com Gherkin em português).

## Personas

| Persona | Elemento ArchiMate | Uso |
| --- | --- | --- |
| Atendente da concessionária | Atendente | App mobile (modo Ford): leads priorizados, ficha do cliente, contato. |
| Gerente de Serviço | Gerente de Serviço | Gestão dos leads e do NPS da concessionária (papel GESTOR). |
| Diretor Regional da Ford | Diretor Regional | Painel web com a visão agregada da frota, IHC e ROI. |
| Cliente Ford | Cliente Ford | Recebe lembretes, responde pelo WhatsApp e agenda revisões. |
| Gestor de Retenção | Gestor de Retenção | Define campanhas de reativação por segmento. |
| Analista ML | Analista ML | Opera e retreina os modelos de segmentação e classificação. |
| Encarregado de dados (DPO) | Ford Brasil (Diretoria) | Responde pela conformidade com a LGPD. |
| Integrador de sistema legado da concessionária | Concessionária (Dealer) | Consome a operação SOAP GetVehicle. |
| Desenvolvedor da Equipe ForwardService | Equipe ForwardService | Constrói e mantém a plataforma. |
| Banca avaliadora FIAP x Ford | n/a (stakeholder acadêmico) | Avalia as entregas do Challenge. |
| Product Owner | Equipe ForwardService | Prioriza o backlog e aceita os incrementos. |

## Exemplo completo (PBI-018)

Como **Atendente da concessionária**, quero **entrar com e-mail e senha e receber um token de acesso**, para **usar o app sem depender de um provedor de autenticação externo**.

```gherkin
# language: pt
Funcionalidade: Autenticação por JWT

  Cenário: Login válido (caminho feliz)
    Dado um usuário com papel ATENDENTE cadastrado
    Quando ele envia POST /api/v1/auth/login com credenciais corretas
    Então recebe 200 com accessToken, tokenType Bearer e expiresIn
    E o token contém os claims sub, role e dealer

  Cenário: Senha incorreta (erro)
    Dado um e-mail cadastrado
    Quando a senha enviada está errada
    Então a API responde 401 em application/problem+json
    E a mensagem não revela se o e-mail existe

  Cenário: Token expirado (caso de borda)
    Dado um token cuja expiração já passou
    Quando ele é usado em um endpoint protegido
    Então a API responde 401
```

## Checklist de revisão do critério

- O cenário pode ser verificado por alguém de fora do time?
- Existe cenário de erro para cada regra de negócio ou de segurança?
- O resultado esperado é único e sem ambiguidade?
- O critério não descreve a implementação (como), só o comportamento (o quê)?
