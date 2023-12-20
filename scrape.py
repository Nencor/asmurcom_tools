import requests,os,re,shutil,glob
from bs4 import BeautifulSoup
import urllib.request
from tabula import read_pdf

link_scrape = {
    'axa':'https://axa.co.id',
    'axa_moc':'https://axa.co.id/maestro-optima-care',
    'pdfs': os.path.join(os.path.dirname(__file__),'pdfs')
}

def get_pdf_urls(linknya,str_in_filename='admedika'):

    #basic scrapes
    page = requests.get(link_scrape[linknya])
    soup = BeautifulSoup(page.content, "html.parser")
    all_downloads = soup.findAll('a',class_='download',href=True)
    hospital_pdfs=[]

    #getting direct link downloads
    for download in all_downloads:
        url = download['href']
        url = re.sub('.pdf.*','',url)+'.pdf'
        final_url = link_scrape['axa']+url
        if str_in_filename in final_url.lower():
            hospital_pdfs.append(final_url)
    print(f"{len(hospital_pdfs)} file(s) found")
    return hospital_pdfs

def delete_files_in_folder(folder):
    print(f"Deleting files in '{folder}'...")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print(f"Files in '{folder}' deleted.")

def download_pdfs(url_to_downloads,empty_directory=True):
    delete_files_in_folder(link_scrape['pdfs']) if empty_directory else None
    for url in url_to_downloads:
        filename = os.path.basename(url)
        urllib.request.urlretrieve(url,os.path.join(link_scrape['pdfs'],filename))
        print(f"'{filename}' downloaded")

# url_to_downloads = get_pdf_urls(linknya='axa_moc')
# if len(url_to_downloads)>0:
    # download_pdfs(url_to_downloads)

for file in glob.glob(os.path.join(link_scrape['pdfs'],'*.pdf')):
    try:
        df = read_pdf(file,pages='all')
    except Exception as e:
        print(e)
    break
