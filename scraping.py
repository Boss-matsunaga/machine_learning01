import requests
from bs4 import BeautifulSoup
import re
from time import sleep

URL = "http://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx"
URL1 = "http://anzeninfo.mhlw.go.jp"
print("aaaaaaaaaaaa")
class Scrap:
    def sc1(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
        
    def sc2(self, soup, flag):
    	li = []
    	if flag == 1:
    		soup = soup.select('a[href^="/anzen/sai/sai_new"]')
    	if flag == 2:
    		soup = soup.select('a[href^="/anzen_pg/SAI_DET.aspx?"]')
    	for a in soup:
    		sleep(1)
    		print(a.get('href'))
    		li.append(a.get('href'))
    	return li
    		
sc = Scrap()

soup = sc.sc1(URL)
data = sc.sc2(soup,1)

for i in data:
	soup2 = sc.sc1(URL1+i)
	data2 = sc.sc2(soup2,2)
	# print(data2)
	for j in data2:
		soup3 = sc.sc1(URL1+j)
		soup3 = soup3.find("table", class_="tbl_1_1_1")
		print(soup3)
		sleep(1)
