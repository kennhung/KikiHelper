import requests
from bs4 import BeautifulSoup
import bs4
import time
from colorama import init, Fore, Back, Style
init(autoreset=True)

from currentCourseList import GetSelectedCourse

kiki_helper_art = '''  _  __  _   _  __  _     _    _          _                       
 | |/ / (_) | |/ / (_)   | |  | |        | |                      
 | ' /   _  | ' /   _    | |__| |   ___  | |  _ __     ___   _ __ 
 |  <   | | |  <   | |   |  __  |  / _ \ | | | '_ \   / _ \ | '__|
 | . \  | | | . \  | |   | |  | | |  __/ | | | |_) | |  __/ | |   
 |_|\_\ |_| |_|\_\ |_|   |_|  |_|  \___| |_| | .__/   \___| |_|   
                                             | |                  
                                             |_|            
'''

def user_info(session_id):
    resp = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Selected_View00.cgi?session_id="+session_id)
    resp.encoding = 'utf8'
    if resp.text.find("您輸入的密碼有誤")!=-1 or resp.text.find("您本次的登入已經無效")!=-1:
        return None
    login_status_bs = BeautifulSoup(resp.text, 'lxml')
    login_status_bs = login_status_bs.find('table').tr.findAll("th")
    return {"name": login_status_bs[0].text[4:], "id": login_status_bs[1].text[4:], "dept": login_status_bs[2].text[4:], "grade": login_status_bs[3].text[4:], "class_id": login_status_bs[4].text[4:],}

def systemStatus():
    resp = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/system_state.php")
    resp.encoding = 'utf8'
    sysStatus_bs = BeautifulSoup(resp.text, 'lxml')
    sysStatus_bs = sysStatus_bs.find('table').find('table')
    sysStatus_bs = sysStatus_bs.findAll('font', attrs={"size":2})
    # print(sysStatus_bs)
    return {"status": sysStatus_bs[0].parent["bgcolor"], "semester": sysStatus_bs[2].font.text, "status_text": sysStatus_bs[3].font.text}

def announce():
    resp = requests.get("https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/announce.php")
    resp.encoding = 'utf8'
    announce_bs = BeautifulSoup(resp.text, 'lxml')
    announce_bs = announce_bs.find('th', attrs={"bgcolor":"YELLOW"})
    announce_bs = announce_bs.parent.parent.findAll("tr")
    announce_bs = announce_bs[2:]
    announce_data = []
    for ann in announce_bs:
        td = ann.findAll("td")
        announce_data.append({
            "pub_date":td[0].text,
            "title": td[1].a.text,
            "top": td[1].font.text.find("(置頂)") != -1,
            "link": td[1].a["href"]
        })
    return announce_data

def announce_mode():
    while True:
        announcements = announce()
        count = 0
        for i in announcements:
            count+=1
            title = ""
            if(i["top"]):
                title+=Fore.RED
            title+=i["title"]
            print("{no} {date}: {title}".format(no=count, date=i["pub_date"], title = title))
        print()
        select = number_input(Fore.BLUE+"Select a announcement (enter 0 to exit):", False)
        if select <= 0:
            break
        elif select > len(announcements):
            print(Fore.RED+"This number is not in the list")
        else:
            print("\nhttps://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/"+announcements[select]["link"])
            


def number_input(texts, useArrow=True):
    input_num = None
    input_str = ""
    print(texts, end='')
    if useArrow:
        print()
        input_str = input("> ")
    else:
        input_str = input(" ")
    try:
        input_num = int(input_str)
    except ValueError:
        print(Fore.RED+"Enter a integer")
        return number_input(texts)
    return input_num

if __name__ == "__main__":

    announce()
    print(Fore.MAGENTA+kiki_helper_art)
    
    authMode = 2
    main_session_id = ""
    login_status = None

    while login_status == None:
        while True:
            authMode = number_input("? Login mode:\n1)password mode\n2)session_id mode")
            print()
            if authMode == 1:
                # TODO: add password & username login
                # break
                print(Fore.RED+"password mode currently not available")
            elif authMode == 2:
                main_session_id = input("session_id: ")
                break

        login_status = user_info(main_session_id)
        if login_status == None:
            print(Fore.RED+"Login failed!!")

    print("Login as {id}: {name} {dept} {grade}{class_id}".format(id=login_status["id"], name=login_status["name"], dept=login_status["dept"], grade=login_status["grade"], class_id=login_status["class_id"]))
    
    sysStatus = systemStatus()
    print("\nSystem Status: {status_text}\nSemester: {semester}\n".format(status_text=sysStatus["status_text"], semester=sysStatus["semester"]))

    mode = -1
    while True:
        mode = number_input(Fore.CYAN + "\n? Select mode:\n1) Show Current Course\n2) Steal Course\n3) Course Monitor\n4) Show announce")
        print()
        if mode == 1:
            if(sysStatus["status_text"].find("暫不開放查詢") != -1):
                print(Fore.RED+"System currently closed!!")
            else:
                print(GetSelectedCourse(main_session_id))
        elif mode == 2:
            if(sysStatus["status_text"].find("先搶先贏") != -1):
                break
            else:
                print(Fore.RED+"Can't do this now!!")
        elif mode == 3:
            break
        elif mode == 4:
            announce_mode()
    pass
