import requests
import sched, time
from bs4 import BeautifulSoup
import bs4
from courseStealler import SoupToData

import datetime

session_id = input("session_id: ")

def steal():
    res = requests.post("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi", "session_id="+session_id+"&dept=I001&grade=1&cge_cate=2&cge_subcate=3&page=1&e=0&m=0&SelectTag=1&7300005_01=3&7300006_01=3&7302028_01=3&7302039_01=3&7302041_01=3&7302042_01=3&7302044_01=3&7302045_01=3&course=7302046_01&7302046_01=3&7303007_01=3")
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find_all("a", attrs={"href":"javascript:history.back()"})
    print(a)

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    res = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi?session_id="+session_id+"&use_cge_new_cate=1&m=0&dept=I001&grade=1&page=2&cge_cate=2&cge_subcate=5")
    soup = BeautifulSoup(res.text, 'lxml')
    d = SoupToData(soup)
    print(datetime.datetime.now() , d[6]["remain"])

    if(d[6]["remain"] != "0"): 
        print("found at:", datetime.datetime.now())
        steal()
    else:
        s.enter(2, 1, do_something, (sc,))

s.enter(2, 1, do_something, (s,))
s.run()
