def set_menu(
    user_data,
    menu
):
    user_data["menu"] = menu


def set_mode(
    user_data,
    mode
):
    user_data["mode"] = mode


def clear_mode(
    user_data
):
    user_data["mode"] = ""


def clear_transaction(
    user_data
):

    keys = [
        "trx_type",
        "selected_item",

        "draft_in",
        "draft_out",

        "in_brand",
        "in_jenis",
        "in_lokasi",
        "in_status",

        "out_brand",
        "out_jenis",
        "out_lokasi",
        "out_status",

        "brand",
        "jenis",
        "lokasi"
    ]

    for key in keys:

        user_data.pop(
            key,
            None
        )

    user_data["menu"] = "MAIN"
    user_data["mode"] = ""


def goto_menu(
    user_data,
    menu
):
    user_data["menu"] = menu
    user_data["mode"] = ""

    print(
        f"STATE -> {menu}"
    )