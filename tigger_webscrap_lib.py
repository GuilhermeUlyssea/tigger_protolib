#-----------------------------------------------------------------------------------------[PERMISSÕES]-------------------------------------------------------------------------------------------------------------------
#Function for unlocking requests:
import requests
def unlock_r(url):
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    response = requests.get(url, headers=HEADERS)
    # Check if the request was successful (status code 200 indicates success)
    if response.status_code == 200: #indicate success
        return print(f"Status code: {response.status_code}","\n")
    else:
        return print(f"Failed to retrieve the page. Status code: {response.status_code}")

import ssl    
def unlock_r1(url):
    try:
        # Specify the SSL version in the request
        response = requests.get(url, verify=True, timeout=5, headers={'User-Agent': 'Mozilla/5.0'}, cert=None, ssl_version=ssl.PROTOCOL_TLSv1_2)
        print(response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")  

#-----------------------------------------------------------------------------------------[DATAS]-------------------------------------------------------------------------------------------------------------------

import datetime
def today_func():
    current_date = datetime.date.today()
    # Format the date as day-month-year
    formatted_date = current_date.strftime("%d/%m/%Y")
    return formatted_date
  
#-----------------------------------------------------------------------------------------[NAVEGAÇÃO]-------------------------------------------------------------------------------------------------------------------
    
#Funções para clicks:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Waiting functions:
def wait_presence_class(browser,time,class_name):
    class_name = str(class_name)
    time = int(time)
    return WebDriverWait(browser,time).until(EC.presence_of_element_located((By.CLASS_NAME,class_name)))

def wait_presence_xpath(browser,time,xpath):
    xpath = str(xpath)
    time = int(time)
    return WebDriverWait(browser,time).until(EC.presence_of_element_located((By.XPATH,xpath)))

def wait_clickable_class(browser,time,class_name):
    class_name = str(class_name)
    time = int(time)
    return WebDriverWait(browser,time).until(EC.element_to_be_clickable((By.CLASS_NAME,class_name)))

def wait_clickable_xpath(browser,time,xpath):
    xpath = str(xpath)
    time = int(time)
    return WebDriverWait(browser,time).until(EC.element_to_be_clickable((By.XPATH,xpath)))

def bigwait_presence_class(browser,time,class_name):
    class_name = str(class_name)
    time = int(time)
    return WebDriverWait(browser,time).until(EC.presence_of_all_elements_located((By.CLASS_NAME,class_name)))

def bigwait_presence_xpath(browser,time,xpath):
    xpath = str(xpath)
    time = int(time)
    return WebDriverWait(browser,time).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))

#Clicking functions:
def click_class(browser,class_name):
    class_name = str(class_name)
    b0 = browser.find_element(By.CLASS_NAME,class_name)   
    return b0.click()

def click_xpath(browser,xpath):
    xpath = str(xpath)
    b0 = browser.find_element(By.XPATH,xpath)
    return b0.click()

from selenium.webdriver.common.keys import Keys
def ENTER_class(browser,class_name):
    class_name = str(class_name)
    b0 = browser.find_element(By.CLASS_NAME,class_name)   
    return b0.send_keys(Keys.ENTER)

def ENTER_xpath(browser,xpath):
    xpath = str(xpath)
    b0 = browser.find_element(By.XPATH,xpath)
    return b0.send_keys(Keys.ENTER)

def TAB_class(browser,class_name):
    class_name = str(class_name)
    b0 = browser.find_element(By.CLASS_NAME,class_name)   
    return b0.send_keys(Keys.TAB)

def TAB_xpath(browser,xpath):
    xpath = str(xpath)
    b0 = browser.find_element(By.XPATH,xpath)
    return b0.send_keys(Keys.TAB)

def CNTA_class(browser,class_name):
    class_name = str(class_name)
    b0 = browser.find_element(By.CLASS_NAME,class_name)   
    return b0.send_keys(Keys.CONTROL+'a')

def CNTA_xpath(browser,xpath):
    xpath = str(xpath)
    b0 = browser.find_element(By.XPATH,xpath)
    return b0.send_keys(Keys.CONTROL+'a')

def DELET_class(browser,class_name):
    class_name = str(class_name)
    b0 = browser.find_element(By.CLASS_NAME,class_name)   
    return b0.send_keys(Keys.BACKSPACE)

def DELET_xpath(browser,xpath):
    xpath = str(xpath)
    b0 = browser.find_element(By.XPATH,xpath)
    return b0.send_keys(Keys.BACKSPACE)

#Text functions:
def txt_class(browser,class_name):
    class_name = str(class_name)
    b0 = browser.find_element(By.CLASS_NAME,class_name)
    return b0.text

def txt_xpath(browser,xpath):
    xpath = str(xpath)
    b0 = browser.find_element(By.CLASS_NAME,xpath)
    return b0.text

#Inserting functions:
def insert_class(browser,class_name,keys):
    class_name = str(class_name)
    keys = str(keys)
    b0 = browser.find_element(By.CLASS_NAME,class_name)
    return b0.send_keys(keys)

def insert_xpath(browser,xpath,keys):
    xpath = str(xpath)
    keys = str(keys)
    b0 = browser.find_element(By.XPATH,xpath)
    return b0.send_keys(keys)

#-----------------------------------------------------------------------------------------[CONVERSÃO DE DTYPES]-------------------------------------------------------------------------------------------------------------------
#string em moeda 
import locale                                                      #Para conversão de moedas: ADD 20/11/23
def float_to_moeda(valor):
    valor = float(valor)
    locale.setlocale(locale.LC_ALL,'')
    moeda = locale.currency(valor)
    return moeda
#valor = float(220.91)
#print(locale.setlocale(locale.LC_ALL,''))
#print(locale.currency(valor))
