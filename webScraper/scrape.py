import httplib2,time,re,sys
from BeautifulSoup import BeautifulSoup
SCRAPING_CONN = httplib2.Http(".cache")
SCRAPING_DOMAIN_RE = re.compile("\w+:/*(?P<domain>[a-zA-Z0-9.]*)/")
SCRAPING_DOMAINS = {}
SCRAPING_CACHE_FOR = 60 * 15 #caching for 15 mins
SCRAPING_REQUEST_STAGGER = 1100 # in milliseconds
SCRAPING_CACHE = {}

def fetch(url,method="GET"):
	#print "in fetch"
	
	key = (url,method)
	now = time.time()
	if SCRAPING_CACHE.has_key(key):
		data,cached_at = SCRAPING_CACHE[key]
		if now - cached_at < SCRAPING_CACHE_FOR:
			return data
	domain = SCRAPING_DOMAIN_RE.findall(url)[0]
	if SCRAPING_DOMAINS.has_key(domain):
		last_scraped = SCRAPING_DOMAINS[domain]
		elapsed = now - last_scraped
		if elapsed < SCRAPING_REQUEST_STAGGER:
			wait_period = (SCRAPING_REQUEST_STAGGER - elapsed) / 1000
			time.sleep(wait_period)
	SCRAPING_DOMAINS[domain] = time.time()
	data = SCRAPING_CONN.request(url,method)

	SCRAPING_CACHE[key] = (data,now)
	return data

def isAvailable(geneID):
	#print "in is available"

	page = fetch(u"http://www.proteinatlas.org/gene_info.php?ensembl_gene_id="+geneID)
	soup = BeautifulSoup(page[1])
	#str titleTag =  u""
	#html = soup.html
	try:
		titleTag = soup.html.head.title.string
	except : 
		#print "unavailable"
		titleTag = "rofl no"
		present = False
	#print titleTag
	#titleTag = titleTag.strip()
	present = (titleTag in "<title>Human Protein Atlas</title>\n")
	return present

def getName(geneID):
	page = fetch(u"http://www.proteinatlas.org/gene_info.php?ensembl_gene_id="+geneID)
	soup = BeautifulSoup(page[1])
	try:
		table = soup.findAll('b')
		return table[0].find(text=True)
	except:
		print "fuckedup"

def removeNL(x):
	"""cleans a string of new lines and spaces"""
	s = x.split('\n')
	s = [x.strip() for x in s]
	x = " ".join(s)
	return x.lstrip()

def getTissue(geneID):
        page = fetch(u"http://www.proteinatlas.org/gene_info.php?ensembl_gene_id="+geneID)
	soup = BeautifulSoup(page[1])
	try:
		linkToTissue = soup('a', href=re.compile('#normal'))
		linkText =  linkToTissue[0]['href']
		page = fetch(u"http://www.proteinatlas.org/"+linkText)
		print "tissue page fetched"
		soup = BeautifulSoup(page[1])
		print "made soup"
		normalTissueTable = soup('table',attrs={"id":"tp_section_1"})
		print "managed"
		#print normalTissueTable[0].findAll(attrs={"class":"tissue0"})
		# this one works myTable = soup('table',attrs={"id":"tp_section_1"})
		select = soup.find('table',{'id':"tp_section_1"})
		
		#print select
		#print "got table"
	 	
		#print select[1]		
		
		#i=0	
		#for td in select:
		#	#print "here"
		#	print "select =%d" % i
		#	i=i+1
		#	print td
			#print td.findAll(text=True)
			#print "here now"
			#print td.findAll('img')
		
		#tissueTypesImages = select.findAll('img')
		#print "--tissueTypesImages--"
	        #print tissueTypesImages
		tissues = select.findAll('td',{"class":re.compile("tissue[10]")})
		tissueTable=[]	
		for i in tissues:
			text=i.findAll(text=True)
			#print text
			if len(text)==3:
				tissueTable.append(text[1])
			if len(text)==1:
				tissueTable.append(tissueTable[len(tissueTable)-1])
		#print len(tissueTable)
		tissueTypes=select.findAll('td',{"class":re.compile("tissuetype[10]")})
		#print tissueTypes
		tissueTypeTable=[]
		
		for j in tissueTypes:
			#print "in for loop"
			text=j.findAll(text=True)
			#print "in text"
		
			#text=text.strip()
			text[0]=text[0].rstrip('\r\n\t&nbsp;')
			text[0]=text[0].lstrip('\r\n\t')
			tissueTypeTable.append(text[0])
		#print len(tissueTypeTable)
		
		images = select.findAll('img')
		#print images
		imageTable=[]
		for k in images:
			imageSrc = k['src']
			imageSrc=imageSrc[21:]
			imageSrc=imageSrc.rstrip('.gif')
			imageTable.append(imageSrc)
		i=0
		for index in images:
			print tissueTable[i]," ", tissueTypeTable[i]," has expression type ", imageTable[i]
			i=i+1
		#print imageTable
		#print len(imageTable)
		#tissuesText = tissues
		#tissuesText('a')
		#print "--tissuesText--"
		#print "\n"
		#print tissuesText
		#print "linkTable"
		#linkTableText = linkTable.findAll(text = True)
		#print linkTableText
		#tissueTypes = select.findAll(text = True)
		#cellTypeList = []
		#for line in tissueTypes:
		#	line = removeNL(line)
		#	if line != "":
		#		if u'&nbsp' in line: 
		#			line=line.rstrip('&nbsp; ')
		#		cellTypeList.append(line)
		#cellTypeList = cellTypeList[1:]
		#print cellTypeList
		#print tissueTypes


		#for blah in soup.fetch('table',attrs={"id":"tp_section_1"}):
		#	print a.string 
		#print myTable
		#print  myTable.contents
		#print "made new table"
		#print table.contents
		
		#print image
		#print image

	except:
		print "no Tissue Data"
		print "Unexpected error:", sys.exc_info()[0]
		
while True:
	#print "At while true\n"
	myFile = open('ids','r')
	line = myFile.readline()
	line = line.strip()
	while line != "":
		line = line.strip()
		#print "in while"
		if isAvailable(line):
			print "GeneID: "+line+" Name: "+getName(line) +" is availabe"
			getTissue(line)
		else:
			print "GeneID: "+line+" is not available"
		time.sleep(2)
		#print isAvailable(line)
		line = myFile.readline()
	break	
