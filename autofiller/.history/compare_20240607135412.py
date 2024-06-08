def read_xlsx(filepath: str) -> list[str]:

    with open(filename, 'r') as file:
        res = file.readlines()

    return res


print(read_xlsx('assets'))