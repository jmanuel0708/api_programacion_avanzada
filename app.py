# Flask es la librería que nos ayudará a crear un servidor para nuestra API
from flask import Flask

# Desde el archivo routes quiero que importes la función "cargar_rutas"
from routes import cargar_rutas

from extensions import db, jwt

# flask: Librería
# Flask: módulo (clase)

# Vamos a crear un objeto que contendrá los métodos necesarios para nuestro servidor
app = Flask(__name__)

# 1.- Configuramos la app para conectarse a una db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.zfhvwerzpdluqbkatson:zawmak-Byrnoj-hafde4@aws-0-us-west-1.pooler.supabase.com:6543/postgres'

# 2.- Desactivamos el seguimiento de modificaciones
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'c6krTENs82o7pib'

app.config['JWT_TOKEN_LOCATION'] = ['cookies']

app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'

app.config['JWT_COOKIE_CSRF_PROTECTION'] = False


db.init_app(app)

jwt.init_app(app)


cargar_rutas(app)

app.run(port=8000, debug=True)

# El método run le va a indicar a nuestro servidor que va a comenzar
# a recibir peticiones (servir)

# puerto 8080: le indica al usuario que accederá al servidor que creamos
# puerto 22: Este puerto crea una conexión ssh con una computadora
# puerto 23: Telnet
# 443: Este puerto usa https para enviar información
# 80: Utiliza http para enviar información
# etc.