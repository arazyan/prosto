def read_xlsx(filename: str) -> list[str]:
    res = []

    with open(filename, 'r') as file:
        file.readlines()