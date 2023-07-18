from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

url='https://12306.cn/'
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(r'C:\Users\Administrator\Documents\meijmPy\chromedriver.exe',options=options)

def element_input(ele_id,ele_input):
    element=driver.find_element(By.ID, ele_id)
    try:#search has no input
        element.clear()
        element.click()
        element.send_keys(ele_input)
    except:
        print(ele_id+' no input')
    element.send_keys(Keys.ENTER)
    time.sleep(1)

#from_station='上海',to_station='郑州',train_date='2023-05-07'
def ticket_find(from_station,to_station,train_date):
    print('enter ticket_find()')
    driver.get(url)

    element_input('fromStationText',from_station)
    element_input('toStationText',to_station)
    element_input('train_date',train_date)
    element_input('search_one','')
    #drive switch 
    print(driver.window_handles)
    print(driver.current_window_handle)
    driver.switch_to.window(driver.window_handles[1])#switch to new tab
    print(driver.current_url)
    time.sleep(3)
    page_text = driver.page_source
    soup = BeautifulSoup(page_text, 'html.parser')

    find_id = soup.find(id='queryLeftTable')
    columlist=['出发站','到达站','出发时间','达到时间','时长','商务座','一等座','二等座','高级软卧','软卧','动卧','硬卧','软座','硬座','无座','其他','预定']
    train_df = pd.DataFrame([],columns=columlist)#to store all info
    #each train info， and all train' id start with ticket in source page
    tr_list=find_id.find_all(name='tr',id=re.compile("ticket_*"))
    for train in tr_list:
        td_list=train.find_all('td')#each seat info
        count=0#we need to extract the train info from the first td
        seat_list=[]#to store seat info
        for treat in td_list:
            if count==0:
                train_id=treat.find(title='点击查看停靠站信息')
                #print(train_id.text)
                for strong in treat.find_all('strong'):#the time and station info in strong
                    #print(strong.text)
                    seat_list.append(strong.text)
            else:
                #print(treat.text)
                seat_list.append(treat.text)
            count=count+1
        train_df1=pd.DataFrame(seat_list,index=columlist,columns=[train_id.text]).T
        train_df=pd.concat([train_df,train_df1],axis=0)
        print(train_df)
    return train_df
    driver.close()

if __name__ == '__main__':
    print('enter statonOP.py')
    ticket_find('上海','郑州','2023-05-07')
