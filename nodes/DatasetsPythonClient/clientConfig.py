from KaggleClient import KaggleClient
from WorkBankClient import WorkBankClient, WebClient

def get_client(host) -> WebClient:
    match host:
        case "data.worldbank.org":
            return WorkBankClient()
        case "kaggle.com":
            return KaggleClient()
        case _:
            raise Exception("No web client sepecified for given host")