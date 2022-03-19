from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import sqlite3
import functools
import operator

stock = sqlite3.connect('Stock.db')
c = stock.cursor()
PATH = Service('C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=PATH)
driver.get("https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/3175/3176/3177/3221/3257/3350/3353/3541/3543")
actions = ActionChains(driver)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="cookiePolicyPopup"]/div/div/div/button'))).click()


def orginal():
    cards = driver.find_elements(By.CLASS_NAME, 'product')
    for card in cards:
        name = card.find_element(By.CLASS_NAME, 'description')
        namez = str(name.text).partition('GDDR')

        c.execute("INSERT INTO GPU (Name, Instock) VALUES (?,?) ", (namez[0], 0))
        stock.commit()
        c.execute("DELETE FROM GPU WHERE Name=''")
        stock.commit()

def stockchange():
    c.execute("SELECT COUNT(Name) FROM GPU")
    i = int(functools.reduce(operator.add, (c.fetchone())))
    for x in range(i+1):
        c.execute("SELECT Instock FROM GPU WHERE GPUID = ?",(x,))
        GPU = c.fetchone()
        c.execute("SELECT Instock FROM NEWGPU WHERE GPUID = ?",(x,))
        NEWGPU = c.fetchone()
        #if GPU != NEWGPU:
            # TO DO : GPU stock changed FIND GPU AND GET LINK THEN TWITTER




def SCAN():

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    cards = driver.find_elements(By.CLASS_NAME, 'product')
    features = driver.find_elements(By.CLASS_NAME, 'featured product')
    for card in cards:
        try:
            price = card.find_element(By.CLASS_NAME, 'price')
            if price.text == "CALL FOR PRICE":
                continue
            name = card.find_element(By.CLASS_NAME, 'description')
            namez = str(name.text).partition('GDDR')
            if len(namez[0]) > 1:
                print(namez[0] + ' : ' + price.text)
                current = c.execute("SELECT Name FROM GPU WHERE Name = ?", (namez[0],))
                record = c.fetchone()
                print(record)
                c.execute("UPDATE GPU SET Price = ?  WHERE Name = ? ",(price.text.strip('£').replace(',', ''), namez[0]))
                c.execute("UPDATE GPU SET Instock = ? WHERE Name = ? ",(1, namez[0]))
                stock.commit()
        except:
            name = card.find_element(By.CLASS_NAME, 'description')
            outofstock = str(name.text).partition('GDDR')
            c.execute("UPDATE GPU SET Instock = 0 WHERE Name = ?", (outofstock[0],))
            c.execute("UPDATE GPU SET Price = ''  WHERE Name = ? ", (outofstock[0],))
            stock.commit()
            pass
        driver.execute_script("window.scrollTo(0, 0);")
#orginal()
for x in range(1):
    c.execute("SELECT SUM(price) FROM GPU")
    prior = round(int(functools.reduce(operator.add,(c.fetchone()))))
    print(prior)
    c.execute("DROP TABLE NEWGPU")
    c.execute("""CREATE TABLE NEWGPU (
                Name text,
                price real,
                Instock integer,
                GPUID integer
                )""")
    c.execute("INSERT INTO NEWGPU SELECT * FROM GPU")
    SCAN()
    c.execute("SELECT SUM(price) FROM GPU")
    after = round(int(functools.reduce(operator.add, (c.fetchone()))))
    print(after)
    if prior != after:
        stockchange()
driver.quit()
stock.close()