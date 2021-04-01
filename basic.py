import requests, csv
import datetime
from zipfile import ZipFile

# global vars

#headers for mimicking a browser
h = {'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"}
# generate today's date
date  = datetime.datetime.now()
d = date.strftime("%d")
d += date.strftime("%m")
d += date.strftime("%y")
# d = '300321' => for debugging purposes
print(d) 

# urls, downloaded zip files 
fname = d+"_CSV.zip"
link = "http://www.bseindia.com/download/BhavCopy/Equity/EQ"+fname
print(link)


# main
r = requests.get(link, headers=h)
if	r.status_code != 200:
	print(str(r.status_code)+" error, exiting program")
	exit()
else:
	print(str("parsing info for the date- " + d ))

#giving a name and saving it in zip format
with open(fname, 'wb') as f:

	f.write(r.content)
	# print(r)

with ZipFile(fname, 'r') as zipObj:
   # Extract all the contents of zip file in current directory
	zipObj.extractall()

#get the required stock codes in list
sc_codes_lst = []

# get the required codes of shares
with open("config.dat") as f:
	for line in f.readlines():
		if len(line)!=0:
			sc_codes_lst.append(line.strip())

print(sc_codes_lst)

valid_tuples = {}
titles = ['SC_CODE', 'SC_NAME', 'HIGH', 'LOW', 'OPEN', 'CLOSE','LAST']
fname = "EQ"+d+".csv"
with open('output.csv', 'w', newline='' ) as op_file:
	writer = csv.writer(op_file)
	writer.writerow(titles)
	for code in sc_codes_lst:
		with open(fname, newline='') as csvfile:
			csv_reader = csv.DictReader(csvfile, delimiter=',')
			found = False
			for row in csv_reader:
				if row.get('SC_CODE')==code:
					found = True
					data_lst = []
					for title in titles:
						data_lst.append(row.get(title).strip())
					print(data_lst)
					writer.writerow(data_lst)
					break;
			if not found:
				print("not found-> " + code)