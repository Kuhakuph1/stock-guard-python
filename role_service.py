from sheet_service import (
    get_user_role_data,
    add_user_role
)

# Inisialisasi variabel global ROLE_MAP di luar fungsi
ROLE_MAP = None


def get_all_users():
    data = get_user_role_data()
    users = []

    for row in data[1:]:
        if len(row) < 4:
            continue

        users.append({
            "id": row[1],
            "username": row[2],
            "role": row[3]
        })

    return users


def get_user_role(telegram_id):
    global ROLE_MAP

    if ROLE_MAP is None:
        ROLE_MAP = {}
        data = get_user_role_data()

        for row in data[1:]:
            if len(row) < 4:
                continue

            ROLE_MAP[row[1]] = row[3]

    return ROLE_MAP.get(str(telegram_id), "VIEWER")


def is_admin(telegram_id):
    return get_user_role(telegram_id) == "ADMIN"


def is_operator(telegram_id):
    return get_user_role(telegram_id) in ["ADMIN", "OPERATOR"]