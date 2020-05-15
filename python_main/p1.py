# _*_ coding: utf-8 _*_

import time
import datetime

list = {i ** 2 for i in range(1, 6)}
print (list)


def print_hello():
    print("TimeNow in func: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return


print ("p1.py hello")


if __name__ == "__main__":
    print_hello()
#	print ('main from p1.py')

