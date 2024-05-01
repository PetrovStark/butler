from entities.nfse import Nfse

class Butler:
    def start(self):
        Nfse().download()

Butler().start()