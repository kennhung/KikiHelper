import requests
import sched, time
from bs4 import BeautifulSoup
import bs4
from courseStealler import SearchCourse, SoupToData

import datetime

def steal(session_id, dept, grade, page, cge_cate, cge_subcate, course):
    res = requests.post("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi", "session_id="+session+"&dept="+dept+"&grade="+grade+"&cge_cate="+cate+"&cge_subcate="+cge_subcate+"&page="+page+"&SelectTag=1&course="+course+"&"+course+"=3")
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find_all("a", attrs={"href":"javascript:history.back()"})
    print(a)

def foundCourseIndex(course_num, d):
    counter = 0
    for data in d:
        if data["input"]["value"] == course_num:
            return counter
        counter+=1 

if __name__ == "__main__":   
    session = input("session_id: ")
    dept = input("dept: ")
    grade = input("grade: ")
    page = input("page: ")
    cate = input("cate: ")
    sub_cate = input("sub cate: ")
    course = input("course: ")

    soup = SearchCourse(session, dept, grade, page, cate, sub_cate)
    d = SoupToData(soup)
    num = foundCourseIndex(course, d)
    print("stealing course {index}: {name}, {current}".format(index=num, name=d[num]["name"], current=d[num]["current"]))

    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc): 
        soup = SearchCourse(session, dept, grade, page, cate, sub_cate)
        d = SoupToData(soup)
        num = foundCourseIndex(course, d)

        print(datetime.datetime.now() , d[num]["remain"])

        #TODO: find course row number
        if(d[num]["remain"] != "0"): 
            print("found at:", datetime.datetime.now())
            steal(session, dept, grade, page,cate,sub_cate, course)
        else:
            s.enter(2, 1, do_something, (sc,))

    s.enter(2, 1, do_something, (s,))
    s.run()
