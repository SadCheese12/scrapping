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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

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
    
    def get_data(self, url):
        
            driver = self.driver
            driver.get(url)     
                
            divs = driver.find_elements(By.CLASS_NAME, 'serp-snippet')
                
            print("Numero de publicaciones en la pagina: ", len(divs))
                
            listaDiccionario = []
            for i in range(len(divs)):
                
                try:
                    print(i+1, " iteracion")
                    
                    wait =  WebDriverWait(self.driver, 30)
                    aviso_legal = wait.until(EC.visibility_of_element_located((By.ID, 'avisoLegalCookies')))
                    
                    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", aviso_legal)
                    
                    divs_2 = driver.find_elements(By.CLASS_NAME, 'serp-snippet')
                        
                    div_container = divs_2[i]
                    
                    div_container.click()
                        
                    wait =  WebDriverWait(self.driver, 10)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                            
                    new_url = driver.current_url
                    print("Nueva URL: ",new_url)
                    slick_track = driver.find_elements(by=By.CLASS_NAME, value="slick-track")
                    titulo = driver.find_element(By.TAG_NAME, 'h1').text
                    print("Titulo: ",titulo)
                            
                    data_slick_index_elements = slick_track[0].find_elements(by=By.CSS_SELECTOR, value="[data-slick-index]")
                        
                            
                    for j in range(len(data_slick_index_elements)):
                        try:
                            element = data_slick_index_elements[j]
                            a_elemnt = element.find_element(by=By.TAG_NAME, value="a")
                            href = a_elemnt.get_attribute("href")
                            print("URL: ", href)
                            dic = {
                                "url": new_url,
                                "img": href,
                                "descripcion": titulo
                            }
                            listaDiccionario.append(dic)
                        except NoSuchElementException:
                            print("Imagen no encontrada, pasando al siguiente elemento")
                            if j + 1 < len(data_slick_index_elements):
                                element = data_slick_index_elements[j + 1]
                                a_elemnt = element.find_element(by=By.TAG_NAME, value="a")
                                href = a_elemnt.get_attribute("href")
                                print("URL: ",href)
                                dic = {
                                    "url": new_url,
                                    "img": href,
                                    "descripcion": titulo
                                }
                                listaDiccionario.append(dic)
                        
                    driver.back()
                    
                except StaleElementReferenceException:
                    print("Error...")
                    #divs = driver.find_elements(By.CLASS_NAME, 'serp-snippet')
                    
                    
            #self.get_data_from_page(driver,url_from_db)
            print("Numero de elementos recopilados: ", len(listaDiccionario))
            driver.close()
            return listaDiccionario
        
       

    def get_data_recursivo(self,driver,url_from_db):
        print("obtaining data from " + driver.current_url)
        
            

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
        