from movements import app
from flask import render_template, request,redirect
from movements import apicoin
from movements import BBDD


#DBFILE = app.config['DBFILE']

#Pagina principal a la que pasaremos todos los datos de la tabla MOVEMENTS para que la muestre por pantalla
@app.route('/') 
def index():
	posts = BBDD.get_data()
	return render_template('index.html', posts=posts)

#Pagina Purchase donde se realizará la compra de las monedas
	#Post: Obtendremos el boton pra saber la accion correspondiente a utilizar
@app.route('/purchase',methods=['GET','POST']) 
def purchase():
	if request.method == 'POST':
		formfromsymbol=request.form["formfrom"]
		fromtosymbol=request.form["fromto"]
		numbercoins=request.form["cryptonumber"]

		if numbercoins == "" or numbercoins == 0:
			return render_template('purchase.html',coinerror=True)

		if(request.form['accion']=="calculadora"):

			#En caso de que no sean iguales calcularemos los datos correspondientes llamando a la API (apicoin.py)
			if not(formfromsymbol==fromtosymbol):
				pu,totalcoins=apicoin.computevaluecoin(formfromsymbol,fromtosymbol,numbercoins)
				return render_template('purchase.html',PU=pu,totalcoins=totalcoins,formfromsymbol=formfromsymbol,fromtosymbol=fromtosymbol,numbercoins=numbercoins)

			#En caso de sean iguales volvemos a la pagina con el error correspondiente activado	
			return render_template('purchase.html',paramerror=True,formfromsymbol=formfromsymbol,fromtosymbol=fromtosymbol)

		if(request.form['accion']=="borrar"):
			return render_template('purchase.html',PU=" ",formfromsymbol="EUR",fromtosymbol="EUR",numbercoins=" ",totalcoins=" ")
		if(request.form['accion']=="comprar"):
			#Para comprobar que el usuario no ha cambiado los datos o la moneda cambia de valor volvemos a calcular el precio actual y lo comparamos
			pu,totalcoins=apicoin.computevaluecoin(formfromsymbol,fromtosymbol,numbercoins)
			if((pu!=float(request.form['PU'])) or (totalcoins!=float(request.form['totalcoins']))):
				#Si ha cambiado entonces volvemos a la pagina con el error correspondiente
				return render_template('purchase.html', changeerror=True,numbercoins=0,PU=0,totalcoins=0)
			else:
				#Sino enviamos los datos para añadir un movimiento a la base de datos
				answer=BBDD.checkaddmove(formfromsymbol,numbercoins,fromtosymbol,totalcoins)
				#En caso de que se efectue correctamente se vuelve al home
				if answer:
					return redirect('/')
				#En caso de no tener monedas suficientes volvemos a la pagina con el error correspondiente
				else:
					return render_template('purchase.html',coinerror=True)


	return render_template('purchase.html')


#Pagina donde mostrara el estado de nuestros movimientos
@app.route('/status',methods=['GET','POST'])
def status():
	if request.method == 'POST':
		#Boton volver
		return redirect('/')

	inversion=BBDD.totalinvertidos()
	currentvalue=BBDD.currentvalue()
	return render_template('status.html',valoractual=currentvalue,inversion=inversion)

#En caso de no encontrar la pagina por un error 404 avisar en una nueva pagina
@app.errorhandler(404)
def page_not_found(error):
	return '<h1>Página no encontrada...</h1>',404

