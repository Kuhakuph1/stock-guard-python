
from sheet_service import (
    get_transaction_data,
    get_stock_data,
    client,
    SPREADSHEET_ID
)
from master_service import (
    get_brand_items,
    get_items_by_brand_type,
    get_item_by_code
)

from sheet_service import (
    refresh_cache
)

from datetime import datetime

def get_brand_summary(
    lokasi,
    brand
):

    stock_data = get_stock_by_location_and_brand(
        lokasi,
        brand
    )

    total_item = len(stock_data)

    item_available = 0
    item_empty = 0
    total_qty = 0

    for qty in stock_data.values():

        total_qty += qty

        if qty > 0:
            item_available += 1
        else:
            item_empty += 1

    return {
        "brand": brand,
        "lokasi": lokasi,
        "total_item": total_item,
        "item_available": item_available,
        "item_empty": item_empty,
        "total_qty": total_qty
    }

def get_stock_by_location_brand_type(
    lokasi,
    brand,
    jenis
):

    stock_sheet = get_stock_data()

    items = get_items_by_brand_type(
        brand,
        jenis
    )

    item_codes = {
        item["kode"]
        for item in items
    }

    stock = {}

    for row in stock_sheet[2:]:

        if len(row) < 8:
            continue

        kode = row[3]

        if kode not in item_codes:
            continue

        try:

            if lokasi == "Gudang":

                qty = int(row[5])

            else:

                qty = int(row[6])

        except:

            qty = 0

        stock[kode] = qty

    return stock

def get_stock_by_location_and_brand(
    lokasi,
    brand
):

    brand_items = get_brand_items(
        brand
    )

    kode_brand = {
        item["kode"]
        for item in brand_items
    }

    data = get_transaction_data()

    stock = {}

    for row in data[2:]:

        if len(row) < 9:
            continue

        lokasi_row = row[2]
        kode_barang = row[3]

        if lokasi_row != lokasi:
            continue

        if kode_barang not in kode_brand:
            continue

        try:
            mutasi = int(row[8])
        except:
            mutasi = 0

        stock[kode_barang] = (
            stock.get(
                kode_barang,
                0
            )
            + mutasi
        )

    return stock

def get_stock_summary():

    data = get_transaction_data()

    stock = {}

    for row in data[2:]:

        if len(row) < 9:
            continue

        kode_barang = row[3]
        mutasi = row[8]

        if not kode_barang:
            continue

        try:
            mutasi = int(mutasi)
        except:
            mutasi = 0

        stock[kode_barang] = (
            stock.get(
                kode_barang,
                0
            )
            + mutasi
        )

    return stock

def get_stock_by_code(
    lokasi,
    kode
):

    stock_data = get_stock_data()

    for row in stock_data[2:]:

        if len(row) < 7:
            continue

        if row[3] != kode:
            continue

        try:

            if lokasi == "Gudang":
                return int(row[5])

            else:
                return int(row[6])

        except:

            return 0

    return 0

def get_current_draft(user_data):

    trx_type = user_data.get(
        "trx_type"
    )

    if trx_type == "OUT":

        return user_data.get(
            "draft_out",
            []
        )

    return user_data.get(
        "draft_in",
        []
    )

def save_current_draft(
    user_data,
    draft
):

    trx_type = user_data.get(
        "trx_type"
    )

    if trx_type == "OUT":

        user_data[
            "draft_out"
        ] = draft

    else:

        user_data[
            "draft_in"
        ] = draft

def get_current_brand(
    user_data
):

    trx_type = user_data.get(
        "trx_type"
    )

    if trx_type == "OUT":

        return user_data.get(
            "out_brand"
        )

    return user_data.get(
        "brand"
    )

def get_current_lokasi(
    user_data
):

    trx_type = user_data.get(
        "trx_type"
    )

    if trx_type == "OUT":

        return user_data.get(
            "out_lokasi"
        )

    return user_data.get(
        "lokasi"
    )

def save_out_transaction(
    draft,
    lokasi,
    status,
    username,
    telegram_id
):

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet_out = spreadsheet.worksheet(
        "OUT"
    )

    sheet_trx = spreadsheet.worksheet(
        "TRANSACTION"
    )

    now = datetime.now()

    tanggal = now.strftime(
        "%Y-%m-%d"
    )

    jam = now.strftime(
        "%H:%M:%S"
    )

    no_doc = (
        f"OUT-{now.strftime('%Y%m%d-%H%M%S')}"
    )

    no_awal = len(
        sheet_out.get_all_values()
    ) - 1

    for i, item in enumerate(
        draft,
        start=1
    ):

        no = no_awal + i

        item_master = get_item_by_code(
            item["kode"]
        )

        if item_master:

            nama_barang = (
                item_master["nama"]
            )

        else:

            nama_barang = ""
    
        row_out = [
            "",
            tanggal,
            jam,
            no_doc,
            lokasi,
            item["kode"],
            nama_barang,
            item["qty"],
            status,
            username,
            telegram_id
        ]

        sheet_out.append_row(
            row_out
        )

        row_trx = [
            "",
            tanggal,
            jam,
            no_doc,
            lokasi,
            item["kode"],
            nama_barang,
            0,
            item["qty"],
            "OUT",
            -item["qty"],
            status,
            username,
            telegram_id
        ]

        sheet_trx.append_row(
            row_trx
        )
    refresh_cache()
    return no_doc

def save_in_transaction(
    draft,
    lokasi,
    status,
    username,
    telegram_id
):

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet_in = spreadsheet.worksheet(
        "IN"
    )

    sheet_trx = spreadsheet.worksheet(
        "TRANSACTION"
    )

    now = datetime.now()

    tanggal = now.strftime(
        "%Y-%m-%d"
    )

    jam = now.strftime(
        "%H:%M:%S"
    )

    no_doc = (
        f"IN-{now.strftime('%Y%m%d-%H%M%S')}"
    )

    no_awal = len(
        sheet_in.get_all_values()
    ) - 1

    for i, item in enumerate(
        draft,
        start=1
    ):

        no = no_awal + i

        item_master = get_item_by_code(
            item["kode"]
        )

        if item_master:

            nama_barang = (
                item_master["nama"]
            )

        else:

            nama_barang = ""
    
        row_in = [
            "",
            tanggal,
            jam,
            no_doc,
            lokasi,
            item["kode"],
            nama_barang,
            item["qty"],
            status,
            username,
            telegram_id
        ]

        sheet_in.append_row(
            row_in
        )

        row_trx = [
            "",
            tanggal,
            jam,
            no_doc,
            lokasi,
            item["kode"],
            nama_barang,
            item["qty"],
            0,
            "IN",
            +item["qty"],
            status,
            username,
            telegram_id
        ]

        sheet_trx.append_row(
            row_trx
        )

    refresh_cache()
    return no_doc

    return stock