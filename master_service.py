from sheet_service import (
get_master_data,
get_setting_data,
get_setting_full
)

def get_all_master():
    data = get_master_data()

    return data[2:]

    print(data[0])
    print(data[1])
    print(data[2])
    print(data[3])

def get_brand_list():

    data = get_setting_data()

    brands = []

    for row in data[4:]:

        if len(row) < 3:
            continue

        brand = row[2].strip()

        if brand:
            brands.append(brand)

    return brands


def get_type_by_brand(brand):


    data = get_setting_full()

    result = []

    for row in data[4:]:
        

        if len(row) < 7:
            continue

        merk = row[5].strip()
        jenis = row[6].strip()

        if merk == brand:
            result.append(jenis)
    
    return result


def get_items_by_brand_type(
brand,
jenis
):

    data = get_all_master()
    items = []

    for row in data:

        if len(row) < 12:
            continue

        if row[2] != brand:
            continue

        if row[4] != jenis:
            continue

        items.append({
            "kode": row[3],
            "nama": row[5],
            "actual_stock": row[10],
            "status": row[11]
        })

    return items

def get_item_name_by_code(
    kode
):

    data = get_all_master()

    for row in data:

        if len(row) < 6:
            continue

        if row[3] == kode:

            return row[5]

    return ""

def get_brand_items(brand):

    data = get_all_master()
    items = []

    for row in data:

        if len(row) < 12:
         continue

        if row[2] == brand:

            items.append({
              "kode": row[3],
             "nama": row[5],
             "class": row[7],
              "min_stock": row[8],
             "max_stock": row[9],
              "actual_stock": row[10],
              "status": row[11]
            })

    return items


def get_item_by_code(kode_barang):

    data = get_all_master()

    for row in data:

        if len(row) < 12:
          continue

        if row[3] == kode_barang:

            return {
            "kode": row[3],
             "jenis": row[4],
             "nama": row[5],
             "satuan": row[6],
             "class": row[7],
             "min_stock": row[8],
              "max_stock": row[9],
             "actual_stock": row[10],
             "status": row[11]
            }

    return None


def get_low_stock():

    result = []

    data = get_all_master()

    for row in data:

        if len(row) < 12:
            continue
        try:
            actual = int(row[10])
            minimum = int(row[8])
        except:
            continue

        if actual <= minimum:

            result.append({
                "kode": row[3],
                "nama": row[5],
                "stock": actual,
                "min": minimum
            })

    return result


def get_over_stock():

    result = []

    data = get_all_master()

    for row in data:

        if len(row) < 12:
         continue

        try:
            actual = int(row[10])
            maximum = int(row[9])
        except:
            continue

        if actual > maximum:

            result.append({
                "kode": row[3],
                "nama": row[5],
                "stock": actual,
                "max": maximum
            })

    return result

def get_empty_stock():

    result = []

    data = get_all_master()

    for row in data:

        if len(row) < 12:
            continue

        try:
            actual = int(row[10])
        except:
            continue

        if actual == 0:

            result.append({
            "kode": row[3],
            "nama": row[5]
        })

    return result

def get_master_report():

    data = get_all_master()

    result = []

    for row in data:

        if len(row) < 12:
            continue

        result.append({

            "merk": row[2],

            "kode": row[3],

            "nama": row[5],

            "class": row[7],

            "min_stock": row[8],

            "max_stock": row[9],

            "actual_stock": row[10],

            "status": row[11]

        })

    return result
