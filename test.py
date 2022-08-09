from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests, json, pickle

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
    
login_msg_str = '로그인 하러 가기'
test_url = 'https://partner.yanolja.com/reservation/search?dateType=RESERVATION_DATE&startDate=2022-08-09&endDate=2022-08-09&reservationStatus=ALL&keywordType=VISITOR_NAME&page=1&size=50&sort=checkInDate,desc&selectedDate=2022-08-09&searchType=detail&useTypeDetail=ALL&useTypeCheckIn=ALL'    
res = requests.get(test_url, headers=headers)
header2 = {"headers":headers}
print(type(headers))
with open('yanolja_header.txt','w') as output:
    json.dump(headers,output)
#pickle.dump(headers, open("yanolja_header.txt","wb"))

while(True):
    pass
