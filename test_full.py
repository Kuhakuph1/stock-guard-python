from sheet_service import get_setting_full

data = get_setting_full()

for row in data[:20]:
    print(row)