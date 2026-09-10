# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express com arquitetura MVC (models, routes, controllers, services, middlewares).

## Como rodar

```bash
cp .env.example .env
npm install
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite é em memória e já carrega seeds automaticamente no boot.

Exemplos de requisições estão em `api.http`.

## Autenticação

Rotas administrativas exigem API key via header `x-api-key` ou `Authorization: Bearer <key>`.

```bash
curl -s http://localhost:3000/api/admin/financial-report \
  -H "x-api-key: dev-admin-key"
```

O checkout (`POST /api/checkout`) é público e não exige autenticação prévia.

## Endpoints

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| POST | `/api/checkout` | — | Checkout de curso (cria usuário se necessário) |
| GET | `/api/admin/financial-report` | admin | Relatório financeiro por curso |
| DELETE | `/api/users/<id>` | admin | Deletar usuário e dependências |

### Body do checkout

| Campo | Descrição |
|-------|-----------|
| `usr` | Nome do usuário |
| `eml` | E-mail |
| `pwd` | Senha (obrigatória para novo usuário e para usuário existente) |
| `c_id` | ID do curso |
| `payment_token` | Token do gateway de pagamento (`tok_visa_ok` = aprovado, `tok_declined` = recusado) |

## Dados de seed

| Tipo | Dados |
|------|-------|
| Usuário | Leonan — `leonan@fullcycle.com.br` / senha `123` |
| Cursos | `1` Clean Architecture (R$ 997) · `2` Docker (R$ 497) |
| Matrícula | Usuário 1 matriculado no curso 1 com pagamento PAID |

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `PORT` | `3000` | Porta do servidor |
| `ADMIN_API_KEY` | obrigatório | Chave para rotas administrativas |
| `PAYMENT_GATEWAY_KEY` | obrigatório | Chave do gateway de pagamento |
| `DB_USER` | obrigatório | Usuário do banco (config externa) |
| `DB_PASS` | obrigatório | Senha do banco (config externa) |
| `SMTP_USER` | obrigatório | Usuário SMTP para notificações |

Copie `.env.example` para `.env` e ajuste os valores antes de rodar.
