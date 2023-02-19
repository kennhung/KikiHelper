import requests
from bs4 import BeautifulSoup
import bs4

def SoupToData(soup):
    # print(soup)
    # return
    titles = soup.find_all('th', attrs={"bgcolor":"yellow"})
    # print(titles)
    # return 
    tr = titles[0].find_parents("tr")[0].find_next_sibling("tr")

    data = []
    while(True):
        if(type(tr) != bs4.element.Tag):
            break

        col = []
        for th in tr.select('th'):
            col.append(th)
    
        inputTag = col[0].find('input')
        
        current = col[1].text
        if col[1].font is not None:
            current = col[1].font.text

        remain = col[2].text
        if col[2].font is not None:
            remain = col[2].font.text

        dict = {
            "input": inputTag,
            "current": current,
            "remain": remain,
            "name": col[3].font.text,
            "course_num": '_'.join(col[12].font.a['href'].split("course=")[1].split("&group="))
        }

        data.append(dict)

        tr = tr.find_next_sibling("tr")

    return data

def SearchCourse(session_id, dept, grade, page, cge_cate, cge_subcate):
    try:
        res = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi?session_id="+session_id+"&use_cge_new_cate=1&dept="+dept+"&grade="+grade+"&page="+page+"&cge_cate="+cge_cate+"&cge_subcate="+cge_subcate)
        res.encoding = 'utf8'
    except requests.ConnectionError:
        print("connection error")
        return 
    if(res.status_code != 200):
        return
    else:
        return BeautifulSoup(res.text, 'lxml')

if __name__ == "__main__":
    session = input("session_id: ")
    dept = input("dept: ")
    grade = input("grade: ")
    page = input("page: ")
    cate = input("cate: ")
    sub_cate = input("sub cate: ")

    soup = SearchCourse(session, dept, grade, page, cate, sub_cate)

    d = SoupToData(soup)

    count = 0
    for i in d:
        print("{count}\t{input}\t{current}, {remain}".format(count=count,input= i["input"]["value"],current=i["current"], remain=i["remain"]))
        count+=1