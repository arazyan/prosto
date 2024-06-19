def read_xlsx(filename: str) -> list[str]:

    with open(filename, 'r') as file:
        res = file.readlines()