import pandas as pd

def write_df(filename: str, dataframe: pd.DataFrame) -> None:
    dataframe.to_excel(filename)