from sheet_service import (
    get_user_role_data,
    add_user_role
)

# Hapus variabel global ROLE_MAP agar selalu mengambil data terbaru atau pastikan ter-refresh

def get_all_users():
    data = get_user_role_data()
    users = []

    for row in data[1:]:
        if len(row) < 4:
            continue

        users.append({
            "id": str(row[1]).strip(),
            "username": row[2],
            "role": row[3].strip().upper()
        })

    return users


def get_user_role(telegram_id):
    # Ambil data terbaru langsung dari sheet_service
    data = get_user_role_data()
    
    target_id = str(telegram_id).strip()

    for row in data[1:]:
        if len(row) < 4:
            continue
        
        # Bersihkan spasi dari ID di spreadsheet
        sheet_id = str(row[1]).strip()
        sheet_role = str(row[3]).strip().upper()

        if sheet_id == target_id:
            return sheet_role

    return "VIEWER"


def is_admin(telegram_id):
    return get_user_role(telegram_id) == "ADMIN"


def is_operator(telegram_id):
    return get_user_role(telegram_id) in ["ADMIN", "OPERATOR"]