import datetime
import urllib2
import zipfile
from StringIO import StringIO
from zipfile import ZipFile

import os

import pandas as pd
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

dir_name = os.path.dirname(os.path.realpath(__file__))
extension = ".zip"

os.chdir(dir_name)

for item in os.listdir(dir_name):
    if item.endswith(extension):
        file_name = os.path.abspath(item)
        zip_ref = zipfile.ZipFile(file_name)
        zip_ref.extractall(dir_name)
        zip_ref.close()
        os.remove(file_name)

csv_extension = '.csv'
file_name_result = 'result.csv'

frame = pd.DataFrame()
list_ = []

for item in os.listdir(dir_name):
    if item.endswith(csv_extension):
        file_name = os.path.abspath(item)
        df = pd.read_csv(file_name, index_col=None, header=0)
        list_.append(df)
        os.remove(file_name)

frame = pd.concat(list_)
frame.to_csv(file_name_result, encoding='utf-8', index=False)
