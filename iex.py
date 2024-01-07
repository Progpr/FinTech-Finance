import requests
import config


class IEXstock:
    def __init__(self,token,symbol):
        self.Base_url = "https://api.iex.cloud/v1/"

        self.token = token
        self.symbol = symbol

    def get_logo(self):
        logo_url = f"{self.Base_url}stock/{self.symbol}/logo?token={config.IEX_P_KEY}"
        logo_res = requests.get(logo_url)

        return logo_res.json()

    def get_company_info(self):
        company_url = f"{self.Base_url}data/core/company/{self.symbol}?token={config.IEX_P_KEY}"
        company_res = requests.get(company_url)

        return company_res.json()

    def get_company_news(self, last=10):
        url = f"{self.Base_url}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_stats(self):
        url = f"{self.Base_url}/stock/{self.symbol}/advanced-stats?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_fundamentals(self, period='quarterly', last=4):
        url = f"{self.Base_url}/time-series/fundamentals/{self.symbol}/{period}?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_dividends(self, range='5y'):
        url = f"{self.Base_url}/stock/{self.symbol}/dividends/{range}?token={self.token}"
        r = requests.get(url)

        return r.json()








