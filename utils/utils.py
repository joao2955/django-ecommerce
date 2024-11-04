def formata_preco(val):
    if val: 
        val = float(val)
        return f'R$ {val:.2f}'.replace('.', ',')
    return val

def cart_total_qtd(carrinho:dict):
    return sum(item['quantidade'] for item in carrinho.values())

def cart_totals(carrinho:dict):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item 
            in carrinho.values()
        ]
    )