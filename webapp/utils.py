def calculate_total_qty(product_stock):
    total_qty = 0

    for stock_entry in product_stock:
        if stock_entry.entry_status:
            total_qty += stock_entry.product_qty
        else:
            total_qty -= stock_entry.product_qty

    return total_qty