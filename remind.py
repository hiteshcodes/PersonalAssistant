import datetime
import json

import pywintypes
from win10toast import ToastNotifier

add = [""]


def remindNow():
    while True:
        data = openJson()
        currTime = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
        for i in data['task']:
            if currTime == i['remindAt'] and i['done'] == "false":
                j = 0
                length = len(add)
                flag = True
                while j < length:
                    if i['message'] == add[j]:
                        flag = False
                    j += 1

                if flag:
                    print(i['message'])
                    add.append(i['message'])
                    toast = ToastNotifier()
                    toast.show_toast(i['message'], "From Echo",
                                     icon_path=None, duration=10)


def openJson():
    with open("list.json", "r+") as source:
        try:
            data = json.load(source)
        except Exception as e:
            if e:
                print(e)
                remindNow()
            else:
                pass
    return data


remindNow()
