from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from config import TOKEN

from sheet_service import (
    refresh_cache
)

from transaction_service import (
    get_stock_summary,
    get_brand_summary,
    get_stock_by_location_and_brand,
    get_stock_by_location_brand_type,
    save_out_transaction,
    save_in_transaction,
    get_current_draft,
    save_current_draft,
    get_stock_by_code
)

from master_service import (
    get_brand_list,
    get_low_stock,
    get_over_stock,
    get_empty_stock,
    get_type_by_brand,
    get_master_report,
    get_items_by_brand_type,
    get_item_by_code
)

from report_service import (
    create_low_stock_excel,
    create_low_stock_txt,
    create_stock_excel,
    create_stock_txt,
    create_master_stock_excel,
    create_master_stock_txt
)

from role_service import (
    get_user_role,
    is_admin,
    is_operator,
    get_all_users
)

from sheet_service import (
    add_user_role
)

async def myid(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        f"ID : {update.effective_user.id}"
    )

async def show_main_menu(
    update,
    role
):

    if role == "ADMIN":

        keyboard = [
            ["📦 Stock", "📥 Barang Masuk"],
            ["📤 Barang Keluar", "⚠ Low Stock"],
            ["📈 Over Stock", "❌ Empty Stock"],
            ["📊 Stock Report"],
            ["👥 User Management"]
        ]

    elif role == "OPERATOR":

        keyboard = [
            ["📦 Stock", "📥 Barang Masuk"],
            ["📤 Barang Keluar", "⚠ Low Stock"],
            ["📈 Over Stock", "❌ Empty Stock"],
            ["📊 Stock Report"]
        ]

    else:

        keyboard = [
            ["📦 Stock"],
            ["⚠ Low Stock"],
            ["📈 Over Stock"],
            ["❌ Empty Stock"]
        ]

    await update.message.reply_text(
        "🏠 Menu Utama",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    role = get_user_role(
    update.effective_user.id
    )
    if role == "ADMIN":

        keyboard = [
        ["📦 Stock", "📥 Barang Masuk"],
        ["📤 Barang Keluar", "⚠ Low Stock"],
        ["📈 Over Stock", "❌ Empty Stock"],
        ["📊 Stock Report"],
        ["👥 User Management"]
        ]

    elif role == "OPERATOR":

        keyboard = [
        ["📦 Stock", "📥 Barang Masuk"],
        ["📤 Barang Keluar", "⚠ Low Stock"],
        ["📈 Over Stock", "❌ Empty Stock"],
        ["📊 Stock Report"]
        ]

    else:

        keyboard = [
            ["📦 Stock"],
            ["⚠ Low Stock"],
            ["📈 Over Stock"],
            ["❌ Empty Stock"]
        ]
   
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
    
    await update.message.reply_text(
        f"🚀 Stock Guard Aktif \nRole : {role}",
        reply_markup=reply_markup
    )


async def stock(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    stock_data = get_stock_summary()

    message = "📦 STOCK SAAT INI\n\n"

    for kode, qty in stock_data.items():

        message += f"{kode} : {qty}\n"

    await update.message.reply_text(
        message
    )

from master_service import (
    get_low_stock,
    get_over_stock,
    get_empty_stock
)

async def send_long_message(
    update,
    message
):

    chunk_size = 3500

    for i in range(
        0,
        len(message),
        chunk_size
    ):

        await update.message.reply_text(
            message[
                i:i+chunk_size
            ]
        )

async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    role = get_user_role(
        user_id
    )

    print(
        f"USER={user_id} ROLE={role}"
    )

    text = update.message.text

    user_data = context.user_data

    # ==========================
    # Barang Keluar
    # ==========================

    if text == "📤 Barang Keluar":

        if not is_operator(
            update.effective_user.id
        ):

            await update.message.reply_text(
                "❌ Tidak memiliki akses"
            )

            return
        user_data["menu"] = "OUT"
        user_data["trx_type"] = "OUT"

        keyboard = [
            ["🏢 Gudang"],
            ["🏪 Toko"],
            ["⬅️ Kembali"]
        ]

        await update.message.reply_text(
            "Pilih Lokasi Barang Keluar",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif text == "📥 Barang Masuk":

        if not is_operator(
            update.effective_user.id
        ):

            await update.message.reply_text(
                "❌ Tidak memiliki akses"
            )

            return

        user_data["menu"] = "IN"
        user_data["trx_type"] = "IN"

        keyboard = [
            ["🏢 Gudang"],
            ["🏪 Toko"],
            ["⬅️ Kembali"]
        ]

        await update.message.reply_text(
            "Pilih Lokasi Barang Masuk",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

        return

    elif text == "📦 Stock":

        keyboard = [
            ["🏢 Gudang"],
            ["🏪 Toko"],
            ["⬅️ Menu Utama"]
        ]
        await update.message.reply_text(
            "Pilih Lokasi",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
    # ==========================
    # PILIH LOKASI
    # ==========================

    elif text in ["🏢 Gudang", "🏪 Toko"]:

        lokasi = (
            text
            .replace("🏢 ", "")
            .replace("🏪 ", "")
        )

        user_data["lokasi"] = lokasi

        if user_data.get(
            "trx_type"
        ) == "OUT":

            user_data[
                "out_lokasi"
            ] = lokasi
        elif user_data.get(
            "trx_type"
        ) == "IN":

            user_data[
                "in_lokasi"
            ] = lokasi
        brands = get_brand_list()

        keyboard = []

        for i in range(0, len(brands), 2):

            keyboard.append(
                brands[i:i+2]
            )

        keyboard.append(
            ["⬅️ Kembali"]
        )

        if user_data.get(
            "trx_type"
        ) == "IN":

            user_data["menu"] = "IN_BRAND"

        elif user_data.get(
            "trx_type"
        ) == "OUT":

            user_data["menu"] = "OUT_BRAND"
        
        await update.message.reply_text(
            f"Pilih Merk ({lokasi})",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
    # ==========================
    # PILIH BRAND
    # ==========================

    elif text in get_brand_list():

        user_data["brand"] = text

        if user_data.get(
            "trx_type"
        ) == "OUT":

            user_data[
                "out_brand"
            ] = text
        elif user_data.get(
            "trx_type"
        ) == "IN":

            user_data[
                "in_brand"
            ] = text
        types = get_type_by_brand(
            text
        )

        keyboard = []

        for i in range(0, len(types), 2):
            keyboard.append(
                types[i:i+2]
            )

        keyboard.append(
            ["⬅️ Kembali"]
        )

        if user_data.get(
            "trx_type"
        ) == "IN":

            user_data["menu"] = "IN_TYPE"

        elif user_data.get(
            "trx_type"
        ) == "OUT":

            user_data["menu"] = "OUT_TYPE"        

        await update.message.reply_text(
            f"Pilih Jenis ({text})",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

# ==========================
# PILIH JENIS
# ==========================

    elif text in get_type_by_brand(
        user_data.get(
            "brand",
            ""
        )
    ):

        lokasi = user_data.get(
            "lokasi"
        )

        brand = user_data.get(
            "brand"
        )

        jenis = text

        user_data["jenis"] = jenis

        if user_data.get(
            "trx_type"
        ) == "OUT":

            user_data[
                "out_jenis"
            ] = jenis

            items = get_items_by_brand_type(
                brand,
                jenis
            )

            keyboard = []

            for item in items:

                keyboard.append(
                    [item["kode"]]
                )

            keyboard.append(
                ["⬅️ Kembali"]
            )

            user_data["menu"] = "OUT_ITEM"

            await update.message.reply_text(
                f"Pilih Barang ({jenis})",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return

        if user_data.get(
            "trx_type"
        ) == "IN":

            user_data[
                "in_jenis"
            ] = jenis

            items = get_items_by_brand_type(
                brand,
                jenis
            )

            keyboard = []

            for item in items:

                keyboard.append(
                    [item["kode"]]
                )

            keyboard.append(
                ["⬅️ Kembali"]
            )

            user_data["menu"] = "IN_ITEM"

            await update.message.reply_text(
                f"Pilih Barang ({jenis})",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return

        stock_data = (
            get_stock_by_location_brand_type(
                lokasi,
                brand,
                jenis
            )
        )

        message = (
            f"📋 DETAIL STOCK\n\n"
            f"Lokasi : {lokasi}\n"
            f"Merk : {brand}\n"
            f"Jenis : {jenis}\n\n"
        )

        for kode, qty in stock_data.items():

            icon = "🟢"

            if qty == 0:
                icon = "🔴"

            message += (
                f"{icon} {kode}\n"
                f"Qty : {qty}\n\n"
            )

        await send_long_message(
            update,
            message
        )
        excel_file = create_stock_excel(
            lokasi,
            brand,
            jenis,
            stock_data
        )

        txt_file = create_stock_txt(
            lokasi,
            brand,
            jenis,
            stock_data
        )

        await update.message.reply_document(
            document=open(
                excel_file,
                "rb"
            )
        )

        await update.message.reply_document(
        document=open(
            txt_file,
            "rb"
        )
        )

        user_data["menu"] = "STOCK_DETAIL"

        keyboard = [
            ["⬅️ Kembali"]
        ]

        await update.message.reply_text(
            "Kembali ke menu utama",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    # ==========================
    # DETAIL STOCK
    # ==========================

    elif text == "📋 Detail Stock":

        lokasi = user_data.get(
            "lokasi"
        )

        brand = user_data.get(
            "brand"
        )

        stock_data = (
            get_stock_by_location_and_brand(
                lokasi,
                brand
            )
        )

        message = (
            f"📋 DETAIL STOCK\n\n"
            f"{lokasi} - {brand}\n\n"
        )

        for kode, qty in stock_data.items():

            status = "🟢"

            if qty == 0:
                status = "🔴"

            message += (
                f"{status} {kode}\n"
                f"Qty : {qty}\n\n"
            )
        user_data["menu"] = "STOCK_DETAIL"

        await update.message.reply_text(
            message
        )
        keyboard = [
        ["⬅️ Kembali"]
        ]

        await update.message.reply_text(
            "Pilih menu",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif text == "👥 User Management":


        if not is_admin(
            update.effective_user.id
        ):

            await update.message.reply_text(
                "❌ Tidak memiliki akses"
            )

            return

        user_data["menu"] = (
            "USER_MANAGEMENT"
        )

        keyboard = [
            ["📋 User List"],
            ["➕ Add User"],
            ["✏ Change Role"],
            ["🚫 Disable User"],
            ["⬅️ Kembali"]
        ]

        await update.message.reply_text(
            "👥 USER MANAGEMENT",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif text == "📋 User List":

        users = get_all_users()

        message = (
            "👥 USER LIST\n\n"
        )

        for user in users:

            message += (
                f"👤 {user['username']}\n"
                f"Role : {user['role']}\n"
                f"ID : {user['id']}\n\n"
            )

        await send_long_message(
            update,
            message
        )

    elif text == "➕ Add User":

        user_data["mode"] = (
            "ADD_USER_ID"
        )

        await update.message.reply_text(
            "Masukkan Telegram ID"
        )

    # ==========================
    # INPUT TELEGRAM ID
    # ==========================

    elif user_data.get(
        "mode"
    ) == "ADD_USER_ID":

        user_data[
            "new_user_id"
        ] = text

        user_data["mode"] = (
            "ADD_USER_USERNAME"
        )

        await update.message.reply_text(
            "Masukkan Username"
        )

    # ==========================
    # INPUT USERNAME
    # ==========================

    elif user_data.get(
        "mode"
    ) == "ADD_USER_USERNAME":

        user_data[
            "new_username"
        ] = text

        user_data["mode"] = (
            "ADD_USER_ROLE"
        )

        keyboard = [
            ["ADMIN"],
            ["OPERATOR"],
            ["VIEWER"]
        ]

        await update.message.reply_text(
            "Pilih Role",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    # ==========================
    # SIMPAN USER
    # ==========================

    elif user_data.get(
        "mode"
    ) == "ADD_USER_ROLE":
        
        print(
            "MODE ADD_USER_ROLE"
        )

        print(
            "TEXT =",
            text
        )

        if text not in [
            "ADMIN",
            "OPERATOR",
            "VIEWER"
        ]:
            return

        add_user_role(
            user_data[
                "new_user_id"
            ],
            user_data[
                "new_username"
            ],
            text
        )

        await update.message.reply_text(
            f"✅ User berhasil ditambahkan\n\n"
            f"ID : {user_data['new_user_id']}\n"
            f"Username : {user_data['new_username']}\n"
            f"Role : {text}"
        )

        user_data["mode"] = ""
    elif text == "✏ Change Role":

        await update.message.reply_text(
            "🚧 Fitur Change Role sedang dibuat"
        )

    elif text == "🚫 Disable User":

        await update.message.reply_text(
            "🚧 Fitur Disable User sedang dibuat"
        )

    elif text == "📊 Stock Report":
        role = get_user_role(
            update.effective_user.id
        )

        if role == "VIEWER":

            await update.message.reply_text(
                "❌ Anda tidak memiliki akses ke menu ini"
            )

            return

        items = get_master_report()
        
        print(items[0])
        excel_file = (
            create_master_stock_excel(
                items
            )
        )

        txt_file = (
            create_master_stock_txt(
                items
            )
        )

        await update.message.reply_text(
            f"📊 MASTER STOCK REPORT\n\n"
            f"Total Item : {len(items)}"
        )

        await update.message.reply_document(
            document=open(
                excel_file,
                "rb"
            )
        )

        await update.message.reply_document(
            document=open(
                txt_file,
                "rb"
            )
        )

    # ==========================
    # Stok keluar Qty
    # ==========================

    elif (
    get_item_by_code(
        text
    ) is not None
    ):

        user_data[
            "selected_item"
        ] = text

        if user_data.get (
            'trx_type'
        )==   "OUT":

            user_data["mode"] = (
            "OUT_QTY"
            )

        elif user_data.get (
            'trx_type'
        )==   "IN":

            user_data["mode"] = (
            "IN_QTY"
            )   

        await update.message.reply_text(
            f"Masukkan Qty untuk\n{text}"
        )
    
    elif user_data.get(
        "mode"
    ) == "OUT_QTY":

        try:

            qty = int(text)

        except:

            await update.message.reply_text(
                "Qty harus angka"
            )

            return

        stock_available = get_stock_by_code(
            user_data.get(
                "out_lokasi"
            ),
            user_data.get(
                "selected_item"
            )
        )

        draft = user_data.get(
            "draft_out",
            []
        )

        draft_qty = 0

        for item in draft:

            if item["kode"] == user_data.get(
                "selected_item"
            ):

                draft_qty += item["qty"]

        if qty + draft_qty > stock_available:

            keyboard = [
                ["➕ Tambah Barang"],
                ["➖ Hapus Barang"],                
                ["📋 Lihat Draft OUT"],
                ["✅ Submit OUT"],
                ["❌ Batal"]
            ]

            user_data["mode"] = ""

            await update.message.reply_text(
                (
                    "❌ Stock tidak mencukupi\n\n"
                    f"Tersedia : {stock_available}\n"
                    f"Sudah di draft : {draft_qty}\n"
                    f"Diminta : {qty}"
                ),
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return

    # BARU LANJUT KE draft.append(...)

        draft.append({

            "lokasi":
            user_data.get(
                "out_lokasi"
            ),

            "brand":
            user_data.get(
                "out_brand"
            ),

            "jenis":
            user_data.get(
                "out_jenis"
            ),

            "kode":
            user_data.get(
                "selected_item"
            ),

            "qty":
            qty

        })

        user_data[
            "draft_out"
        ] = draft

        user_data["mode"] = ""

        keyboard = [
        ["➕ Tambah Barang"],
        ["➖ Hapus Barang"],
        ["📋 Lihat Draft OUT"],
        ["✅ Submit OUT"],
        ["❌ Batal"]
        ]

        await update.message.reply_text(
            (
                "✅ Barang masuk draft\n\n"
                f"{user_data['selected_item']}\n"
                f"Qty : {qty}"
            ),
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
    elif user_data.get(
        "mode"
    ) == "IN_QTY":

        try:

            qty = int(text)

        except:

            await update.message.reply_text(
                "Qty harus angka"
            )

            return

        draft = user_data.get(
            "draft_in",
            []
        )

        draft.append({

            "lokasi":
            user_data.get(
                "in_lokasi"
            ),

            "brand":
            user_data.get(
                "in_brand"
            ),

            "jenis":
            user_data.get(
                "in_jenis"
            ),

            "kode":
            user_data.get(
                "selected_item"
            ),

            "qty":
            qty

        })

        user_data[
            "draft_in"
        ] = draft

        user_data["mode"] = ""

        keyboard = [
            ["➕ Tambah Barang"],
            ["➖ Hapus Barang"],
            ["📋 Lihat Draft IN"],
            ["✅ Submit IN"],
            ["❌ Batal"]
        ]

        await update.message.reply_text(
            (
                "✅ Barang masuk draft\n\n"
                f"{user_data['selected_item']}\n"
                f"Qty : {qty}"
            ),
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
    

    elif (
        user_data.get(
            "mode"
        ) == "DELETE_DRAFT"
        and text.startswith("🗑")
    ):

        try:

            index = int(
                text.replace(
                    "🗑 ",
                    ""
                )
            ) - 1

        except:

            return

        draft = get_current_draft(
            user_data
        )

        if (
            index < 0
            or
            index >= len(draft)
        ):

            return

        deleted = draft.pop(
            index
        )

        save_current_draft(
            user_data,
            draft
        )

        user_data[
            "mode"
        ] = ""

        await update.message.reply_text(
            (
                "✅ Draft dihapus\n\n"
                f"{deleted['kode']}\n"
                f"Qty : {deleted['qty']}"
            )
        )


    elif text == "📋 Lihat Draft OUT":

        draft = user_data.get(
            "draft_out",
            []
        )

        if not draft:

            await update.message.reply_text(
                "Draft kosong"
            )

            return

        message = (
            "🛒 DRAFT BARANG KELUAR\n\n"
        )

        for i, item in enumerate(
            draft,
            start=1
        ):

            message += (
                f"{i}. "
                f"{item['kode']}\n"
                f"Qty : {item['qty']}\n\n"
            )

        await update.message.reply_text(
            message
        )

    elif text == "📋 Lihat Draft IN":

        draft = user_data.get(
            "draft_in",
            []
        )

        if not draft:

            await update.message.reply_text(
                "Draft kosong"
            )

            return

        message = (
            "📥 DRAFT BARANG MASUK\n\n"
        )

        for i, item in enumerate(
            draft,
            start=1
        ):

            message += (
                f"{i}. "
                f"{item['kode']}\n"
                f"Qty : {item['qty']}\n\n"
            )

        await update.message.reply_text(
            message
        )

    elif text == "✅ Submit OUT":

        draft = user_data.get(
            "draft_out",
            []
        )

        if not draft:

            await update.message.reply_text(
                "Draft kosong"
            )

            return

        message = (
            "📤 KONFIRMASI BARANG KELUAR\n\n"
        )

        message += (
            f"Lokasi : "
            f"{user_data.get('out_lokasi')}\n\n"
        )

        for i, item in enumerate(
            draft,
            start=1
        ):

            message += (
                f"{i}. "
                f"{item['kode']}\n"
                f"Qty : {item['qty']}\n\n"
            )
        keyboard = [
            ["🏭 PRODUKSI"],
            ["💰 PENJUALAN"],
            ["🔧 SERVICE"],
            ["↩️ RETUR"],
            ["❌ Batal"]
        ]

        await update.message.reply_text(
            message +
            "\nPilih Status Keluar",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )  

    elif text in [
    "🏭 PRODUKSI",
    "💰 PENJUALAN",
    "🔧 SERVICE",
    "↩️ RETUR"
    ]:

        status = (
        text
        .replace("🏭 ", "")
        .replace("💰 ", "")
        .replace("🔧 ", "")
        .replace("↩️ ", "")
        )

        user_data["out_status"] = status

        keyboard = [
            ["✅ Approve OUT"],
            ["❌ Batal"]
        ]

        await update.message.reply_text(
            f"""
        Status Keluar :

        {status}

        Lanjut Approve?
        """,
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )



    elif text == "✅ Submit IN":

            draft = user_data.get(
                "draft_in",
                []
            )

            if not draft:

                await update.message.reply_text(
                    "Draft kosong"
                )

                return

            message = (
                "📥 KONFIRMASI BARANG MASUK\n\n"
            )

            message += (
                f"Lokasi : "
                f"{user_data.get('in_lokasi')}\n\n"
            )

            for i, item in enumerate(
                draft,
                start=1
            ):

                message += (
                    f"{i}. "
                    f"{item['kode']}\n"
                    f"Qty : {item['qty']}\n\n"
                )

            keyboard = [
                ["🛒 PEMBELIAN"],
                ["↩️ RETUR"],
                ["🔄 TRANSFER MASUK"],
                ["📋 STOCK OPNAME"],
                ["❌ Batal"]
            ]

            await update.message.reply_text(
                message +
                "\nPilih Status Masuk",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

    elif text in [
            "🛒 PEMBELIAN",
            "↩️ RETUR",
            "🔄 TRANSFER MASUK",
            "📋 STOCK OPNAME"
        ]:

            status = (
                text
                .replace("🛒 ", "")
                .replace("↩️ ", "")
                .replace("🔄 ", "")
                .replace("📋 ", "")
            )

            user_data["in_status"] = status

            keyboard = [
                ["✅ Approve IN"],
                ["❌ Batal"]
            ]

            await update.message.reply_text(
                f"""
        Status Masuk :

        {status}

        Lanjut Approve?
        """,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

    elif text == "✅ Approve OUT":
        status = user_data.get(
           "out_status",
            ""
        )

        draft = user_data.get(
            "draft_out",
            []
        )


        if not draft:

            await update.message.reply_text(
                "Draft kosong"
            )

            return

        total_item = len(
            draft
        )

        username = (
            update.effective_user.username
        )

        if not username:

            username = (
                update.effective_user.first_name
            )

        telegram_id = (
            update.effective_user.id
        )

        no_doc = save_out_transaction(
            draft,
            user_data["out_lokasi"],
            user_data["out_status"],
            username,
            telegram_id
        )
        user_data.pop(
            "draft_out",
            None
        )

        user_data.pop(
            "out_brand",
            None
        )

        user_data.pop(
            "out_jenis",
            None
        )

        user_data.pop(
            "out_status",
            None
        )

        user_data.pop(
            "out_lokasi",
            None
        )

        user_data.pop(
            "trx_type",
            None
        )
        role = get_user_role(
            update.effective_user.id
        )

        await update.message.reply_text(
            
                "✅ TRANSAKSI BERHASIL\n\n"
                f"No Dokumen : {no_doc}\n"
                f"Status : {status}\n"
                f"Jumlah Item : {total_item}"
            )

        await show_main_menu(
            update,
            role
        )
        

    elif text == "✅ Approve IN":

        status = user_data.get(
            "in_status",
            ""
        )

        draft = user_data.get(
            "draft_in",
            []
        )

        if not draft:

            await update.message.reply_text(
                "Draft kosong"
            )

            return

        total_item = len(
            draft
        )

        username = (
            update.effective_user.username
        )

        if not username:

            username = (
                update.effective_user.first_name
            )

        telegram_id = (
            update.effective_user.id
        )

        no_doc = save_in_transaction(
            draft,
            user_data["in_lokasi"],
            user_data["in_status"],
            username,
            telegram_id
        )

        user_data.pop(
            "draft_in",
            None
        )

        user_data.pop(
            "in_brand",
            None
        )

        user_data.pop(
            "in_jenis",
            None
        )

        user_data.pop(
            "in_status",
            None
        )

        user_data.pop(
            "in_lokasi",
            None
        )

        user_data.pop(
            "trx_type",
            None
        )

        role = get_user_role(
            update.effective_user.id
        )

        await show_main_menu(
            update,
            role
        )

        await update.message.reply_text(
            (
                "✅ TRANSAKSI MASUK BERHASIL\n\n"
                f"No Dokumen : {no_doc}\n"
                f"Status : {status}\n"
                f"Jumlah Item : {total_item}"
            )
        )
    elif text == "➖ Hapus Barang":

        draft = get_current_draft(
            user_data
        )

        if not draft:

            await update.message.reply_text(
                "Draft kosong"
            )

            return

        keyboard = []

        for i, item in enumerate(
            draft,
            start=1
        ):

            keyboard.append(
                [f"🗑 {i}"]
            )

        keyboard.append(
            ["⬅️ Kembali"]
        )

        user_data[
            "mode"
        ] = "DELETE_DRAFT"

        user_data[
            "menu"
        ] = "DRAFT_MENU"
        await update.message.reply_text(
            "Pilih item yang akan dihapus",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
    elif text == "➕ Tambah Barang":

        brands = get_brand_list()

        keyboard = []

        for i in range(
            0,
            len(brands),
            2
        ):
            keyboard.append(
                brands[i:i+2]
            )

        keyboard.append(
            ["📋 Lihat Draft"]
        )

        keyboard.append(
            ["❌ Batal"]
        )

        await update.message.reply_text(
            "Pilih Merk",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
    elif text == "❌ Batal":

        user_data.pop(
            "draft_out",
            None
        )

        user_data.pop(
            "trx_type",
            None
        )

        user_data.pop(
            "selected_item",
            None
        )

        user_data.pop(
            "out_brand",
            None
        )

        user_data.pop(
            "out_jenis",
            None
        )

        user_data.pop(
            "out_lokasi",
            None
        )

        keyboard = [
            ["📦 Stock", "📥 Barang Masuk"],
            ["📤 Barang Keluar", "⚠ Low Stock"],
            ["📈 Over Stock", "❌ Empty Stock"],
            ["📊 Stock Report"]
        ]

        await update.message.reply_text(
            "❌ Draft dibatalkan",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

        return
    # ==========================
    # LOW STOCK
    # ==========================

    elif text == "⚠ Low Stock":

        items = get_low_stock()

        excel_file = (
            create_low_stock_excel(
                items
            )
        )

        txt_file = (
            create_low_stock_txt(
                items
            )
        )

        await update.message.reply_text(
            f"⚠ LOW STOCK\n\n"
            f"Total Item : {len(items)}"
            )

        await update.message.reply_document(
            document=open(
                excel_file,
                "rb"
            ),
            filename="low_stock_report.xlsx"
        )

        await update.message.reply_document(
            document=open(
                txt_file,
                "rb"
            ),
            filename="low_stock_report.txt"
        )

    # ==========================
    # OVER STOCK
    # ==========================

    elif text == "📈 Over Stock":

        items = get_over_stock()

        message = "📈 OVER STOCK\n\n"

        for item in items[:50]:

            message += (
                f"{item['kode']}\n"
                f"Stock : {item['stock']}\n"
                f"Max : {item['max']}\n\n"
            )

        await update.message.reply_text(
            message
        )

    # ==========================
    # EMPTY STOCK
    # ==========================

    elif text == "❌ Empty Stock":

        items = get_empty_stock()

        message = "❌ STOCK KOSONG\n\n"

        for item in items[:50]:

            message += (
                f"{item['kode']}\n"
                f"{item['nama']}\n\n"
            )

        await update.message.reply_text(
            message
        )

    # ==========================
    # MENU UTAMA
    # ==========================
    elif text == "⬅️ Menu Utama":

        role = get_user_role(
            update.effective_user.id
        )

        await show_main_menu(
            update,
            role
        ) 
        return
    
    elif text == "⬅️ Kembali":

        current_menu = (
            user_data.get(
                "menu",
                ""
            )
        )
        if user_data.get(
            "menu"
        ) == "DRAFT_MENU":

            trx_type = user_data.get(
                "trx_type"
            )

            submit_text = (
                "✅ Submit"
            )

            if trx_type == "IN":

                keyboard = [
                    ["➕ Tambah Barang"],
                    ["➖ Hapus Barang"],
                    ["📋 Lihat Draft IN"],
                    ["✅ Submit IN"],
                    ["❌ Batal"]
                ]

            else:

                keyboard = [
                    ["➕ Tambah Barang"],
                    ["➖ Hapus Barang"],
                    ["📋 Lihat Draft OUT"],
                    ["✅ Submit OUT"],
                    ["❌ Batal"]
                ]

            user_data["mode"] = ""
            user_data["menu"] = ""

            await update.message.reply_text(
                "Menu Draft",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return
        
        elif current_menu == "IN_ITEM":

            brand = user_data.get(
                "in_brand"
            )

            types = get_type_by_brand(
                brand
            )

            keyboard = []

            for i in range(
                0,
                len(types),
                2
            ):
                keyboard.append(
                    types[i:i+2]
                )

            keyboard.append(
                ["⬅️ Kembali"]
            )

            user_data["menu"] = "IN_TYPE"

            await update.message.reply_text(
                f"Pilih Jenis ({brand})",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return
    
        elif current_menu == "IN_TYPE":

            brands = get_brand_list()

            keyboard = []

            for i in range(
                0,
                len(brands),
                2
            ):
                keyboard.append(
                    brands[i:i+2]
                )

            keyboard.append(
                ["⬅️ Kembali"]
            )

            user_data["menu"] = "IN_BRAND"

            await update.message.reply_text(
                "Pilih Merk",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return
        
        elif current_menu == "IN_BRAND":

            role = get_user_role(
                update.effective_user.id
            )

            await show_main_menu(
                update,
                role
            )

            return
        

        
            return
        
        elif current_menu == "OUT_ITEM":

            brand = user_data.get(
                "out_brand"
            )

            types = get_type_by_brand(
                brand
            )

            keyboard = []

            for i in range(
                0,
                len(types),
                2
            ):
                keyboard.append(
                    types[i:i+2]
                )

            keyboard.append(
                ["⬅️ Kembali"]
            )

            user_data["menu"] = "OUT_TYPE"

            await update.message.reply_text(
                f"Pilih Jenis ({brand})",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return
    
        elif current_menu == "OUT_TYPE":

            brands = get_brand_list()

            keyboard = []

            for i in range(
                0,
                len(brands),
                2
            ):
                keyboard.append(
                    brands[i:i+2]
                )

            keyboard.append(
                ["⬅️ Kembali"]
            )

            user_data["menu"] = "OUT_BRAND"

            await update.message.reply_text(
                "Pilih Merk",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return
        
        elif current_menu == "OUT_BRAND":

            role = get_user_role(
                update.effective_user.id
            )

            await show_main_menu(
                update,
                role
            )

            return

        elif current_menu == "STOCK_DETAIL":

            role = get_user_role(
                update.effective_user.id
            )
            await show_main_menu(
                update,
                role
            )

            return

        elif current_menu == "OUT":

            keyboard = [
                ["📦 Stock", "📥 Barang Masuk"],
                ["📤 Barang Keluar", "⚠ Low Stock"],
                ["📈 Over Stock", "❌ Empty Stock"],
                ["📊 Stock Report"]
            ]

            await update.message.reply_text(
                "🏠 Menu Utama",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard,
                    resize_keyboard=True
                )
            )

            return

        elif current_menu == "USER_MANAGEMENT":

            role = get_user_role(
                update.effective_user.id
            )

            await show_main_menu(
                update,
                role
            )

def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "myid",
            myid
        )
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_handler
    )
)

    print("Bot Running...Ngeeeeng")

    app.run_polling()



if __name__ == "__main__":
    main()