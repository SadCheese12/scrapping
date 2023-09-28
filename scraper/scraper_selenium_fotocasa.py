from selenium import webdriver
import sys

from utils_app.util_summary_builder import UtilsSummaryBuilder
from dto.real_state_entry_dto import RealStateEntryDTO 
from dto.summary_scrapped_dto import SummaryScrappedDTO
import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
#https://www.seleniumhq.org/download/
#14393
#https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

class ScraperSeleniumFotocasa:

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
            #driver.set_window_position(-4000,0)
            return self.get_data_from_page(driver,url_from_db) 
        driver.close()
       
    def get_data_from_page(self, driver, url_from_db):
        print("Obteniendo datos desde: " + driver.current_url)
        search_results = self.driver.find_elements(by=By.CLASS_NAME, value="info-wrapper")
        print("Número de resultados en la página: ", len(search_results))
        listaDiccionario = []
        for i in range(len(search_results)):#len(search_results)):
            div_element = search_results[i]
            div_element.click()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(4)
            new_page_url = driver.current_url
            titulo = self.driver.find_element(by=By.ID, value="title-container")
            elemento_h3 = titulo.find_element(By.TAG_NAME, value = "h3")
            tituloPropiedad = elemento_h3.get_attribute("textContent")            
            print("La nueva URL es: ", new_page_url)
            while True:
                try:
                    flechaLateral = self.driver.find_element(by=By.CLASS_NAME, value="next")
                    if "swiper-button-disabled" in flechaLateral.get_attribute("class"):
                        break
                    else:
                        flechaLateral.click()
                        time.sleep(1)
                except NoSuchElementException:
                    break
            time.sleep(2)
            try: 
                contenedorImagenes = self.driver.find_element(by=By.CLASS_NAME, value="swiper-wrapper")
                images = contenedorImagenes.find_elements(By.TAG_NAME, "img")
                unique_links = set()
                for image in images:
                    image_source = image.get_attribute("src")
                    if image_source:
                        unique_links.add(image_source)
            except: 
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue 
            unique_links_list = list(unique_links)
            for element in unique_links_list: 
                dicImg = {
                        "url": new_page_url,  
                        "img": element, 
                        "descripcion": tituloPropiedad,  
                    }
                listaDiccionario.append(dicImg)
            
            print("Se encontraron: ", len(unique_links_list), " imágenes")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        print("Número de elementos recopilados", len(listaDiccionario))
        print("El typo del objeto listaDiccionario es: ", type(listaDiccionario))
        return listaDiccionario

    def is_next_page(self):
        try:
            controls=self.driver.find_element_by_xpath("//*[text()='>']")
        except:
            return False
        return not controls==None

    def parse_search_result_item_and_update_data(self,info_container_array,url_from_db):
            if(self.data==None): self.data = {}
            if(not url_from_db in self.data.keys()): self.data[url_from_db]=[]

            for home in info_container_array:
                title=home.find_element_by_class_name('re-Card-title').text.strip()
                url_element=home.find_element_by_tag_name('a').get_attribute("href").strip()
                prize=home.find_elements_by_class_name('re-Card-price')[0].text.replace("<span>","").replace("</span>","").replace(" €","").replace("\u20ac","").strip()
                features = home.find_elements_by_class_name('re-Card-feature')
                if(not features == []):
                    rooms=features[0].text.replace(" habs.","").strip()
                else: rooms=""
                
                if(len(features)>1):
                    meters=features[1].text.replace(" m²","").strip()
                else:
                    meters=""
                print(title + ".." + meters + ".." + rooms + "--" + prize)
                dto=RealStateEntryDTO(title,prize,meters,rooms,self.driver.current_url,url_element,url_from_db)
                self.data[url_from_db]=self.data[url_from_db] + [dto]


    def get_summary(self,driver,url_from_db):
        util_summary_builder=UtilsSummaryBuilder(self.data[url_from_db],url_from_db,"")
        util_summary_builder.obtain_summary()
        summary = util_summary_builder.summary
        self.summaries[url_from_db] = summary