import pandas as pd

def write_output(filename: str, dataframe: pd.DataFrame) -> None:
    dataframe.to_excel(filename)