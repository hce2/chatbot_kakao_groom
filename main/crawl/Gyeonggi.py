from selenium import webdriver
import chromedriver_autoinstaller
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = options)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = options)

driver.implicitly_wait(300)


#경로
url = 'C:\\chatbot\\'
myURL = 'https://www.myhome.go.kr/hws/portal/mtx/selectFixesSportView.do?tySe=FIXES100'
driver.get(myURL)


driver.find_element_by_xpath('//*[@id="MENU000003"]/img').click()
driver.find_element_by_xpath('//*[@id="srchPrgrStts_1"]/span').click()
driver.find_element_by_xpath('//*[@id="schMapDiv"]/div[1]/div[1]/div[2]/span[2]/a/img').click()
driver.find_element_by_xpath('//*[@id="frm"]/div[3]/span[1]').click()
time.sleep(10)

gyeonggi_title_list = []
gyeonggi_status_list = []
gyeonggi_area_list = []
gyeonggi_name_list = []
gyeonggi_re_date_list = []
gyeonggi_pre_date_list = []
gyeonggi_corporation_list = []

for i in range(10):
        title = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[1]'.format(num=i+1)).text
        status = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[2]/span'.format(num=i+1)).text
        area = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[3]'.format(num=i+1)).text
        name1 = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[4]/a'.format(num=i+1)).text
        re_date = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[6]'.format(num=i+1)).text
        pre_date = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[7]'.format(num=i+1)).text
        corporation = driver.find_element_by_xpath('//*[@id="schTbody"]/tr[{num}]/td[8]/a'.format(num=i+1)).text

        gyeonggi_title_list.append(title)
        gyeonggi_status_list.append(status)
        gyeonggi_area_list.append(area)
        gyeonggi_name_list.append(name1)
        gyeonggi_re_date_list.append(re_date)
        gyeonggi_pre_date_list.append(pre_date)
        gyeonggi_corporation_list.append(corporation)
        print(i)
    
for i in range(len(gyeonggi_area_list)):
    gyeonggi_area_list[i] = gyeonggi_area_list[i].replace('\n', '')

df = pd.DataFrame((zip(gyeonggi_title_list, gyeonggi_status_list, gyeonggi_area_list, gyeonggi_name_list, gyeonggi_re_date_list, gyeonggi_pre_date_list, gyeonggi_corporation_list)),    
                   columns = ['title', 'status', 'area', 'name', 're_date', 'pre_date', 'corporation'])


df.to_csv('./region_data/Gyeonggi_notice.csv', index = False, encoding='utf-8')


myhome_titles = driver.find_elements_by_css_selector(".al > a")
a = []
b = 0

detail_url = 'https://m.myhome.go.kr/hws/mbl/sch/selectRsdtLttotListView.do#detailPage?pblancId='

for i in myhome_titles:
    href = i.get_attribute('href')
    num1 = href[27:32]
    num = str(detail_url) + str(num1) + chr(38) + 'searchSe=R'
    a.append(num)
    b += 1


df = pd.DataFrame((a), columns = ['url'])

df.to_csv('./region_data/Gyeonggi_url.csv', index = False, encoding='utf-8')

print("9. 경기 완료")