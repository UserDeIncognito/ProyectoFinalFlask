from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

#Funcion que llama con el formato dado a la API para obtener el precio unitario entre las dos monedass
def conversorcoins(symbolfrom,symbolto):
	url="https://pro-api.coinmarketcap.com/v1/tools/price-conversion"
	#API HAY QUE ARREGLARLO
	api='7abe7181-5688-41ab-bee0-52eea94a1d41'
	url="https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol="+symbolfrom+"&convert="+symbolto+"&CMC_PRO_API_KEY="+api
	session = Session()

	try:
		response = session.get(url)
		data = json.loads(response.text)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
	return data

#Funcion que devuelve el precio unitario y el valor total de la moneda a cambiar
def computevaluecoin(symbolfrom,symbolto,amount):

	dataconversorcoin=conversorcoins(symbolfrom,symbolto)
	PUcointo=dataconversorcoin['data']['quote'][symbolto]['price']
	return round(float(PUcointo),8), round((float(PUcointo)*float(amount)),8)

