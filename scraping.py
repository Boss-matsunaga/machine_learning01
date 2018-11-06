import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import csv

URL = "http://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx"
base_URL = "http://anzeninfo.mhlw.go.jp"

class Scrap:
    def get_html(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
        
    def select_href(self, soup, flag):
    	li = []
    	if flag == 1:
    		soup = soup.select('a[href^="/anzen/sai/sai_new"]')
    		for a in soup:
    			yield a.get('href')

    	if flag == 2:
    		soup = soup.select('a[href^="/anzen_pg/SAI_DET.aspx?joho_no="]')
    		for hre in soup[::2]:
    			yield hre.get('href')

    	if flag == 3:
    		soup = soup.find("table", class_="tbl_1_1_1")
    		soup = soup.find_all("td")
    		num_data = []
    		for num_html in soup:
    			if num_html != None:
    				num_tmp = num_html.text.split("\t")[18]
    				num_data.append(num_tmp[-4])
    		print(num_data)
    		yield num_data
    	
    		
sc = Scrap()

for cases_path in sc.select_href(sc.get_html(URL),1):
	print(cases_path)
	for case_path in sc.select_href(sc.get_html(base_URL+cases_path),2):
		print(case_path)
		sleep(1)
		with open('result.csv','a',newline="") as file:
			writer = csv.writer(file)
			writer.writerow(sc.select_href(sc.get_html(base_URL+case_path),3))
			print("入れた")


# soup = sc.sc1(URL)
# data = sc.sc2(soup,1)
# print(data)
# with open('result.csv', 'a') as file:
# 	result = []
# 	for i in data:
# 		soup2 = sc.sc1(URL1+i)
# 		for data2 in sc.sc2(soup2,2):
# 			print(data2)
# 			soup3 = sc.sc1(URL1+data2)
# 			soup3 = soup3.find("table", class_="tbl_1_1_1")
# 			soup3 = soup3.find_all("td")
# 			l = []
# 			for j in soup3:
# 				if j != None:
# 				    print(j.text.split("\t")[18])
# 				    l.append(j.text.split("\t")[18])
		
# 			# print(soup3.text)
# 			# hoge = str(soup3.text)
# 			# hoge = hoge.replace("\t","")
# 			# hoge = hoge.split("\n")
# 			# print(hoge)
# 			# hoge = hoge.remove("a")
# 			#print(hoge)
# 			# hoge2 = hoge.split(" ")
# 			# print(hoge2)
# 			print(l)
# 			writer = csv.writer(file, lineterminator = '\n')
# 			writer.writerow(l)
# 			print("入れた")