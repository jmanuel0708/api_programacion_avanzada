from flask import Flask, render_template, request, redirect, url_for

from methods import crear_cuenta, iniciar_sesion, encontrar_todos_los_usuarios

def cargar_rutas(app):
  # Ruta raíz
  @app.route('/<status>')
  def pagina(status):
#     for usuario in lista_usuarios:
#       print(f''' 
#     nombre usuario: {usuario.name}
#     correo usuario: {usuario.email}
#     contraseña usuario: {usuario.password}
    
# ''')


    print(status)
    return render_template('index.html')

  # Esta es otra ruta
  @app.route('/login')
  def informacion_jose():
    resultado = request.args.get('status')
    return render_template('login.html', estado=resultado)

  # Esta es otra ruta
  @app.route('/signup')
  def datos():
    resultado = request.args.get('status')
    return render_template('signup.html', estado=resultado)

  # Esta ruta va a manejar la información
  # Este método solo funcionará para el inicio de sesión
  @app.route('/manipulacion', methods=['POST'])
  def manipular_datos():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f'''
      Correo: {email}
      Contraseña: {password}
    ''')

    respuesta_login = iniciar_sesion(email, password)

    if respuesta_login['status'] == 'error':
      return redirect(url_for('informacion_jose', status=respuesta_login['status']))

    return redirect(url_for('pagina'))

  # Interceptamos la información del Sign Up del usuario
  @app.route('/datos_crear_cuenta', methods=['POST'])
  def obtener_datos_cuenta():
    nombre = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    print(f'''
    nombre: {nombre}
    correo: {email}
    passoword: {password}
    ''')

    respuesta_signup = crear_cuenta(nombre, email, password)

    print(respuesta_signup)

    if respuesta_signup['status'] == 'error':
      return redirect(url_for('datos', status=respuesta_signup['status']))

    return redirect(url_for('pagina', status=respuesta_signup['status']))

  @app.route('/error')
  def pantalla_error():
    return render_template('error.html')