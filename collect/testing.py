from selenium.common import JavascriptException
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException
import os
import time
from selenium.webdriver.common.by import By

#driver = webdriver.Chrome('/Users/a2/tools/chromedriver')
driver = webdriver.Safari()
driver.get(f"https://www.immowelt.de")
def button():
    try:
        driver.execute_script('document.querySelector("#usercentrics-root").shadowRoot.querySelector("#uc-center-container > div.sc-ikJyIC.gpszuz > div > div > div > button.sc-gsDKAQ.fILFKg").click()')
    except JavascriptException:
        time.sleep(0.1)
        button()
button()
driver.maximize_window()
import json
_time = 1671801363
with open(f'/Users/a2/.cache/immodynamics/{_time}/links.json', "r") as f:
    filed = json.load(f)
for n, i in enumerate(filed):
    del filed[0]
    if n== 4:
        break
len(filed)
del filed[0]
def get_id(driver, s): 
    if s == "immowelt":
        raw = driver.current_url
        return f"iwe{raw[-7:]}"

# def first_seen(id):
#     try:
#         dirs = os.listdir(f"/Users/a2/.cache/immodynamics/{id}")
#     except FileNotFoundError:
#         return None
#     else:
#         dirs.sort()
#         #catch wrong files
#         for i in dirs:
#             if os.path.isdir(f"/Users/a2/.cache/immodynamics/{id}/{i}"):
#                 return i


def get_en_wrapper(driver):
    return driver.find_element(By.XPATH, '//*[@id="js_innerBody"]/div[2]/main/app-expose/div[3]/div[3]/sd-container[1]/sd-row[6]/sd-col/app-energy/sd-card')
def get_ensource(driver):
    try:
        wrapper = get_en_wrapper(driver)
        h3 = wrapper.find_element(By.TAG_NAME, 'h3')
        div = driver.execute_script("return arguments[0].nextElementSibling", h3)
        et = div.find_elements(By.TAG_NAME, 'p')[1]
        return et.text
    except NoSuchElementException:
        return

def get_enbed(driver):
    try:
        wrapper = get_en_wrapper(driver)
        ps = wrapper.find_elements(By.TAG_NAME, 'p')

        for p in ps:
            if p.text == 'Endenergiebedarf':
                return int(driver.execute_script("return arguments[0].nextElementSibling", p).text.split(',')[0])
            if  p.text == 'Endenergieverbrauch':
                return int(driver.execute_script("return arguments[0].nextElementSibling", p).text.split(',')[0])
        raise RuntimeError
    except (NoSuchElementException):
        return 0
    except TypeError:
        print(driver.current_url)
        raise('Energiebedarf fehlt')


def get_effclass(driver):
    try:
        wrapper = get_en_wrapper(driver)
        ps = wrapper.find_elements(By.TAG_NAME, 'p')

        for p in ps:
            if p.text == 'Effizienzklasse':
                enbed = driver.execute_script("return arguments[0].nextElementSibling", p).text
                ec = ['A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                return ec.index(enbed)
        enbed = get_enbed(driver)
        if enbed != 0:
            if enbed<30:
                return 0
            if enbed<50:
                return 1
            if enbed<75:
                return 2
            if enbed<100:
                return 3
            if enbed<130:
                return 4
            if enbed<160:
                return 5
            if enbed<200:
                return 6
            if enbed<250:
                return 7
            if enbed<300:
                return 8
            else:
                raise RuntimeError("Keine Energiedaten")
        else:
            raise RuntimeError("Keine Energiedaten")

    except:
        enbed = get_enbed(driver)
        if enbed != 0:
            if enbed<30:
                return 0
            if enbed<50:
                return 1
            if enbed<75:
                return 2
            if enbed<100:
                return 3
            if enbed<130:
                return 4
            if enbed<160:
                return 5
            if enbed<200:
                return 6
            if enbed<250:
                return 7
            if enbed<300:
                return 8
            else:
                return -1
        else:
            return -1

def get_built(driver):
    wrapper = driver.find_element(By.XPATH, '//*[@id="aImmobilie"]/sd-card')
    spans = wrapper.find_elements(By.TAG_NAME, 'span')
    for s in spans:
        if s.text.startswith('Baujahr'):
            li = s.find_element(By.XPATH, '..')
            return int(li.text.strip()[-4:]) #.split(",")[0].replace('.', "")
    try:
        wrapper = get_en_wrapper(driver)
        ps = wrapper.find_elements(By.TAG_NAME, 'p')
        for p in ps:
            if p.text.startswith('Baujahr'):
                return int(driver.execute_script("return arguments[0].nextElementSibling", p).text) 
    except NoSuchElementException:
        raise RuntimeError("Baujahr fehlt")
    



def decode_expose_immowelt(driver):
    time.sleep(2)
    df = pd.DataFrame()
    df["id"] = np.array([get_id(driver, "immowelt")], dtype=str)
    df["url"] = np.array([driver.current_url])
    temp = driver.find_element(By.XPATH, "//*[@id=\"aUebersicht\"]/app-hardfacts/div/div/div[1]/div[1]/strong").get_attribute("innerHTML")[:-2]
    temp = temp.split('&')[0].split(',')[0].replace('.', "")
    try: 
        df["preis"] = np.array([int(temp)])    
    except ValueError:
        raise RuntimeError('Preis auf Anfrage')
    df["typ"] = np.array([1], dtype=np.int8)
    try: 
        df["qm"] = np.array([int(float((driver.find_element(By.XPATH, "//*[@id=\"aUebersicht\"]/app-hardfacts/div/div/div[2]/div[1]/span").get_attribute("innerHTML")[:-3]).replace(".", "").replace(",", ".")))], dtype=np.int16)
    except ValueError:
        raise RuntimeError("keine qm gegeben")
    try:
        df["zimmer"] = np.array([int(float(driver.find_element(By.XPATH, "//*[@id=\"aUebersicht\"]/app-hardfacts/div/div/div[2]/div[2]/span").get_attribute("innerHTML").replace(".", "").replace(",", ".")))], dtype=np.int8)
    except ValueError:
        raise RuntimeError('Zimmer keine Angabe')
    df["plz"] = np.array([int(driver.find_element(By.XPATH, '//*[@id="exposeAddress"]/sd-cell/sd-cell-row/sd-cell-col[2]/span[2]/div[1]').get_attribute("innerHTML")[:5])], dtype=np.int32)

    try:
        driver.find_element(By.XPATH, "//*[@id=\"js_innerBody\"]/div[2]/main/app-expose/div[3]/div[3]/sd-container[1]/sd-row[7]/sd-col/app-details/sd-card/app-texts/sd-read-more[1]/a").click()
    except:
        try:
            time.sleep(0.5)
            driver.find_element(By.XPATH, "//*[@id=\"js_innerBody\"]/div[2]/main/app-expose/div[3]/div[3]/sd-container[1]/sd-row[7]/sd-col/app-details/sd-card/app-texts/sd-read-more[1]/a").click()
        except: 
            pass

    time.sleep(1)

    df["description"] = np.array([driver.find_element(By.XPATH, "//*[@id=\"js_innerBody\"]/div[2]/main/app-expose/div[3]/div[3]/sd-container[1]/sd-row[7]/sd-col/app-details/sd-card/app-texts/sd-read-more[1]/div").text])
    
    df['ensource'] = np.array([get_ensource(driver)], dtype=str)
    df['effclass'] = np.array([get_effclass(driver)], dtype=np.float64)

    df['enbed'] = np.array([get_enbed(driver)], dtype=np.int32)
    built = get_built(driver)
    assert(built is not None)
    df['built'] = np.array([built], dtype=np.int64)

    return df
links = filed
def extract_data(driver):
    return decode_expose_immowelt(driver)

def export_immo(df, _time):
    df.to_csv(f"/Users/a2/.cache/immodynamics/{_time}/properties{df['id'][0]}.csv")


for l in links:
    if l.startswith("https://www.immowelt.de/expose/"):
        f = []
        if l not in f:
            driver.get(l)
    else:
        continue
    try:
        immo_anzeige = extract_data(driver)
    except RuntimeError as R:
        print(R, driver.current_url)
        continue
    except NoSuchElementException as N:
        print(N, driver.current_url)
        continue
    except AssertionError as A:
        print(A, driver.current_url)
        continue
    id = export_immo(immo_anzeige, _time)