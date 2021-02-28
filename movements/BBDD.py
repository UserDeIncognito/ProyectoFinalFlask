import sqlite3
import datetime
from movements import apicoin

#Funcion que obtiene el numero total de monedas de un tipo en la BD
def numbersinglecoin(symbolfrom):
	try:
		conn = sqlite3.connect("movements/data/movimientos.db")
		conn.row_factory = sqlite3.Row
		fromcoin = conn.execute('SELECT SUM(form_quantity) as RESTA FROM MOVEMENTS WHERE from_currency=\''+str(symbolfrom)+'\'').fetchall()
		tocoin = conn.execute('SELECT SUM(to_quantity) as SUMA FROM MOVEMENTS WHERE TO_currency=\''+str(symbolfrom)+'\'').fetchall()
	except:
			print("Base de datos no se encuentra")
	finally:
			conn.close()
	suma=0
	resta=0
	if(fromcoin[0]['RESTA']):
		resta=-fromcoin[0]['RESTA']
	if(tocoin[0]['SUMA']):
		suma=tocoin[0]['SUMA']
	return suma+resta

#Funcion que comprueba si la cantidad de monedas que tiene es suficiente para gastar
def checkcoins(symbolfrom,ncoinsfrom):

	check=False
	#EUR son infinitos
	if symbolfrom=="EUR" :
		check=True
	#Si numero de monedas a utilizar es menor que el que numero de monedas que tienes
	elif(float(ncoinsfrom)<numbersinglecoin(symbolfrom)):
		check=True

	return check
#Funcion que llama a la funcion agregar nuevo movimiento, comprobando previamente si tiene suficientes monedas
#Devolvera valor booleano con el resultado de la operacion
def checkaddmove(formfromsymbol,numbercoins,fromto,totalcoins):

	check=checkcoins(formfromsymbol,numbercoins)
	if(check):
		now=datetime.datetime.now()
		today = now.strftime("%d-%m-%Y")
		time = now.strftime("%H:%M:%S")
		addMove(today,time,formfromsymbol,numbercoins,fromto,totalcoins)
	return check

#Funcion que obtiene de la BD la cantidad de un tipo de moneda actual real invertido
def totalinvertidocoin(symbol):
	try:
		conn = sqlite3.connect("movements/data/movimientos.db")
		conn.row_factory = sqlite3.Row
		coininvertidas = conn.execute('SELECT SUM(form_quantity) as INVERTDO FROM MOVEMENTS WHERE from_currency=\''+str(symbol)+'\'').fetchall()
	except:
			print("Base de datos no se encuentra")
	finally:
			conn.close()
	inversion=0
	if(coininvertidas[0]['INVERTDO']):
		inversion=coininvertidas[0]['INVERTDO']
	return inversion

#En nuestro caso el total de invertido solo corresponde a la moneda euro, que es desde proviene nuestra inversion
def totalinvertidos():
	invertido=0
	invertido=invertido + totalinvertidocoin("EUR")
	return invertido

#Funcion que devuelve todo los beneficios de toda las BD: saldo de beneficios sacados de EUR y ganancias (presentes) de cada moneda
def currentvalue():
	total=0
	#Value coins estan todas menos EUR
	valuecoins= ["BTC","ETH","LTC","BNB","EOS","XLM","TRX","XRP","BCH","USDT","BSV","ADA"]
	
	#Comprobar las cuentas de la moneda EUR, si valor >0 entonces son ganancias
	profit=numbersinglecoin("EUR")
	if(profit>0):
		total=profit
	#Comprobar cada monedas e ir sumando al total
	for coin in valuecoins:
		profitcoin=numbersinglecoin(coin)
		if(profitcoin>0):
			pu,profitEUR=apicoin.computevaluecoin(coin,"EUR",profitcoin)
			total=total+profitEUR
	return total

#Funcion para obetenr todas las filas de la BD
def get_data():
	post=[]
	try:
		conn = sqlite3.connect("movements/data/movimientos.db")
		conn.row_factory = sqlite3.Row
		posts = conn.execute('SELECT * FROM MOVEMENTS').fetchall()
	except:
		print("Base de datos no se encuentra")
	finally:
		conn.close()
	return posts

#Funcion que crea un nuevo registro en la tabla MOVEMENTS
def addMove(date,time,from_currency,form_quantity,to_currency,to_quantity):
	try:
		miConexion=sqlite3.connect("movements/data/movimientos.db")
		miCursor2 = miConexion.cursor()

		data = date,time,from_currency,form_quantity,to_currency,to_quantity

		miCursor2.execute("INSERT INTO MOVEMENTS VALUES (NULL,?,?,?,?,?,?)",(data))
		miConexion.commit()
	finally:
		miConexion.close()
