#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Description: crawl shop information from www.dianping.com     
#  Author: Kalvin Ni                           
#  Date: Dec 12th, 2015                         
#  Version: 1         

#**********************************************#

import requests
import re
import sys
import xlrd
import decodePOI
from bs4 import BeautifulSoup
import csv
import time

# to sovle the problem about Chinese characters
reload(sys)  
sys.setdefaultencoding("utf8")  
sys.setrecursionlimit(1000000)

def fetch(CircleID):
	URL = 'http://www.dianping.com/search/category/1/0/'+CircleID
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'}
	s = requests.session()
	PAGE = 1

	f = open('./results/BCircle'+CircleID+'.csv','w')
	f.write('\xEF\xBB\xBF');
	f.write('ID,Name,Address,Latitude,Longitude,Rank,Review Number,Mean Price,Category,Business Circle\n')

	while URL!=None:
		ShopDic = {}
		ShopID = []
		print 'Processing Page',PAGE
		content = s.get(URL, headers = headers).content
		Soup = BeautifulSoup(content,'html.parser')


		for line in Soup.find_all(class_='operate J_operate Hide'):
			ID = line.find('a', class_ = 'o-map J_o-map').get('data-shopid')
			Name = line.find('a', class_ = 'o-favor J_o-favor').get('data-name')
			Address = line.find('a', class_ = 'o-map J_o-map').get('data-address')
			Position = line.find('a', class_ = 'o-map J_o-map').get('data-poi')
			POS = decodePOI.decode(Position)
	
			ShopDic[ID] = []
			ShopDic[ID].append(Name)
			ShopDic[ID].append(Address)
			ShopDic[ID].append(POS['lat'])
			ShopDic[ID].append(POS['lng'])
			ShopID.append(ID)
			
		for line in Soup.find_all(class_='txt'):
			ID = line.find(class_='tit').find('a').get('href').split('/')[2]
			try:
				Price = re.sub('</?\w+[^>]*>','',str(line.find(class_='comment').find(class_='mean-price').find('b')))
			except:
				Price = None
			
			try:
				CommentNum = re.sub('</?\w+[^>]*>','',str(line.find(class_='review-num').find('b').get_text()))
			except:
				CommentNum = None
				
			ShopDic[ID].append(line.find(class_='comment').find('span').get('title'))
			ShopDic[ID].append(CommentNum)
			ShopDic[ID].append(Price)
	
		TagAddr = Soup.find_all(class_ = 'tag-addr')
	
		for i in range(0,len(TagAddr)):
			line = TagAddr[i]
			addr = line.find(class_='addr').get_text()
			span = line.find_all('span')
			category = span[0].get_text()
			BCircle = span[1].get_text()
			ID = ShopID[i]
			ShopDic[ID].append(category)
			ShopDic[ID].append(BCircle)

		for key,value in ShopDic.items():
			line = key
			for term in value:
				line = line+','+'"'+str(term)+'"'
			f.write(line+'\n')

		print 'Page', PAGE, 'Done'
		PAGE += 1
		nextpage = Soup.find(title = '下一页')
		if nextpage == None:
			URL = None
		else:
			URL = 'http://www.dianping.com'+nextpage.get('href')
		print '...Sleep 5 seconds\n'
		time.sleep(5)
	
	f.close()

if __name__ == '__main__':
	fetch('r801')


