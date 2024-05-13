from entities.nfse import Nfse

class Butler:
    def start(self):
        Nfse(True).download()

Butler().start()