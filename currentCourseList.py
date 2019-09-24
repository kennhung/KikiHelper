from bs4 import BeautifulSoup
import bs4
import requests

def GetSelectedCourse(session_id):
    res = requests.get('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Selected_View00.cgi?session_id='+session_id)
    res.encoding = "utf8"
    soup = BeautifulSoup(res.text, 'lxml')
    d = Selected_View00(soup)
    return d


def Selected_View00(soup):
    tables = soup.find_all('table', attrs={"border":"1"})
    titles = tables[0].find_all('th', attrs={"bgcolor":"yellow"})
    tr = titles[0].find_parents("tr")[0].find_next_sibling("tr")

    data = []
    while(True):
        if(type(tr) != bs4.element.Tag):
            break

        col = []
        for th in tr.select('th'):
            col.append(th)
    
        okCirc = col[0].find('img', attrs={"src":"../../Graph/O.gif"})
        
        dict = {
            "ok": (type(okCirc) == bs4.element.Tag) or True,
            "code": col[0].font.text,
            "num": col[1].font.text,
            "name": col[2].font.text,
            "teacher": col[3].font.text,
            "type": col[5].font.text,
            "time": col[6].font.text,
            "room": col[7].font.text
        }

        data.append(dict)

        tr = tr.find_next_sibling("tr")

    return data
