from transaction_service import get_stock_summary

stock = get_stock_summary()

for kode, qty in stock.items():

    print(kode, qty)