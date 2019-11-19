import requests
from bs4 import BeautifulSoup
import re
import pydotplus


preq = dict()

name = dict()

def get_preq(url):
	global preq
	print(url)
	reqq = requests.get(url)
	soup = BeautifulSoup(reqq.text)
	print (url)
	print ()
	sss = soup.find(id='div_course_code_and_title').text.split(' - ')[0]
	preq[sss] = re.findall('(MA\d\d\d\d)',str(soup.find_all('tr')[5].text))
	name[sss] = soup.find(id='div_course_code_and_title').text.split(' - ')[1].replace('-',' ')



def draw():
	graph = pydotplus.graph_from_dot_data(dot_data)
	graph.write_png("relation.png")

if __name__ == "__main__":
	req = requests.get('https://www.cityu.edu.hk/ma/ug/minor/courselist-new.htm')
	b = BeautifulSoup(req.text)
	all_tr = b.find_all('tr')
	all_a = [ atr.find_all('a') for atr in all_tr  ]
	all_a = list(filter(lambda x: len(x)>0,all_a))
	all_a =  [ atr[0] for atr in all_a  ]

	for i in all_a:
		# print (i)
		get_preq(i['href'])

	dot_data = "digraph Tree {"+';'.join([ i + '[label="'+i+'\n'+name[i]+'"]'for i in preq.keys() ])+';'+';'.join([';'.join([ str(i)+'->'+j for j in preq[i] ]) for i in preq.keys()])+';'+"}"
	draw();
	pass