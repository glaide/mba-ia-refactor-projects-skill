# code-smells-project

API de E-commerce em Python/Flask com arquitetura MVC (models, views/routes, controllers, services, middlewares).

## Como rodar

```bash
pip install -r requirements.txt
DEBUG=true python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo.

## Autenticação

Endpoints protegidos exigem token Bearer obtido via `POST /login`.

```bash
curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@loja.com","senha":"admin123"}'
```

Use o token retornado:

```bash
curl -s http://localhost:5000/pedidos/usuario/2 \
  -H "Authorization: Bearer <token>"
```

Rotas de escrita em produtos, listagem de usuários, pedidos administrativos e relatórios exigem role `admin`.

## Endpoints

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/` | — | Info da API |
| GET | `/health` | — | Health check |
| GET | `/produtos` | — | Listar produtos |
| GET | `/produtos/busca` | — | Buscar produtos (filtros via query) |
| GET | `/produtos/<id>` | — | Detalhe do produto |
| POST | `/produtos` | admin | Criar produto |
| PUT | `/produtos/<id>` | admin | Atualizar produto |
| DELETE | `/produtos/<id>` | admin | Deletar produto |
| POST | `/usuarios` | — | Registrar usuário |
| POST | `/login` | — | Login (retorna token assinado) |
| GET | `/usuarios` | admin | Listar usuários |
| GET | `/usuarios/<id>` | auth | Detalhe do usuário (próprio ou admin) |
| POST | `/pedidos` | auth | Criar pedido |
| GET | `/pedidos` | admin | Listar todos os pedidos |
| GET | `/pedidos/usuario/<id>` | auth | Pedidos do usuário (próprio ou admin) |
| PUT | `/pedidos/<id>/status` | admin | Atualizar status do pedido |
| GET | `/relatorios/vendas` | admin | Relatório de vendas |

## Usuários de seed

| Email | Senha | Tipo |
|-------|-------|------|
| admin@loja.com | admin123 | admin |
| joao@email.com | 123456 | cliente |
| maria@email.com | senha123 | cliente |

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | obrigatório em produção | Chave para tokens |
| `DEBUG` | `false` | Modo debug (usa chave dev quando `true`) |
| `DB_PATH` | `loja.db` | Caminho do banco SQLite |
| `HOST` | `0.0.0.0` | Host do servidor |
| `PORT` | `5000` | Porta do servidor |
| `TOKEN_MAX_AGE` | `86400` | Validade do token (segundos) |
