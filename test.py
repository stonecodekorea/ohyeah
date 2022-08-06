from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
login_url = 'https://account.yanolja.biz/?serviceType=PC&redirectURL=%2F&returnURL=https%3A%2F%2Fpartner.yanolja.com%2Fauth%2Flogin'
driver.get(login_url)
driver.find_element(By.XPATH,'//*[@id="input-28"]').send_keys('0319973230')
driver.find_element(By.XPATH,'//*[@id="input-34"]').send_keys('#assem3070')
driver.find_element(By.XPATH,'//*[@id="app"]/div/div[1]/div/a/span').click()
driver.implicitly_wait(10) # seconds
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/aside/div[1]/div[1]/div[3]/div/div[2]/div').click()
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/aside/div[1]/div[1]/div[3]/div[2]/a/div[2]/div').click()
driver.implicitly_wait(10) # seconds
result_xpath = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/main/div/div/div/div[5]/div[2]/div')
result = result_xpath.text
while(True):
    pass
