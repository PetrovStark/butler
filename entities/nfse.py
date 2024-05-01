from entities.navigator import Navigator

class Nfse(Navigator):
    def __init__(self):
        Navigator.__init__(self)

        self.urls = {
            "nfse": "https://www.nfse.gov.br/EmissorNacional/"
        }
    
    def download(self):
        self.cursor.get(self.urls['nfse'])
        self.action.pause(50000)