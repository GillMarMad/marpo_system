import requests
from bs4 import BeautifulSoup
import json


def findInList(value, list):
    result = [i for i in list if i['code'] == str(value)]
    return result[0] if len(result) > 0 else {}

def getAlternative(code):
    url = "https://www.truper.com/restDataSheet/api/search/products.php"
    response = requests.post(url, headers={}, data={'word': code})
    if(response.status_code==200):
        data = json.loads(response.content)
    if len(data) > 1:
        product = [item for item in data if item['code'] == code]
        if len(product) == 0:
            return None
    elif len(data) == 1:
        product = data
    else:
        return None
    url_id = product[0]['url']
    d = requests.get(url_id, headers={}, data={})
    soup = BeautifulSoup(d.text, 'html.parser')
    input = soup.find(id="dataSheetId")
    if input:
        id = input['idproduct']
    else:
        id = None
    return id

def getMain(code):
    url = "https://www.truper.com/restDataSheet2/api/products/searchDownloads.php"
    response = requests.post(url, headers={}, data={'word': code})
    try:
        if(response.status_code==200):
            data = json.loads(response.content)
            if len(data) < 1:
                return None
            else:
                data = data['data']
            if len(data) > 1:
                product = findInList(value=code,list = data)
                if len(product) > 1:
                    id = product['id']
                else:
                    id = None
            elif len(data) == 1:
                id = data[0]['id']
            else:
                id = None
        else:
            id = None
    except Exception as e:
        id = None
    return id

def getProductInfo(code) -> str:
    pdf = None
    try:
        url = "https://www.truper.com/restDataSheet/api/search/products.php"

        payload = {'word': code}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        # parse response to the new url --> [{"code":18630,"sku":"ZP-7M","name":"Zapapico 7 lb, mango fibra de vidrio 36\", Truper","imgUrl":"https:\/\/www.truper.com\/admin\/images\/ch\/18630.jpg","url":"https:\/\/www.truper.com\/ficha_tecnica\/Zapapicos.html"}]
        prodcutsResponse = json.loads(response.text)

        newurl = prodcutsResponse[0]['url']

        response = requests.request("GET", newurl)

        soup = BeautifulSoup(response.text, 'html.parser')

        #find div with id="dataSheetId"
        input = soup.find(id="descargables_pdf")
        pdf = input.find('a')['href']
    except Exception as e:
        pdf = None
        
    return pdf


def getIdFromCode(code):
    id = getMain(code)
    if id:
        return id
    id =  getAlternative(code)
    if id:
        return id
    return None