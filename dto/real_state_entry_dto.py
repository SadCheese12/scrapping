from datetime import datetime
import hashlib

class RealStateEntryDTO:

    def __init__(self, title,prize,meters,rooms,url_scrapped,url_element,url_first_page):
        self.rooms = rooms
        self.title = title
        self.prize = prize
        self.meters = meters
        self.url_scraped=url_scrapped
        self.url_element=url_element
        self.url_first_page=url_first_page
        self.date = str(datetime.now())

        self.construct_id_and_clean()

    def construct_id_and_clean(self):
        hashed_url = self.get_hash_from_url_first()
        if(self.title=="" or self.title==None):
            self._id = hashed_url + "---"+ self.meters+"---" + self.rooms+"---"+self.prize
            self.title = hashed_url
        else:
            self._id = hashed_url + "---" + self.title + "---" + self.meters+"---" + self.rooms+"---"+self.prize

    def get_hash_from_url_first(self):
        hash_object = hashlib.sha1(self.url_first_page.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def __str__(self):
        return (
            f"Title: {self.title},"
            f"Price: {self.prize},"
            f"Meters: {self.meters},"
            f"Rooms: {self.rooms},"
            f"URL Scrapped: {self.url_scraped},"
            f"URL Element: {self.url_element},"
            f"URL First Page: {self.url_first_page},"
            f"Date: {self.date},"
            f"ID: {self._id},"
        )
    