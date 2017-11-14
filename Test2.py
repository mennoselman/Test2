from bs4 import BeautifulSoup 
import urllib2
import selenium
import signal
from contextlib import closing
#from selenium.webdriver import Firefox # pip install selenium
#from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from IPython import get_ipython
import platform
import time
import os
import requests
import sys


def init_phantomjs_driver(*args, **kwargs):

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    driver =  webdriver.PhantomJS(*args, **kwargs)
    # driver.set_window_size(1400, 1000)

    return driver

class Crawler():
    def __init__(self):

        self.driver = init_phantomjs_driver(executable_path='driver/phantomjs')

        self.driver.implicitly_wait(10)  # seconds
        self.driver.set_page_load_timeout(30)

        self.starting()

    def subproducts(self, page_source, url):
        soup = BeautifulSoup(page_source)
        int_href_tags = soup.find_all(href=True)
        int_hrefs = []
        for t in int_href_tags:
            #if "producten/verse-kant-en-klaar-maaltijden-salades/" in str(t):
            if url + "/" in str(t):
                if "bonus" not in t.get("href"):
                    if "=" not in t.get("href"):
                        if t.get("href") not in int_hrefs:
                            int_hrefs.append(t.get("href"))
        return int_hrefs

    def get_category(self, var, set1, set2):
        su = 0
        count_i = -1
        while count_i < len(set1)-1 and su < var:
            count_j = -1
            count_i = count_i + 1
            while count_j < len(set2[count_i][:])-1 and su < var:
                count_j = count_j+1
                su = su + 1
                
        return set2[count_i][count_j]
    
    def subproducts2(self, page_source, url):
        soup = BeautifulSoup(page_source)
        int_href_tags = soup.find_all(href=True)
        int_hrefs = []
        for t in int_href_tags:
            #if "producten/verse-kant-en-klaar-maaltijden-salades/" in str(t):
            if "product/wi" in str(t):
                if "bonus" not in t.get("href"):
                    if "=" not in t.get("href"):
                        if t.get("href") not in int_hrefs:
                            int_hrefs.append(t.get("href"))
        return int_hrefs


    def starting(self):
        self.driver.get("https://www.ah.nl/producten")
        #wait = WebDriverWait(self.driver, 200)
        WebDriverWait(self.driver, timeout=30).until(
         lambda x: x.find_element_by_xpath("//div[@class='lane row product-category-navigation-lane  product-category-navigation-lane--ah']"))
        page_source = self.driver.page_source
        print(page_source)
        soup = BeautifulSoup(page_source)
        new_soup = (soup.find_all("a", class_="column grid-item category-link heading--9 link--2 link-color--dark small-12 medium-4 large-3 xlarge-2 xxlarge-2 color-white__bg--1"))
        hrefs1 = []
        for t in new_soup:
            if "producten" in str(t):
                hrefs1.append(t.get("href"))
        hrefs1
        results_subproducts = []
        count = -1
        while count < len(hrefs1)-1:
            # use firefox to get page with javascript generated content
            count = count + 1
            #with closing(Firefox()) as browser:
            url2 = "https://www.ah.nl" + hrefs1[count]
            self.driver.get(url2)
            time.sleep(30)
            # wait for the page to load
            WebDriverWait(self.driver, timeout=100).until(
                    lambda x: x.find_element_by_id('Filters'))
            # store it to string variable
            page_source = self.driver.page_source
            subs = self.subproducts(page_source, hrefs1[count])  
            results_subproducts.append(subs)
        count
        results_subproducts
        url3 = "https://www.ah.nl" + results_subproducts[0][6]
        print(url3)
        self.driver.get(url3)
        # wait for the page to load
        #WebDriverWait(browser, timeout=200).until(
        #    lambda x: x.find_element_by_class_name('lane row product-lane lane--gutter'))
        WebDriverWait(self.driver, timeout=200).until(
                lambda x: x.find_element_by_id('Filters'))
        #lambda x: x.find_element_by_xpath("//div[@class='lane row product-lane lane--gutter' or @class = 'lane row see-more-lane or @class = 'lane row product-lane']"))
        # store it to string variable
        page_source = self.driver.page_source
        results_subproducts_low = []
        count_i = -1
        count_j = -1
        while count_i < len(hrefs1)-1:
            count_i = count_i + 1
            count_j = -1
            while count_j < len(results_subproducts[count_i])-1:
                count_j = count_j + 1
                #with closing(Firefox()) as browser:
                url3 = "https://www.ah.nl" + results_subproducts[count_i][count_j]
                self.driver.get(url3)
                time.sleep(30)
                # wait for the page to load
                WebDriverWait(self.driver, timeout=100).until(
                        #lambda x: x.find_element_by_id('Filters'))
                        lambda x: x.find_element_by_xpath("//div[@class='canvas-page']"))
                #lambda x: x.find_element_by_xpath("//div[@class='lane row product-lane lane--gutter' or @class = 'lane row see-more-lane or @class = 'lane row product-lane']"))
                # store it to string variable
                page_source = self.driver.page_source
                subs = self.subproducts(page_source, results_subproducts[count_i][count_j])  
                results_subproducts_low.append(subs)
        results_subproducts_low
        test = results_subproducts_low
        url4 = "https://www.ah.nl" + results_subproducts_low[6][6]
        print(url4)
        print(self.get_category(260))
        results_subproducts_low_f = []
        count_i = -1
        count_j = -1
        while count_i < len(results_subproducts_low[:][:])-1:
            count_i = count_i + 1
            if len(results_subproducts_low[count_i][:]) == 0:
                if self.get_category(count_i+1, hrefs1,results_subproducts) not in results_subproducts_low_f:
                    results_subproducts_low_f.append(self.get_category(count_i+1, hrefs1,results_subproducts))
                    print(results_subproducts_low_f)
        results_subproducts_total = []
        count_i = -1
        count_j = -1
        while count_i < len(results_subproducts_low[:][:])-1:
            count_i = count_i + 1
            count_j = -1
            while count_j < len(results_subproducts_low[count_i][:])-1:
                count_j = count_j + 1
                results_subproducts_total.append(results_subproducts_low[count_i][count_j])
                
                count_i = -1
                while count_i < len(results_subproducts_low_f[:])-1:
                    count_i = count_i + 1
                    results_subproducts_total.append(results_subproducts_low_f[count_i])
                    
                    len(results_subproducts_total)
        url4 = "https://www.ah.nl" + results_subproducts_total[6]
        print(url4)
        Individual_products = []
        count_j = -1
        while count_j < len(results_subproducts_total[:])-1:
            count_j = count_j + 1
            #with closing(Firefox()) as browser:
            url4 = "https://www.ah.nl" + results_subproducts_total[count_j]
            self.driver.get(url4)
            time.sleep(5)
            # wait for the page to load
            #WebDriverWait(browser, timeout=100).until(
            #   lambda x: x.find_element_by_xpath("//a[@class=' row collapse product__content product__content--link']")) 
            # store it to string variable
            page_source = self.driver.page_source
            subs = self.subproducts(page_source, results_subproducts_total[count_j])  
            Individual_products.append(subs)
        results_subproducts_total
        Individual_products
        results_subproducts_low_i = []
        count_i = -1
        count_j = -1
        while count_i < len(Individual_products[:][:])-1:
            count_i = count_i + 1
            if len(Individual_products[count_i][:]) == 0:
                results_subproducts_low_i.append(results_subproducts_total[count_i])
                print(results_subproducts_low_i)
        results_individual_total = []
        count_i = -1
        count_j = -1
        while count_i < len(Individual_products[:][:])-1:
            count_i = count_i + 1
            count_j = -1
            while count_j < len(Individual_products[count_i][:])-1:
                count_j = count_j + 1
                results_individual_total.append(Individual_products[count_i][count_j])
                
                count_i = -1
                while count_i < len(results_subproducts_low_i[:])-1:
                    count_i = count_i + 1
                    results_individual_total.append(results_subproducts_low_i[count_i])
                    
                    len(results_individual_total)
        results_individual_total
        products = []
        count_j = -1
        while count_j < len(results_individual_total[:])-1:
            count_j = count_j + 1
            #with closing(Firefox()) as browser:
            url5 = "https://www.ah.nl" + results_individual_total[count_j]
            self.driver.get(url5)
            time.sleep(5)
            # wait for the page to load
            #WebDriverWait(browser, timeout=100).until(
            #   lambda x: x.find_element_by_xpath("//a[@class=' row collapse product__content product__content--link']")) 
            # store it to string variable
            page_source = self.driver.page_source
            subs = self.subproducts(page_source, results_individual_total[count_j])  
            products.append(subs)
        products
        results_subproducts_low_u = []
        count_i = -1
        count_j = -1
        while count_i < len(products[:][:])-1:
            count_i = count_i + 1
            if len(products[count_i][:]) == 0:
                results_subproducts_low_u.append(results_individual_total[count_i])
                print(results_subproducts_low_u)
        results_individual_total_2 = []
        count_i = -1
        count_j = -1
        while count_i < len(products[:][:])-1:
            count_i = count_i + 1
            count_j = -1
            while count_j < len(products[count_i][:])-1:
                count_j = count_j + 1
                results_individual_total_2.append(products[count_i][count_j])
                
                count_i = -1
                while count_i < len(results_subproducts_low_u[:])-1:
                    count_i = count_i + 1
                    results_individual_total_2.append(results_subproducts_low_u[count_i])
                    
                    len(results_individual_total_2)
        products_final = []
        count_j = -1
        while count_j < len(results_individual_total_2[:])-1:
            count_j = count_j + 1
            #with closing(Firefox()) as browser:
            url6 = "https://www.ah.nl" + results_individual_total_2[count_j]
            self.driver.get(url6)
            time.sleep(5)
            # wait for the page to load
            #WebDriverWait(browser, timeout=100).until(
            #   lambda x: x.find_element_by_xpath("//div[@class='lane row product-lane']")) 
            # store it to string variable
            page_source = self.driver.page_source
            subs = self.subproducts2(page_source, results_individual_total_2[count_j])  
            products_final.append(subs)
        products_final
        len(products_final[:][:])
        thefile = open('test.txt', 'w')
        for item in products_final: #result?
            thefile.write("%s\n" % item)
        results = []
        count_i = -1
        count_j = -1
        while count_i < len(products_final[:][:])-1:
            count_i = count_i + 1
            count_j = -1
            while count_j < len(products_final[count_i][:])-1:
                count_j = count_j + 1
                results.append(products_final[count_i][count_j])
        len(results)
        products_char = []
        count_j = -1
        while count_j < len(results[:])-1:
            count_j = count_j + 1
            #with closing(Firefox()) as browser:
            url7 = "https://www.ah.nl" + results[count_j]
            self.driver.get(url7)
            time.sleep(5)
            # wait for the page to load
            #WebDriverWait(browser, timeout=100).until(
            #   lambda x: x.find_element_by_xpath("//div[@class='lane row product-lane']")) 
            # store it to string variable
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source)
            a = soup.find('span', class_='price__integer')
            b = soup.find('span', class_='price__fractional')
            c = soup.find('span', class_='product-description__unit-size -multiline')
            d = soup.find('span', class_='product-description__price-per-usage')
            products_char.append([url7, a, b, c, d])
        products_char
        os.chdir('C:/Users/Menno/Documents/Scanrs/')
        count_j = -1
        while count_j < len(results[:])-1:
            url8 = "https://www.ah.nl" + results[count_j]
            get_ipython().magic('run dowloader.py url8')
        sys.version_info
         #self.driver.save_screenshot('check.png')
        
    def quit(self):
        try:
            self.driver.service.process.send_signal(signal.SIGTERM)
            self.driver.quit()
        except:
            self.driver.quit()

Crawler().quit()
crawler = Crawler()