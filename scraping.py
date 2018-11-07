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
    		num_data = []
    		soup_href = soup.find("table", class_="tbl_1_1_1")
    		soup_href = soup_href.find_all("td")
    		for num_html in soup_href:
    			if num_html != None:
    				num_tmp = num_html.text.split("\t")[18]
    				# print(num_tmp)
    				num_data.append(num_tmp[-4])
    		# print(num_data)
    		yield num_data

    def get_text(self, soup):
    	text_data = ""
    	soup_text = soup.find("table", class_="tbl_1")
    	soup_text = soup_text.find_all("table", border="0")
    	th_text = soup_text[0].find("th")
    	th_text = th_text.find("h1")
    	th_text = th_text.text.splitlines()
    	text_data += th_text[1].replace("\t","").replace(" ","")
    	for table_text_num in range(len(soup_text)):
    		if table_text_num == 0: continue
    		td_text = soup_text[table_text_num].find_all("td")
    		# print("-----------------------------------------------------")
    		for text in td_text:
    			# print(text.text)
    			text_data += text.text
    		yield text_data.replace("\u3000","").replace("\u2460","").replace("\u2461","").replace("\u2462","").replace("\ufffd","")
    		
sc = Scrap()

for cases_path in sc.select_href(sc.get_html(URL),1):
	# print(cases_path)
	for case_path in sc.select_href(sc.get_html(base_URL+cases_path),2):
		result = []
		# print(case_path)
		sleep(1)
		three_soup = sc.get_html(base_URL+case_path)
		result = list(sc.select_href(three_soup,3))[0]
		result.insert(0,list(sc.get_text(three_soup))[0])
		with open('result.csv','a',newline="",encoding='shift_jis') as file:
			writer = csv.writer(file)
			writer.writerow(result)
			# print(result)
			print("入れた")