from src.config.settings import DISCOUNT_TIERS


def calculate_discount(faturamento):
    for threshold, rate in DISCOUNT_TIERS:
        if faturamento > threshold:
            return faturamento * rate
    return 0


def build_sales_report(stats):
    faturamento = stats["faturamento_bruto"]
    desconto = calculate_discount(faturamento)
    total_pedidos = stats["total_pedidos"]

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": stats["pedidos_pendentes"],
        "pedidos_aprovados": stats["pedidos_aprovados"],
        "pedidos_cancelados": stats["pedidos_cancelados"],
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
    }
