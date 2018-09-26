import datetime
import urllib2
from StringIO import StringIO
from zipfile import ZipFile

from BeautifulSoup import BeautifulSoup
import requests
from dateutil.relativedelta import relativedelta


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

base_url = "https://nseindia.com"
url = base_url + "/ArchieveSearch"
query_parameter = '?h_filetype=eqbhav&section=EQ'

current_date = datetime.datetime.now().date() - relativedelta(days=1)
one_year_back = current_date - relativedelta(years=1)
list_links = []
date_query_parameter = '&date=' + str(current_date.strftime("%d-%m-%Y"))
file_name_partial = 'downlaod_file'
extension = '.zip'


for date in daterange(one_year_back, current_date):
    date_query_parameter = '&date=' + str(date.strftime("%d-%m-%Y"))
    request_url = url + query_parameter + date_query_parameter
    r = requests.get(request_url, allow_redirects=True)
    soup = BeautifulSoup(r.text)
    for link in soup.findAll('a'):
        if link.text:
            list_links.append(link['href'])

i = 0
for link in list_links:
    target_path = file_name_partial + str(i) + extension
    handle = open(target_path, "wb")
    query_url = base_url + str(link)
    print query_url
    response = requests.get(query_url, stream=True)
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()
    i += 1
