import pandas as pd

from datetime import datetime

import qrs
import times

# типа append'а
# df2 = pd.DataFrame([[2,3,4]], columns=['A','B','C'])
# pd.concat([df2, df])
#


# -----------
# times и qrs без лишних пробелов и переносов

def beaty_times(datetimezones: list[str]) -> list[str]:
  """Возвращает время в красивом формате, если оно задано как:\n\t2024-06-17 22:01:19 +0300\n\t->22:01"""
  if '+' in datetimezones[0]: times = [datetime.fromisoformat(elem.strip()).strftime("%H:%M") for elem in datetimezones]
  else:
    times = [datetime.strptime(elem.strip(), '%H:%M:%S').strftime("%H:%M") for elem in datetimezones]
  return times


# allqrs   = qrs.qrs1.split('\n')
# allqrs.extend(qrs.qrs2.split('\n'))
allqrs = qrs.qr3.split('\n')

# alltimes = (beaty_times(times.times1.split('\n')))
# alltimes.extend(beaty_times(times.times2.split('\n')))
alltimes = beaty_times(times.time3.split('\n'))

# print(len(allqrs), len(alltimes))
# print(allqrs)
# print(alltimes)


qr_time_sorted = sorted([[qr, time] for qr, time in zip(allqrs, alltimes)], key=lambda x: x[1])

# for pair in qr_time_sorted:
  # print(pair)

# print(len(allqrs), len(alltimes))
