from transaction_service import (
    get_stock_by_location_brand_type
)

print(
    get_stock_by_location_brand_type(
        "Gudang",
        "CHINT",
        "MCB_1P"
    )
)