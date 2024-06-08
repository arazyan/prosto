def read_xlsx(filepath: str) -> list[str]:

    with open(filepath, 'r') as file:
        res = file.readlines()

    return res

print('amogus')
print(read_xlsx('assets/ondeal.xlsx'))
