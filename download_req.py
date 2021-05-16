from os import link
import requests, csv
import datetime
from zipfile import ZipFile
# NOTE for development - remember to use venv -> source ./bin/env/activate

#get codes from config.dat
#download sheet and get the values for selected codes

# global vars
#headers for mimicking a browser
h = {'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"}
base_link = "http://www.bseindia.com/download/BhavCopy/Equity/EQ" #base link,add params at the end


# functions 

# generate today's date
def get_date():
	date  = datetime.datetime.now()
	d = date.strftime("%d")
	d += date.strftime("%m")
	d += date.strftime("%y")
	# d = '300321' => for debugging purposes
	print(d) 
	return(d)

# get the req data for link, return a tuple of req,date
def make_req(date):
	if( len(date.strip())==0 ):
		# default behaviour - today's date
		date = get_date()
	link= base_link + (date+"_CSV.ZIP")
	print("requesting link: "+link)
	r = requests.get(link, headers=h)
	return (r,date)

# download given file type with given filename 
def download(request,ftype,fname):
	with open(fname, 'wb') as f:
	#giving a name and saving it in any required format, opening the file in write mode
		print("downloading: " + fname )
		f.write(request.content)

#extract zip file with given name
def extract_zip(fname):
	with ZipFile(fname, 'r') as zipObj:
    # Extract all the contents of zip file in current directory
		zipObj.extractall()

# process ip files, and give an output
def proc(ip_fname,req_fname,op_fname):
	# get target codes from req_fname 
	# get the reuired codes of stocks
	sc_codes_lst = []
	with open(req_fname) as f:
		for line in f.readlines():
			if len(line)!=0:
				sc_codes_lst.append(line.strip())
	
	valid_tuples = {}
	titles = ['SC_CODE', 'SC_NAME', 'HIGH', 'LOW', 'OPEN', 'CLOSE','LAST']
	with open('output.csv', 'w', newline='' ) as op_file:
		writer = csv.writer(op_file)
		writer.writerow(titles)
		for code in sc_codes_lst:
			with open(op_fname, newline='') as csvfile:
				csv_reader = csv.DictReader(open(ip_fname), delimiter=',')
				found = False
				print(ip_fname)
				# print(csv_reader)
				for row in csv_reader:
					print(row)
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



def main():
	print ("Input required date in the format ddmmyy (ex 300321 for 30th may 2001) \n OR ")
	print ("Just input enter to try on today's date")
	d = input("Input:")
	(req,date) = make_req(d)

	if	req.status_code != 200:
		print(str(req.status_code)+" error, exiting program")
		exit()
	# if code is 200 ie req is success	
	print(str("parsing info for the date- " + date ))
	fname = date+"_CSV.ZIP"
	download(req,"zip",fname)
	extract_zip(fname)
	proc("EQ"+date+".CSV","config.dat","output.csv")


if __name__ == "__main__":
	main()	


