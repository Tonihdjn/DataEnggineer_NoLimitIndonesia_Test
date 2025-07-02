import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import re
import unicodedata
import time
import pandas as pd 
def get_soup(url) : #dapatkan soup agar tidak dipanggil berulang di tiap func 
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_judul(soup) : # mendapatkan judul yang sudah bersih 
    try : 
        jdl = soup.find('h1', class_ = "detailsTitleCaption").text
    except Exception as e:
        try : 
            jdl = soup.find('h1', class_ = "text-jet dark:text-white font-black lg:line-clamp-3 lg:text-center text-[24px] lg:text-[36px] lg:leading-[48px] mb-[16px]").text.strip()
        except : 
            jdl = "berita premium"
    return jdl

def get_tgl(soup) : #mendapatkann tgl yang sudah sesuai dengan ISO 8601 
    try :
        date_str = soup.find('div', class_="detailsAttributeDates").text.strip()
        locale.setlocale(locale.LC_TIME, 'ind')
        date_obj = datetime.strptime(date_str, "%A, %d %B %Y | %H:%M")
    except Exception as e:
        try:
            date_str = soup.find('div', class_="authorTime text-[12px] leading-[16px] text-gray dark:text-timberwolf").text.strip()
            date_obj = datetime.strptime(date_str, "%A, %d %B %Y | %H:%M")
        except Exception as e:
            # Jika kedua cara gagal, kita set tanggal default atau tangani sesuai kebutuhan
            print(f"Error: {e}")
            return None

    return date_obj.isoformat()

def clean_text(text): #membersihkan text 
    text = ''.join((c for c in text if unicodedata.category(c) != 'Cn'))
    text = text.replace("â€™", "'").replace("â€œ", '"').replace("â€", '"')
    text = re.sub(r'[^a-zA-Z0-9\s\.,;?!]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()    
    return text
def get_isi(soup) : #mendapatkan isi artikel yang sudah bersih 
    article = soup.find('article', class_="detailsContent force-17 mt40")
    try :
        if article:
            paragraphs = article.find_all('p', class_=lambda x: x != 'baca-juga-title')
            isi = ""
            for para in paragraphs:
                isi = isi + para.text + " "
        else:
            article = soup.find('article', class_="detailsContent force-17 detailsLive mt40")
            paragraphs = article.find_all('p', class_=lambda x: x != 'baca-juga-title')
            isi = ""
            for para in paragraphs:
                isi = isi + para.text + "\n"
    except : 
        isi = "konten berbayar"
    isi = clean_text(isi)
    return isi

def get_all(url) : # untuk mendapatkan seluruh informas 
    soupAll = get_soup(url)
    jdl = get_judul(soupAll) 
    print(jdl)
    tgl = get_tgl(soupAll)
    print("mendapatkan tgl")
    isi = get_isi(soupAll)
    print("mendapatkan isi")
    return jdl, isi , tgl 

def one_page(output, soupOne) : #ngambil seluruh informasih dalam 1 page list/indeks berita
    soupOne.find_all('a', class_ = "artLink")
    hrefs = [a['href'] for a in soupOne.find_all('a', class_ = "artLink")]
    hrefs = list(dict.fromkeys(hrefs))
    for href in hrefs : 
        print(f"Masuk ke page {href}")
        jdl, isi, tgl = get_all(href) 
        output.append({
            'link' : href, 
            'Judul' : jdl,
            'tanggal' : tgl, 
            'isi' : isi 
        })
def navigate_many_page(url) : #untuk ngambil seluruh indeks 
    output = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(5)
            soup = get_soup(url)
            one_page(output, soup)
            next_page = soup.find('a', {'rel': 'next'})
            if next_page:
                url = next_page['href']
                print(f"Melanjutkan ke Page List: {url}")
            else:
                print("Tidak ada Page List berikutnya.")
                url = None
        else:
            print(f"Error: {response.status_code}")
            url = None
    return output
# untuk membuat URL berdasarkan tanggal
def generate_url(date):
    return f'https://www.bisnis.com/index?categoryId=0&type=indeks&date={date}&page=1'

# untuk melakukan scraping berdasarkan rentang tanggal
def scrape_by_date_range(start_date, end_date):
    output = []
    date_range = pd.date_range(start=start_date, end=end_date)
    for single_date in date_range:
        date_str = single_date.strftime('%Y-%m-%d')
        url = generate_url(date_str)
        output += navigate_many_page(url)
    return output

