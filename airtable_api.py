import requests,json,os
import urllib.parse


class airtable_services(object):
    def __init__(self, db_super=-1):
        with open(os.path.dirname(os.path.realpath(__file__))+"\\airtable_parameters.txt") as f:
            at_par_json = json.load(f)
        at_key = at_par_json['key']
        self.at_base = at_par_json['base']
        self.at_table = at_par_json['table']
        self.headers = {"Authorization": "Bearer " + at_key,
                   "Content-Type": "application/json"}

    def get(self,key,field):
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(
            self.at_table) + "?filterByFormula="+field+"=%22" + urllib.parse.quote(key)  + "%22"
        file = requests.get(url, headers=self.headers).text
        data = json.loads(file)
        return data['records']

    def find(self,key,field):
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(
            self.at_table) + "?filterByFormula=FIND(%22" + urllib.parse.quote(key)  + "%22%2C+"+field+")"
        file = requests.get(url, headers=self.headers).text
        data = json.loads(file)
        return data['records']

    def set(self,key,field,val):
        get_object = self.get(key,field)
        if not get_object: return False
        id = get_object[0]['id']
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table) + '/' + id
        updates = {
            "fields": {
                'Status': val
            }
        }
        file = requests.patch(url, headers=self.headers, json=updates)
        return True

    def clear(self,id):
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table) + '/' + id
        file = requests.delete(url, headers=self.headers).text
        return file

    def add(self,key,val):
        url = "https://api.airtable.com/v0/" + self.at_base + '/' + urllib.parse.quote(self.at_table)
        updates = {
            "fields": {
                'Name' : key,
                'Status': val
            }
        }
        file = requests.post(url, headers=self.headers, json=updates)
        return file



a = airtable_services().add('123','321')
##print (a)

