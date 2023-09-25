from selenium import webdriver
import selenium
import sys

from utils_app.util_summary_builder import UtilsSummaryBuilder
from dto.real_state_entry_dto import RealStateEntryDTO
from dto.summary_scrapped_dto import SummaryScrappedDTO

import time 
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#https://www.seleniumhq.org/download/
#14393
#https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

class ScraperSeleniumIdealista:

    def __init__(self, urls):
        self.urls = urls
        #self.driver = webdriver.Edge()
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        self.data ={}
        self.summaries = {}
    
    def get_data(self):
        for url_from_db in self.urls:
            driver = self.driver
            driver.get(url_from_db) 
            
            ul_element = self.driver.find_element(by=By.CLASS_NAME, value="listAds")
            li_elements = ul_element.find_elements(by=By.TAG_NAME, value="li")
            cantidad_de_li = len(li_elements)
            
            
            if cantidad_de_li != 0:
                
                for li in li_elements:
                    
                    wait = WebDriverWait(self.driver, 10)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    
                    print("UL: ",ul_element)
                    print("LI: ",li)

                    li.click()
                    
                    wait = WebDriverWait(self.driver, 10)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    
                    new_url = self.driver.current_url
                    print(new_url)
                    slick_track = self.driver.find_elements(by=By.CLASS_NAME, value="slick-track")
                    print(len(slick_track))
                    
                    data_slick_index_elements = slick_track[0].find_elements(by=By.CSS_SELECTOR, value="[data-slick-index]")
                    
                    cant = len(data_slick_index_elements)
                    print(cant)
                    
                    for element in data_slick_index_elements:
                        a_elemnt = element.find_element(by=By.TAG_NAME, value="a")
                        href = a_elemnt.get_attribute("href")
                        print(href)
                        
                    self.driver.back()
                    
                    
            else:
                print("Hubo un error")
                
            #self.get_data_from_page(driver,url_from_db) 
        driver.close()
       

    def get_data_from_page(self,driver,url_from_db):
        print("obtaining data from " + driver.current_url)
        item_info_container = self.driver.find_elements(by=By.CLASS_NAME, value="serp-snippet ad premier")
        time.sleep(5)
        print(len(item_info_container))
            
        random_int =8573 + random.randint(-3, 3)
        driver.execute_script("window.scrollTo(0, "+str(random_int) +");")
        time.sleep(random.uniform(0.5,0.9))
        self.parse_info_container_and_update_data(item_info_container,url_from_db)

        print("obtained " + str(len(self.data[url_from_db])) + " entries")


        time.sleep(random.uniform(0.5,1))
        if (self.is_next_page()):
            url=self.driver.find_elements(by=By.CLASS_NAME, value="icon-arrow-right-after")[0].get_attribute("href")
            self.driver.get(url)
            self.get_data_from_page(driver,url_from_db)
        else: 
            self.get_summary(driver,url_from_db)
            

    def is_next_page(self):
        next_button=self.driver.find_elements(by=By.CLASS_NAME, value="icon-arrow-right-after")
        return not next_button == []

    def parse_info_container_and_update_data(self,info_container_array,url_from_db):
            if(self.data==None): self.data = {}
            if(not url_from_db in self.data.keys()): self.data[url_from_db]=[]

            for home in info_container_array:
                title=home.find_element(by=By.CLASS_NAME, value="title").text
                print(title)
                price = home.find_element(by=By.CLASS_NAME, value = "price").text
                print(price)
                #url_element=self.driver.find_element(by=By.TAG_NAME, value='a').get_attribute("href")
                #prize=home.find_elements(by=By.CLASS_NAME, value='item-price')[0].text.replace(" €","").replace("\u20ac","")
                #rooms=home.find_elements(by=By.CLASS_NAME, value='item-detail')[0].text.replace(" hab.","")
                #meters=home.find_elements(by=By.CLASS_NAME,value='item-detail')[1].text.replace(" m²","")
                dto=RealStateEntryDTO(title,price,"","",self.driver.current_url,"",url_from_db)
                self.data[url_from_db]=self.data[url_from_db] + [dto]

    def get_summary(self,driver,url_from_db):
        #average_prize=self.driver.find_elements(by=By.CLASS_NAME, value="items-average-price")[0].text.replace("Precio medio","").replace("eur/m²","").strip()
        #print(len(average_prize))
        util_summary_builder=UtilsSummaryBuilder(self.data[url_from_db],url_from_db,"")
        util_summary_builder.obtain_summary()
        summary = util_summary_builder.summary
        self.summaries[url_from_db] = summary
        