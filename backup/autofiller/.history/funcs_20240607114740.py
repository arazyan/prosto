def write_output(filename: str, string: str) -> None:
    with open(filename, 'w') as file:
        file.write(string)