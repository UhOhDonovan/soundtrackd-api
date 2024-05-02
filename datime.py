from datetime import date
from time import strftime, gmtime
import time

thedate = date.fromtimestamp(time.time())
thetime = strftime("%H:%M:%S", time.localtime())
print(thedate, thetime)
