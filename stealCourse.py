import requests
import sched, time
from bs4 import BeautifulSoup
import bs4

session_id = input("session_id: ")

def steal():
    res = requests.post("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi", "session_id="+session_id+"&dept=I001&grade=1&cge_cate=2&cge_subcate=5&page=2&e=0&m=0&SelectTag=1&7405018_01=3&7406018_01=3&7406018_02=3&7406032_01=3&7406032_02=3&7406035_01=3&course=7406036_01&7406036_01=3&7406036_02=3")
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find_all("a", attrs={"href":"javascript:history.back()"})
    print(a)

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    steal()
   
    # print(r)
    # do your stuff
    s.enter(5, 1, do_something, (sc,))

s.enter(5, 1, do_something, (s,))
s.run()
