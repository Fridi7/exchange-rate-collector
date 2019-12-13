import urllib.request
import mongo_rw

from pymongo import MongoClient
from xml.dom import minidom


def req(client):
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    webFile = urllib.request.urlopen(url)
    data = webFile.read()
    doc = minidom.parseString(data)
    root = doc.getElementsByTagName("ValCurs")[0]
    date = root.getAttribute('Date')
    currency = minidom.parseString(data).getElementsByTagName("Valute")
    mongo_rw.mongo_login(client)
    for rate in currency:
        valuta = {}
        valuta["ID"] = (rate.getAttribute("ID"))
        charcode = rate.getElementsByTagName("CharCode")[0]
        valuta["charcode"] = charcode.firstChild.data
        name = rate.getElementsByTagName("Name")[0]
        valuta["name"] = name.firstChild.data
        value = rate.getElementsByTagName("Value")[0]
        valuta["value"] = value.firstChild.data
        nominal = rate.getElementsByTagName("Nominal")[0]
        valuta["nominal"] = nominal.firstChild.data
        valuta["date"] = date
        mongo_rw.mongo_write(mongo_rw.mongo_login(client), valuta)
