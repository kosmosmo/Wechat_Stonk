import os, argparse, shutil, json, sys
import requests
import urllib.parse,time


class airtable_talk():
    def __init__(self, db_super=-1):
        with open(os.path.dirname(os.path.realpath(__file__)) + "\\airtable_parameters") as f:
            at_par_json = json.load(f)
        at_key = at_par_json['key']
        self.at_base = at_par_json['base']
        self.at_table = at_par_json['table']
        self.headers = {"Authorization": "Bearer " + at_key,
                        "Content-Type": "application/json"}

    def find_ticker(self, ticker):
        ticker = ticker.upper()
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(
            self.at_table) + "?filterByFormula=Ticker=%22" +ticker + "%22"
        #print (requests.get(url, headers=self.headers).text)
        file = json.loads(requests.get(url, headers=self.headers).text)['records']
        if not file: return None
        return [file[0]['id'],file[0]['fields']['Count']]

    def push_count(self,ticker,count):
        ticker = ticker.upper()
        ticker_get = self.find_ticker(ticker)
        if not ticker_get: self.add_ticker(ticker,count)
        else:
            url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table) + '/' + ticker_get[0]
            updates = {
                "fields": {
                    'Count': ticker_get[1]+count
                }
            }
            file = requests.patch(url, headers=self.headers, json=updates)

    def increm_count(self,ticker):
        ticker = ticker.upper()
        ticker_get = self.find_ticker(ticker)
        if not ticker_get: self.add_ticker(ticker)
        else:
            url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table) + '/' + ticker_get[0]
            updates = {
                "fields": {
                    'Count': ticker_get[1]+1
                }
            }
            file = requests.patch(url, headers=self.headers, json=updates)

    def add_ticker(self,ticker,ct = 1):
        ticker = ticker.upper()
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table)
        updates = {
            "fields": {
                'Ticker': ticker,
                'Count': ct
            }
        }
        file = requests.post(url, headers=self.headers, json=updates)
        #print (file.text)
        return file

    def reset_ticker(self,ticker):
        ticker = ticker.upper()
        ticker_get = self.find_ticker(ticker)
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table) + '/' + ticker_get[0]
        file = requests.delete(url, headers=self.headers).text
        return file

    def top_ten(self):
        res = []
        url = "https://api.airtable.com/v0/"+ self.at_base + '/' + urllib.parse.quote(
            self.at_table) + "?maxRecords=10&sort%5B0%5D%5Bfield%5D=Count&sort%5B0%5D%5Bdirection%5D=desc"
        datas = json.loads(requests.get(url, headers=self.headers).text)['records']
        for data in datas:
            res.append(data['fields']["Ticker"] + ', '+str(data['fields']["Count"]))
        return res


#a = airtable_talk().add_ticker('GOOG')
#print (a.push_count('H',10))