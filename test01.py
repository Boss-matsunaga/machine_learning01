import requests, bs4
res = requests.get('https://crowdworks.jp/public/employees/14218')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elems = soup.select('span.score.contracts')
print(elems)
