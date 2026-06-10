from sheet_service import (
    get_user_role_data,
    add_user_role
)

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

def get_user_role(
    telegram_id
):

    data = get_user_role_data()

    for row in data[1:]:

        if len(row) < 4:
            continue

        if row[1] == str(
            telegram_id
        ):

            return row[3]

    return "VIEWER"

def is_admin(
    telegram_id
):

    return (
        get_user_role(
            telegram_id
        )
        == "ADMIN"
    )


def is_operator(
    telegram_id
):

    return (
        get_user_role(
            telegram_id
        )
        in [
            "ADMIN",
            "OPERATOR"
        ]
    )