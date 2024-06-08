

def write_output(filename: str, string: str) -> None:
    with open(filename, 'wb') as file:
        file.write(string)