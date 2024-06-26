from scraper.scraper_selenium_idealista import ScraperSeleniumIdealista
from scraper.scraper_selenium_fotocasa import ScraperSeleniumFotocasa


from mongodb_dao.mongodb_data_recorder import MongoDBDataRecorder
from mongodb_dao.mongodb_config_grabber import MongoConfigGrabber
from mongodb_dao.mongodb_summary_recorder import MongoDBSummaryRecorder
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

class ScrapAndSaveFromURL():
    def main(self):
        #urls=['https://www.idealista.com/venta-viviendas/galapagar-madrid/con-precio-hasta_300000,chalets,casas-de-pueblo/']
        #urls=['http://127.0.0.1:5500/index.html']
        #Conexion con la base de datos
        uri = "mongodb+srv://monterosuniga:monterosunigadb@cluster0.6sh1gzt.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client.BaseScrapping
        collection1 = db.Imagenes
        collection2 = db.ImgLimpias
        urls = [#'https://www.icasas.ec/venta/departamentos/quito',
                #'https://www.icasas.ec/venta/departamentos/quito/p_2']
                #'https://www.icasas.ec/venta/departamentos/quito/p_3']
                #'https://www.icasas.ec/venta/departamentos/quito/p_4']
                #'https://www.icasas.ec/venta/departamentos/quito/p_5']
                'https://www.icasas.ec/venta/departamentos/quito/p_10']
        '''scraper_idealista = ScraperSeleniumIdealista(urls)
        
        listaScrapping = scraper_idealista.get_data(urls[0])
        to_json = json.dumps(listaScrapping, indent=4)
        with open("datos9.json", "w") as arch:
            arch.write(to_json)'''
        
        nombres_archivos = ['datos0.json','datos1.json','datos2.json','datos3.json','datos4.json',
                    'datos5.json','datos6.json','datos7.json','datos8.json','datos9.json',]
        
        '''for archivo in archivos:
            cantidad_dicc = 0
            with open(archivo, 'r') as a:
                data = json.load(a)
                if isinstance(data, list):
                    cantidad_dicc = len(data)
                else:
                    cantidad_dicc = 0
            print(f'El archivo {archivo} contiene {cantidad_dicc} elementos')'''

        for nombre_archivo in nombres_archivos:
            with open(nombre_archivo, 'r') as archivo:
                data = json.load(archivo)
                print(f'Insertando {nombre_archivo} en la base de datos...')
                collection2.insert_many(data)
        
        client.close()
        
        #data_idealista = scraper_idealista.data
        #summary_dictionary_idealista = scraper_idealista.summaries
        
        #print(data_idealista)
        #print(summary_dictionary_idealista)
        

        # mongodb_data_recorder = MongoDBDataRecorder(data_idealista)
        # mongodb_data_recorder.post_data()

        # mongodb_summary_recorder_idealista = MongoDBSummaryRecorder(summary_dictionary_idealista)
        # mongodb_summary_recorder_idealista.post_data()

if __name__ == '__main__':
    ScrapAndSaveFromURL().main()
