"""tigger_lib: personal library with daily use functions"""
import ssl    
import locale     
import requests
import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class tigger_bot(object):
    """Special class dedicated to webscraping. Build uppon selenium library."""

    def __init__(self, browser: str, url: str, headers: dict):
        self.browser = browser
        self.url = url
        self.request_config = {'verify':True, 'timeout': 5, 'headers':{'User-Agent': 'Mozilla/5.0'}, 'cert': None, 'ssl_version': ssl.PROTOCOL_TLSv1_2}


        
    def unlock_r(self):
        """HTTPS request unlock (generic version)"""
        response = requests.get(self.url, headers=self.request_config['headers'])
        if response.status_code == 200: #indicate success
            return print(f"Status code: {response.status_code}","\n")
        else:
            return print(f"Failed to retrieve the page. Status code: {response.status_code}")

    def unlock_custom_r(self):
        """HTTPS request with custom configuration."""
        try:
            # Specify the SSL version in the request
            response = requests.get(self.url, verify=self.request_config['verify'], timeout=self.request_config['timeout'], headers=self.request_config['headers'], cert=self.request_config['cert'], ssl_version=self.request_config['ssl_version'])
            print(response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  

    
    def today_BR_format():
        """Get brazilian current date format."""
        current_date = datetime.date.today()
        # Format the date as day-month-year
        formatted_date = current_date.strftime("%d/%m/%Y")
        return formatted_date


    def float_to_currency(valor):
        """Converts a float value to brazilian currency."""
        valor = float(valor)
        locale.setlocale(locale.LC_ALL,'')
        currency = locale.currency(valor)
        return currency
    

    def wait_presence(self, timeout, locator_type, locator, clickable=False):
        """Waits until an element is present on the page."""

        valid_locators = {
            "class": By.CLASS_NAME,
            "xpath":By.XPATH
        }

        if locator_type not in valid_locators:
            raise ValueError(
                f"Invalid locator type: {locator_type}. "
                f"Expected one of: {list(valid_locators)}"
            )
        if clickable:
            condition = EC.element_to_be_clickable(valid_locators[locator_type], locator)
            
        else:
            condition = EC.presence_of_element_located(valid_locators[locator_type], locator)

        return WebDriverWait(self.browser, timeout).until(condition)


    def big_wait_presence(self,timeout,locator_type, locator):
        """Waits until all elements are present on the page."""

        valid_locators = {
            "class": By.CLASS_NAME,
            "xpath":By.XPATH
        }

        if locator_type not in valid_locators:
            raise ValueError(
                f"Invalid locator type: {locator_type}. "
                f"Expected one of: {list(valid_locators)}"
            )

        condition = EC.presence_of_all_elements_located((valid_locators[locator_type],locator))
        return WebDriverWait(self.browser,timeout).until(condition)


    def click(self, locator_type, locator):
        """Clicking into elements."""
        valid_locators = {
                    "class": By.CLASS_NAME,
                    "xpath":By.XPATH
                }
        
        if locator_type not in valid_locators:
            raise ValueError(
                f"Invalid locator type: {locator_type}. "
                f"Expected one of: {list(valid_locators)}"
            )

        element = self.browser.find_element(valid_locators[locator_type],locator)
        return element.click()


    def press(self,key,locator_type,locator):
        r"""Press keyboard keys. Current available keys:
            'ENTER': Keys.ENTER,
            'TAB': Keys.TAB,
            'CTRA': Keys.CONTROL+'a',
            'DEL': Keys.BACKSPACE
        """

        valid_locators = {
                            "class": By.CLASS_NAME,
                            "xpath":By.XPATH
                        }

        valid_keys = {
            'ENTER': Keys.ENTER,
            'TAB': Keys.TAB,
            'CTRA': Keys.CONTROL+'a',
            'DEL': Keys.BACKSPACE
        }

        if key not in valid_keys:
            raise ValueError(
                f"Invalid key: {key}. "
                f"Expected one of: {list(valid_keys)}"
            )
                
        if locator_type not in valid_locators:
            raise ValueError(
                f"Invalid locator type: {locator_type}. "
                f"Expected one of: {list(valid_locators)}"
            )

        element = self.browser.find_element(valid_locators[locator_type],locator)
        return element.send_keys(valid_keys[key]) 

                
    def insert_text(self, text_keys,locator_type, locator):

        valid_locators = {
                "class": By.CLASS_NAME,
                "xpath":By.XPATH
        }

        if locator_type not in valid_locators:
            raise ValueError(
                f"Invalid locator type: {locator_type}. "
                f"Expected one of: {list(valid_locators)}"
            )

        text_keys = str(text_keys)
        element = self.browser.find_element(valid_locators[locator_type],locator)
        return element.send_keys(text_keys)

        
    def text_extraction(self, locator_type, locator):
        valid_locators = {
                        "class": By.CLASS_NAME,
                        "xpath":By.XPATH
                }
        
        if locator_type not in valid_locators:
            raise ValueError(
                f"Invalid locator type: {locator_type}. "
                f"Expected one of: {list(valid_locators)}"
            )

        element = self.browser.find_element(valid_locators[locator_type],locator)
        return element.text

class warehouse(object):

    """[Prototype]: manipulating a warehouse through a class. Constructed uppon pandas library."""

    def __init__(self, path, file_name, column_names, param_function):
        self.path = path
        self.file_name = file_name
        self.pandas_function = param_function
        self.header = column_names

    def gen_empty_warehouse(self):
        wh = dict()
        for i in range(len(self.header)): wh[f'{self.header[i]}'] = []

        empty_wh = pd.Dataframe()
        empty_wh.self.pandas_function(rf'{self.path}/{self.file_name}')
        
        return print("\n[warehouse status]: Empty warehouse generated.\n")

    def fill_warehouse(self):
        """Under construction..."""
        return    
