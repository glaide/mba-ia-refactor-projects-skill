from flask import request, jsonify
from src.models import produto_model

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]


def listar():
    produtos = produto_model.get_all()
    return jsonify({"dados": produtos, "sucesso": True}), 200


def buscar(produto_id):
    produto = produto_model.get_by_id(produto_id)
    if produto:
        return jsonify({"dados": produto, "sucesso": True}), 200
    return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404


def criar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    for campo in ("nome", "preco", "estoque"):
        if campo not in dados:
            return jsonify({"erro": f"{campo.capitalize()} é obrigatório"}), 400

    nome = dados["nome"]
    preco = dados["preco"]
    estoque = dados["estoque"]
    categoria = dados.get("categoria", "geral")

    if preco < 0 or estoque < 0:
        return jsonify({"erro": "Preço e estoque não podem ser negativos"}), 400
    if len(nome) < 2 or len(nome) > 200:
        return jsonify({"erro": "Nome deve ter entre 2 e 200 caracteres"}), 400
    if categoria not in CATEGORIAS_VALIDAS:
        return jsonify({"erro": f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"}), 400

    produto_id = produto_model.create(
        nome, dados.get("descricao", ""), preco, estoque, categoria
    )
    return jsonify({"dados": {"id": produto_id}, "sucesso": True, "mensagem": "Produto criado"}), 201


def atualizar(produto_id):
    if not produto_model.get_by_id(produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    produto_model.update(
        produto_id,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def deletar(produto_id):
    if not produto_model.get_by_id(produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    produto_model.delete(produto_id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def buscar_com_filtros():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria")
    preco_min = request.args.get("preco_min", type=float)
    preco_max = request.args.get("preco_max", type=float)
    resultados = produto_model.search(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
