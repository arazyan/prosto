import pandas as pd

def export_time(csv_path: 'str'):
  """Вычленяет время и возвращает его в виде списка"""
  df         = pd.read_csv(csv_path)
  df['DATE'] = pd.to_datetime(df['DATE'])
  times      = [':'.join(str(t).split(':')[:2]) for t in df['DATE'].dt.time]
  return times



if __name__ == '__main__':
  print(export_time('exported.csv'))

