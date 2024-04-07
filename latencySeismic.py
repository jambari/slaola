from bs4 import BeautifulSoup
import requests
import mysql.connector
from datetime import datetime

# Custom format (dd/mm/YY H:M:S)


# Masukan alamat website
url = "https://geof.bmkg.go.id/slmon/"

# akses url
response = requests.get(url)
html_content = response.text

# Parsing isi html
soup = BeautifulSoup(html_content, "html.parser")

#siapkan dictionary penampung
latencies = []

#daftar stasiun yang dimonitor
stations = ['JAY','MTJPI','SJPM','ARKPI','GENI','SKPM','LJPI','BTSPI',
            'SATPI','SMPI','WAMI','DYPI','MTMPI','MIBPI','TRPI','OBMPI','MIPI',
            'WWPI','SRPI','ERPI','YBYPI','BAKI','EDMPI','ELMPI','UWNPI','NBPI',
            'SUSPI','WANPI','FKMPM','KIMPI','SOMPI','MMPI','IWPI','RKPI','MWPI','ANAPI',
            'MBPI','KMPI','BATPI','SWPM','AMPM','FAKI','FKSPI','TSPI','STPI','SIJI',
            'SWI','KARPI','RAPI','MBRPI','KORPI','GARPI']

#cari element tr pada tabel
rows = soup.find_all('tr')


#inisiasi database
host = "localhost"
user = "admin"
password = "su97696"
database = "datin"

j = 1
#looping tiap tr
for row in rows:
    tt_elements = row.find_all('tt') #ambil element tt pada tiap baris tr
    aa_elements = row.find_all('a') #ambil element tt pada tiap baris a
    
    if len(tt_elements) >= 2 and len(aa_elements) ==1 : # jika di baris tersebut ada elemen tt lebih dari 2 (berarti baris isi latensi)
        latency_in_general = tt_elements[1].text  #ambil nilai latensi yang masih ada keterangan waktunya
        latency_in_general_splitted = latency_in_general.split() #pecah latency dan tanda waktunya
        latency_number = latency_in_general_splitted[0] #ambil angka latency nya
        latency_remark = latency_in_general_splitted[1] #ambil keterangan waktu
        latency_in_second = 0 #deklarasikan variabel latensi dalam detik
        status = ''
        if latency_remark == 's':
            latency_in_second = float(latency_number) # simpan latensi dalam sekon
            status = 1 
        elif latency_remark == 'm':
            latency_in_second = float(latency_number)*60 #jika latensi dalam menit, maka kali 60 untuk mengubah ke detik
            if latency_in_second <= 900: #jika latensi kurang dari 30 menit
                status = 1 #status mati
            else:
                status = 0
        elif latency_remark == 'h': #jika keterangan latensi dalam h(jam)
            latency_in_second = float(latency_number)*60*60 #angka dikali 60 untuk ke menit, dan dikali 60 lagi menjadi second
            status = 0 #status mati
        else:
            latency_in_second = float(latency_number)*24*60*60 #jika status dalam d(hari) maka dikali 24 dikali 3600
            status = 0
        stasiun_code = aa_elements[0].text #catat kode site, ex JAY, JMPI
        j += 1
        latency_dict = [stasiun_code, latency_in_second, status] #buat list isinya kode site, nilai latensi, dan status
        # print(f'{j} | {stasiun_code} | {latency_in_second} | {status}')
        latencies.append(latency_dict)

i=1

#catat tanggal waktu


# #masukan data ke database
for latency in latencies:
    if latency[0] in stations:
        try: 
            ##conn = sqlite3.connect('jambari.db')
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            created_at = datetime.now()
            print("Connection to the database successful!")
            cursor = conn.cursor()
            data = (i, latency[0], latency[1], latency[2], created_at)
            #print(data)
            sql = "INSERT INTO latencies (number_code,site, latency, status, created_at) VALUES (%s, %s,%s,%s,%s)"
            #cursor.execute('INSERT INTO slaola (number_code, station, latency, status) VALUES (?,?,?,?)', data)
            i += 1
            # print(f'{i} | {latency[0]} | {latency[1]} | {latency[2]}')
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
        except mysql.connector.Error  as err:
            print(f"Error connecting to the database: {err}")


# #ambil data dari database
# conn = sqlite3.connect('jambari.db')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM slaola')

# rows = cursor.fetchall()

# for row in rows:
#     print(row)
    
# conn.close()
        
# k=1
# for latency in latencies:
#     if latency[0] in stations:
#         print(f'{k} {latency[0]} {latency[1]} {latency[2]}')
#         k += 1
