from movements import views
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



#Funcion que llama con el formato dado a la API para obtener el precio unitario entre las dos monedass
def conversorcoins(symbolfrom,symbolto):
    
    url="https://pro-api.coinmarketcap.com/v1/tools/price-conversion"
    parameters={
        'symbol': str(symbolfrom),
        'convert': str(symbolto),
        'amount':1
    }
    headers= {
          'X-CMC_PRO_API_KEY': views.API_KEY,
          "Accept": "application/json",
        };
    session = Session()
    session.headers.update(headers)
    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    return data

#Funcion que devuelve el precio unitario y el valor total de la moneda a cambiar
def computevaluecoin(symbolfrom,symbolto,amount):

	dataconversorcoin=conversorcoins(symbolfrom,symbolto)
	if (dataconversorcoin.get("statusCode") == None):
		if dataconversorcoin["status"]["error_code"]==0:
			PUcointo=dataconversorcoin['data']['quote'][symbolto]['price']
			return round(float(PUcointo),8), round((float(PUcointo)*float(amount)),8)
	return 0,0
