import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# baca file berisi lintang bujur sesuaikan nama filenya ya
df = pd.read_csv('pga_grid.csv')

# buat file untuk menyimpan nilai pga
with open('results.txt', 'w') as file:
    # tulis nama kolom tabel
    file.write('Loop, Bujur, Lintang, PGA\n')
    
    # urutan iterasi, silahkan disesuaikan
    iterasi = 0

    # iterasi sesuai isi grid
    for index, row in df.iterrows():
        # ambil lintang dan bujur
        # current_lintang = -2.9
        # current_bujur = 140.0
        driver = webdriver.Chrome()

        # masukan alamat
        driver.get("https://rsa.ciptakarya.pu.go.id/2021/#grafik")

        # cari kolom input koordinat
        lintang = driver.find_element(By.NAME, "lintang")
        bujur = driver.find_element(By.NAME, "bujur")
        current_lintang = row['Latitude']
        current_bujur = row['Longitude']
        # wait = WebDriverWait(driver, 100)

        # ketikan nilai
        lintang.send_keys(current_lintang)
        bujur.send_keys(current_bujur)

        # klik tombol hitung
        hitung_button = driver.find_element(By.NAME,"hitungBTN")
        hitung_button.click()

        # tunggu hasilnya
        time.sleep(10)
        result_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#pga"))
        )

        # ambil nilai pga
        pga_element = driver.find_element(By.CSS_SELECTOR,"#pga")
        pga_value = pga_element.get_attribute("value")

        iterasi += 1
        
        # print hasilnya di terminal
        print(str(iterasi)+" "+str(current_lintang)+" "+str(current_bujur)+" "+pga_value)

        # tulis hasilnya ke file dengan urutan nomor, bujur, lintang, nilai pga
        file.write(f"{iterasi}, {current_bujur}, {current_lintang}, {pga_value}\n")

        # clear the input fields
        # lintang.clear()
        # bujur.clear()

    # close the browser
        driver.quit()


    #     # iterasi sesuai isi grid
    # for index, row in df.iterrows():
    #     # ambil lintang dan bujur
    #     current_lintang = row['Latitude']
    #     current_bujur = row['Longitude']
    #     wait = WebDriverWait(driver, 100)

    #     # ketikan nilai
    #     lintang.send_keys(current_lintang)
    #     bujur.send_keys(current_bujur)

    #     # klik tombol hitung
    #     hitung_button = driver.find_element(By.NAME,"hitungBTN")
    #     hitung_button.click()

    #     # tunggu hasilnya
    #     result_element = WebDriverWait(driver, 100).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "#pga"))
    #     )

    #     # ambil nilai pga
    #     pga_element = driver.find_element(By.CSS_SELECTOR,"#pga")
    #     pga_value = pga_element.get_attribute("value")

    #     # print hasilnya di terminal
    #     print(pga_value)

    #     # tulis hasilnya ke file dengan urutan nomor, bujur, lintang, nilai pga
    #     file.write(f"{index}, {current_bujur}, {current_lintang}, {pga_value}\n")

    #     # clear the input fields
    #     lintang.clear()
    #     bujur.clear()

    # # close the browser
    # driver.quit()
