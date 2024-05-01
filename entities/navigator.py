from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import os
import json

class Navigator:
    def __init__(self):
        driver = Service(ChromeDriverManager().install())
        self.urls = {}
        self.download_folder = self.__create_download_folder()       
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", {
        "download.default_directory": self.download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })
        self.cursor = webdriver.Chrome(service=driver, chrome_options=self.options)
        self.action = ActionChains(driver)
    
    def __create_download_folder(self):
        folder_name = f'{os.getcwd()}/downloads/'
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)
        
        return folder_name