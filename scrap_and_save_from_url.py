from scraper.scraper_selenium_idealista import ScraperSeleniumIdealista
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ScrapAndSaveFromURL():
    def main(self):
        #Conexion a la base de datos y a la colección
        uri = 'mongodb+srv://monterosuniga:monterosunigadb@cluster0.6sh1gzt.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'
        
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client.BaseScrapping
        collection = db.Imagenes

        
        #Scrapping de Remax
    #       'https://www.remax.com.ec/listings/buy?page=0&pageSize=12&sort=-createdAt&in:operationId=1&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=0&viewMode=list',
    #'https://www.remax.com.ec/listings/buy?page=1&pageSize=12&sort=-createdAt&in:operationId=1&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=0&viewMode=list',
        urlsRemaxs = [
'https://www.remax.com.ec/listings/buy?page=15&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=16&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=17&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=18&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=19&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=20&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=21&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=22&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=23&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list',
'https://www.remax.com.ec/listings/buy?page=24&pageSize=12&sort=-createdAt&in:operationId=1&in:typeId=2,1,5,6,11,14,17&locations=in:::1701@%3Cb%3EQuito%3C%2Fb%3E::::&filterCount=1&viewMode=list'
        ]
       
        for url in urlsRemaxs:
            scraper_remax = ScraperSeleniumFotocasa([url])
            listaScrapping = scraper_remax.get_data()
            for elem in listaScrapping: 
                collection.insert_one(elem)
        client.close() 
        

        #urls=['https://www.idealista.com/venta-viviendas/galapagar-madrid/con-precio-hasta_300000,chalets,casas-de-pueblo/']
        #urls=['http://127.0.0.1:5500/index.html']
        '''urls = ['https://www.icasas.ec/venta/departamentos/quito']
        scraper_idealista = ScraperSeleniumIdealista(urls)
        scraper_idealista.get_data()
        
        data_idealista = scraper_idealista.data
        summary_dictionary_idealista = scraper_idealista.summaries
        
        print(data_idealista)
        print(summary_dictionary_idealista)'''
        





        # mongodb_data_recorder = MongoDBDataRecorder(data_idealista)
        # mongodb_data_recorder.post_data()

        # mongodb_summary_recorder_idealista = MongoDBSummaryRecorder(summary_dictionary_idealista)
        # mongodb_summary_recorder_idealista.post_data()

if __name__ == '__main__':
    ScrapAndSaveFromURL().main()
