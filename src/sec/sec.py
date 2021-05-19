import json
import urllib.request as request
import os
import configparser


class SEC(object):

    def __init__(self):
        self._BASEURL: str = "https://api.sec-api.io?token="
        self._TOKEN: str = ""
        self.set_token('config' + '/' + 'config.ini')
        self._API: str = ""
        self.set_api()
        self._ticker: str = ""
        self._year_range: tuple = (2019, 2020)
        self._filing_type: str = "10-K"
        self._filings: json = ""

    # get ticker
    @property
    def ticker(self) -> str:
        return self._ticker

    # get year range
    @property
    def year_range(self) -> tuple:
        return self._year_range

    # get filing type
    @property
    def filing_type(self) -> str:
        return self._filing_type

    # get filings
    @property
    def filings(self) -> json:
        return self._filings

    # set ticker
    @ticker.setter
    def ticker(self, value: str):
        self._ticker = value

    # set year range
    @year_range.setter
    def year_range(self, value: tuple):
        self._year_range = value

    # set filing type
    @filing_type.setter
    def filing_type(self, value: str):
        self._filing_type = value

    # set token from config.ini
    def set_token(self, token_directory):
        token_full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', token_directory))
        config = configparser.ConfigParser()
        config.read(token_full_path)
        self._TOKEN = config.get('sec-api-trial', 'api_key')

    # set API to base + token
    def set_api(self):
        self._API = self._BASEURL + self._TOKEN

    # api request
    def initiate_request(self):
        get_request(self._API, self.ticker, self._year_range, self.filing_type)


def get_request(api, ticker, year_range, form_type):
    # TODO: ticker, filledAt, formType, from/size to be passed from SEC.initiate_request like api is
    payload = {
        "query": {"query_string": {"query": "ticker:AAPL AND "
                                            "filedAt:{2018-01-01 TO 2018-12-31} AND formType:\"10-K\""}},
        "sort": [{"filedAt": {"order": "desc"}}]
    }
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')
    req = request.Request(api)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = request.urlopen(req, jsondataasbytes)
    res_body = response.read()
    filings = json.loads(res_body.decode("utf-8"))
    print(filings)
    #print(filings['filings'][0]['linkToTxt'])
    #print(filings['filings'][0]['linkToFilingDetails'])
    #print(filings['filings'][0]['documentFormatFiles'][0]['documentUrl'])


def main():
    while True:
        try:
            # TODO: error checking for ticker/filing_type
            ticker = input("Enter stock ticker: ")
            filing_type = input("Enter filing type (eg. 10-K, 10-Q etc.): ")
            year_start = int(input("Enter start year: "))
            year_end = int(input("Enter end year: "))
            break
        except ValueError as e:
            print(e)
    f = SEC()
    f.ticker = ticker
    f.year_range = (year_start, year_end)
    f.filing_type = filing_type
    f.initiate_request()


if __name__ == "__main__":
    main()
