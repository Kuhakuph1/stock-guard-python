from telegram import ReplyKeyboardMarkup


def main_menu(role):

    if role == "ADMIN":

        return [
            ["📦 Stock", "📥 Barang Masuk"],
            ["📤 Barang Keluar", "⚠ Low Stock"],
            ["📈 Over Stock", "❌ Empty Stock"],
            ["📊 Stock Report"],
            ["👥 User Management"]
        ]

    elif role == "OPERATOR":

        return [
            ["📦 Stock", "📥 Barang Masuk"],
            ["📤 Barang Keluar", "⚠ Low Stock"],
            ["📈 Over Stock", "❌ Empty Stock"],
            ["📊 Stock Report"]
        ]

    return [
        ["📦 Stock"],
        ["⚠ Low Stock"],
        ["📈 Over Stock"],
        ["❌ Empty Stock"]
    ]


def location_menu():

    return [
        ["🏢 Gudang"],
        ["🏪 Toko"],
        ["⬅️ Kembali"]
    ]


def stock_location_menu():

    return [
        ["🏢 Gudang"],
        ["🏪 Toko"],
        ["⬅️ Menu Utama"]
    ]


def draft_menu(trx_type):

    if trx_type == "IN":

        return [
            ["➕ Tambah Barang"],
            ["➖ Hapus Barang"],
            ["📋 Lihat Draft IN"],
            ["✅ Submit IN"],
            ["❌ Batal"]
        ]

    return [
        ["➕ Tambah Barang"],
        ["➖ Hapus Barang"],
        ["📋 Lihat Draft OUT"],
        ["✅ Submit OUT"],
        ["❌ Batal"]
    ]


def approve_menu(trx_type):

    if trx_type == "IN":

        return [
            ["✅ Approve IN"],
            ["❌ Batal"]
        ]

    return [
        ["✅ Approve OUT"],
        ["❌ Batal"]
    ]