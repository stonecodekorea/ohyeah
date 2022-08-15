import requests, json, pickle, re
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def yanolja_selenium():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    login_url = 'https://account.yanolja.biz/?serviceType=PC&redirectURL=%2F&returnURL=https%3A%2F%2Fpartner.yanolja.com%2Fauth%2Flogin'
    driver.get(login_url)
    driver.implicitly_wait(10) # seconds
    driver.find_element(By.XPATH,'//*[@id="input-28"]').send_keys('0319973230')
    driver.find_element(By.XPATH,'//*[@id="input-34"]').send_keys('#assem3070')
    driver.find_element(By.XPATH,'//*[@id="app"]/div/div[1]/div/a/span').click()
    driver.implicitly_wait(10) # seconds
    driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/aside/div[1]/div[1]/div[3]/div/div[2]/div').click()
    #driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/aside/div[1]/div[1]/div[3]/div[2]/a/div[2]/div').click()
    #driver.implicitly_wait(10) # seconds
    #result_xpath = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/div/main/div/div/div/div[5]/div[2]/div')
    #result = result_xpath.text        
    for request2 in driver.requests:
        headers = request2.headers    
   
    return headers
       
def write_yanolja_headers(headers):
    head = {'host':headers['host'], 'Connection':headers['Connection'], 'sec-ch-ua':headers['sec-ch-ua'], 'sec-ch-ua-mobile':headers['sec-ch-ua-mobile'],
            'User-Agent':headers['User-Agent'], 'sec-ch-ua-platform':headers['sec-ch-ua-platform'], 'Accept':headers['Accept'], 'Sec-Fetch-Site':headers['Sec-Fetch-Site'],
            'Sec-Fetch-Mode':headers['Sec-Fetch-Mode'], 'Sec-Fetch-Dest':headers['Sec-Fetch-Dest'],'Referer':headers['Referer'], 'Accept-Encoding':headers['Accept-Encoding'],
            'Accept-Language':headers['Accept-Language'], 'Cookie':headers['Cookie']}
    with open('yanolja_header.json', 'w') as outfile:
        json.dump(head, outfile)               
    return head
       

headers = ""
try:
    with open('yanolja_header.json', "r") as json_file:
        json_data = json.load(json_file)
        headers = json_data
except:
    headers = yanolja_selenium()
    write_yanolja_headers(headers)


log_msg = '김포 HOTEL ASSEM'
#test_url = test_url + date_str+start_date+end_date+res_status_str+keyword_type+sort_str+selectdate_str+search_type+use_type
test_url = 'https://partner.yanolja.com/reservation/search?dateType=RESERVATION_DATE&startDate=2022-08-09&endDate=2022-08-09&reservationStatus=ALL&keywordType=VISITOR_NAME&page=1&size=50&sort=checkInDate,desc&selectedDate=2022-08-09&searchType=detail&useTypeDetail=STAY&useTypeCheckIn=STAY'
res = requests.get(test_url, headers=headers)
temp_test = res.text.encode('utf-8','ignore')
with open('test2.txt', 'wb') as temp_text :
    temp_text.write(temp_test)

p = re.compile('김포 HOTEL ASSEM')
result = p.findall(res.text)
if not result :
    headers = yanolja_selenium()
    res = requests.get(test_url, headers=headers)
    write_yanolja_headers(headers)

# 예약현황 추출하기
res_data = 0
html = BeautifulSoup(res.text, 'html.parser')
infos = html.select('tr.ReservationSearchListItem')
res_name = []
res_room_type = []
res_chk_data = []
temp = {}
res_data = []
temp_name = ''
temp_phone = ''
t_chkin = ''
t_chkout = ''

p = re.compile('([가-힣]+)([0-9]+)')
p_chkinout = re.compile('([0-9\.]+\s\([가-힣]\)\s[0-9]*:[0-9]0)')
f = open('.test.txt','w')

#test2
try:
    test = infos[0].select_one('td.ReservationSearchListItem__visitor').text
    test2 = infos[0].select_one('td.ReservationSearchListItem__date').text
    
    #headers = yanolja_selenium()
    headers = write_yanolja_headers(headers)
    res = requests.get(test_url, headers=headers)  
    #f.write(res.text)  
    html = BeautifulSoup(res.text, 'html.parser')
    infos = html.select('tr.ReservationSearchListItem')

    for i in range(len(infos)) :
        test = infos[i].select_one('td.ReservationSearchListItem__visitor').text
        test2 = infos[i].select_one('td.ReservationSearchListItem__date').text
    
        test = test.replace('\n','')
        test = test.replace(' ','')
    
        pat_temp = p.findall(test)
        pat_chk = p_chkinout.findall(test2)
        #f.write(pat_chk)
        for j in range(len(pat_temp)):
            temp_name = pat_temp[j][0]
            temp_phone = pat_temp[j][1]
        #for j in range(len(pat_chk)):    
        t_chkin = pat_chk[0]
        t_chkout = pat_chk[1]
        
        temp['name'] =  temp_name
        temp['phone'] = temp_phone
        temp['room'] = infos[i].select_one('div.body-2').text
        temp['chk'] = infos[i].select_one('td.ReservationSearchListItem__date').text
        temp['chkin'] = t_chkin
        temp['chkout'] = t_chkout
        res_data.append(temp)
        temp={}
        res_name.append(infos[i].select_one('td.ReservationSearchListItem__visitor').text)
        res_room_type.append(infos[i].select_one('div.body-2').text)
        res_chk_data.append(infos[i].select_one('td.ReservationSearchListItem__date').text)
except:
    res_name = []
    res_room_type = []
    res_chk_data = []
    temp = {}
    res_data = []   
    test2 = []     
    pat_chk = []   
f.close()

print(res_data)
while(True):
    pass
