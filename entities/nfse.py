from entities.navigator import Navigator
from datetime import datetime
import json

class Nfse(Navigator):
    def __init__(self, debug=False):
        Navigator.__init__(self, debug)

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
            {
                "selectors": [
                    {
                        "name": "Inscricao"
                    }
                ],
                "action": "send_keys",
                "send_keys": self.data["cnpj"]
            },
            {
                "selectors": [
                    {
                        "name": "Senha"
                    }
                ],
                "action": "send_keys",
                "send_keys": self.data["password"]
            }
        ]
        self.cursor.get(self.urls['login_url'])
        self.fillForm()
        self.cursor.find_element(self.by.CSS_SELECTOR, 'button[type="submit"]').click()
        self.fields = {}
    
    def create(self):
        self.fields = [
            {
                "selectors": [
                    {
                        "name": "DataCompetencia"
                    }
                ],
                "action": "send_keys",
                "send_keys": self.__getDataCompetencia(),
            },
            {
                "selectors": [
                    {
                        "element": "div",
                        "id": "pnlTomador"
                    }
                ],
                "action": "click",
                "wait": 2
            },
            {
                "selectors": [
                    {
                        "name": "Tomador.LocalDomicilio",
                        "value": 1
                    }
                ],
                "parent": True,
                "action": "click",
                "wait": 1
            },
            {
                "selectors": [
                    {
                        "id": "Tomador_Inscricao"
                    }
                ],
                "action": "send_keys",
                "send_keys": self.tomador["cnpj"]
            },
            {
                "selectors": [
                    {
                        "element": "button",
                        "id": "btn_Tomador_Inscricao_pesquisar"
                    }
                ],
                "action": "click",
                "wait": 1
            },
            {
                "selectors": [
                    {
                        "element": "button",
                        "id": "btnAvancar"
                    }
                ],
                "action": "click",
                "wait": 1
            }
        ]
        self.cursor.get(self.urls['create_url'])
        self.fillForm()