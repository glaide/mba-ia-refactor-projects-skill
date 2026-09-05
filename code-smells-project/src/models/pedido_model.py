from src.database import get_db
from src.services.report_service import build_sales_report


def _item_from_row(row):
    return {
        "produto_id": row["produto_id"],
        "produto_nome": row["produto_nome"] or "Desconhecido",
        "quantidade": row["quantidade"],
        "preco_unitario": row["preco_unitario"],
    }


def _load_items_by_pedido_ids(cursor, pedido_ids):
    if not pedido_ids:
        return {}

    placeholders = ",".join("?" * len(pedido_ids))
    cursor.execute(
        f"""
        SELECT ip.pedido_id, ip.produto_id, ip.quantidade, ip.preco_unitario, p.nome AS produto_nome
        FROM itens_pedido ip
        LEFT JOIN produtos p ON p.id = ip.produto_id
        WHERE ip.pedido_id IN ({placeholders})
        """,
        pedido_ids,
    )

    items_by_pedido = {pid: [] for pid in pedido_ids}
    for row in cursor.fetchall():
        items_by_pedido[row["pedido_id"]].append(_item_from_row(row))
    return items_by_pedido


def _rows_to_pedidos(rows, cursor):
    pedido_ids = [row["id"] for row in rows]
    items_by_pedido = _load_items_by_pedido_ids(cursor, pedido_ids)
    return [
        {
            "id": row["id"],
            "usuario_id": row["usuario_id"],
            "status": row["status"],
            "total": row["total"],
            "criado_em": row["criado_em"],
            "itens": items_by_pedido.get(row["id"], []),
        }
        for row in rows
    ]


def create(usuario_id, itens):
    db = get_db()
    cursor = db.cursor()
    total = 0

    try:
        for item in itens:
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            if produto is None:
                return {"erro": f"Produto {item['produto_id']} não encontrado"}
            if produto["estoque"] < item["quantidade"]:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            total += produto["preco"] * item["quantidade"]

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total),
        )
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute("SELECT preco FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"]),
            )

        db.commit()
        return {"pedido_id": pedido_id, "total": total}
    except Exception:
        db.rollback()
        raise


def get_by_usuario(usuario_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (usuario_id,))
    return _rows_to_pedidos(cursor.fetchall(), cursor)


def get_all():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos")
    return _rows_to_pedidos(cursor.fetchall(), cursor)


def update_status(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    db.commit()
    return True


def get_sales_stats():
    cursor = get_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0]

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": faturamento,
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
    }


def sales_report():
    return build_sales_report(get_sales_stats())
