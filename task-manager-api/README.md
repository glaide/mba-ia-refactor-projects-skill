# task-manager-api

API de Task Manager em Python/Flask com arquitetura MVC (models, routes, controllers, services, middlewares).

## Como rodar

```bash
pip install -r requirements.txt
DEBUG=true python seed.py
DEBUG=true python app.py
```

A aplicação sobe em `http://localhost:5000`. Rode o `seed.py` antes do primeiro boot.

## Autenticação

A maioria dos endpoints exige token Bearer obtido via `POST /login`.

```bash
curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@email.com","password":"admin1234"}'
```

Use o token retornado:

```bash
curl -s http://localhost:5000/tasks \
  -H "Authorization: Bearer <token>"
```

## Endpoints

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/` | — | Info da API |
| GET | `/health` | — | Health check |
| POST | `/login` | — | Login (retorna token assinado) |
| POST | `/users` | — | Registro (role forçado para `user`) |
| GET | `/users` | admin | Listar usuários |
| GET | `/users/<id>` | auth | Detalhe do usuário |
| PUT | `/users/<id>` | auth | Atualizar usuário |
| DELETE | `/users/<id>` | admin | Deletar usuário |
| GET | `/users/<id>/tasks` | auth | Tasks do usuário |
| GET/POST | `/tasks` | auth | Listar / criar tasks |
| GET/PUT/DELETE | `/tasks/<id>` | auth | CRUD de task |
| GET | `/tasks/search` | auth | Busca de tasks |
| GET | `/tasks/stats` | auth | Estatísticas de tasks |
| GET | `/categories` | auth | Listar categorias |
| POST/PUT/DELETE | `/categories` | admin | CRUD de categorias |
| GET | `/reports/summary` | manager/admin | Relatório geral |
| GET | `/reports/user/<id>` | manager/admin | Relatório por usuário |

## Usuários de seed

| Email | Senha | Role |
|-------|-------|------|
| joao@email.com | admin1234 | admin |
| maria@email.com | user12345 | user |
| pedro@email.com | manager12 | manager |

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | obrigatório em produção | Chave para tokens |
| `DEBUG` | `false` | Modo debug |
| `DATABASE_URI` | `sqlite:///tasks.db` | URI do banco |
| `HOST` | `0.0.0.0` | Host do servidor |
| `PORT` | `5000` | Porta do servidor |
| `TOKEN_MAX_AGE` | `86400` | Validade do token (segundos) |
| `SMTP_HOST` | `smtp.gmail.com` | Host SMTP |
| `SMTP_PORT` | `587` | Porta SMTP |
| `SMTP_USER` | — | Usuário SMTP |
| `SMTP_PASSWORD` | — | Senha SMTP |
