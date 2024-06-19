import pandas as pd


def create_df() -> pd.DataFrame:
  return pd.DataFrame(data=[['A', 'B'], ['C', 'D']],columns=['Имя/Мероприятие', 'Время посещения'])

# def append_to_df(username: str, meetup: str, time: str):

# df = pd.DataFrame()
#
if __name__ == "__main__":
  df = create_df()
  print(df)
  # pd.DataFrame.join()
  # df = df.append(pd.DataFrame(data=['John', '00:00']))
  # print(df)

