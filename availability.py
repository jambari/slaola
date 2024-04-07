from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException
# Set up the Selenium WebDriver
driver = webdriver.Chrome() 

#daftar stasiun yang dimonitor
stations = ['JAY','MTJPI','SJPM','ARKPI','GENI','SKPM','LJPI','BTSPI',
            'SATPI','SMPI','WAMI','DYPI','MTMPI','MIBPI','TRPI','OBMPI','MIPI',
            'WWPI','SRPI','ERPI','YBYPI','BAKI','EDMPI','ELMPI','UWNPI','NBPI',
            'SUSPI','WANPI','FKMPM','KIMPI','SOMPI','MMPI','IWPI','RKPI','MWPI','ANAPI',
            'MBPI','KMPI','BATPI','SWPM','AMPM','FAKI','FKSPI','TSPI','STPI','SIJI',
            'SWI','KARPI','RAPI','MBRPI','KORPI','GARPI']

# stations = ['AMPM','ANAPI','ARKPI','ARMI','ARPI','BAKI']

total_time = 0
i = 0
for station in stations:
    start_time = time.time()
    # Masukan alamat website
    url = "http://202.90.198.40/sismon-wrs/web/detail_slmon2/"+station
    driver.get(url)
    # tunggu hasilnya
    time.sleep(10)
    try:
        # tunggu hasilnya
        row_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#z-row"))
        )
        
        # Once the row is loaded, you can extract its contents
        try:
            third_td = row_element.find_element(By.XPATH,".//td[4]")
            third_td_text = third_td.text
            print(f"The availability data of {station} is {third_td_text}")
        except:
            print(f"The availability data of {station} is 0")
            continue
            
    except TimeoutException:
        print(f"Timeout waiting for element on {station}. Continuing to the next station.")
        continue
    end_time = time.time()  # Record the end time
    iteration_time = end_time - start_time  # Calculate the elapsed time for this iteration
    print(f"Iteration for station {station} took {iteration_time:.2f} seconds")
    print(f"number of iteration is{i}")
    i += 1
    total_time += iteration_time


driver.quit()
print(f"Total time for all iterations: {total_time:.2f} seconds")
