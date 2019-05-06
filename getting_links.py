
"""We start be creating a Config.txt file where we set the last month we retrieved
The file will be updated during the code running."""


import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import ast

"""getting the links to the law from the table on site"""
def get_links(links):
    the_real_links = []
    cells = links.find_elements_by_xpath('//*[@id="ctl00_B_Center_VoturiPlen1_GridVoturi"]/tbody/tr/td[3]/a')
    for cell in cells:
        if cell.get_attribute('innerHTML').startswith('L'):
            the_real_links.append(cell.get_attribute('href'))
    return the_real_links

"""saving the links in files named under the yeara and the month"""
def save_links(links): # monthly
    with open("legi{}{}.csv".format(current_month['anul'], current_month['luna']), mode = 'w', encoding="utf-8") as f:
        f.write("\n".join(links))
        

def next_month(current_month = None):
    if current_month['luna'] == 12:
        current_month['luna'] = 1
        current_month['anul'] += 1
    else: 
        current_month['luna'] += 1
    return current_month

def update_config(current_month):
    with open("config.txt", mode = 'w', encoding="utf-8") as f:
       f.write(str(current_month))

"""the structure to work with is a calendar with the general assembly days colored in cyan """
def get_month (curent):
    laws = []
    driver.get(url)
    time.sleep(10)

    year = Select(driver.find_element_by_id("ctl00_B_Center_VoturiPlen1_drpYearCal"))
    year.select_by_value(str(curent['anul']))
    time.sleep(5)
    month = Select(driver.find_element_by_id("ctl00_B_Center_VoturiPlen1_drpMonthCal"))
    month.select_by_value(str(curent['luna']))
    time.sleep(5)

    days = driver.find_elements_by_xpath('//td[@style="background-color:Cyan;width:14%;"]/a')
    cate_zile = len(days) + 1
    print('zile: ', cate_zile)

    for ziua_curenta in range(cate_zile):
        driver.get(url)
        year = Select(driver.find_element_by_id("ctl00_B_Center_VoturiPlen1_drpYearCal"))
        year.select_by_value(str(curent['anul']))
        time.sleep(5)
        month = Select(driver.find_element_by_id("ctl00_B_Center_VoturiPlen1_drpMonthCal"))
        month.select_by_value(str(curent['luna']))
        time.sleep(5)

        days = driver.find_elements_by_xpath('//td[@style="color:White;background-color:#666666;font-weight:bold;width:14%;"]/a')+driver.find_elements_by_xpath('//td[@style="background-color:Cyan;width:14%;"]/a')
        time.sleep(5)

        print(days[ziua_curenta].get_attribute('innerHTML'))
        days[ziua_curenta].click()
        time.sleep(10)
        print(driver.find_element_by_id("ctl00_B_Center_VoturiPlen1_lblDate").get_attribute('innerHTML'))
        laws = laws+get_links(driver)

        try:
            pagini = driver.find_element_by_xpath('//*[@id="ctl00_B_Center_VoturiPlen1_GridVoturi"]/tbody/tr[12]/td')
            if pagini.is_displayed:
                pag_urmatoare = pagini.find_elements_by_tag_name('a')
                numar_pag = len(pag_urmatoare)
                pagina_curenta = 1
                print(pag_urmatoare)
                for pagina in range(numar_pag):
                    pagini = driver.find_element_by_xpath('//*[@id="ctl00_B_Center_VoturiPlen1_GridVoturi"]/tbody/tr[12]/td')
                    pag_urmatoare = pagini.find_elements_by_tag_name('a')
                    pag_urmatoare[pagina_curenta-1].click()
                    time.sleep(25)
                    laws = laws+get_links(driver)
                    pagina_curenta += 1
        except:
            pass
    return laws


with open('config.txt', mode ='r', encoding="utf-8") as f:
    processsed_month = ast.literal_eval(f.read())
current_month = next_month(processsed_month)

url = 'https://www.senat.ro/Voturiplen.aspx'
driver = webdriver.Chrome('C:/Users/User/Anaconda3/Scripts/chromedriver_win32/chromedriver.exe')

while not (datetime.datetime.today().year == current_month['anul'] and datetime.datetime.today().month == current_month['luna']):
    current_month_links = get_month(current_month)
    save_links(current_month_links)
    update_config(current_month)
    current_month = next_month(current_month)

