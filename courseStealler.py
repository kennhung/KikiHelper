import requests
from bs4 import BeautifulSoup
import bs4

def Selected_View00(soup):
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
    
        okCirc = col[0].find('input')
        
        dict = {
            "input": okCirc,
            "current": col[1].font.text,
            "remain": col[2].font.text
        }

        data.append(dict)

        tr = tr.find_next_sibling("tr")

    return data

if __name__ == "__main__":
    session_id = input("session_id: ")
    page = input("page: ")
    cate = input("cate: ")
    sub_cate = input("sub cate: ")


    # res = requests.get('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi?session_id='+session_id+'&dept=I001&grade=1&page='+page+'&cge_cate='+cate+'&cge_subcate'+sub_cate)
    res = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi?session_id="+session_id+"&dept=I001&grade=1&page=2&cge_cate=2&cge_subcate=5")
    soup = BeautifulSoup(res.text, 'lxml')

    d = Selected_View00(soup)

    count = 0
    for i in d:
        print("{count}\t{input}\t{current}, {remain}".format(count=count,input= i["input"]["value"],current=i["current"], remain=i["remain"]))
        count+=1