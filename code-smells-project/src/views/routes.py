from flask import jsonify
from src.controllers import produto_controller, usuario_controller, pedido_controller, health_controller


def register_routes(app):
    app.add_url_rule("/produtos", "listar_produtos", produto_controller.listar, methods=["GET"])
    app.add_url_rule("/produtos/busca", "buscar_produtos", produto_controller.buscar_com_filtros, methods=["GET"])
    app.add_url_rule("/produtos/<int:produto_id>", "buscar_produto", produto_controller.buscar, methods=["GET"])
    app.add_url_rule("/produtos", "criar_produto", produto_controller.criar, methods=["POST"])
    app.add_url_rule("/produtos/<int:produto_id>", "atualizar_produto", produto_controller.atualizar, methods=["PUT"])
    app.add_url_rule("/produtos/<int:produto_id>", "deletar_produto", produto_controller.deletar, methods=["DELETE"])

    app.add_url_rule("/usuarios", "listar_usuarios", usuario_controller.listar, methods=["GET"])
    app.add_url_rule("/usuarios/<int:usuario_id>", "buscar_usuario", usuario_controller.buscar, methods=["GET"])
    app.add_url_rule("/usuarios", "criar_usuario", usuario_controller.criar, methods=["POST"])
    app.add_url_rule("/login", "login", usuario_controller.login, methods=["POST"])

    app.add_url_rule("/pedidos", "criar_pedido", pedido_controller.criar, methods=["POST"])
    app.add_url_rule("/pedidos", "listar_todos_pedidos", pedido_controller.listar_todos, methods=["GET"])
    app.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", pedido_controller.listar_por_usuario, methods=["GET"])
    app.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", pedido_controller.atualizar_status, methods=["PUT"])

    app.add_url_rule("/relatorios/vendas", "relatorio_vendas", pedido_controller.relatorio_vendas, methods=["GET"])
    app.add_url_rule("/health", "health_check", health_controller.health_check, methods=["GET"])

    @app.route("/")
    def index():
        return jsonify({
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "1.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            },
        })
