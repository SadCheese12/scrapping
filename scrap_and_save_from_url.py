from scraper.scraper_selenium_idealista import ScraperSeleniumIdealista
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa
#from scraper.scraper_selenium import ScraperOwn

from mongodb_dao.mongodb_data_recorder import MongoDBDataRecorder
from mongodb_dao.mongodb_config_grabber import MongoConfigGrabber
from mongodb_dao.mongodb_summary_recorder import MongoDBSummaryRecorder

class ScrapAndSaveFromURL():
    def main(self):
        #urls=['https://www.idealista.com/venta-viviendas/galapagar-madrid/con-precio-hasta_300000,chalets,casas-de-pueblo/']
        #urls=['http://127.0.0.1:5500/index.html']
        '''urls = ['https://www.icasas.ec/venta/departamentos/quito']
        scraper_idealista = ScraperSeleniumIdealista(urls)
        scraper_idealista.get_data()
        
        data_idealista = scraper_idealista.data
        summary_dictionary_idealista = scraper_idealista.summaries
        
        print(data_idealista)
        print(summary_dictionary_idealista)'''
        
        urlsRemax = ["https://www.remax.com.ec/listings/buy?page=0&pageSize=21&sort=-createdAt&in:operationId=1&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E#%20Pichincha::::&filterCount=0&viewMode=list"]
        scraper_remax = ScraperSeleniumFotocasa(urlsRemax)
        scraper_remax.get_data()




        # mongodb_data_recorder = MongoDBDataRecorder(data_idealista)
        # mongodb_data_recorder.post_data()

        # mongodb_summary_recorder_idealista = MongoDBSummaryRecorder(summary_dictionary_idealista)
        # mongodb_summary_recorder_idealista.post_data()

if __name__ == '__main__':
    ScrapAndSaveFromURL().main()
