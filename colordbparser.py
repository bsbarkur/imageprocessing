from bs4 import BeautifulSoup
import requests

def parser(url):
	hex_code = []
	rgb_tuple = []
	color_name = []
	r  = requests.get(url)
	data = r.text

	soup = BeautifulSoup(data)

	for link in soup.find_all('p'):
		if str(link)[10:20] == "width:10em":
			pos = str(link).find("rgb")
			tmpstr = str(link)[pos+3:]
			epos = tmpstr.find(";")
			tup = tmpstr[:epos]
			rgb_tuple.append(tup)
		
                        cpos = tmpstr.find("#")
			newstr = tmpstr[cpos+1:]
			hashpos = newstr.find("#")
			hasstr = newstr[hashpos:hashpos+7]
			hex_code.append(hasstr)
					
		else:
			pos = str(link).find("title")
			#print str(link)
			colstr = str(link)[pos-1:]
			cpos = colstr.find(">")
			tmpstr = colstr[cpos+1:]
			epos = tmpstr.find("<")
			ccode = tmpstr[:epos]
			if ccode != "A\xe2\x80\x93F":
				if(len(ccode) != 0):
					color_name.append(ccode)

	#print len(color_name)
	#print rgb_tuple
	#print len(hex_code)

	for idx, val in enumerate(color_name):
		print color_name[idx], rgb_tuple[idx], hex_code[idx]

if __name__ == "__main__":
	parser("http://en.wikipedia.org/wiki/List_of_colors_%28compact%29")
