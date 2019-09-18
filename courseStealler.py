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
            "remain": remain
        }

        data.append(dict)

        tr = tr.find_next_sibling("tr")

    return data

def SearchCourse(dept, grade, page, cge_cate, cge_subcate):
    res = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi?session_id="+session_id+"&dept="+dept+"&grade="+grade+"&page="+page+"&cge_cate="+cge_cate+"&cge_subcate="+cge_subcate)
    return BeautifulSoup(res.text, 'lxml')

if __name__ == "__main__":
    session_id = input("session_id: ")
    dept = input("dept: ")
    grade = input("grade: ")
    page = input("page: ")
    cate = input("cate: ")
    sub_cate = input("sub cate: ")

    soup = SearchCourse(dept, grade, page, cate, sub_cate)

    d = SoupToData(soup)

    count = 0
    for i in d:
        print("{count}\t{input}\t{current}, {remain}".format(count=count,input= i["input"]["value"],current=i["current"], remain=i["remain"]))
        count+=1