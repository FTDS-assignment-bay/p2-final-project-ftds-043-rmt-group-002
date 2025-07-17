from bs4 import BeautifulSoup # berfungsi untuk mempermudah proses web scraping dengan cara memproses dan mengurai kode HTML dan XML.
from selenium import webdriver # berfungsi untuk mengotomatiskan browser web dan mengekstrak data dari halaman web.
import pandas as pd # berfungsi untuk mengolah data yang telah di dapatkan dari web 
import numpy as np # berfungsi untuk mengolah data
import time # berfungsi untuk mengimpor pustaka time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException # berfungis untuk melakukan load button 
from selenium.webdriver.common.by import By # berfungsi untuk menentukan cara mencari elemen di halaman web.


# Berfungsi untuk membuka aplikasi chrome
driver = webdriver.Chrome() 

# List untuk menyimpan data
brd = [] # Nama Brand 
prdk = [] # Nama Produk
sub = [] # Nama Sub-Produk 
qty = [] # Barang yang telah di review
rtg = [] # Rating Produk 

# Berfungsi untuk menyimpan url yang akan diakses 
url = f"https://reviews.femaledaily.com/products/fragrance/edp?brand=&order=popular&page=1"
driver.get(url)

time.sleep(5) # Untuk memberikan jeda agar website bisa load content terlebih dahulu

target_produk = 1020

# Loop klik tombol 'Load More'
while True:
    # Berfungsi untuk cek jumlah produk saat ini
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('a', {'class': 'product-card'})
    print(f"Jumlah produk saat ini: {len(items)}")

    if len(items) >= target_produk:
        print("Target jumlah produk tercapai.")
        break

    try:
        load_more_btn = driver.find_element(By.CLASS_NAME, 'btn-load-more')
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
        time.sleep(1)
        load_more_btn.click()
        time.sleep(2)  # Waktu tunggu agar produk bisa dimuat

    except NoSuchElementException:
        print("Tombol Load More tidak ditemukan. Mungkin semua produk sudah dimuat.")
        break

    except ElementClickInterceptedException:
        print("Tombol tidak bisa diklik. Scroll dan coba lagi.")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

# Parsing HTML
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Cari semua produk
items = soup.find_all('a', {'class': 'product-card'})

# Loop semua produk
for item in items:
    product_info = item.find('div', {'class': 'info-product'})
    if product_info:
        brand_tag = product_info.find('p', {'class': 'fd-body-md-bold'})
        product_tag = product_info.find_all('p', {'class': 'fd-body-md-regular'})

        brand = brand_tag.get_text().strip() if brand_tag else None
        product = product_tag[0].get_text().strip() if product_tag else None
        sub_product = product_tag[1].get_text().strip() if product_tag else None

        # Ambil rating dan jumlah review dari dalam info-product
        rating_info = item.find('div', {'class': 'rating'})
        if rating_info:
            rating_tags = rating_info.find_all('span', {'class': 'fd-body-sm-regular'})

            rating = rating_tags[0].get_text() if len(rating_tags) > 0 else None
            review = rating_tags[1].get_text() if len(rating_tags) > 1 else None
            
        else:
            rating = None
            review = None
        
    else:
        brand = None
        product = None

    brd.append(brand)
    prdk.append(product)
    sub.append(sub_product)
    rtg.append(rating)
    qty.append(review)
    
# Tutup browser
driver.quit()

# Tampilkan hasil
print(f"Total produk ditemukan: {len(prdk)}")
for b, p, s, r, q in zip(brd, prdk, sub, rtg, qty):
    print(f"{b} - {p} - {s} - {r} - {q}")

# Menyimpan ke dalam Data Frame 
data_asli = pd.DataFrame({
    'nama_brand': brd,
    'nama_produk': prdk,
    'nama_sub_produk' : sub,
    'rating_produk': rtg,
    'total_review': qty
})

# Menyimpan DataFrame ke dalam CSV untuk melakukan crosscek
data_asli.to_csv('data_asli_final_project.csv', index=False)