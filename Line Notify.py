#reference:http://pythonorz.blogspot.com/2017/12/python-line-notify-line-notify-line.html
import requests
import requests
from bs4 import BeautifulSoup
def stock_crawler(stockID):
    url = 'https://tw.stock.yahoo.com/q/q?s={}'.format(stockID)
    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'html.parser')
    table = html.findAll(text='個股資料')[0].parent.parent.parent
    dataRow = table.select('tr')[1].select('td')
    closingPrice = dataRow[7].text
    closingPrice_text=""
    closingPrice_text += str(stockID) + " 收盤價 : " + closingPrice
    return closingPrice_text
def weather_yahooAPI():
    #Taoyuan's woeid = 2028752467 
    res=requests.get("https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%2028752467%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys")
    data=res.json()
    fdata=data["query"]["results"]["channel"]["item"]["forecast"]
    today=fdata[0]
    str_=""
    str_="最低溫 : "+today['low']+"  最高溫 : "+today['high']+"  天氣狀況 : "+today['text']
    return str_
def currency_crawler():
    res = requests.get('https://tw.money.yahoo.com/currency-converter')
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    #end = soup.find_all('td',class_='end')#24
    all_items = soup.find_all('tr'>'td')[310:311] #307-308 change to 310-311

    #get text
    for item in all_items:
        allCur=item.text
    #spilt the text
    spilt = allCur.splitlines()

    curList=[]
    i=2
    while(i<len(spilt)):
        curList.append(spilt[i])
        i+=8


    def getCurrency(num):
        str1=  spilt[num+1] +" "+ spilt[num+2] +" "+ spilt[num+3] +" "+ spilt[num+4] +" "+ spilt[num+5]  +" "+spilt[num+6]
        return str1

    strr=""
    num=2
    for curID in curList:
        strr = strr+curID+" : "+getCurrency(num)+"        "
        num+=8

    return strr
def lineNotify(token, msg):
        url = "https://notify-api.line.me/api/notify"
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        
        payload = {'message': msg}
        r = requests.post(url, headers = headers, params = payload)
        return r.status_code

# 這是放明碼，不建議，以免不小心就 push 到 github 上了
token = "YOUR_TOKEN" #請自行修改
msg = "\n1. 股票:\n"+stock_crawler(2330)+"\n"+"2. 天氣:\n"+weather_yahooAPI()+"\n"+"3. 匯率:\n"+currency_crawler()
lineNotify(token, msg)
