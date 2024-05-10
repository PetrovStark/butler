from entities.navigator import Navigator
from datetime import datetime
import json
import time

class Nfse(Navigator):
    def __init__(self):
        Navigator.__init__(self)

        self.data = json.load(open("nfse.json"))
        self.emission = self.data["emission"]
        self.tomador = self.data["tomador"]
        self.urls = {
            "login_url": "https://www.nfse.gov.br/EmissorNacional/",
            "create_url": "https://www.nfse.gov.br/EmissorNacional/DPS/Pessoas"
        }
        self.fields = {}
    
    def __getDataCompetencia(self):
        if not self.emission["day"]:
            self.emission["day"] = 1
        if bool(self.emission["custom"]):
            custom_date = datetime(
                self.emission["year"],
                self.emission["month"],
                self.emission["day"]
            )
        else :
            custom_date = datetime(
                datetime.now().year,
                datetime.now().month,
                self.emission["day"]
            )
        return custom_date.strftime('%d-%m-%Y')

    def download(self):
        self.login()
        self.create()
    
    def login(self):
        self.fields = [
            ["Inscricao", self.data["cnpj"]],
            ["Senha", self.data["password"]]
        ]
        self.cursor.get(self.urls['login_url'])
        self.fillFormByCSSSelector()
        self.cursor.find_element(self.by.CSS_SELECTOR, 'button[type="submit"]').click()
        self.fields = {}
    
    def create(self):
        self.fields = [
            ["DataCompetencia", self.__getDataCompetencia()]
        ]
        self.cursor.get(self.urls['create_url'])
        self.fillFormByCSSSelector()
        time.sleep(10)
