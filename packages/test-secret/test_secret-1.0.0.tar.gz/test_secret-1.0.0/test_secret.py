import requests
from bs4 import BeautifulSoup

def test_code(url):
	# url = 'http://www.iyuji.cn/iyuji/s/M0poUUp4YWYzSFZZTTM1T25oSjhkUT09/1543494806371534'
	f = requests.get(url, timeout=2)
	f.encoding='utf-8'
	g = f.text
	bsp = BeautifulSoup(g, 'lxml')
	# print(bsp)
	# 所有id属性为divid的所有元素
	tt = (bsp.select('#content'))
	end = str(tt[0]).split(',')
	print(end)
	return end