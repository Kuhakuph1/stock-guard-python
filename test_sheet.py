from sheet_service import get_master_data

data = get_master_data()

for row in data[:10]:
    print(row)