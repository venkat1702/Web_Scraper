import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import json 

search=input("what do you want to search: ")# i had searched for mobiles
class Scraper():

    def __init__(self):
        self.url = 'https://www.flipkart.com'
        self.driver = webdriver.Firefox()

    def page_load(self):

        self.driver.get(self.url)
        try:
            login_pop = self.driver.find_element_by_class_name('_29YdH8')
            # Here .click function use to tap on desire elements of webpage
            login_pop.click()
            print('pop-up closed')
        except:
            pass
        search_field = self.driver.find_element_by_class_name('LM6RPg')
        # Here .send_keys is use to input text in search field
        search_field.send_keys(search)
        search_field.submit()
        time.sleep(2)
        # Here we fetched driver page source from driver.
        page_html = self.driver.page_source
        # Here BeautifulSoup is dump page source into html format
        self.soup = BeautifulSoup(page_html, 'html.parser')

    def create_csv_file(self):

        # Here I created CSV file with desired header.
        rowHeaders = ["Name","Price in Rupees","Ratings"]
        self.file_csv = open('output.csv', 'w', newline='', encoding='utf-8')
        self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
        # Writeheader is pre-defined function to write header
        self.mycsv.writeheader()

    def data_scrap(self):

        first_page_mobiles = (self.soup.find_all('div', class_='_1UoZlX'))
        for i in first_page_mobiles:
            Name = i.find('img', class_='_1Nyybr')['alt']
            price = i.find('div', class_='_1vC4OE _2rQ-NK')
            price = price.text[1:]
            rating=i.find('div',class_='hGSR34')
            Rating=rating.text[:]
            self.mycsv.writerow({"Name": Name,"Price in Rupees": price,"Ratings":Rating})

    def tearDown(self):
        # Here we also need to close Csv file which I generated above
        self.file_csv.close()
    def make_json(self,csvFilePath, jsonFilePath): 
        data = {} 
        with open(csvFilePath, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf) 
            for rows in csvReader: 
                key = rows['Name'] 
                data[key] = rows
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
            jsonf.write(json.dumps(data, indent=4)) 
    
if __name__ == "__main__":
    csvFilePath = r'output.csv'
    jsonFilePath = r'output.json'
    Scraper = Scraper()
    Scraper.page_load()
    Scraper.create_csv_file()
    Scraper.data_scrap()
    Scraper.tearDown()
    Scraper.make_json(csvFilePath, jsonFilePath)
    print("Hurray! csv and json file are created!!!")
