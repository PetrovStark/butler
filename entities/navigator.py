from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import time

class Navigator:
    def __init__(self, debug=False):
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
        self.by = By
        self.fields = []
        self.__debug = debug
    
    def __create_download_folder(self):
        folder_name = f'{os.getcwd()}/downloads/'

        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)

        return folder_name
    
    def __selectBy(self, selectors):
        data = ""

        if "id" in selectors:
            data = self.by.ID
        else:
            data = self.by.CSS_SELECTOR
        
        return data

    def __getSelector(self, selectors):
        data = ""
        element = "input"
        selectBy = self.__selectBy(selectors)

        for selector in selectors:
            for key, value in selector.items():
                if key == "element":
                    element = value
                    continue

                if selectBy == self.by.CSS_SELECTOR:
                    data += f"[{key}='{value}']"
                elif selectBy == self.by.ID and key == "id":
                    data = value
                    break

        return f"{element}{data}"

    def __setElement(self, field, selectBy, selector):
        element = self.cursor.find_element(selectBy, selector)

        if "parent" in field and bool(field["parent"]):
            element = element.find_element(By.XPATH, './..')

        return element     

    
    def __doAction(self, element, field):
        self.cursor.execute_script("arguments[0].scrollIntoView(true);", element)
        if "action" in field and field["action"] == "click":
            element.click()
        elif "action" in field and field["action"] == "send_keys":
            if self.__debug:
                print("KEYS:")
                print(field["send_keys"])

            element.send_keys(field["send_keys"])
    
    def fillForm(self):
        selector = ""

        for field in self.fields:
            selectBy = self.__selectBy(field["selectors"])
            selector = self.__getSelector(field["selectors"])
            element = self.__setElement(field, selectBy, selector)

            # Debug System
            if self.__debug:
                print("SELECTOR:\n")
                print(selector)
                print("ACTION:")
                print(field["action"])

            self.__doAction(element, field)

            if "wait" in field:
                if field["wait"] == 0:
                    field["wait"] = 1
                
                time.sleep(field["wait"])