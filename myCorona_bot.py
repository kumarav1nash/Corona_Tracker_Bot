import os
from gtts import gTTS
import datetime
import json
import time
import requests
import argparse
import logging
from bs4 import BeautifulSoup
from tabulate import tabulate
URL = 'https://www.mohfw.gov.in/'
FILE_NAME = 'corona_india_dashboard.json'

changed = False
r = requests.get(URL)
htmlContent = r.text

def save(x):
    with open(FILE_NAME, 'w') as f:
        json.dump(x, f)

def load():
    res = {}
    with open(FILE_NAME, 'r') as f:
        res = json.load(f)
    return res
while True:
    past_data = load()


    def extract_contents(row): return [x.text.replace('\n', '') for x in row]
    soup = BeautifulSoup(htmlContent, "html.parser")


    overall_look = soup.find_all(class_="site-stats-count")
    _active_case = 0
    _total_death = 0
    _cured = 0


    number = extract_contents(overall_look[0].find_all('strong'))
    _active_case = number[0]
    _total_death = number[2]
    _cured = number[1]

    cur_data = {}
    cur_data['case'] = {'_active_case':_active_case,'_cured':_cured,'_total_death':_total_death}
    save(cur_data)

    if cur_data != past_data:
        changed = True
    else:
        changed = False



    if changed:
        all_rows = soup.find_all('tr')
        for row in all_rows:
            stat = extract_contents(row.find_all('td'))
            print(stat)
        print("---------------------------------------------------------------------------")
        print("\n it will take some time depending on your network coneection, plese wait! \n")
        print("---------------------------------------------------------------------------")

        alert = "Attention Please!, The Number of cases of Covid 19 has increased and total active cases till now is {0}. The total death toll so far is {1}. I request you to please stay at home and help the country to fight this pandemic".format(
        _active_case, _total_death)
        alert_hindi = "कृपया ध्यान दें!, कोविद 19 के मामलों की संख्या में वृद्धि हुई है और अब तक के कुल सक्रिय मामले {0} हैं। अब तक कुल {1} मौते हुये है। मेरा आपसे अनुरोध है कि कृपया घर पर रहें और देश को इस महामारी से लड़ने में मदद करें".format(
        _active_case, _total_death)
        alert_sound = gTTS(text=alert, lang='en', slow=False)
        alert_sound_hi = gTTS(text=alert_hindi, lang='hi', slow=False)
        alert_sound.save("alarm.mp3")
        alert_sound_hi.save("alarm_hi.mp3")
        # Playing the converted file
        os.system("mpg321 alarm.mp3")
        os.system("mpg321 alarm_hi.mp3")
        
    else:
        print("No Change! {}".format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        print(past_data)
        time.sleep(5)






