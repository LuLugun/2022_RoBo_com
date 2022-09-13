from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chromeoptions = Options()
chromeoptions.add_argument("--log-level=3")
chromeoptions.add_argument("--headless")


def input_Keyword_search(chrome_driver,Keyword):
    Keyword_input = chrome_driver.find_element(By.XPATH,'//*[@id="arrive_search"]')
    Keyword_input.send_keys(Keyword)
    search_button = chrome_driver.find_element(By.XPATH,"/html/body/app-root/ng-component/tya-layout/intro-layout/section/div/flight-search/div/p[1]/img")
    search_button.click()

def Web_Driver_Wait(chrome_driver,str_class):
    while True:
        try:
            element = WebDriverWait(chrome_driver,10,0.5).until(
                EC.presence_of_element_located((By.CLASS_NAME,str_class))
            )
        except:
            print("loding")
        else:
            break

def change_time(chrome_driver):
    dropdown_select = chrome_driver.find_element(By.XPATH,'/html/body/app-root/ng-component/tya-layout/intro-layout/section/div/flight-search/div/flight-input[1]/div/div/img')
    dropdown_select.click()
    time_text = chrome_driver.find_element(By.XPATH,'/html/body/app-root/ng-component/tya-layout/intro-layout/section/div/flight-search/div/flight-input[1]/div/div/ul/li[3]')
    time_text.click()

def get_data(chrome_driver):
    data_dic = {'label':[]}
    flowd_text_list_all = []
    flowd_list = chrome_driver.find_elements(By.CLASS_NAME,'board')
    for flowd in flowd_list:
        flowd_text = flowd.get_attribute("textContent")
        flowd_text = flowd_text.replace('時間','\n').replace(' 目的地 ',',').replace(' 班機資訊',',').replace(' 航廈',',').replace(' 登機門',',').replace('報到櫃台',',').replace('狀態',',').replace('目的地班機資訊航廈登機門,,\n','').replace('    ','')
        flowd_text_list = flowd_text.split('\n')
        for i in flowd_text_list:
            if i != '':
                flowd_information = i.split(',')
                #print(flowd_information)
                if flowd_information[-1] != ' 出發  已飛 ' and flowd_information[-1] != '取消  ' and flowd_information[-1] != ' -   ':
                    company_number_list = flowd_information[2].replace('  ',',').split(',')
                    #print(company_number_list)
                    if len(company_number_list) >= 2:
                        for company_number in company_number_list:
                            use_list = flowd_information.copy()
                            #print('old_use_list:',use_list)
                            use_list[2] = company_number
                            #print('new_use_list:',use_list)
                            flowd_text_list_all.append(use_list)
                            data_dic['label'].append(company_number)
                    else:
                        flowd_text_list_all.append(flowd_information)
                        data_dic['label'].append(company_number_list[0])
                
    for flowd_list in flowd_text_list_all:
        data_dic[flowd_list[2]] = {'terminal':flowd_list[3],
                                    'counter':flowd_list[5],
                                    'type':flowd_list[-1]
                                                            }
    #chrome_driver.close()
    return data_dic
        
def run_get():
    driver = webdriver.Chrome(chrome_options = chromeoptions)
    driver.get("https://www.taoyuan-airport.com/flight_depart?k=&time=all")
    Web_Driver_Wait(driver,'board')

    local_time = time.localtime()
    if local_time.tm_hour >= 18:
        change_time(driver)

    input_Keyword_search(driver,'香港')
    time.sleep(2)
    get_data(driver)

    
