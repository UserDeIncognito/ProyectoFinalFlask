# Instalacion
Damos por sentado que ya tienes un entorno virtual levantado

Para instalar las dependencias en un ide como VSCode ejecutar en la consola
```
pip install -r requierements.txt
```
## Tambien es necesesario tener una cuenta  en la siguiente API

https://pro.coinmarketcap.com/account

## Hace falta crear el fichero " config_template.py"con la sigueintes variables

- API_KEY="clave de la api"
- SECRET_KEY="clave"
- DBFILE="movements/data/movimientos.db"

# Ejecucion
Ejecutar el siguiente comando para lanzar el entorno virtual
```
flask run
```
