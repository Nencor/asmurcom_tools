import requests,os,tabula,ssl,re
from bs4 import BeautifulSoup
from tabula.io import *

ssl._create_default_https_context = ssl._create_unverified_context

link_scrape = {
    'axa':'https://axa.co.id',
    'axa_moc':'https://axa.co.id/maestro-optima-care'
}

#basic scrapes
page = requests.get(link_scrape['axa_moc'])
soup = BeautifulSoup(page.content, "html.parser")
all_downloads = soup.findAll('a',class_='download',href=True)
hospital_pdfs=[]

#getting direct link downloads
for download in all_downloads:
    url = download['href']
    url = re.sub('.pdf.*','',url)+'.pdf'
    final_url = link_scrape['axa']+url
    if 'admedika' in final_url.lower():
        hospital_pdfs.append(final_url)
        print(final_url)
print(f"{len(hospital_pdfs)} file(s) found")

#looping hospital_pdfs
for hospital_pdf in hospital_pdfs:
    print(hospital_pdf)
    df = tabula.read_pdf(hospital_pdf)
    break
print(df)